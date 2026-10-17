import io
import tempfile
from pathlib import Path

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.core.management.base import CommandError
from django.db import IntegrityError, transaction
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse
from django.http import Http404

from .media_views import public_media
from .models import Bolimcha, Guruh, OvozJavob, Savol, SavolNatija, User
from .tests import correct_answers


class RoleAndGroupTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_superuser('role-admin', password='admin-pass-123')
        cls.teacher = User.objects.create_user('teacher-one', password='teacher-pass-123',
                                             role=User.Role.TARBIYACHI, teacher_approved=True, first_name='Dilnoza')
        cls.other_teacher = User.objects.create_user('teacher-two', password='teacher-pass-123',
                                                   role=User.Role.TARBIYACHI, teacher_approved=True, first_name='Malika')
        cls.pending = User.objects.create_user('teacher-pending', password='teacher-pass-123', role=User.Role.TARBIYACHI)
        cls.group = Guruh.objects.create(nom='Kamalak guruhi', tarbiyachi=cls.teacher)
        cls.foreign_group = Guruh.objects.create(nom='Begona guruh', tarbiyachi=cls.other_teacher)
        cls.pupil = User.objects.create_user('pupil-one', password='child-pass-123', first_name='Ali', guruh=cls.group)
        cls.foreign_pupil = User.objects.create_user('foreign-pupil', password='child-pass-123', first_name='Begona bola', guruh=cls.foreign_group)
        cls.unassigned = User.objects.create_user('unassigned-pupil', password='child-pass-123', first_name='Guruhsiz bola')
        cls.question = Savol.objects.filter(kvest__isnull=True, tur=Savol.Tur.TANLOV, order=1).first()
        SavolNatija.objects.create(user=cls.pupil, savol=cls.question, stars=2)
        SavolNatija.objects.create(user=cls.foreign_pupil, savol=cls.question, stars=3)
        # Historical teacher results are retained, but never counted as pupils' work.
        SavolNatija.objects.create(user=cls.teacher, savol=cls.question, stars=1)

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        setting = self.settings(PRIVATE_VOICES_ROOT=root / 'private', MEDIA_ROOT=root / 'public')
        setting.enable()
        self.addCleanup(setting.disable)
        self.voice = OvozJavob.objects.create(
            user=self.pupil, savol=self.question,
            fayl=SimpleUploadedFile('own.webm', b'private-own-audio', content_type='audio/webm'),
        )
        self.foreign_voice = OvozJavob.objects.create(
            user=self.foreign_pupil, savol=self.question,
            fayl=SimpleUploadedFile('foreign.webm', b'private-foreign-audio', content_type='audio/webm'),
        )
        self.client.force_login(self.teacher)

    def audio_status(self, user, voice):
        client = Client()
        if user:
            client.force_login(user)
        response = client.get(reverse('ovoz_fayl', args=[voice.pk]))
        status = response.status_code
        response.close()
        return status

    def test_home_routes_each_role_to_its_own_experience(self):
        self.assertRedirects(self.client.get(reverse('home')), reverse('kabinet'))
        self.client.force_login(self.admin)
        self.assertTrue(self.admin.is_superadmin)
        self.assertFalse(self.admin.is_oquvchi)
        self.assertRedirects(self.client.get(reverse('home')), reverse('kabinet'))
        self.client.force_login(self.pupil)
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Kamalak guruhi')
        self.assertContains(response, 'Natijalarim va tarbiyachi baholari')
        self.client.force_login(self.pending)
        self.assertContains(self.client.get(reverse('home')), 'tasdiq kutmoqda')

    def test_pending_teacher_cannot_access_management_preview_or_student_tests(self):
        self.client.force_login(self.pending)
        for name in ['kabinet', 'oquvchilar', 'ovozlar', 'sinov', 'guruh_yangi', 'tarbiyachilar']:
            with self.subTest(name=name):
                self.assertEqual(self.client.get(reverse(name)).status_code, 403)
        self.assertEqual(self.client.get(reverse('savol', args=[self.question.pk])).status_code, 403)
        self.assertEqual(self.client.get(reverse('kutubxona')).status_code, 200)
        self.assertEqual(self.audio_status(self.pending, self.voice), 404)

    def test_student_cannot_access_teacher_or_admin_routes(self):
        self.client.force_login(self.pupil)
        for name in ['kabinet', 'oquvchilar', 'ovozlar', 'sinov', 'guruh_yangi', 'tarbiyachilar']:
            self.assertEqual(self.client.get(reverse(name)).status_code, 403)
        self.assertEqual(self.client.post(reverse('guruh_yangi'), {'nom': 'Forbidden'}).status_code, 403)
        self.assertEqual(self.client.post(reverse('tarbiyachi_approval', args=[self.pending.pk]), {'action': 'approve'}).status_code, 403)

    def test_teachers_and_admins_cannot_earn_student_results(self):
        before = list(SavolNatija.objects.order_by('pk').values())
        for actor in [self.teacher, self.admin]:
            self.client.force_login(actor)
            for name, pk in [('bolim', self.question.bolimcha.bolim.order), ('bolimcha', self.question.bolimcha.pk), ('savol', self.question.pk)]:
                self.assertEqual(self.client.get(reverse(name, args=[pk])).status_code, 403)
            response = self.client.post(reverse('savol', args=[self.question.pk]), correct_answers(self.question))
            self.assertEqual(response.status_code, 403)
        self.assertEqual(list(SavolNatija.objects.order_by('pk').values()), before)

    def test_student_still_completes_questions_and_earns_stars(self):
        self.client.force_login(self.pupil)
        response = self.client.post(reverse('savol', args=[self.question.pk]), correct_answers(self.question))
        self.assertContains(response, 'Barakalla!')
        self.assertEqual(SavolNatija.objects.get(user=self.pupil, savol=self.question).stars, 3)

    def test_teacher_preview_works_for_every_top_level_question_without_saving(self):
        results = list(SavolNatija.objects.order_by('pk').values())
        voices = list(OvozJavob.objects.order_by('pk').values())
        for question in Savol.objects.filter(kvest__isnull=True):
            with self.subTest(question=question.pk, type=question.tur):
                data = dict(correct_answers(question).lists())
                response = self.client.post(reverse('sinov_savol', args=[question.pk]), data)
                self.assertEqual(response.status_code, 200)
                self.assertTrue(response.context['yutuq'], f'Question {question.pk} failed in preview')
                self.assertNotContains(response, 'ta yulduz yutdingiz')
        self.assertEqual(list(SavolNatija.objects.order_by('pk').values()), results)
        self.assertEqual(list(OvozJavob.objects.order_by('pk').values()), voices)
        self.assertFalse(any(key.startswith('urinish_') for key in self.client.session.keys()))

    def test_preview_upload_does_not_store_voice_files(self):
        question = Savol.objects.filter(tur=Savol.Tur.MIKROFON, kvest__isnull=True).first()
        before = {path for path in Path(settings.PRIVATE_VOICES_ROOT).rglob('*') if path.is_file()}
        response = self.client.post(reverse('sinov_savol', args=[question.pk]), {
            f'ovoz_{question.pk}': 'preview.webm',
            f'ovoz_fayl_{question.pk}': SimpleUploadedFile('preview.webm', b'preview voice', content_type='audio/webm'),
        })
        self.assertContains(response, 'To‘g‘ri bajarildi!')
        self.assertEqual(OvozJavob.objects.count(), 2)
        self.assertEqual({path for path in Path(settings.PRIVATE_VOICES_ROOT).rglob('*') if path.is_file()}, before)

    def test_preview_is_unlocked_and_rejects_malformed_answers_cleanly(self):
        later = Savol.objects.filter(kvest__isnull=True, order=10).first()
        self.assertContains(self.client.get(reverse('sinov_savol', args=[later.pk])), 'Sinov rejimi')
        self.assertEqual(self.client.get(reverse('sinov')).context['sections'].count(), Bolimcha.objects.count())
        response = self.client.post(reverse('sinov_savol', args=[self.question.pk]), {'javob': 'not-an-id'})
        self.assertContains(response, 'Yana urinib')

    def test_dashboard_counts_only_own_students_not_teacher_history(self):
        response = self.client.get(reverse('kabinet'))
        self.assertContains(response, self.group.nom)
        self.assertNotContains(response, self.foreign_group.nom)
        self.assertEqual(response.context['student_count'], 1)
        self.assertEqual(response.context['result_count'], 1)
        self.assertEqual(response.context['pending_audio'], 1)
        self.assertEqual(len(response.context['groups']), 1)

    def test_student_lists_and_profiles_hide_other_classes(self):
        response = self.client.get(reverse('oquvchilar'))
        self.assertContains(response, self.pupil.username)
        self.assertNotContains(response, self.foreign_pupil.username)
        self.assertNotContains(response, self.unassigned.username)
        self.assertEqual(self.client.get(reverse('oquvchi_detail', args=[self.foreign_pupil.pk])).status_code, 404)
        self.assertEqual(self.client.get(reverse('oquvchilar'), {'guruh': self.foreign_group.pk}).status_code, 404)
        self.assertEqual(self.client.get(reverse('oquvchilar'), {'guruh': 'invalid'}).status_code, 404)
        self.assertEqual(self.client.get(reverse('oquvchi_detail', args=[self.pupil.pk])).status_code, 200)

    def test_admin_sees_all_students_and_pending_teachers(self):
        self.client.force_login(self.admin)
        response = self.client.get(reverse('kabinet'))
        self.assertEqual(response.context['student_count'], 3)
        self.assertEqual(response.context['result_count'], 2)
        self.assertEqual(response.context['pending_teachers'], 1)
        self.assertEqual(response.context['unassigned_count'], 1)
        self.assertEqual(self.client.get(reverse('oquvchilar')).context['students'].count(), 3)

    def test_teacher_group_creation_cannot_forge_another_owner(self):
        response = self.client.post(reverse('guruh_yangi'), {'nom': 'Yangi guruh', 'tarbiyachi': self.other_teacher.pk})
        self.assertRedirects(response, reverse('kabinet'))
        self.assertEqual(Guruh.objects.get(nom='Yangi guruh').tarbiyachi, self.teacher)

    def test_foreign_groups_cannot_be_changed_or_deleted(self):
        for name in ['guruh_edit', 'guruh_delete', 'oquvchi_add']:
            url = reverse(name, args=[self.foreign_group.pk])
            self.assertEqual(self.client.get(url).status_code, 404)
            self.assertEqual(self.client.post(url, {'nom': 'Tampered'}).status_code, 404)
        self.foreign_group.refresh_from_db()
        self.assertEqual(self.foreign_group.nom, 'Begona guruh')

    def test_admin_can_transfer_group_and_previous_teacher_loses_access(self):
        self.client.force_login(self.admin)
        response = self.client.post(reverse('guruh_edit', args=[self.group.pk]), {'nom': self.group.nom, 'tarbiyachi': self.other_teacher.pk})
        self.assertRedirects(response, reverse('kabinet'))
        self.client.force_login(self.teacher)
        self.assertEqual(self.client.get(reverse('oquvchi_detail', args=[self.pupil.pk])).status_code, 404)
        self.assertEqual(self.audio_status(self.teacher, self.voice), 404)
        self.assertEqual(self.audio_status(self.other_teacher, self.voice), 200)

    def test_admin_cannot_assign_group_to_unapproved_teacher_or_student(self):
        self.client.force_login(self.admin)
        for owner in [self.pending, self.pupil]:
            response = self.client.post(reverse('guruh_yangi'), {'nom': 'Invalid group', 'tarbiyachi': owner.pk})
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.context['form'].errors)
        self.assertFalse(Guruh.objects.filter(nom='Invalid group').exists())

    def test_teacher_creates_student_without_granting_privileged_roles(self):
        response = self.client.post(reverse('oquvchi_add', args=[self.group.pk]), {
            'action': 'create', 'new-username': 'new-child', 'new-first_name': 'Yangi', 'new-last_name': 'Bola',
            'new-password1': 'child-strong-987', 'new-password2': 'child-strong-987',
            'role': 'superadmin', 'teacher_approved': '1', 'is_staff': '1', 'is_superuser': '1', 'guruh': self.foreign_group.pk,
        })
        pupil = User.objects.get(username='new-child')
        self.assertRedirects(response, reverse('oquvchi_detail', args=[pupil.pk]))
        self.assertTrue(pupil.is_oquvchi)
        self.assertFalse(pupil.teacher_approved or pupil.is_staff or pupil.is_superuser)
        self.assertEqual(pupil.guruh, self.group)
        self.assertTrue(pupil.check_password('child-strong-987'))
        self.assertEqual(self.client.session['_auth_user_id'], str(self.teacher.pk))

    def test_existing_unassigned_account_requires_its_correct_credentials(self):
        url = reverse('oquvchi_add', args=[self.group.pk])
        data = {'action': 'attach', 'existing-username': self.unassigned.username, 'existing-password': 'wrong'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['attach_form'].errors)
        self.unassigned.refresh_from_db()
        self.assertIsNone(self.unassigned.guruh)
        data['existing-password'] = 'child-pass-123'
        self.assertEqual(self.client.post(url, data).status_code, 302)
        self.unassigned.refresh_from_db()
        self.assertEqual(self.unassigned.guruh, self.group)

    def test_even_valid_credentials_do_not_allow_claiming_another_teachers_pupil(self):
        response = self.client.post(reverse('oquvchi_add', args=[self.group.pk]), {
            'action': 'attach', 'existing-username': self.foreign_pupil.username, 'existing-password': 'child-pass-123',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['attach_form'].errors)
        self.foreign_pupil.refresh_from_db()
        self.assertEqual(self.foreign_pupil.guruh, self.foreign_group)

    def test_admin_can_assign_existing_account_without_child_password(self):
        self.client.force_login(self.admin)
        response = self.client.post(reverse('oquvchi_add', args=[self.group.pk]), {
            'action': 'attach', 'existing-username': self.unassigned.username,
        })
        self.assertEqual(response.status_code, 302)
        self.unassigned.refresh_from_db()
        self.assertEqual(self.unassigned.guruh, self.group)

    def test_student_edit_cannot_change_role_or_move_to_a_foreign_group(self):
        url = reverse('oquvchi_edit', args=[self.pupil.pk])
        response = self.client.post(url, {'first_name': 'Ali', 'last_name': '', 'guruh': self.foreign_group.pk})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)
        self.client.post(url, {'first_name': 'Ali', 'last_name': '', 'guruh': self.group.pk, 'role': 'superadmin', 'teacher_approved': '1'})
        self.pupil.refresh_from_db()
        self.assertEqual(self.pupil.guruh, self.group)
        self.assertTrue(self.pupil.is_oquvchi)
        self.assertFalse(self.pupil.teacher_approved)

    def test_removing_student_membership_preserves_records_and_revokes_teacher_access(self):
        self.client.post(reverse('oquvchi_edit', args=[self.pupil.pk]), {'first_name': 'Ali', 'last_name': '', 'guruh': ''})
        self.pupil.refresh_from_db()
        self.assertIsNone(self.pupil.guruh)
        self.assertTrue(SavolNatija.objects.filter(user=self.pupil).exists())
        self.assertTrue(OvozJavob.objects.filter(pk=self.voice.pk).exists())
        self.assertEqual(self.audio_status(self.teacher, self.voice), 404)
        self.assertEqual(self.audio_status(self.pupil, self.voice), 200)

    def test_deleting_group_only_removes_membership(self):
        url = reverse('guruh_delete', args=[self.group.pk])
        self.assertEqual(self.client.get(url).status_code, 200)
        self.assertTrue(Guruh.objects.filter(pk=self.group.pk).exists())
        self.assertRedirects(self.client.post(url), reverse('kabinet'))
        self.pupil.refresh_from_db()
        self.assertIsNone(self.pupil.guruh)
        self.assertTrue(SavolNatija.objects.filter(user=self.pupil).exists())
        self.assertTrue(OvozJavob.objects.filter(pk=self.voice.pk).exists())

    def test_only_admin_can_approve_and_revoke_teachers(self):
        url = reverse('tarbiyachi_approval', args=[self.pending.pk])
        self.assertEqual(self.client.post(url, {'action': 'approve'}).status_code, 403)
        self.client.force_login(self.admin)
        self.assertEqual(self.client.get(url).status_code, 405)
        self.assertRedirects(self.client.post(url, {'action': 'approve'}), reverse('tarbiyachilar'))
        self.pending.refresh_from_db()
        self.assertTrue(self.pending.is_approved_teacher)
        self.assertRedirects(self.client.post(url, {'action': 'revoke'}), reverse('tarbiyachilar'))
        self.pending.refresh_from_db()
        self.assertFalse(self.pending.teacher_approved)

    def test_revocation_takes_effect_for_existing_teacher_session(self):
        self.assertEqual(self.client.get(reverse('kabinet')).status_code, 200)
        admin_client = Client()
        admin_client.force_login(self.admin)
        admin_client.post(reverse('tarbiyachi_approval', args=[self.teacher.pk]), {'action': 'revoke'})
        self.assertEqual(self.client.get(reverse('kabinet')).status_code, 403)
        self.assertEqual(self.audio_status(self.teacher, self.voice), 404)
        self.assertContains(self.client.get(reverse('home')), 'tasdiq kutmoqda')

    def test_voice_access_is_limited_to_its_owner_teacher_and_admin(self):
        for user in [self.pupil, self.teacher, self.admin]:
            self.assertEqual(self.audio_status(user, self.voice), 200)
        for user in [self.foreign_pupil, self.other_teacher, self.pending, self.unassigned]:
            self.assertEqual(self.audio_status(user, self.voice), 404)
        self.assertEqual(self.audio_status(None, self.voice), 302)
        response = self.client.get(reverse('ovoz_fayl', args=[self.voice.pk]))
        self.assertEqual(response['Content-Type'], 'audio/webm')
        self.assertIn('no-store', response['Cache-Control'])
        self.assertEqual(b''.join(response.streaming_content), b'private-own-audio')
        response.close()
        with self.assertRaises(ValueError):
            _ = self.voice.fayl.url

    def test_public_media_cannot_bypass_voice_authorization(self):
        legacy = Path(settings.MEDIA_ROOT) / self.voice.fayl.name
        legacy.parent.mkdir(parents=True)
        legacy.write_bytes(b'public-copy-must-not-be-served')
        for path in [self.voice.fayl.name, 'other/../' + self.voice.fayl.name]:
            with self.assertRaises(Http404):
                public_media(RequestFactory().get('/media/' + path), path, document_root=settings.MEDIA_ROOT)
        self.assertEqual(Client().get('/media/' + self.voice.fayl.name).status_code, 404)

    def test_voice_review_is_scoped_audited_and_visible_to_child(self):
        response = self.client.post(reverse('ovoz_review', args=[self.voice.pk]), {
            'tarbiyachi_bahosi': '1', 'tarbiyachi_izohi': 'Yaxshi aytding, yana mashq qilamiz.', 'user': self.foreign_pupil.pk,
        })
        self.assertRedirects(response, reverse('ovozlar'))
        self.voice.refresh_from_db()
        self.assertEqual(self.voice.user, self.pupil)
        self.assertEqual(self.voice.tarbiyachi_bahosi, 1)
        self.assertEqual(self.voice.baholagan, self.teacher)
        self.assertIsNotNone(self.voice.baholangan_at)
        self.assertEqual(SavolNatija.objects.get(user=self.pupil, savol=self.question).stars, 2)
        self.client.force_login(self.pupil)
        response = self.client.get(reverse('natijalarim'))
        self.assertContains(response, 'Yaxshi aytding, yana mashq qilamiz.')
        self.assertNotContains(response, self.foreign_pupil.username)

    def test_foreign_voice_cannot_be_reviewed_and_invalid_grades_are_rejected(self):
        self.assertEqual(self.client.post(reverse('ovoz_review', args=[self.foreign_voice.pk]), {'tarbiyachi_bahosi': '3'}).status_code, 404)
        for grade in ['', '0', '4', '-1', 'not-a-number']:
            response = self.client.post(reverse('ovoz_review', args=[self.voice.pk]), {'tarbiyachi_bahosi': grade})
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.context['form'].errors)
        self.voice.refresh_from_db()
        self.assertIsNone(self.voice.tarbiyachi_bahosi)

    def test_microphone_submission_saves_only_in_private_storage(self):
        section = Bolimcha.objects.create(bolim=self.question.bolimcha.bolim, name='Ovoz sinovi', order=99)
        question = Savol.objects.create(bolimcha=section, order=1, daraja='oson', tur='mikrofon', matn='Gapiring')
        self.client.force_login(self.pupil)
        response = self.client.post(reverse('savol', args=[question.pk]), {
            f'ovoz_{question.pk}': 'answer.webm',
            f'ovoz_fayl_{question.pk}': SimpleUploadedFile('answer.webm', b'child audio', content_type='audio/webm'),
        })
        self.assertContains(response, 'Barakalla!')
        voice = OvozJavob.objects.get(user=self.pupil, savol=question)
        self.assertTrue(Path(voice.fayl.path).is_relative_to(Path(settings.PRIVATE_VOICES_ROOT)))
        self.assertFalse((Path(settings.MEDIA_ROOT) / voice.fayl.name).exists())

    def test_registration_cannot_self_approve_or_grant_admin_privileges(self):
        client = Client()
        response = client.post(reverse('register'), {
            'username': 'registered-teacher', 'first_name': 'Yangi', 'last_name': 'Tarbiyachi',
            'password1': 'strong-signup-987', 'password2': 'strong-signup-987', 'role': 'tarbiyachi',
            'teacher_approved': '1', 'is_superuser': '1', 'is_staff': '1', 'guruh': self.group.pk,
        })
        self.assertRedirects(response, reverse('home'))
        teacher = User.objects.get(username='registered-teacher')
        self.assertFalse(teacher.teacher_approved or teacher.is_superuser or teacher.is_staff)
        self.assertIsNone(teacher.guruh)
        self.assertContains(client.get(reverse('home')), 'tasdiq kutmoqda')

    def test_admin_actions_still_require_csrf(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.admin)
        url = reverse('tarbiyachi_approval', args=[self.pending.pk])
        self.assertEqual(client.post(url, {'action': 'approve'}).status_code, 403)
        client.get(reverse('tarbiyachilar'))
        token = client.cookies[settings.CSRF_COOKIE_NAME].value
        response = client.post(url, {'action': 'approve', 'csrfmiddlewaretoken': token}, HTTP_ORIGIN='http://testserver')
        self.assertEqual(response.status_code, 302)

    def test_accidental_staff_teacher_cannot_use_admin_to_bypass_scope(self):
        self.teacher.is_staff = True
        self.teacher.save(update_fields=['is_staff'])
        for url in [reverse('admin:home_user_changelist'), reverse('admin:home_guruh_add'),
                    reverse('admin:home_ovozjavob_change', args=[self.foreign_voice.pk])]:
            self.assertEqual(self.client.get(url).status_code, 403)

    def test_model_constraints_reject_teacher_membership_and_invalid_group_owner(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            User.objects.filter(pk=self.teacher.pk).update(guruh=self.group)
        with self.assertRaises(ValidationError):
            Guruh(nom='Invalid', tarbiyachi=self.pending).full_clean()
        self.teacher.role = User.Role.OQUVCHI
        with self.assertRaises(ValidationError):
            self.teacher.clean()

    def test_protect_legacy_voice_moves_verified_copy_and_is_idempotent(self):
        name = 'ovoz/old/legacy.webm'
        voice = OvozJavob.objects.create(user=self.pupil, savol=self.question, fayl=name)
        public = Path(settings.MEDIA_ROOT) / name
        public.parent.mkdir(parents=True)
        public.write_bytes(b'legacy recording')
        call_command('protect_voice_files', dry_run=True, stdout=io.StringIO())
        self.assertTrue(public.exists())
        call_command('protect_voice_files', stdout=io.StringIO())
        self.assertFalse(public.exists())
        self.assertEqual(Path(voice.fayl.path).read_bytes(), b'legacy recording')
        call_command('protect_voice_files', stdout=io.StringIO())
        voice.refresh_from_db()
        self.assertEqual(voice.fayl.name, name)

    def test_protect_voice_collision_never_deletes_public_source(self):
        public = Path(settings.MEDIA_ROOT) / self.voice.fayl.name
        public.parent.mkdir(parents=True)
        public.write_bytes(b'different source')
        with self.assertRaises(CommandError):
            call_command('protect_voice_files', stdout=io.StringIO())
        self.assertTrue(public.exists())
        self.assertEqual(Path(self.voice.fayl.path).read_bytes(), b'private-own-audio')
