import asyncio
import tempfile
from pathlib import Path
from unittest.mock import AsyncMock, patch

from django.contrib import admin, messages
from django.core.management import call_command
from django.template.loader import render_to_string
from django.test import SimpleTestCase, TestCase, override_settings

from .admin import SavolAdmin
from .models import Savol
from .tts import generate_speech, prepare_speech, question_texts, speech_path, speech_url
from .views import _oyin_holati


class SpeechCacheTests(SimpleTestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        (self.root / 'static').mkdir()
        override = override_settings(BASE_DIR=self.root, STATICFILES_DIRS=[self.root / 'static'],
                                     BILIMBO_TTS_VOICE='uz-UZ-MadinaNeural', BILIMBO_TTS_RATE='-10%')
        override.enable()
        self.addCleanup(override.disable)

    def test_uzbek_letters_numbers_and_blank_slots_are_spoken_correctly(self):
        self.assertEqual(prepare_speech("🔊 O‘yin: 12 ta g'isht, toʻrt oʼrindiq va __."),
                         'Oʻyin: oʻn ikki ta gʻisht, toʻrt oʻrindiq va boʻsh joy.')

    def test_changed_text_or_voice_cannot_return_old_audio(self):
        old = speech_path('Qizil olmani tanla.')
        target = self.root / 'static' / old
        target.parent.mkdir(parents=True)
        target.write_bytes(b'old audio' * 256)
        self.assertTrue(speech_url('Qizil olmani tanla.').endswith(old))
        self.assertEqual(speech_url('Yashil olmani tanla.'), '')
        with override_settings(BILIMBO_TTS_VOICE='uz-UZ-SardorNeural'):
            self.assertEqual(speech_url('Qizil olmani tanla.'), '')
        with override_settings(BILIMBO_TTS_RATE='-20%'):
            self.assertEqual(speech_url('Qizil olmani tanla.'), '')

    def test_repeated_generation_uses_cache_without_network(self):
        async def save(path):
            Path(path).write_bytes(b'new audio' * 256)

        with patch('edge_tts.Communicate') as communicate:
            communicate.return_value.save = AsyncMock(side_effect=save)
            first = asyncio.run(generate_speech('Olmani tanla.'))
            second = asyncio.run(generate_speech('Olmani tanla.'))
        self.assertTrue(first[1])
        self.assertEqual(second, (first[0], False))
        communicate.assert_called_once()

    def test_failed_regeneration_keeps_complete_audio_and_removes_partial_file(self):
        destination = self.root / 'static' / speech_path('Olmani tanla.')
        destination.parent.mkdir(parents=True)
        old_audio = b'complete audio' * 256
        destination.write_bytes(old_audio)

        async def fail(path):
            Path(path).write_bytes(b'incomplete')
            raise OSError('Tarmoq uzildi')

        with patch('edge_tts.Communicate') as communicate:
            communicate.return_value.save = AsyncMock(side_effect=fail)
            with self.assertRaises(OSError):
                asyncio.run(generate_speech('Olmani tanla.', force=True, attempts=1))
        self.assertEqual(destination.read_bytes(), old_audio)
        self.assertEqual(list(destination.parent.glob('*.part')), [])


class QuestionSpeechTests(TestCase):
    def test_real_sounds_are_not_synthesized_and_kvest_steps_are_included(self):
        texts = list(question_texts(Savol.objects.all()))
        spoken_questions = {pk for pk, kind, _ in texts if kind == 'savol'}
        self.assertEqual(spoken_questions, set(Savol.objects.values_list('pk', flat=True)))
        real_sounds = set(Savol.objects.exclude(audio_fayl='').values_list('pk', flat=True))
        self.assertTrue(real_sounds)
        self.assertFalse(any(pk in real_sounds and kind == 'audio' for pk, kind, _ in texts))

    def test_template_uses_cached_speech_and_separate_real_sound(self):
        question = Savol.objects.exclude(audio_fayl='').first()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            relative = speech_path(question.aytiladigan_matn)
            target = root / relative
            target.parent.mkdir(parents=True)
            target.write_bytes(b'audio' * 256)
            with override_settings(STATICFILES_DIRS=[root]):
                body = render_to_string('topshiriq/_topshiriq.html', {'h': _oyin_holati(question, 1)})
            self.assertIn(f'data-audio="/static/{relative}"', body)
            self.assertIn(f'data-play="/static/{question.audio_fayl}"', body)

    def test_command_includes_kvest_children(self):
        question = Savol.objects.filter(tur=Savol.Tur.KVEST).first()
        with tempfile.TemporaryDirectory() as directory, override_settings(BASE_DIR=Path(directory)):
            with patch('home.management.commands.generate_question_audio.generate_speech',
                       new=AsyncMock(return_value=('audio/tts/test.mp3', True))) as generate:
                call_command('generate_question_audio', ids=[question.pk], verbosity=0)
            self.assertEqual(generate.await_count, question.bosqichlar.count() + 1)

    def test_admin_reports_generation_failure_without_discarding_question(self):
        question = Savol.objects.first()
        question.ovoz_matn = 'Yangi savol saqlandi.'
        question.save(update_fields=['ovoz_matn'])
        model_admin = SavolAdmin(Savol, admin.site)
        with tempfile.TemporaryDirectory() as directory, override_settings(BASE_DIR=Path(directory)):
            with patch('home.admin.generate_speech', new=AsyncMock(side_effect=OSError('Tarmoq uzildi'))):
                with patch.object(model_admin, 'message_user') as message:
                    model_admin._prepare_audio(object(), [question])
        self.assertEqual(Savol.objects.get(pk=question.pk).ovoz_matn, 'Yangi savol saqlandi.')
        self.assertEqual(message.call_args.kwargs['level'], messages.WARNING)
