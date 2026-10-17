"""Assemble supplied cover, body and barcode into a private book library."""

import hashlib
import io
import json
import re
import tempfile
from pathlib import Path

import pypdfium2 as pdfium
from PIL import Image
from pypdf import PdfReader, PdfWriter, Transformation

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from home.books import PDFIUM_LOCK, private_asset, render_pdf_page
from home.models import Kitob


BUILD_VERSION = b'bilimbo-private-book-v1'
COVER_NAMES = {'обложка', 'muqova', 'cover'}


def stamp_barcode(back, cover_path, barcode_path):
    width, height = float(back.mediabox.width), float(back.mediabox.height)
    with Image.open(barcode_path) as barcode:
        barcode_pdf = io.BytesIO()
        barcode.convert('RGB').save(barcode_pdf, format='PDF', resolution=72)
        aspect = barcode.height / barcode.width
    # Existing cover PDFs already have a barcode placeholder. Replace it exactly.
    barcode_width = width * .27
    bounds = ((width - barcode_width) / 2, height * .12,
              (width + barcode_width) / 2, height * .12 + barcode_width * aspect)
    with PDFIUM_LOCK, pdfium.PdfDocument(cover_path) as document:
        page = document[1]
        try:
            candidates = []
            for obj in page.get_objects():
                if obj.type != 3:
                    continue
                left, bottom, right, top = obj.get_bounds()
                image_width, image_height = right - left, top - bottom
                if (0 < image_width < width * .8 and 0 < image_height < height * .3
                        and bottom < height * .4
                        and abs(image_width / image_height - 1 / aspect) <= .25 / aspect):
                    candidates.append((left, bottom, right, top))
            if len(candidates) == 1:
                bounds = candidates[0]
        finally:
            page.close()
    left, bottom, right, top = bounds
    overlay = PdfReader(barcode_pdf).pages[0]
    overlay.add_transformation(Transformation().scale(
        (right - left) / float(overlay.mediabox.width),
        (top - bottom) / float(overlay.mediabox.height),
    ).translate(left, bottom))
    # The transformed barcode must also expand its crop box for merge_page.
    overlay.mediabox = back.mediabox
    overlay.cropbox = back.cropbox
    back.merge_page(overlay)


def assemble_book(cover_path, body_path, barcode_path, target, title):
    body = PdfReader(body_path)
    cover = PdfReader(cover_path) if cover_path else None
    if not body.pages or (cover and len(cover.pages) != 2):
        raise ValueError('Muqova 2 sahifa, kitob esa kamida 1 sahifa bo‘lishi kerak.')
    if cover and barcode_path:
        stamp_barcode(cover.pages[1], cover_path, barcode_path)
    with PdfWriter() as writer:
        if cover:
            writer.add_page(cover.pages[0], excluded_keys=('/Annots', '/AA'))
        for page in body.pages:
            writer.add_page(page, excluded_keys=('/Annots', '/AA'))
        if cover:
            writer.add_page(cover.pages[1], excluded_keys=('/Annots', '/AA'))
        writer.add_metadata({'/Title': title, '/Producer': 'Bilimbo'})
        writer.write(target)
    return len(body.pages) + (2 if cover else 0)


def book_folders(source):
    """Descend through collection folders, retaining incomplete leaf folders for validation."""
    children = list(source.iterdir())
    if any(path.is_file() and path.suffix.lower() == '.pdf' for path in children):
        return [source]
    directories = sorted((path for path in children if path.is_dir()), key=lambda path: path.name)
    result = []
    for directory in directories:
        nested = book_folders(directory)
        result.extend(nested or [directory])
    return result


def source_key(folder, source):
    library = (settings.BASE_DIR / 'kitoblar').resolve()
    if folder.is_relative_to(library):
        return folder.relative_to(library).as_posix()
    return folder.relative_to(source).as_posix() if folder != source else folder.name


def source_sort_key(key):
    return tuple((0, int(part)) if part.isdigit() else (1, part.casefold())
                 for part in key.split('/'))


