from .models import Guruh, OvozJavob, User


def groups_for(user):
    groups = Guruh.objects.select_related('tarbiyachi')
    if user.is_superadmin:
        return groups
    if user.is_approved_teacher:
        return groups.filter(tarbiyachi=user)
    return groups.none()


def students_for(user):
    students = User.objects.filter(role=User.Role.OQUVCHI, is_superuser=False).select_related('guruh__tarbiyachi')
    if user.is_superadmin:
        return students
    if user.is_approved_teacher:
        return students.filter(guruh__tarbiyachi=user)
    return students.none()


def voices_for(user):
    voices = OvozJavob.objects.select_related('user__guruh__tarbiyachi', 'savol__bolimcha', 'baholagan')
    if user.is_superadmin:
        return voices
    if user.is_approved_teacher:
        return voices.filter(user__in=students_for(user))
    if user.is_oquvchi:
        return voices.filter(user=user)
    return voices.none()
