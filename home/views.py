import random
from collections import Counter
from datetime import timedelta

from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.decorators.cache import never_cache

from .forms import LoginForm, RegisterForm
from .decorators import oquvchi_required
from .models import Bolim, Bolimcha, OvozJavob, Savol, SavolNatija


def _seriya(kunlar):
    """Bugundan (yoki kechadan) orqaga qarab uzluksiz kunlar soni."""
    if not kunlar:
        return 0
    bugun = timezone.localdate()
    oxirgi = max(kunlar)
    # Bugun hali o'ynamagan bo'lsa ham, kechagi seriya uzilmagan hisoblanadi
    if (bugun - oxirgi).days > 1:
        return 0
    n = 1
    kun = oxirgi
    while kun - timedelta(days=1) in kunlar:
        kun -= timedelta(days=1)
        n += 1
    return n


@never_cache
def home(request):
    if not request.user.is_authenticated:
        return render(request, 'index.html', {'bolimlar': None})
    if request.user.is_superadmin or request.user.is_tarbiyachi:
        if request.user.is_tarbiyachi and not request.user.is_approved_teacher:
            return render(request, 'portal/kutilmoqda.html')
        return redirect('kabinet')

    bolimlar = Bolim.objects.prefetch_related('bolimchalar')
    natijalar = SavolNatija.objects.filter(user=request.user)

    # Tugatilgan bo'limcha = undagi barcha topshiriq yechilgan
    yechilgan = Counter(
        natijalar.values_list('savol__bolimcha_id', flat=True))
    jami = dict(
        Bolimcha.objects
        .filter(savollar__kvest__isnull=True)
        .annotate(n=Count('savollar'))
        .values_list('id', 'n')
    )
    yutuqlar = sum(1 for pk, n in jami.items() if n and yechilgan.get(pk, 0) >= n)

    return render(request, 'index.html', {
        'bolimlar': bolimlar,
        'guruh': request.user.guruh,
        'yutuqlar': yutuqlar,
        'ballar': natijalar.aggregate(j=Sum('stars'))['j'] or 0,
        'seriya': _seriya({
            timezone.localtime(v).date()
            for v in natijalar.values_list('updated_at', flat=True)
        }),
    })


def _asosiy_savollar(sub):
    """Bo'limchaning savollari — kvest ichidagi bosqichlar bundan tashqarida."""
    return sub.savollar.filter(kvest__isnull=True)


@never_cache
@oquvchi_required
def bolim(request, num):
    bolim = get_object_or_404(Bolim, order=num)
    items = []
    for sub in bolim.bolimchalar.all():
        jami = SavolNatija.objects.filter(
            user=request.user, savol__bolimcha=sub,
        ).aggregate(total=Sum('stars'))['total'] or 0
        items.append({
            'sub': sub,
            'jami_yulduz': jami,
            'max_yulduz': _asosiy_savollar(sub).count() * 3,
        })
    return render(request, 'bolim.html', {'bolim': bolim, 'items': items})


@never_cache
@oquvchi_required
def bolimcha(request, pk):
    sub = get_object_or_404(Bolimcha, pk=pk)
    natijalar = {
        n.savol_id: n.stars
        for n in SavolNatija.objects.filter(user=request.user, savol__bolimcha=sub)
    }
    savollar = []
    ochiq = True
    for s in _asosiy_savollar(sub):
        stars = natijalar.get(s.pk)
        hozirgi = stars is None and ochiq
        savollar.append({
            'savol': s,
            'stars': stars,
            'stars_str': '⭐' * (stars or 0),
            'ochiq': ochiq,
            'hozirgi': hozirgi,
        })
        if hozirgi:
            ochiq = False
    return render(request, 'bolimcha.html', {
        'bolimcha': sub,
        'savollar': savollar,
        'jami_yulduz': sum(natijalar.values()),
        'max_yulduz': len(savollar) * 3,
    })


