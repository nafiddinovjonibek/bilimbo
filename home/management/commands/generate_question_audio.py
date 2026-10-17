import asyncio
import html
import json

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from home.models import Savol
from home.narakeet import require_api_key
from home.tts import (DEFAULT_RATE, EDGE_VOICES, VOICES, audio_ready, generate_speech,
                      prepare_speech, question_texts, speech_path, speech_profile)


class Command(BaseCommand):
    help = 'Savollarni o‘zbekcha MP3 qiladi; tayyor fayllarni qayta yaratmaydi.'

    def add_arguments(self, parser):
        parser.add_argument('--voice', choices=VOICES)
        parser.add_argument('--rate', help='Masalan: --rate=-10%%')
        parser.add_argument('--ids', nargs='+', type=int, help='Savol ID lari (kvest bosqichlari ham olinadi).')
        parser.add_argument('--limit', type=int)
        parser.add_argument('--samples', action='store_true', help='Ikkala ovozda uchta savol va tinglash sahifasi.')
        parser.add_argument('--force', action='store_true', help='Tayyor fayllarni ham qayta yaratish.')
        parser.add_argument('--jobs', type=int, help='Odina uchun odatda 1, Edge ovozlari uchun 3.')

    def handle(self, *args, **options):
        if options['jobs'] is None:
            selected = options['voice'] or getattr(settings, 'BILIMBO_TTS_VOICE', '')
            options['jobs'] = 1 if selected == 'odina' and not (options['samples'] and not options['voice']) else 3
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
            if options['samples'] and not options['voice']:
                voices = EDGE_VOICES
                rate = options['rate'] or DEFAULT_RATE
            else:
                voices = (voice,)
            if 'odina' in voices and (options['force'] or any(
                    not audio_ready(settings.BASE_DIR / 'static' / speech_path(text, 'odina', rate))
                    for _, _, text in texts)):
                require_api_key()
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
            voice = ('Odina' if row['voice'] == 'odina' else
                     row['voice'].removeprefix('uz-UZ-').removesuffix('Neural'))
            audio = ('<p>Audio yaratilmagan.</p>' if 'error' in row else
                     f'<audio controls preload="none" src="{html.escape(row["path"].removeprefix("audio/tts/"), quote=True)}"></audio>')
            cards.append(f'<article><h2>{voice} · {row["pk"]}-savol</h2>'
                         f'<p>{html.escape(row["text"])}</p>{audio}</article>')

        # Qo'shimcha namunalarning ro'yxati qayta generatsiyada ham saqlanadi.
        demo_cards = []
        extra_file = folder / 'QOSHIMCHA_NAMUNALAR.json'
        extra_records = json.loads(extra_file.read_text(encoding='utf-8')) if extra_file.exists() else []
        for row in extra_records:
            voice = html.escape(row['voice'])
            provider = html.escape(row['provider'])
            source = html.escape(row['source_url'], quote=True)
            selected = '<span class="selected">Tanlangan ovoz</span>' if row.get('selected') else ''
            manba = row.get('audio_url') or row['path'].removeprefix('audio/tts/')
            audio = (f'<audio controls preload="none" src="{html.escape(manba, quote=True)}"></audio>'
                     '<p class="audio-error" hidden>Audio yuklanmadi. Xizmat sahifasidan tinglang.</p>')
            if row['kind'] == 'provider_demo':
                description = 'Xizmatning tayyor demo matni. Tinglash uchun internet kerak.'
                destination = demo_cards
            else:
                description = row['text']
                destination = cards
            destination.append(f'<article><p class="provider">{provider}</p><h2>{voice} {selected}</h2>'
                               f'<p>{html.escape(description)}</p>{audio}'
                               f'<p><a href="{source}" target="_blank" rel="noopener noreferrer">Xizmat sahifasi ↗</a></p></article>')

        demos = ('<section><h2 class="section-title">Boshqa ovozlar — xizmatning tayyor namunalari</h2>'
                 '<p>Bu yozuvlarda xizmatning o‘z demo matni o‘qiladi.</p>'
                 f'<div class="samples">{"".join(demo_cards)}</div></section>') if demo_cards else ''
        page = ('<!doctype html><html lang="uz"><meta charset="utf-8">'
                '<meta name="viewport" content="width=device-width, initial-scale=1">'
                '<title>Bilimbo — o‘zbekcha ovoz namunalari</title>'
                '<style>body{font:18px/1.6 system-ui;margin:32px auto;max-width:900px;padding:0 20px;'
                'background:#f5f5fb;color:#25233b}.samples{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:20px}'
                'article{background:white;padding:20px;border-radius:18px}h2{font-size:22px}audio{width:100%}'
                'section{margin:32px 0}.section-title{font-size:26px}.provider{color:#625878;font-size:14px;margin:0}'
                '.selected{display:inline-block;font-size:12px;background:#e8e3ff;color:#4d349e;'
                'padding:3px 8px;border-radius:20px;vertical-align:middle}'
                'a{color:#5443ad}.audio-error{color:#983a3a;font-size:14px}</style>'
                '<h1>O‘zbekcha ovoz namunalari</h1><p>Ovozlarni tinglab, talaffuz va ohangini solishtiring.</p>'
                '<main><section><h2 class="section-title">Bilimbo savollarida</h2>'
                f'<div class="samples">{"".join(cards)}</div></section>{demos}</main>'
                '<script>document.addEventListener("play",function(e){if(e.target.tagName!=="AUDIO")return;'
                'document.querySelectorAll("audio").forEach(function(a){if(a!==e.target)a.pause();});},true);'
                'document.addEventListener("error",function(e){if(e.target.tagName!=="AUDIO")return;'
                'var p=e.target.closest("article").querySelector(".audio-error");if(p)p.hidden=false;},true);</script></html>')
        preview = folder / 'namunalar.html'
        preview.write_text(page, encoding='utf-8')
        self.stdout.write(f'Namuna sahifasi: {preview}')
