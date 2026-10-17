from collections import Counter
from pathlib import Path

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Count, Prefetch, Q, Sum
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET, require_http_methods, require_POST
from django.contrib.auth.decorators import login_required

from .access import groups_for, students_for, voices_for
from .decorators import educator_required, oquvchi_required, superadmin_required
from .models import Bolimcha, Guruh, Savol, SavolNatija, User
from .portal_forms import AttachStudentForm, GroupForm, NewStudentForm, StudentEditForm, VoiceReviewForm
from .views import _oyin_holati


def _form_page(request, form, title, back_url, **context):
    return render(request, 'portal/form.html', {
        'form': form, 'page_title': title, 'back_url': back_url, **context,
    })


@never_cache
@educator_required
@require_GET
def dashboard(request):
    students = students_for(request.user)
    groups = groups_for(request.user).annotate(pupils=Count('oquvchilar', filter=Q(
        oquvchilar__role=User.Role.OQUVCHI, oquvchilar__is_superuser=False,
    )))
    return render(request, 'portal/dashboard.html', {
        'groups': groups,
        'student_count': students.count(),
        'result_count': SavolNatija.objects.filter(user__in=students).count(),
        'pending_audio': voices_for(request.user).filter(user__in=students, tarbiyachi_bahosi__isnull=True).count(),
        'unassigned_count': students.filter(guruh__isnull=True).count() if request.user.is_superadmin else 0,
        'pending_teachers': User.objects.filter(role=User.Role.TARBIYACHI, teacher_approved=False, is_superuser=False).count()
        if request.user.is_superadmin else 0,
    })


@never_cache
@educator_required
@require_http_methods(['GET', 'POST'])
def group_edit(request, pk=None):
    group = get_object_or_404(groups_for(request.user), pk=pk) if pk else Guruh()
    form = GroupForm(request.POST if request.method == 'POST' else None, actor=request.user, instance=group)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Guruh saqlandi.')
        return redirect('kabinet')
    return _form_page(request, form, 'Guruhni tahrirlash' if pk else 'Yangi guruh', reverse('kabinet'))


@never_cache
@educator_required
@require_http_methods(['GET', 'POST'])
def group_delete(request, pk):
    group = get_object_or_404(groups_for(request.user), pk=pk)
    if request.method == 'POST':
        group.delete()
        messages.success(request, 'Guruh o‘chirildi. O‘quvchi hisoblari va natijalari saqlandi.')
        return redirect('kabinet')
    return render(request, 'portal/group_delete.html', {'group': group})


@never_cache
@educator_required
@require_GET
def student_list(request):
    students = students_for(request.user)
    group = None
    if request.GET.get('guruh'):
        try:
            group_pk = int(request.GET['guruh'])
        except (ValueError, TypeError):
            raise Http404 from None
        group = get_object_or_404(groups_for(request.user), pk=group_pk)
        students = students.filter(guruh=group)
    if request.GET.get('biriktirilmagan') == '1' and request.user.is_superadmin:
        students = students.filter(guruh__isnull=True)
    students = students.annotate(
        solved=Count('natijalar', filter=Q(natijalar__savol__kvest__isnull=True)),
        points=Sum('natijalar__stars', filter=Q(natijalar__savol__kvest__isnull=True)),
    ).order_by('first_name', 'last_name', 'username')
    return render(request, 'portal/students.html', {'students': students, 'group': group, 'groups': groups_for(request.user)})


@never_cache
@educator_required
@require_http_methods(['GET', 'POST'])
def student_add(request, pk):
    group = get_object_or_404(groups_for(request.user), pk=pk)
    if request.method == 'POST' and request.POST.get('action') not in ('create', 'attach'):
        raise PermissionDenied
    creating = request.POST.get('action') == 'create'
    new_form = NewStudentForm(request.POST if request.method == 'POST' and creating else None, prefix='new')
    attach_form = AttachStudentForm(
        request.POST if request.method == 'POST' and not creating else None,
        actor=request.user, group=group, request=request, prefix='existing',
    )
    if request.method == 'POST':
        if creating and new_form.is_valid():
            with transaction.atomic():
                # Recheck ownership immediately before changing membership.
                group = get_object_or_404(groups_for(request.user).select_for_update(), pk=pk)
                pupil = new_form.save(commit=False)
                pupil.role, pupil.guruh = User.Role.OQUVCHI, group
                pupil.teacher_approved = pupil.is_staff = pupil.is_superuser = False
                pupil.save()
            messages.success(request, 'O‘quvchi hisobi yaratildi va guruhga biriktirildi.')
            return redirect('oquvchi_detail', pk=pupil.pk)
        if not creating and attach_form.is_valid():
            with transaction.atomic():
                group = get_object_or_404(groups_for(request.user).select_for_update(), pk=pk)
                pupil = User.objects.select_for_update().get(pk=attach_form.cleaned_data['pupil'].pk)
                if (not pupil.is_oquvchi or not pupil.is_active or
                        (not request.user.is_superadmin and pupil.guruh_id not in (None, group.pk))):
                    raise PermissionDenied
                pupil.guruh = group
                pupil.save(update_fields=['guruh'])
            messages.success(request, 'O‘quvchi guruhga biriktirildi.')
            return redirect('oquvchi_detail', pk=pupil.pk)
    return render(request, 'portal/student_add.html', {'group': group, 'new_form': new_form, 'attach_form': attach_form})