def _oyin_holati(savol, seed):
    """Shablon uchun topshiriqni o'ynaladigan ko'rinishga keltiradi.

    `seed` — urinishlar davomida aralashtirish tartibi o'zgarmasligi uchun.
    """
    variantlar = list(savol.variantlar.all())
    rnd = random.Random(f'{savol.pk}-{seed}')

    holat = {'savol': savol, 'variantlar': variantlar}

    if savol.tur == Savol.Tur.TARTIB:
        aralash = variantlar[:]
        rnd.shuffle(aralash)
        # Tasodifan to'g'ri tartibda chiqib qolmasin
        if len(aralash) > 1 and aralash == variantlar:
            aralash.reverse()
        holat['variantlar'] = aralash

    elif savol.tur == Savol.Tur.MOSLASH:
        juftlar = variantlar[:]
        rnd.shuffle(juftlar)
        holat['juftlar'] = juftlar

    elif savol.tur == Savol.Tur.GURUH:
        # Savatlar variantlardagi juftlik matnidan olinadi (birinchi uchrashi bo'yicha)
        savatlar = []
        korilgan = set()
        for v in variantlar:
            if v.juft_matn not in korilgan:
                korilgan.add(v.juft_matn)
                savatlar.append({'nom': v.juft_matn, 'rasm': v.juft_rasm})
        holat['savatlar'] = savatlar
        aralash = variantlar[:]
        rnd.shuffle(aralash)
        holat['variantlar'] = aralash

    elif savol.tur == Savol.Tur.QURISH:
        # Uyalar namunadagi tartibda, bo'laklar esa savatda aralashtirilgan holda
        holat['uyalar'] = sorted(variantlar, key=lambda v: v.togri_order or 0)
        bolaklar = [v for v in variantlar if not v.oldindan]
        rnd.shuffle(bolaklar)
        holat['bolaklar'] = bolaklar

    elif savol.tur == Savol.Tur.KVEST:
        holat['bosqichlar'] = [
            _oyin_holati(b, seed) for b in savol.bosqichlar.all()
        ]

    return holat


def _ovozni_saqla(request, savol):
    """Mikrofonli topshiriqda yozilgan ovozni saqlaydi (bo'lsa)."""
    for s in [savol, *savol.bosqichlar.all()]:
        if s.tur != Savol.Tur.MIKROFON:
            continue
        fayl = request.FILES.get(f'ovoz_fayl_{s.pk}')
        if fayl:
            OvozJavob.objects.create(user=request.user, savol=s, fayl=fayl)


@never_cache
@oquvchi_required
def savol(request, pk):
    savol = get_object_or_404(Savol, pk=pk, kvest__isnull=True)

    # Bosqichlilik: oldingi savollar yechilmagan bo'lsa, xaritaga qaytaramiz
    oldingi_yechilmagan = (
        _asosiy_savollar(savol.bolimcha)
        .filter(order__lt=savol.order)
        .exclude(natijalar__user=request.user)
        .exists()
    )
    if oldingi_yechilmagan:
        return redirect('bolimcha', pk=savol.bolimcha.pk)

    session_key = f'urinish_{savol.pk}'
    urinishlar = request.session.get(session_key, 0)
    xato = False

    if request.method == 'POST':
        urinishlar += 1
        if savol.tekshir(request.POST):
            _ovozni_saqla(request, savol)
            stars = max(4 - urinishlar, 1)
            request.session.pop(session_key, None)
            natija = SavolNatija.objects.filter(user=request.user, savol=savol).first()
            if natija is None:
                SavolNatija.objects.create(user=request.user, savol=savol, stars=stars)
            elif stars > natija.stars:
                natija.stars = stars
                natija.save()
            next_savol = (
                _asosiy_savollar(savol.bolimcha).filter(order__gt=savol.order).first()
            )
            return render(request, 'savol.html', {
                'savol': savol,
                'yutuq': True,
                'stars': stars,
                'stars_str': '⭐' * stars,
                'next_savol': next_savol,
            })
        request.session[session_key] = urinishlar
        xato = True

    holat = _oyin_holati(savol, urinishlar)
    potentsial = max(3 - urinishlar, 1)
    return render(request, 'savol.html', {
        'savol': savol,
        'h_self': holat,
        'bosqichlar': holat.get('bosqichlar', []),
        'xato': xato,
        'potentsial_str': '⭐' * potentsial,
    })


class UserLoginView(LoginView):
    template_name = 'auth/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'auth/register.html', {'form': form})


@require_POST
def logout_view(request):
    logout(request)
    return redirect('login')
