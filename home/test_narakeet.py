import asyncio
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from unittest.mock import patch

from django.test import SimpleTestCase, override_settings

from .narakeet import NarakeetError, save_audio


@override_settings(NARAKEET_API_KEY='test-only-key')
class NarakeetApiTests(SimpleTestCase):
    def request_audio(self, status, content_type, payload):
        calls = []

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def do_POST(self):
                length = int(self.headers['Content-Length'])
                calls.append({'query': parse_qs(urlparse(self.path).query),
                              'key': self.headers.get('x-api-key'),
                              'accept': self.headers.get('Accept'),
                              'content_type': self.headers.get('Content-Type'),
                              'body': self.rfile.read(length)})
                self.send_response(status)
                self.send_header('Content-Type', content_type)
                self.send_header('Content-Length', str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)

        server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with tempfile.TemporaryDirectory() as directory:
                destination = Path(directory) / 'test.mp3'
                endpoint = f'http://127.0.0.1:{server.server_port}/text-to-speech/mp3'
                with patch('home.narakeet.API_URL', endpoint):
                    asyncio.run(save_audio('Oʻn ikki gʻisht.', destination, '+0%', timeout=5))
                data = destination.read_bytes()
                return calls, data
        finally:
            server.shutdown()
            server.server_close()

    def test_request_uses_odina_utf8_body_and_header_authentication(self):
        payload = b'ID3' + bytes(2048)
        calls, result = self.request_audio(200, 'audio/mpeg', payload)
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0]['query'], {'voice': ['odina'], 'voice-speed': ['1.00']})
        self.assertEqual(calls[0]['key'], 'test-only-key')
        self.assertEqual(calls[0]['accept'], 'application/octet-stream')
        self.assertTrue(calls[0]['content_type'].startswith('text/plain'))
        self.assertEqual(calls[0]['body'], 'Oʻn ikki gʻisht.'.encode('utf-8'))
        self.assertEqual(result, payload)

    def test_empty_audio_and_json_cannot_be_saved_as_mp3(self):
        for mime, data in [('audio/mpeg', b''), ('application/json', b'{"result": "error"}')]:
            with self.subTest(mime=mime):
                with self.assertRaises(NarakeetError):
                    self.request_audio(200, mime, data)

    def test_provider_error_does_not_expose_its_response_body_or_credentials(self):
        with self.assertRaises(NarakeetError) as caught:
            self.request_audio(403, 'application/json', b'{"message":"test-only-key"}')
        self.assertNotIn('test-only-key', str(caught.exception))
        self.assertIn('HTTP 403', str(caught.exception))