def _student_context(pupil):
    results = list(SavolNatija.objects.filter(user=pupil, savol__kvest__isnull=True)
                   .select_related('savol__bolimcha__bolim').order_by('-updated_at'))
    solved = Counter(result.savol.bolimcha_id for result in results)
    points = Counter()
    for result in results:
        points[result.savol.bolimcha_id] += result.stars
    sections = []
    for section in Bolimcha.objects.select_related('bolim').annotate(
        total=Count('savollar', filter=Q(savollar__kvest__isnull=True)),
    ).order_by('bolim__order', 'order'):
        sections.append({'section': section, 'total': section.total,
                         'solved': solved[section.pk], 'points': points[section.pk],
                         'percent': round(100 * solved[section.pk] / section.total) if section.total else 0})
    return {'pupil': pupil, 'sections': sections, 'recent_results': results[:12],
            'solved_count': len(results), 'points': sum(result.stars for result in results)}


@never_cache
@educator_required
@require_GET
def student_detail(request, pk):
    pupil = get_object_or_404(students_for(request.user), pk=pk)
    return render(request, 'portal/student_detail.html', {
        **_student_context(pupil), 'voices': voices_for(request.user).filter(user=pupil),
    })


@never_cache
@oquvchi_required
@require_GET
def my_results(request):
    return render(request, 'portal/student_detail.html', {
        **_student_context(request.user), 'voices': voices_for(request.user), 'own_results': True,
    })


@never_cache
@educator_required
@require_http_methods(['GET', 'POST'])
def student_edit(request, pk):
    pupil = get_object_or_404(students_for(request.user), pk=pk)
    form = StudentEditForm(request.POST if request.method == 'POST' else None, actor=request.user, instance=pupil)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'O‘quvchi ma’lumotlari saqlandi.')
        return redirect('oquvchilar')
    return _form_page(request, form, 'O‘quvchini tahrirlash', reverse('oquvchi_detail', args=[pupil.pk]))


@never_cache
@superadmin_required
@require_GET
def teacher_list(request):
    return render(request, 'portal/teachers.html', {
        'teachers': User.objects.filter(role=User.Role.TARBIYACHI, is_superuser=False)
        .annotate(group_count=Count('guruhlar')).order_by('teacher_approved', 'first_name', 'username'),
    })


@never_cache
@superadmin_required
@require_POST
def teacher_approval(request, pk):
    teacher = get_object_or_404(User, pk=pk, role=User.Role.TARBIYACHI, is_superuser=False)
    action = request.POST.get('action')
    if action not in ('approve', 'revoke'):
        raise PermissionDenied
    teacher.teacher_approved = action == 'approve'
    teacher.save(update_fields=['teacher_approved'])
    messages.success(request, 'Tarbiyachi tasdiqlandi.' if teacher.teacher_approved else 'Tarbiyachining tasdig‘i bekor qilindi.')
    return redirect('tarbiyachilar')


@never_cache
@educator_required
@require_GET
def voice_list(request):
    voices = voices_for(request.user).filter(user__in=students_for(request.user))
    if request.GET.get('holat') != 'hammasi':
        voices = voices.filter(tarbiyachi_bahosi__isnull=True)
    return render(request, 'portal/voices.html', {'voices': voices, 'all_voices': request.GET.get('holat') == 'hammasi'})


@never_cache
@educator_required
@require_http_methods(['GET', 'POST'])
def voice_review(request, pk):
    voice = get_object_or_404(voices_for(request.user), pk=pk)
    form = VoiceReviewForm(request.POST if request.method == 'POST' else None, instance=voice)
    if request.method == 'POST' and form.is_valid():
        voice.baholagan, voice.baholangan_at = request.user, timezone.now()
        form.save()
        messages.success(request, 'Ovozli javob baholandi.')
        return redirect('ovozlar')
    return render(request, 'portal/voice_review.html', {'voice': voice, 'form': form})


@never_cache
@login_required
@require_GET
def voice_file(request, pk):
    voice = get_object_or_404(voices_for(request.user), pk=pk)
    try:
        stream = voice.fayl.open('rb')
    except FileNotFoundError:
        raise Http404 from None
    suffix = Path(voice.fayl.name).suffix.lower()
    content_type = {'.webm': 'audio/webm', '.ogg': 'audio/ogg', '.mp4': 'audio/mp4',
                    '.m4a': 'audio/mp4', '.mp3': 'audio/mpeg', '.wav': 'audio/wav'}.get(suffix, 'application/octet-stream')
    response = FileResponse(stream, content_type=content_type)
    response['X-Content-Type-Options'] = 'nosniff'
    response['Cross-Origin-Resource-Policy'] = 'same-origin'
    response['Referrer-Policy'] = 'same-origin'
    return response


@never_cache
@educator_required
@require_GET
def preview_catalog(request):
    return render(request, 'portal/preview_catalog.html', {
        'sections': Bolimcha.objects.select_related('bolim').prefetch_related(
            Prefetch('savollar', queryset=Savol.objects.filter(kvest__isnull=True)),
        ).order_by('bolim__order', 'order'),
    })


@never_cache
@educator_required
@require_http_methods(['GET', 'POST'])
def preview_question(request, pk):
    question = get_object_or_404(Savol, pk=pk, kvest__isnull=True)
    passed = request.method == 'POST' and question.tekshir(request.POST)
    state = _oyin_holati(question, 0)
    return render(request, 'savol.html', {
        'savol': question, 'sinov': True, 'yutuq': passed,
        'h_self': state, 'bosqichlar': state.get('bosqichlar', []),
        'xato': request.method == 'POST' and not passed,
        'next_savol': question.bolimcha.savollar.filter(kvest__isnull=True, order__gt=question.order).first(),
    })
