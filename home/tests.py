import json
import importlib
from collections import Counter, deque
from xml.etree import ElementTree

from django.conf import settings
from django.apps import apps
from django.template.loader import render_to_string
from django.test import TestCase
from django.utils.datastructures import MultiValueDict

from .models import OvozJavob, Savol, SavolNatija, User, Variant
from .views import _oyin_holati


def maze_solution(question):
    grid = question.labirint_qatorlari
    start = question._labirint_joyi('R')
    goal = question._labirint_joyi('H')
    queue = deque([(start, '')])
    seen = {start}
    while queue:
        (x, y), route = queue.popleft()
        if (x, y) == goal:
            return route
        for command, dx, dy in [('U', 0, -1), ('D', 0, 1), ('L', -1, 0), ('R', 1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= ny < len(grid) and 0 <= nx < len(grid[ny]) \
                    and grid[ny][nx] != '#' and (nx, ny) not in seen:
                seen.add((nx, ny))
                queue.append(((nx, ny), route + command))
    raise AssertionError(f'{question.pk}: labirint yechimsiz')


def correct_answers(question):
    answer = MultiValueDict()
    variants = list(question.variantlar.all())
    pk = question.pk
    if question.tur == 'tanlov':
        answer[f'javob_{pk}'] = str(next(v.pk for v in variants if v.togri))
    elif question.tur in ('koptanlov', 'xarid'):
        answer.setlist(f'tanlangan_{pk}', [str(v.pk) for v in variants if v.togri])
    elif question.tur == 'tartib':
        answer.setlist(f'tartib_{pk}', [str(v.pk) for v in sorted(variants, key=lambda v: v.togri_order)])
    elif question.tur == 'moslash':
        for variant in variants:
            answer[f'moslash_{pk}_{variant.pk}'] = str(variant.pk)
    elif question.tur == 'guruh':
        for variant in variants:
            answer[f'guruh_{pk}_{variant.pk}'] = variant.juft_matn
    elif question.tur == 'qurish':
        for variant in variants:
            answer[f'qurish_{pk}_{variant.togri_order}'] = str(variant.pk)
    elif question.tur == 'boyash':
        palette = next(v.rang for v in variants if v.rang)
        answer[f'boyash_{pk}'] = json.dumps({name: expected or palette for name, expected in question.boyash_sohalari.items()})
    elif question.tur == 'labirint':
        answer[f'labirint_{pk}'] = maze_solution(question)
    elif question.tur == 'mikrofon':
        answer[f'ovoz_{pk}'] = 'test-voice.webm'
    elif question.tur == 'kvest':
        for child in question.bosqichlar.all():
            for key, values in correct_answers(child).lists():
                answer.setlist(key, values)
    return answer


class RefinedContentTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        path = settings.BASE_DIR / 'home/migrations/0022_topshiriqlarni_takomillashtirish.json'
        cls.content = json.loads(path.read_text(encoding='utf8'))
        update_path = settings.BASE_DIR / 'home/migrations/0023_sanoq_topshirigini_yangilash.json'
        update = json.loads(update_path.read_text(encoding='utf8'))
        next(row for row in cls.content if row['key'] == update['key'])['after'].update(update['after'])
        house_path = settings.BASE_DIR / 'home/migrations/0024_yogoch_uycha_topshirigi.json'
        house = json.loads(house_path.read_text(encoding='utf8'))
        row = next(row for row in cls.content if row['key'] == house['key'])
        row['after'].update(house['after'])
        for values, latest in zip(row['variants_after'], house['variants_after']):
            values.update(latest)
        robot_path = settings.BASE_DIR / 'home/migrations/0025_robot_topshirigini_yangilash.json'
        robot = json.loads(robot_path.read_text(encoding='utf8'))
        row = next(row for row in cls.content if row['key'] == robot['key'])
        row['after'].update(robot['after'])
        for values, latest in zip(row['variants_after'], robot['variants_after']):
            values.update(latest)
        castle_path = settings.BASE_DIR / 'home/migrations/0026_qasr_topshirigini_yangilash.json'
        castle = json.loads(castle_path.read_text(encoding='utf8'))
        row = next(row for row in cls.content if row['key'] == castle['key'])
        row['after'].update(castle['after'])
        for values, latest in zip(row['variants_after'], castle['variants_after']):
            values.update(latest)
        butterfly_path = settings.BASE_DIR / 'home/migrations/0027_kapalak_simmetriyasini_yangilash.json'
        butterfly = json.loads(butterfly_path.read_text(encoding='utf8'))
        row = next(row for row in cls.content if row['key'] == butterfly['key'])
        row['after'].update(butterfly['after'])
        for values, latest in zip(row['variants_after'], butterfly['variants_after']):
            values.update(latest)
        rocket_path = settings.BASE_DIR / 'home/migrations/0028_raketa_tahlilini_yangilash.json'
        rocket = json.loads(rocket_path.read_text(encoding='utf8'))
        row = next(row for row in cls.content if row['key'] == rocket['key'])
        row['after'].update(rocket['after'])
        for values, latest in zip(row['variants_after'], rocket['variants_after']):
            values.update(latest)
        bridge_path = settings.BASE_DIR / 'home/migrations/0029_koprik_loyihasini_yangilash.json'
        bridge = json.loads(bridge_path.read_text(encoding='utf8'))
        row = next(row for row in cls.content if row['key'] == bridge['key'])
        row['after'].update(bridge['after'])
        for values, latest in zip(row['variants_after'], bridge['variants_after']):
            values.update(latest)

    def find_question(self, key):
        primary, _, step = key.partition('/')
        section, level, order = map(int, primary.split('.'))
        question = Savol.objects.get(bolimcha__bolim__order=section,
                                    bolimcha__order=level, order=order, kvest__isnull=True)
        return question.bosqichlar.get(order=int(step)) if step else question

    def test_question_types_counts_and_variants_are_preserved(self):
        self.assertEqual(Savol.objects.filter(kvest__isnull=True).count(), 150)
        self.assertEqual(Savol.objects.filter(kvest__isnull=False).count(), 29)
        self.assertEqual(Counter(Savol.objects.values_list('tur', flat=True)),
                         Counter(row['tur'] for row in self.content))
        for row in self.content:
            with self.subTest(key=row['key']):
                question = self.find_question(row['key'])
                self.assertEqual(question.tur, row['tur'])
                self.assertEqual(question.variantlar.count(), len(row['variants_before']))
                self.assertNotEqual(question.matn, row['before']['matn'])
                self.assertEqual(question.ovoz_matn, row['after']['ovoz_matn'])

    def test_content_rollback_keeps_ids_and_student_results(self):
        user = User.objects.create(username='content-rollback-test')
        question = Savol.objects.filter(tur='mikrofon').first()
        SavolNatija.objects.create(user=user, savol=question, stars=2)
        OvozJavob.objects.create(user=user, savol=question, fayl='test/existing-recording.webm')
        questions = list(Savol.objects.order_by('pk').values())
        variants = list(Variant.objects.order_by('pk').values())
        results = list(SavolNatija.objects.values())
        recordings = list(OvozJavob.objects.values())
        migration = importlib.import_module('home.migrations.0022_topshiriqlarni_takomillashtirish')
        counting = importlib.import_module('home.migrations.0023_sanoq_topshirigini_yangilash')
        house = importlib.import_module('home.migrations.0024_yogoch_uycha_topshirigi')
        robot = importlib.import_module('home.migrations.0025_robot_topshirigini_yangilash')
        castle = importlib.import_module('home.migrations.0026_qasr_topshirigini_yangilash')
        butterfly = importlib.import_module('home.migrations.0027_kapalak_simmetriyasini_yangilash')
        rocket = importlib.import_module('home.migrations.0028_raketa_tahlilini_yangilash')
        bridge = importlib.import_module('home.migrations.0029_koprik_loyihasini_yangilash')
        bridge.rewrite(apps, 'before')
        rocket.rewrite(apps, 'before')
        butterfly.rewrite(apps, 'before')
        castle.rewrite(apps, 'before')
        robot.rewrite(apps, 'before')
        house.rewrite(apps, 'before')
        counting.rewrite(apps, 'before')
        migration.rewrite(apps, 'before')
        self.assertEqual(set(Savol.objects.values_list('pk', flat=True)), {q['id'] for q in questions})
        for row in self.content:
            self.assertEqual(self.find_question(row['key']).matn, row['before']['matn'])
        migration.rewrite(apps, 'after')
        counting.rewrite(apps, 'after')
        house.rewrite(apps, 'after')
        robot.rewrite(apps, 'after')
        castle.rewrite(apps, 'after')
        butterfly.rewrite(apps, 'after')
        rocket.rewrite(apps, 'after')
        bridge.rewrite(apps, 'after')
        self.assertEqual(list(Savol.objects.order_by('pk').values()), questions)
        self.assertEqual(list(Variant.objects.order_by('pk').values()), variants)
        self.assertEqual(list(SavolNatija.objects.values()), results)
        self.assertEqual(list(OvozJavob.objects.values()), recordings)

    def test_all_tasks_accept_their_solution_and_reject_empty_answer(self):
        for question in Savol.objects.prefetch_related('variantlar', 'bosqichlar'):
            with self.subTest(pk=question.pk, tur=question.tur):
                self.assertTrue(question.tekshir(correct_answers(question)))
                self.assertFalse(question.tekshir(MultiValueDict()))

    def test_choice_answer_is_unambiguous_and_not_always_first(self):
        positions = Counter()
        for question in Savol.objects.filter(tur='tanlov').prefetch_related('variantlar'):
            with self.subTest(pk=question.pk):
                choices = list(question.variantlar.all())
                self.assertEqual(sum(v.togri for v in choices), 1)
                positions[next(i for i, v in enumerate(choices) if v.togri)] += 1
                for wrong in (v for v in choices if not v.togri):
                    self.assertFalse(question.tekshir(MultiValueDict({f'javob_{question.pk}': [str(wrong.pk)]})))
        self.assertGreaterEqual(len(positions), 3)
        self.assertLess(positions[0], 60)

    def test_every_referenced_image_and_audio_exists(self):
        images = set()
        for question in Savol.objects.prefetch_related('variantlar'):
            if question.rasm:
                images.add(question.rasm)
            if question.audio_fayl:
                self.assertTrue((settings.BASE_DIR / 'static' / question.audio_fayl).is_file())
                self.assertFalse(question.audio_matn)
            for variant in question.variantlar.all():
                images.update(path for path in [variant.rasm, variant.juft_rasm] if path)
        for image in images:
            with self.subTest(image=image):
                path = settings.BASE_DIR / 'static' / image
                self.assertTrue(path.is_file())
                if path.suffix == '.svg':
                    ElementTree.fromstring(path.read_text(encoding='utf8'))

    def test_learner_hints_do_not_publish_answers_or_implementation(self):
        forbidden = ['kutilgan javob', 'to‘g‘ri ketma-ketlik:', 'mosliklar:',
                     'koordinat', 'data-soha', 'data-togri', 'ta’rifdan tayyorlangan']
        for question in Savol.objects.all():
            with self.subTest(pk=question.pk):
                self.assertTrue(all(word not in question.izoh.lower() for word in forbidden))

    def test_painting_regions_and_required_colors_are_valid(self):
        for question in Savol.objects.filter(tur='boyash').prefetch_related('variantlar'):
            with self.subTest(pk=question.pk):
                tree = ElementTree.fromstring(question.boyash)
                names = [node.get('data-soha') for node in tree.iter() if node.get('data-soha')]
                self.assertTrue(names)
                self.assertEqual(len(names), len(set(names)))
                colors = {variant.rang.lower() for variant in question.variantlar.all()}
                self.assertTrue(all(not color or color in colors for color in question.boyash_sohalari.values()))
                complete = {name: color or next(iter(colors)) for name, color in question.boyash_sohalari.items()}
                complete.pop(next(iter(complete)))
                self.assertFalse(question.boyash_toldirilganmi(json.dumps(complete)))

    def test_construction_slots_and_sequence_orders_are_valid(self):
        for question in Savol.objects.filter(tur__in=['qurish', 'tartib']).prefetch_related('variantlar'):
            with self.subTest(pk=question.pk):
                variants = list(question.variantlar.all())
                self.assertEqual(sorted(v.togri_order for v in variants), list(range(1, len(variants) + 1)))
                if question.tur == 'qurish':
                    for variant in variants:
                        x, y, w, h = map(float, variant.slot.split(','))
                        self.assertGreater(w, 0)
                        self.assertGreater(h, 0)
                        self.assertGreaterEqual(x, 0)
                        self.assertGreaterEqual(y, 0)
                        self.assertLessEqual(x + w, 100)
                        self.assertLessEqual(y + h, 100)

    def test_purchase_list_has_exact_budget(self):
        for question in Savol.objects.filter(tur='xarid').prefetch_related('variantlar'):
            with self.subTest(pk=question.pk):
                self.assertEqual(sum(v.narx for v in question.variantlar.all() if v.togri), question.byudjet)
                self.assertTrue(all(v.narx and v.narx > 0 for v in question.variantlar.all()))

    def test_every_task_body_renders_with_existing_templates(self):
        for question in Savol.objects.prefetch_related('variantlar'):
            if question.tur == 'kvest':
                continue
            with self.subTest(pk=question.pk):
                html = render_to_string('topshiriq/_topshiriq.html', {'h': _oyin_holati(question, 24), 'kvestda': bool(question.kvest_id)})
                self.assertIn('data-pk="' + str(question.pk) + '"', html)
                self.assertNotIn('None', html)