class Command(BaseCommand):
    help = 'Kitob, old/orqa muqova va shtrix-kodni yopiq kutubxonaga qo‘shadi.'

    def add_arguments(self, parser):
        parser.add_argument('--source', type=Path, default=settings.BASE_DIR / 'kitoblar')
        parser.add_argument('--dry-run', action='store_true', help='Fayllarni tekshiradi; hech narsa yozmaydi.')
        parser.add_argument('--force', action='store_true', help='Tayyor fayllarni qayta yig‘adi.')

    def handle(self, *args, **options):
        source = Path(options['source']).resolve()
        if not source.is_dir():
            raise CommandError(f'Manba papkasi topilmadi: {source}')
        metadata = json.loads((settings.BASE_DIR / 'home/data/kitoblar.json').read_text(encoding='utf8'))
        folders = sorted(book_folders(source), key=lambda path: source_sort_key(source_key(path, source)))
        if not folders:
            raise CommandError('Manba papkasida kitob to‘plamlari yo‘q.')
        planned, aliases, barcode_hashes = [], [], {}
        # Validate every folder before changing the library.
        for folder in folders:
            key = source_key(folder, source)
            info = metadata.get(key, {})
            pdfs = sorted(p for p in folder.iterdir() if p.is_file() and p.suffix.lower() == '.pdf')
            if info.get('duplicate_of'):
                if (len(pdfs) != 1 or hashlib.sha256(pdfs[0].read_bytes()).hexdigest()
                        != info.get('duplicate_sha256')):
                    raise CommandError(f'{key}: takroriy nusxa o‘zgargan; manba ma’lumotlarini tekshiring.')
                aliases.append((key, info['duplicate_of']))
                continue
            covers = [p for p in pdfs if re.sub(r'\s*\(\d+\)$', '', p.stem.casefold()).strip() in COVER_NAMES]
            barcodes = [p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in {'.jpg', '.jpeg', '.png'}]
            try:
                counts = {path: len(PdfReader(path).pages) for path in pdfs}
                # Some supplied covers are named after the book instead of "muqova".
                if not covers and len(pdfs) == 2:
                    covers = [path for path in pdfs if counts[path] == 2]
                bodies = [p for p in pdfs if p not in covers]
                if len(covers) > 1 or len(bodies) != 1 or len(barcodes) > 1:
                    raise ValueError('1 ta kitob PDF, ixtiyoriy 2 sahifali muqova va shtrix-kod rasmi kerak.')
                cover, body = covers[0] if covers else None, bodies[0]
                barcode = barcodes[0] if barcodes else None
                if not counts[body] or (cover and counts[cover] != 2):
                    raise ValueError('Muqova 2 sahifali bo‘lishi kerak.')
                if barcode:
                    if not cover:
                        raise ValueError('Alohida shtrix-kod uchun old/orqa muqova PDF ham kerak.')
                    with Image.open(barcode) as image:
                        image.verify()
            except Exception as exc:
                raise CommandError(f'{key}: fayl yaroqsiz: {exc}') from exc
            digest = hashlib.sha256(BUILD_VERSION)
            for path in (cover, body, barcode):
                if path:
                    digest.update(hashlib.sha256(path.read_bytes()).digest())
            fingerprint = digest.hexdigest()
            if barcode:
                barcode_hashes.setdefault(hashlib.sha256(barcode.read_bytes()).hexdigest(), []).append(key)
            planned.append((key, folder, cover, body, barcode, fingerprint, info))

        planned_keys = {row[0] for row in planned}
        for key, canonical in aliases:
            if canonical not in planned_keys and not Kitob.objects.filter(manba=canonical).exists():
                raise CommandError(f'{key}: asosiy nusxa {canonical} topilmadi.')
            self.stdout.write(self.style.WARNING(f'Takroriy nusxa: {key} → {canonical}; katalogda takrorlanmaydi.'))

        for duplicates in barcode_hashes.values():
            if len(duplicates) > 1:
                self.stdout.write(self.style.WARNING(
                    f'Bir xil shtrix-kod: {", ".join(duplicates)}. Berilgan rasmlar saqlanadi.'))

        for key, folder, cover, body, barcode, fingerprint, info in planned:
            if options['dry_run']:
                self.stdout.write(f'Tekshirildi: {key} — {body.name}')
                continue
            directory = f'{hashlib.sha256(key.encode()).hexdigest()[:12]}-{fingerprint[:16]}'
            pdf_name, cover_name = f'{directory}/book.pdf', f'{directory}/cover.webp'
            existing = Kitob.objects.filter(manba=key).first()
            if (not options['force'] and existing and existing.fingerprint == fingerprint
                    and private_asset(pdf_name).is_file() and private_asset(cover_name).is_file()):
                self.stdout.write(f'Avval qo‘shilgan: {existing.nom}')
                continue
            title = info.get('nom', body.stem.replace('_', ' '))
            destination = private_asset(directory)
            destination.mkdir(parents=True, exist_ok=True)
            try:
                with tempfile.TemporaryDirectory(dir=settings.PRIVATE_BOOKS_ROOT) as temp:
                    temp = Path(temp)
                    count = assemble_book(cover, body, barcode, temp / 'book.pdf', title)
                    image = render_pdf_page(temp / 'book.pdf', 0, max_size=720)
                    image.save(temp / 'cover.webp', format='WEBP', quality=88)
                    for name in ('book.pdf', 'cover.webp'):
                        (temp / name).replace(destination / name)
                with transaction.atomic():
                    book, created = Kitob.objects.get_or_create(manba=key, defaults={
                        'nom': title, 'mualliflar': info.get('mualliflar', ''),
                        'order': info.get('order', int(folder.name) if folder.name.isdigit() else 0),
                        'sahifalar': count, 'fayl': pdf_name, 'muqova': cover_name,
                        'fingerprint': fingerprint,
                    })
                    if not created:
                        book.sahifalar, book.fayl, book.muqova, book.fingerprint = count, pdf_name, cover_name, fingerprint
                        book.save(update_fields=['sahifalar', 'fayl', 'muqova', 'fingerprint'])
            except Exception as exc:
                raise CommandError(f'{key}: kitob yig‘ilmadi: {exc}') from exc
            self.stdout.write(self.style.SUCCESS(f'Qo‘shildi: {book.nom} ({count} sahifa)'))
        self.stdout.write(self.style.SUCCESS(f'Jami: {len(planned)} ta kitob, {len(aliases)} ta takroriy nusxa.'))
