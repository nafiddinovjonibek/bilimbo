"""Private book assets. No view may return an original or assembled PDF."""

import hashlib
import io
import threading
from pathlib import Path

import pypdfium2 as pdfium
from PIL import Image, ImageDraw, ImageFont

from django.conf import settings
from django.core import signing
from django.core.exceptions import SuspiciousFileOperation
from django.utils import timezone


# PDFium must never run concurrently in threads, even for separate documents.
PDFIUM_LOCK = threading.RLock()
TOKEN_SALT = 'bilimbo.book-reader.v1'


def private_asset(relative):
    root = Path(settings.PRIVATE_BOOKS_ROOT).resolve()
    path = (root / relative).resolve()
    if not path.is_relative_to(root) or path == root:
        raise SuspiciousFileOperation('Kitob yo‘li yopiq papkadan tashqariga chiqdi.')
    return path


def render_pdf_page(path, index, max_size=1600):
    with PDFIUM_LOCK, pdfium.PdfDocument(path) as document:
        page = document[index]
        try:
            width, height = page.get_size()
            bitmap = page.render(scale=max_size / max(width, height))
            try:
                return bitmap.to_pil().convert('RGB')
            finally:
                bitmap.close()
        finally:
            page.close()


def _reader_identity(request, book):
    if not request.session.session_key:
        request.session.save()
    return {
        'book': book.pk,
        'version': book.fingerprint,
        'user': request.user.pk,
        'session': hashlib.sha256(request.session.session_key.encode()).hexdigest(),
    }


def reader_token(request, book):
    return signing.dumps(_reader_identity(request, book), salt=TOKEN_SALT)


def valid_reader_token(request, book, token):
    try:
        payload = signing.loads(token, salt=TOKEN_SALT, max_age=settings.BOOK_READER_TOKEN_AGE)
    except (signing.BadSignature, TypeError, ValueError):
        return False
    return payload == _reader_identity(request, book)


def watermarked_page(book, number, user_id):
    image = render_pdf_page(private_asset(book.fayl), number - 1)
    overlay = Image.new('RGBA', image.size)
    draw = ImageDraw.Draw(overlay)
    font = ImageFont.load_default(size=max(14, image.width // 55))
    label = f'Bilimbo | ID {user_id} | {timezone.localdate():%Y-%m-%d}'
    # Burn the mark into the pixels; removing a DOM overlay cannot remove it.
    for y in (image.height // 3, image.height * 2 // 3):
        draw.text((image.width // 7, y), label, font=font, fill=(65, 80, 130, 65))
    draw.text((18, image.height - 32), label, font=font, fill=(65, 80, 130, 150))
    marked = Image.alpha_composite(image.convert('RGBA'), overlay).convert('RGB')
    output = io.BytesIO()
    marked.save(output, format='WEBP', quality=88)
    return output.getvalue()
