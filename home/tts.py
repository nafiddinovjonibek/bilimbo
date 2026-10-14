"""O'zbekcha savol ovozlarini oldindan yaratish va statik keshdan olish."""

import asyncio
import hashlib
import html
import json
import re
import tempfile
import unicodedata
from pathlib import Path

from django.conf import settings
from django.contrib.staticfiles import finders
from django.templatetags.static import static
from django.utils.html import strip_tags


VOICES = ('uz-UZ-MadinaNeural', 'uz-UZ-SardorNeural')
DEFAULT_VOICE = VOICES[0]
DEFAULT_RATE = '-10%'
EMOJI = re.compile('[\U0001f000-\U0001faff\u2190-\u2bff\ufe0f\u200d\u20e3]')
APOSTROPHES = "’‘'ʻʼ`"
ONES = ('nol', 'bir', 'ikki', 'uch', 'toʻrt', 'besh', 'olti', 'yetti', 'sakkiz', 'toʻqqiz')
TENS = ('', 'oʻn', 'yigirma', 'oʻttiz', 'qirq', 'ellik', 'oltmish', 'yetmish', 'sakson', 'toʻqson')


def number_words(number):
    if number < 10:
        return ONES[number]
    for value, name in ((10**12, 'trillion'), (10**9, 'milliard'),
                        (10**6, 'million'), (1000, 'ming'), (100, 'yuz')):
        if number >= value:
            quotient, remainder = divmod(number, value)
            result = f'{number_words(quotient)} {name}'
            return f'{result} {number_words(remainder)}' if remainder else result
    quotient, remainder = divmod(number, 10)
    return f'{TENS[quotient]} {ONES[remainder]}' if remainder else TENS[quotient]


def prepare_speech(text):
    """O' va g' saqlanadi; emoji, sonlar va bo'sh uyalar o'qishga moslanadi."""
    text = unicodedata.normalize('NFC', html.unescape(strip_tags(str(text or ''))))
    text = EMOJI.sub(' ', text)
    text = text.translate(str.maketrans({character: 'ʼ' for character in APOSTROPHES}))
    text = re.sub(r'([oOgG])ʼ', r'\1ʻ', text)
    text = text.replace('«', '"').replace('»', '"')
    text = re.sub(r'_{2,}', ' boʻsh joy ', text)
    text = re.sub(r'\d+', lambda match: number_words(int(match.group())), text)
    text = re.sub(r'\s+([,.;:!?])', r'\1', text)
    return re.sub(r'\s+', ' ', text).strip()


def speech_profile(voice=None, rate=None):
    voice = voice or getattr(settings, 'BILIMBO_TTS_VOICE', DEFAULT_VOICE)
    rate = rate or getattr(settings, 'BILIMBO_TTS_RATE', DEFAULT_RATE)
    if voice not in VOICES:
        raise ValueError('Faqat Madina yoki Sardor o‘zbekcha ovozini tanlang.')
    if not re.fullmatch(r'[+-]\d{1,3}%', rate):
        raise ValueError('Ovoz tezligi +0% yoki -10% ko‘rinishida bo‘lishi kerak.')
    return voice, rate


def speech_path(text, voice=None, rate=None):
    voice, rate = speech_profile(voice, rate)
    prepared = prepare_speech(text)
    if not prepared:
        return ''
    # Tezlik, ovoz yoki matn o'zgarsa, brauzer yangi faylni oladi.
    key = json.dumps([1, voice, rate, prepared], ensure_ascii=False).encode('utf-8')
    digest = hashlib.sha256(key).hexdigest()[:32]
    return f'audio/tts/{voice}/{digest}.mp3'


def audio_ready(path):
    return path.is_file() and path.stat().st_size > 1024


def speech_url(text):
    """Bu funksiya tarmoqqa chiqmaydi va sahifa ochilishini kutdirmaydi."""
    relative = speech_path(text)
    if not relative:
        return ''
    found = finders.find(relative)
    return static(relative) if found and audio_ready(Path(found)) else ''


def question_texts(questions):
    """Hayvon tovushlari hech qachon TTS matni bilan almashtirilmaydi."""
    for question in questions:
        yield question.pk, 'savol', question.aytiladigan_matn
        if question.audio_matn and not question.audio_fayl:
            yield question.pk, 'audio', question.audio_matn


async def generate_speech(text, voice=None, rate=None, *, force=False,
                          timeout=30, attempts=2):
    """MP3 avval vaqtinchalik faylga yoziladi, so'ng atomik almashtiriladi."""
    voice, rate = speech_profile(voice, rate)
    relative = speech_path(text, voice, rate)
    if not relative:
        return '', False
    destination = settings.BASE_DIR / 'static' / relative
    if not force and audio_ready(destination):
        return relative, False

    # Saytning ishlashi uchun edge-tts o'rnatilgan bo'lishi shart emas.
    import edge_tts

    destination.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(attempts):
        with tempfile.NamedTemporaryFile(dir=destination.parent, suffix='.part', delete=False) as file:
            temporary = Path(file.name)
        try:
            speech = edge_tts.Communicate(prepare_speech(text), voice, rate=rate,
                                         connect_timeout=10, receive_timeout=20)
            await asyncio.wait_for(speech.save(str(temporary)), timeout=timeout)
            if not audio_ready(temporary):
                raise RuntimeError('TTS xizmati bo‘sh audio qaytardi.')
            temporary.replace(destination)
            return relative, True
        except Exception:
            if attempt + 1 == attempts:
                raise
            await asyncio.sleep(attempt + 1)
        finally:
            temporary.unlink(missing_ok=True)
