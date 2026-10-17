import hashlib
import shutil
import tempfile
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from home.models import OvozJavob


class Command(BaseCommand):
    help = 'Mavjud ovozli javoblarni media papkasidan yopiq saqlashga o‘tkazadi.'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true')

    def handle(self, *args, **options):
        public_root = Path(settings.MEDIA_ROOT).resolve()
        private_root = Path(settings.PRIVATE_VOICES_ROOT).resolve()
        if private_root.is_relative_to(public_root) or public_root.is_relative_to(private_root):
            raise CommandError('Ovoz uchun yopiq papka media papkasidan alohida bo‘lishi kerak.')
        plans, ready, missing = [], 0, 0
        for name in OvozJavob.objects.exclude(fayl='').values_list('fayl', flat=True).distinct():
            source = (public_root / name).resolve()
            destination = (private_root / name).resolve()
            if (not source.is_relative_to(public_root) or source == public_root
                    or not destination.is_relative_to(private_root) or destination == private_root):
                raise CommandError('Ovoz fayli yo‘li saqlash papkasidan tashqariga chiqdi.')
            if not source.is_file():
                if destination.is_file():
                    ready += 1
                else:
                    missing += 1
                continue
            digest = hashlib.sha256(source.read_bytes()).digest()
            if destination.exists() and hashlib.sha256(destination.read_bytes()).digest() != digest:
                raise CommandError('Yopiq papkadagi fayl bilan eski ovoz fayli bir xil emas. Ko‘chirish to‘xtatildi.')
            plans.append((source, destination, digest))
        if options['dry_run']:
            self.stdout.write(f'Ko‘chiriladi: {len(plans)}; avval ko‘chirilgan: {ready}; topilmagan: {missing}.')
            return
        for source, destination, digest in plans:
            destination.parent.mkdir(parents=True, exist_ok=True)
            if not destination.exists():
                with tempfile.NamedTemporaryFile(dir=destination.parent, delete=False) as stream:
                    temporary = Path(stream.name)
                try:
                    shutil.copyfile(source, temporary)
                    if hashlib.sha256(temporary.read_bytes()).digest() != digest:
                        raise CommandError('Ko‘chirilgan ovoz fayli tekshiruvdan o‘tmadi.')
                    temporary.replace(destination)
                finally:
                    temporary.unlink(missing_ok=True)
            # Only the verified public copy is removed. Record paths stay unchanged.
            if hashlib.sha256(destination.read_bytes()).digest() != digest:
                raise CommandError('Yopiq ovoz fayli o‘zgargan; ommaviy nusxa saqlandi.')
            source.unlink()
        self.stdout.write(self.style.SUCCESS(
            f'Yopiq saqlashga o‘tkazildi: {len(plans)}; tayyor: {ready}; topilmagan: {missing}.'))
