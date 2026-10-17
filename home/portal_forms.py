from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

from .access import groups_for
from .models import Guruh, OvozJavob, User


def style_fields(form):
    for field in form.fields.values():
        field.widget.attrs['class'] = 'input'


class GroupForm(forms.ModelForm):
    class Meta:
        model = Guruh
        fields = ('nom', 'tarbiyachi')

    def __init__(self, *args, actor, **kwargs):
        super().__init__(*args, **kwargs)
        if actor.is_superadmin:
            self.fields['tarbiyachi'].queryset = User.objects.filter(
                role=User.Role.TARBIYACHI, teacher_approved=True, is_active=True, is_superuser=False,
            ).order_by('first_name', 'username')
            self.fields['tarbiyachi'].help_text = 'Ro‘yxatda yo‘q bo‘lsa, avval Tarbiyachilar bo‘limida hisobni tasdiqlang.'
        else:
            self.fields.pop('tarbiyachi')
            self.instance.tarbiyachi = actor
        style_fields(self)


class NewStudentForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')
        labels = {'username': 'Login', 'first_name': 'Ism', 'last_name': 'Familiya'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['username'].help_text = '150 tagacha belgi. Harf, raqam va @/./+/-/_ ishlatish mumkin.'
        self.fields['password1'].label = 'Boshlang‘ich parol'
        self.fields['password1'].help_text = 'Bola eslab qoladigan, boshqalar taxmin qila olmaydigan parol tanlang.'
        self.fields['password2'].label = 'Parolni takrorlang'
        self.fields['password2'].help_text = 'Tasdiqlash uchun parolni yana kiriting.'
        style_fields(self)


class AttachStudentForm(forms.Form):
    username = forms.CharField(max_length=150, label='O‘quvchi logini')
    password = forms.CharField(label='O‘quvchi paroli', widget=forms.PasswordInput)

    def __init__(self, *args, actor, group, request=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.actor, self.group, self.request = actor, group, request
        if actor.is_superadmin:
            self.fields.pop('password')
        else:
            self.fields['password'].help_text = 'Mavjud hisobni biriktirish uchun uning egasi ma’lumotlarini tasdiqlang.'
        style_fields(self)

    def clean(self):
        cleaned = super().clean()
        if self.errors:
            return cleaned
        if self.actor.is_superadmin:
            pupil = User.objects.filter(username=cleaned['username'], is_active=True).first()
        else:
            pupil = authenticate(self.request, username=cleaned['username'], password=cleaned['password'])
        if (not pupil or not pupil.is_oquvchi or
                (not self.actor.is_superadmin and pupil.guruh_id not in (None, self.group.pk))):
            raise forms.ValidationError('Bu hisobni guruhga biriktirib bo‘lmadi. Ma’lumotlarni tekshiring yoki administratorga murojaat qiling.')
        cleaned['pupil'] = pupil
        return cleaned


class StudentEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'guruh')
        labels = {'first_name': 'Ism', 'last_name': 'Familiya', 'guruh': 'Guruh'}

    def __init__(self, *args, actor, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['guruh'].queryset = groups_for(actor)
        self.fields['guruh'].empty_label = 'Guruhga biriktirilmagan'
        style_fields(self)


class VoiceReviewForm(forms.ModelForm):
    tarbiyachi_bahosi = forms.TypedChoiceField(
        choices=[('', 'Bahoni tanlang'), (1, '⭐ 1 yulduz'), (2, '⭐⭐ 2 yulduz'), (3, '⭐⭐⭐ 3 yulduz')],
        coerce=int, label='Tarbiyachi bahosi',
    )

    class Meta:
        model = OvozJavob
        fields = ('tarbiyachi_bahosi', 'tarbiyachi_izohi')
        widgets = {'tarbiyachi_izohi': forms.Textarea(attrs={'rows': 4})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        style_fields(self)
