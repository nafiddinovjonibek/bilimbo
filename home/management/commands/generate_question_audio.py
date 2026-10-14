import asyncio
import html
import json

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from home.models import Savol
from home.tts import VOICES, generate_speech, prepare_speech, question_texts, speech_profile


class Command(BaseCommand):
    help = 'Savollarni o‘zbekcha MP3 qiladi; tayyor fayllarni qayta yaratmaydi.'

    def add_arguments(self, parser):
        parser.add_argument('--voice', choices=VOICES)
        parser.add_argument('--rate', help='Masalan: --rate=-10%%')
        parser.add_argument('--ids', nargs='+', type=int, help='Savol ID lari (kvest bosqichlari ham olinadi).')
        parser.add_argument('--limit', type=int)
        parser.add_argument('--samples', action='store_true', help='Ikkala ovozda uchta savol va tinglash sahifasi.')
        parser.add_argument('--force', action='store_true', help='Tayyor fayllarni ham qayta yaratish.')
        parser.add_argument('--jobs', type=int, default=3)

    def handle(self, *args, **options):
        if options['jobs'] < 1 or options['jobs'] > 8:
            raise CommandError('--jobs 1 dan 8 gacha bo‘lishi kerak.')
        if options['limit'] is not None and options['limit'] < 1:
            raise CommandError('--limit musbat son bo‘lishi kerak.')
        questions = Savol.objects.order_by('pk')
        if options['ids']:
            from django.db.models import Q
            questions = questions.filter(Q(pk__in=options['ids']) | Q(kvest_id__in=options['ids']))
        elif options['samples']:
            questions = questions.filter(kvest__isnull=True)
        limit = options['limit'] or (3 if options['samples'] else None)
        if limit:
            questions = questions[:limit]
        texts = list(question_texts(questions))
        if not texts:
            raise CommandError('Savollar topilmadi.')
        try:
            voice, rate = speech_profile(options['voice'], options['rate'])
            voices = VOICES if options['samples'] and not options['voice'] else (voice,)
            records = asyncio.run(self.generate(texts, voices, rate, options))
        except ImportError as error:
            raise CommandError('Avval pip install -r requirements.txt bajaring.') from error
        except ValueError as error:
            raise CommandError(str(error)) from error

        folder = settings.BASE_DIR / 'static/audio/tts'
        folder.mkdir(parents=True, exist_ok=True)
        if options['samples']:
            self.write_preview(folder, records)
        else:
            (folder / 'SAVOLLAR.json').write_text(
                json.dumps(records, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        failed = sum('error' in row for row in records)
        created = sum(row.get('created', False) for row in records)
        cached = len(records) - failed - created
        self.stdout.write(f'Yaratildi: {created}; tayyor: {cached}; xato: {failed}.')
        if failed:
            raise CommandError('Ayrim audiolar yaratilmagan. Qayta ishga tushiring: tayyorlari o‘tkazib yuboriladi.')
        self.stdout.write(self.style.SUCCESS('O‘zbekcha audiolar tayyor.'))

    async def generate(self, texts, voices, rate, options):
        semaphore = asyncio.Semaphore(options['jobs'])
        results = {}
        completed = 0

        async def make(text, voice):
            nonlocal completed
            async with semaphore:
                try:
                    path, created = await generate_speech(text, voice, rate, force=options['force'])
                    completed += 1
                    self.stdout.write(f'{completed}: {voice} — {"yaratildi" if created else "tayyor"}')
                    return {'path': path, 'created': created}
                except ImportError:
                    raise
                except Exception as error:
                    self.stderr.write(f'{voice}: {type(error).__name__}: {error}')
                    return {'error': f'{type(error).__name__}: {error}'}

        # Bir xil matn bir necha savolda ishlatilsa, faqat bir marta yaratiladi.
        for voice in voices:
            for _, _, text in texts:
                if (voice, text) not in results:
                    results[voice, text] = asyncio.create_task(make(text, voice))
        await asyncio.gather(*results.values())
        return [dict(pk=pk, kind=kind, voice=voice, rate=rate,
                     text=text, prepared=prepare_speech(text), **results[voice, text].result())
                for voice in voices for pk, kind, text in texts]

    def write_preview(self, folder, records):
        cards = []
        for row in records:
            voice = row['voice'].removeprefix('uz-UZ-').removesuffix('Neural')
            audio = ('<p>Audio yaratilmagan.</p>' if 'error' in row else
                     f'<audio controls preload="none" src="{html.escape(row["path"].removeprefix("audio/tts/"), quote=True)}"></audio>')
            cards.append(f'<article><h2>{voice} · {row["pk"]}-savol</h2>'
                         f'<p>{html.escape(row["text"])}</p>{audio}</article>')
        page = ('<!doctype html><html lang="uz"><meta charset="utf-8">'
                '<meta name="viewport" content="width=device-width, initial-scale=1">'
                '<title>Bilimbo — o‘zbekcha ovoz namunalari</title>'
                '<style>body{font:18px/1.6 system-ui;margin:32px auto;max-width:900px;padding:0 20px;'
                'background:#f5f5fb;color:#25233b}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px}'
                'article{background:white;padding:20px;border-radius:18px}h2{font-size:22px}audio{width:100%}</style>'
                '<h1>O‘zbekcha ovoz namunalari</h1><p>Bir xil savollarni Madina va Sardor ovozlarida tinglang.</p>'
                f'<main>{"".join(cards)}</main></html>')
        preview = folder / 'namunalar.html'
        preview.write_text(page, encoding='utf-8')
        self.stdout.write(f'Namuna sahifasi: {preview}')
