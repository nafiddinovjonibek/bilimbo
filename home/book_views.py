import time
from functools import wraps

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET

from .books import private_asset, reader_token, valid_reader_token, watermarked_page
from .models import Kitob


def protected_book_view(view):
    @wraps(view)
    @never_cache
    def protected(request, *args, **kwargs):
        response = view(request, *args, **kwargs)
        response['X-Content-Type-Options'] = 'nosniff'
        # Same-origin form submissions (including logout) need their real Origin.
        # External sites still receive no referrer information.
        response['Referrer-Policy'] = 'same-origin'
        response['Cross-Origin-Resource-Policy'] = 'same-origin'
        response['X-Frame-Options'] = 'DENY'
        response['X-Robots-Tag'] = 'noindex, noarchive, noimageindex'
        return response
    return protected


@protected_book_view
@login_required
@require_GET
def kutubxona(request):
    return render(request, 'kitoblar/index.html', {'kitoblar': Kitob.objects.filter(faol=True)})


@protected_book_view
@login_required
@require_GET
def kitob_oqish(request, pk):
    book = get_object_or_404(Kitob, pk=pk, faol=True)
    return render(request, 'kitoblar/oqish.html', {
        'kitob': book,
        'reader_config': {
            'pageUrl': reverse('kitob_sahifa', args=[book.pk, 1]),
            'token': reader_token(request, book),
            'pages': book.sahifalar,
        },
    })


@protected_book_view
@login_required
@require_GET
def kitob_muqova(request, pk):
    book = get_object_or_404(Kitob, pk=pk, faol=True)
    try:
        data = private_asset(book.muqova).read_bytes()
    except FileNotFoundError:
        raise Http404 from None
    return HttpResponse(data, content_type='image/webp')


@protected_book_view
@login_required
@require_GET
def kitob_sahifa(request, pk, number):
    book = get_object_or_404(Kitob, pk=pk, faol=True)
    if request.headers.get('Sec-Fetch-Site') in {'cross-site', 'same-site'}:
        return HttpResponse(status=403)
    if not valid_reader_token(request, book, request.headers.get('X-Book-Token', '')):
        return HttpResponse(status=403)
    if not 1 <= number <= book.sahifalar:
        raise Http404

    # A shared cache (Redis/Memcached) is required when running multiple workers.
    key = f'book-pages:{request.user.pk}:{int(time.time() // 60)}'
    cache.add(key, 0, timeout=65)
    try:
        count = cache.incr(key)
    except ValueError:
        cache.set(key, 1, timeout=65)
        count = 1
    if count > settings.BOOK_READER_REQUESTS_PER_MINUTE:
        response = HttpResponse(status=429)
        response['Retry-After'] = '60'
        return response
    try:
        data = watermarked_page(book, number, request.user.pk)
    except (FileNotFoundError, IndexError):
        raise Http404 from None
    return HttpResponse(data, content_type='image/webp')
