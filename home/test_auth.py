from django.conf import settings
from django.test import Client, TestCase
from django.urls import reverse

from .models import Kitob, User


class LogoutCsrfTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='logout-reader', password='test-password')
        cls.book = Kitob.objects.create(
            manba='logout-test', nom='Test kitob', sahifalar=1,
            fayl='private-test/book.pdf', muqova='private-test/cover.webp',
            fingerprint='a' * 64,
        )

    def signed_in_client(self, source='kutubxona', secure=False):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.user)
        args = [self.book.pk] if source == 'kitob_oqish' else []
        response = client.get(reverse(source, args=args), secure=secure)
        self.assertContains(response, 'csrfmiddlewaretoken')
        return client, client.cookies[settings.CSRF_COOKIE_NAME].value, response

    def test_book_html_allows_same_origin_form_submissions(self):
        for source in ['kutubxona', 'kitob_oqish']:
            with self.subTest(source=source):
                _, _, response = self.signed_in_client(source)
                self.assertEqual(response['Referrer-Policy'], 'same-origin')
                self.assertEqual(response['Cross-Origin-Resource-Policy'], 'same-origin')
                self.assertIn('no-store', response['Cache-Control'])

    def test_logout_from_home_library_and_reader_with_valid_csrf(self):
        for source in ['home', 'kutubxona', 'kitob_oqish']:
            with self.subTest(source=source):
                client, token, _ = self.signed_in_client(source)
                response = client.post(reverse('logout'), {'csrfmiddlewaretoken': token},
                                       HTTP_ORIGIN='http://testserver')
                self.assertRedirects(response, reverse('login'))
                self.assertNotIn('_auth_user_id', client.session)

    def test_https_logout_accepts_same_origin(self):
        client, token, _ = self.signed_in_client(secure=True)
        response = client.post(reverse('logout'), {'csrfmiddlewaretoken': token},
                               secure=True, HTTP_ORIGIN='https://testserver')
        self.assertRedirects(response, reverse('login'))
        self.assertNotIn('_auth_user_id', client.session)

    def test_https_logout_accepts_same_origin_referer_without_origin(self):
        client, token, _ = self.signed_in_client(secure=True)
        response = client.post(reverse('logout'), {'csrfmiddlewaretoken': token},
                               secure=True, HTTP_REFERER='https://testserver/kutubxona/')
        self.assertRedirects(response, reverse('login'))
        self.assertNotIn('_auth_user_id', client.session)

    def test_null_and_foreign_origins_remain_blocked_with_valid_token(self):
        for origin in ['null', 'https://untrusted.example']:
            with self.subTest(origin=origin):
                client, token, _ = self.signed_in_client()
                response = client.post(reverse('logout'), {'csrfmiddlewaretoken': token},
                                       HTTP_ORIGIN=origin)
                self.assertEqual(response.status_code, 403)
                self.assertEqual(client.session['_auth_user_id'], str(self.user.pk))

    def test_missing_or_incorrect_token_remains_blocked(self):
        for token in ['', 'b' * 32]:
            with self.subTest(token=token):
                client, _, _ = self.signed_in_client()
                response = client.post(reverse('logout'), {'csrfmiddlewaretoken': token},
                                       HTTP_ORIGIN='http://testserver')
                self.assertEqual(response.status_code, 403)
                self.assertEqual(client.session['_auth_user_id'], str(self.user.pk))

    def test_get_logout_does_not_change_the_session(self):
        client, _, _ = self.signed_in_client()
        response = client.get(reverse('logout'))
        self.assertEqual(response.status_code, 405)
        self.assertEqual(client.session['_auth_user_id'], str(self.user.pk))
