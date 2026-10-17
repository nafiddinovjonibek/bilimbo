"""Narakeet'ning qisqa matn API si orqali Odina MP3 faylini yaratish."""

import asyncio

from django.conf import settings


API_URL = 'https://api.narakeet.com/text-to-speech/mp3'


class NarakeetConfigurationError(ValueError):
    pass


class NarakeetError(RuntimeError):
    pass


def api_key():
    return (getattr(settings, 'NARAKEET_API_KEY', '') or '').strip()


def require_api_key():
    key = api_key()
    if not key:
        raise NarakeetConfigurationError(
            'Odina uchun NARAKEET_API_KEY sozlanmagan. Kalitni loyiha .env fayliga qo‘ying.')
    return key


async def save_audio(text, destination, rate, timeout):
    import aiohttp

    key = require_api_key()
    body = text.encode('utf-8')
    if len(body) > 1024:
        raise NarakeetConfigurationError('Odina uchun ovoz matni 1024 baytdan oshmasligi kerak.')
    speed = 1 + int(rate[:-1]) / 100
    if speed <= 0:
        raise NarakeetConfigurationError('Odina ovozining tezligi noldan katta bo‘lishi kerak.')

    headers = {'x-api-key': key, 'Content-Type': 'text/plain; charset=utf-8',
               'Accept': 'application/octet-stream'}
    params = {'voice': 'odina', 'voice-speed': f'{speed:.2f}'}
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as session:
            # Kalit faqat rasmiy API ga yuboriladi, boshqa manzilga redirect qilinmaydi.
            async with session.post(API_URL, data=body, headers=headers, params=params,
                                    allow_redirects=False) as response:
                if response.status != 200:
                    raise NarakeetError(
                        f'Narakeet HTTP {response.status} qaytardi. API kaliti va hisobni tekshiring.')
                content_type = response.headers.get('Content-Type', '').split(';')[0].lower()
                if content_type not in ('audio/mpeg', 'audio/mp3', 'application/octet-stream'):
                    raise NarakeetError('Narakeet MP3 o‘rniga boshqa turdagi javob qaytardi.')
                with destination.open('wb') as file:
                    async for chunk in response.content.iter_chunked(16384):
                        file.write(chunk)
        with destination.open('rb') as file:
            prefix = file.read(3)
        if not (prefix.startswith(b'ID3') or
                len(prefix) >= 2 and prefix[0] == 0xff and prefix[1] & 0xe0 == 0xe0):
            raise NarakeetError('Narakeet bo‘sh yoki yaroqsiz MP3 qaytardi.')
    except (aiohttp.ClientError, asyncio.TimeoutError):
        # Pullik so'rov natijasi noma'lum bo'lishi mumkin: avtomatik takrorlanmaydi.
        raise NarakeetError(
            'Narakeet so‘rovining natijasi aniqlanmadi. Avtomatik takroriy so‘rov yuborilmadi.') from None
