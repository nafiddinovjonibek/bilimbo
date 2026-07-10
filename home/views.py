from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from .forms import LoginForm, RegisterForm
from .models import Bolim, Bolimcha, Savol, SavolNatija


def home(request):
    bolimlar = Bolim.objects.all() if request.user.is_authenticated else None
    return render(request, 'index.html', {'bolimlar': bolimlar})


@login_required
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
            'max_yulduz': sub.savollar.count() * 3,
        })
    return render(request, 'bolim.html', {'bolim': bolim, 'items': items})


@login_required
def bolimcha(request, pk):
    sub = get_object_or_404(Bolimcha, pk=pk)
    natijalar = {
        n.savol_id: n.stars
        for n in SavolNatija.objects.filter(user=request.user, savol__bolimcha=sub)
    }
    savollar = []
    ochiq = True
    for s in sub.savollar.all():
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


@login_required
def savol(request, pk):
    savol = get_object_or_404(Savol, pk=pk)

    # Bosqichlilik: oldingi savollar yechilmagan bo'lsa, xaritaga qaytaramiz
    oldingi_yechilmagan = (
        savol.bolimcha.savollar
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
        javob = request.POST.get('javob')
        urinishlar += 1
        if javob == savol.togri_javob:
            stars = max(4 - urinishlar, 1)
            request.session.pop(session_key, None)
            natija = SavolNatija.objects.filter(user=request.user, savol=savol).first()
            if natija is None:
                SavolNatija.objects.create(user=request.user, savol=savol, stars=stars)
            elif stars > natija.stars:
                natija.stars = stars
                natija.save()
            next_savol = savol.bolimcha.savollar.filter(order__gt=savol.order).first()
            return render(request, 'savol.html', {
                'savol': savol,
                'yutuq': True,
                'stars': stars,
                'stars_str': '⭐' * stars,
                'next_savol': next_savol,
            })
        request.session[session_key] = urinishlar
        xato = True

    potentsial = max(3 - urinishlar, 1)
    return render(request, 'savol.html', {
        'savol': savol,
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


def logout_view(request):
    logout(request)
    return redirect('login')
