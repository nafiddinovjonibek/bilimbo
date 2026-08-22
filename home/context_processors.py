from django.utils import timezone


def kun_tuni(request):
    soat = timezone.localtime().hour
    tun = soat >= 19 or soat < 6
    return {'tun': tun}
