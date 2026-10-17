import io
import hashlib
import json
import tempfile
from pathlib import Path
from unittest.mock import patch

from PIL import Image
from pypdf import PdfReader, PdfWriter, Transformation

from django.conf import settings
from django.core.cache import cache
from django.core.management import call_command
from django.core.management.base import CommandError
from django.core.exceptions import SuspiciousFileOperation
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from .books import private_asset, render_pdf_page
from .checks import private_books_location
from .models import Kitob, User


def source_fixture(root):
    folder = root / '2'
    folder.mkdir(parents=True)
    with PdfWriter() as writer:
        writer.add_blank_page(width=300, height=420)
        writer.add_blank_page(width=300, height=420)
        writer.write(folder / 'muqova.pdf')
    with PdfWriter() as writer:
        writer.add_blank_page(width=200, height=280)
        writer.add_blank_page(width=210, height=297)
        writer.write(folder / 'body.pdf')
    Image.new('RGB', (100, 50), 'red').save(folder / 'barcode.png')
    return folder


class BookLibraryTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='reader', password='test-pass')
        cls.other = User.objects.create_user(username='other-reader', password='test-pass')

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.settings_override = override_settings(PRIVATE_BOOKS_ROOT=root / 'private')
        self.settings_override.enable()
        self.addCleanup(self.settings_override.disable)
        source_fixture(root / 'source')
        self.source = root / 'source'
        self.import_books()
        self.book = Kitob.objects.get(manba='2')
        cache.clear()
        self.client.force_login(self.user)

    def import_books(self, **kwargs):
        source = kwargs.pop('source', self.source)
        call_command('import_kitoblar', source=source, stdout=io.StringIO(), **kwargs)

    def nested_library(self, metadata=None):
        base = Path(self.temp.name) / 'project'
        data = base / 'home/data'
        data.mkdir(parents=True)
        (data / 'kitoblar.json').write_text(json.dumps(metadata or {}), encoding='utf8')
        return base, base / 'kitoblar'

    def token(self, client=None, book=None):
        client = client or self.client
        response = client.get(reverse('kitob_oqish', args=[(book or self.book).pk]))
        return response.context['reader_config']['token']

    def page_url(self, book=None, number=1):
        return reverse('kitob_sahifa', args=[(book or self.book).pk, number])

    def test_import_preserves_sources_and_page_order_and_adds_barcode(self):
        assembled = PdfReader(private_asset(self.book.fayl))
        self.assertEqual(self.book.sahifalar, 4)
        self.assertEqual([int(p.mediabox.width) for p in assembled.pages], [300, 200, 210, 300])
        self.assertEqual(len(assembled.pages[-1].images), 1)
        self.assertEqual(len(PdfReader(self.source / '2/muqova.pdf').pages[-1].images), 0)
        self.assertEqual(len(PdfReader(self.source / '2/body.pdf').pages), 2)
        with Image.open(private_asset(self.book.muqova)) as cover:
            self.assertEqual(cover.format, 'WEBP')

    def test_reimport_is_idempotent_and_preserves_admin_edits(self):
        path = private_asset(self.book.fayl)
        stamp = path.stat().st_mtime_ns
        self.book.nom = 'Tahrirlangan nom'
        self.book.faol = False
        self.book.save()
        self.import_books()
        self.book.refresh_from_db()
        self.assertEqual(Kitob.objects.count(), 1)
        self.assertEqual(path.stat().st_mtime_ns, stamp)
        self.assertEqual(self.book.nom, 'Tahrirlangan nom')
        self.assertFalse(self.book.faol)

    def test_changed_source_rebuilds_and_invalidates_old_grant(self):
        token = self.token()
        old_fingerprint = self.book.fingerprint
        Image.new('RGB', (100, 50), 'blue').save(self.source / '2/barcode.png')
        self.import_books()
        self.book.refresh_from_db()
        self.assertNotEqual(self.book.fingerprint, old_fingerprint)
        self.assertEqual(self.client.get(self.page_url(), HTTP_X_BOOK_TOKEN=token).status_code, 403)

    def test_incomplete_folder_rejected_before_library_changes(self):
        incomplete = self.source / '3'
        incomplete.mkdir()
        with self.assertRaises(CommandError):
            self.import_books()
        self.assertEqual(Kitob.objects.count(), 1)

    def test_dry_run_does_not_import(self):
        self.book.delete()
        self.import_books(dry_run=True)
        self.assertEqual(Kitob.objects.count(), 0)

    def test_numbered_cover_preserves_embedded_barcode_without_separate_image(self):
        folder = self.source / '2'
        original = PdfReader(private_asset(self.book.fayl))
        with PdfWriter() as writer:
            writer.add_page(original.pages[0])
            writer.add_page(original.pages[-1])
            writer.write(folder / 'muqova.pdf')
        embedded = PdfReader(folder / 'muqova.pdf').pages[-1].images[0].data
        (folder / 'muqova.pdf').rename(folder / 'Обложка (2).pdf')
        (folder / 'barcode.png').unlink()
        self.import_books()
        self.book.refresh_from_db()
        assembled = PdfReader(private_asset(self.book.fayl))
        self.assertEqual(len(assembled.pages), 4)
        self.assertEqual(assembled.pages[-1].images[0].data, embedded)

    def test_unnamed_two_page_cover_is_identified_by_page_count(self):
        folder = self.source / '2'
        (folder / 'muqova.pdf').rename(folder / 'storybook.pdf')
        original = PdfReader(folder / 'body.pdf')
        with PdfWriter() as writer:
            for page in original.pages:
                writer.add_page(page)
            writer.add_blank_page(width=220, height=310)
            writer.write(folder / 'body.pdf')
        self.import_books()
        self.book.refresh_from_db()
        assembled = PdfReader(private_asset(self.book.fayl))
        self.assertEqual([int(page.mediabox.width) for page in assembled.pages], [300, 200, 210, 220, 300])

    def test_separate_barcode_replaces_placeholder_among_other_cover_images(self):
        def image_page(size, color):
            stream = io.BytesIO()
            Image.new('RGB', size, color).save(stream, format='PDF', resolution=72)
            return PdfReader(stream).pages[0]

        with PdfWriter() as writer:
            writer.add_blank_page(width=300, height=420)
            back = writer.add_blank_page(width=300, height=420)
            back.merge_page(image_page((300, 420), 'white'))
            barcode = image_page((100, 50), 'blue')
            back.merge_transformed_page(barcode, Transformation().translate(20, 60))
            writer.write(self.source / '2/muqova.pdf')
        self.import_books()
        self.book.refresh_from_db()
        image = render_pdf_page(private_asset(self.book.fayl), self.book.sahifalar - 1, max_size=420)
        red, green, blue = image.getpixel((25, 350))
        self.assertGreater(red, 200)
        self.assertLess(green, 50)
        self.assertLess(blue, 50)

    def test_already_complete_pdf_preserves_its_page_order(self):
        folder = self.source / '2'
        (folder / 'muqova.pdf').unlink()
        (folder / 'barcode.png').unlink()
        self.import_books()
        self.book.refresh_from_db()
        assembled = PdfReader(private_asset(self.book.fayl))
        self.assertEqual([int(page.mediabox.width) for page in assembled.pages], [200, 210])
        self.assertEqual(self.book.sahifalar, 2)

    def test_nested_and_selected_collection_imports_never_overwrite_root_book(self):
        base, library = self.nested_library()
        source_fixture(library)
        source_fixture(library / 'yangi')
        original_name = self.book.nom
        with override_settings(BASE_DIR=base):
            self.import_books(source=library)
            nested = Kitob.objects.get(manba='yangi/2')
            self.import_books(source=library / 'yangi')
            self.assertEqual(Kitob.objects.get(manba='yangi/2').pk, nested.pk)
        self.book.refresh_from_db()
        self.assertEqual(self.book.manba, '2')
        self.assertEqual(self.book.nom, original_name)
        self.assertEqual(Kitob.objects.count(), 2)

    def test_verified_duplicate_is_skipped_but_changed_source_requires_review(self):
        copied = (self.source / '2/body.pdf').read_bytes()
        metadata = {'3': {'duplicate_of': '2', 'duplicate_sha256': hashlib.sha256(copied).hexdigest()}}
        base, library = self.nested_library(metadata)
        source_fixture(library)
        duplicate = library / '3'
        duplicate.mkdir()
        file = duplicate / 'combined.pdf'
        file.write_bytes(copied)
        with override_settings(BASE_DIR=base):
            self.import_books(source=library)
            self.assertEqual(Kitob.objects.count(), 1)
            file.write_bytes(copied + b'\n% changed source\n')
            with self.assertRaises(CommandError):
                self.import_books(source=library)
            self.assertEqual(Kitob.objects.count(), 1)

    def test_all_library_endpoints_require_login(self):
        anonymous = Client()
        for url in [reverse('kutubxona'), reverse('kitob_oqish', args=[self.book.pk]),
                    reverse('kitob_muqova', args=[self.book.pk]), self.page_url()]:
            with self.subTest(url=url):
                response = anonymous.get(url)
                self.assertEqual(response.status_code, 302)
                self.assertIn('/login/', response.url)
                self.assertIn('no-store', response['Cache-Control'])

    def test_catalog_and_reader_do_not_publish_pdf_paths(self):
        for url in [reverse('kutubxona'), reverse('kitob_oqish', args=[self.book.pk])]:
            response = self.client.get(url)
            self.assertContains(response, self.book.nom)
            self.assertNotContains(response, self.book.fayl)
            self.assertNotContains(response, '.pdf')
            self.assertIn('no-store', response['Cache-Control'])

    def test_valid_page_is_watermarked_image_with_private_headers(self):
        response = self.client.get(self.page_url(), HTTP_X_BOOK_TOKEN=self.token())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'image/webp')
        self.assertEqual(response['Cross-Origin-Resource-Policy'], 'same-origin')
        self.assertEqual(response['X-Frame-Options'], 'DENY')
        self.assertIn('no-store', response['Cache-Control'])
        self.assertNotIn('Content-Disposition', response)
        with Image.open(io.BytesIO(response.content)) as image:
            self.assertEqual(max(image.size), 1600)
            self.assertLess(min(image.convert('L').getextrema()), 240)

    def test_cover_is_authenticated_image(self):
        response = self.client.get(reverse('kitob_muqova', args=[self.book.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'image/webp')

    def test_missing_and_tampered_tokens_are_rejected(self):
        for token in ['', 'invalid', self.token() + 'tamper']:
            with self.subTest(token=token):
                response = self.client.get(self.page_url(), HTTP_X_BOOK_TOKEN=token)
                self.assertEqual(response.status_code, 403)
                self.assertIn('no-store', response['Cache-Control'])

    def test_token_cannot_be_shared_with_another_user_or_session(self):
        token = self.token()
        for user in [self.other, self.user]:
            with self.subTest(user=user.pk):
                other_session = Client()
                other_session.force_login(user)
                self.assertEqual(other_session.get(self.page_url(), HTTP_X_BOOK_TOKEN=token).status_code, 403)

    def test_token_cannot_be_used_for_another_book(self):
        other = Kitob.objects.create(manba='other', nom='Other', sahifalar=4,
                                    fayl=self.book.fayl, muqova=self.book.muqova,
                                    fingerprint=self.book.fingerprint)
        self.assertEqual(self.client.get(self.page_url(book=other), HTTP_X_BOOK_TOKEN=self.token()).status_code, 403)

    def test_expired_token_rejected(self):
        with patch('django.core.signing.time.time', return_value=1):
            token = self.token()
        self.assertEqual(self.client.get(self.page_url(), HTTP_X_BOOK_TOKEN=token).status_code, 403)

    def test_deactivated_book_revokes_reader_cover_and_existing_grant(self):
        token = self.token()
        self.book.faol = False
        self.book.save()
        self.assertNotContains(self.client.get(reverse('kutubxona')), self.book.nom)
        for url in [reverse('kitob_oqish', args=[self.book.pk]),
                    reverse('kitob_muqova', args=[self.book.pk]), self.page_url()]:
            self.assertEqual(self.client.get(url, HTTP_X_BOOK_TOKEN=token).status_code, 404)

    def test_logged_out_session_cannot_use_old_grant(self):
        token = self.token()
        self.client.logout()
        self.assertEqual(self.client.get(self.page_url(), HTTP_X_BOOK_TOKEN=token).status_code, 302)

    def test_cross_origin_requests_rejected_even_with_valid_grant(self):
        token = self.token()
        for site in ['cross-site', 'same-site']:
            self.assertEqual(self.client.get(self.page_url(), HTTP_X_BOOK_TOKEN=token,
                                             HTTP_SEC_FETCH_SITE=site).status_code, 403)

    def test_page_bounds_checked(self):
        token = self.token()
        for number in [0, self.book.sahifalar + 1]:
            self.assertEqual(self.client.get(self.page_url(number=number), HTTP_X_BOOK_TOKEN=token).status_code, 404)
        self.assertEqual(self.client.get(self.page_url(number=4), HTTP_X_BOOK_TOKEN=token).status_code, 200)

    @override_settings(BOOK_READER_REQUESTS_PER_MINUTE=1)
    def test_bulk_page_requests_are_limited(self):
        token = self.token()
        self.assertEqual(self.client.get(self.page_url(), HTTP_X_BOOK_TOKEN=token).status_code, 200)
        limited = self.client.get(self.page_url(), HTTP_X_BOOK_TOKEN=token)
        self.assertEqual(limited.status_code, 429)
        self.assertEqual(limited['Retry-After'], '60')

    def test_original_and_generated_pdf_files_have_no_public_routes(self):
        for url in [f'/private/books/{self.book.fayl}', f'/media/{self.book.fayl}',
                    f'/static/{self.book.fayl}', '/kitoblar/2/body.pdf',
                    f'/kutubxona/{self.book.pk}/download/', f'/kutubxona/{self.book.pk}/book.pdf']:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 404)

    def test_private_asset_rejects_path_traversal(self):
        for path in ['../secret.pdf', str(Path(self.temp.name) / 'outside.pdf')]:
            with self.assertRaises(SuspiciousFileOperation):
                private_asset(path)

    def test_public_storage_configuration_is_rejected(self):
        with override_settings(PRIVATE_BOOKS_ROOT=Path(settings.MEDIA_ROOT) / 'books'):
            self.assertEqual(private_books_location(None)[0].id, 'home.E001')
