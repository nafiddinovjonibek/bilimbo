from django.urls import path

from . import book_views
from . import portal_views
from .views import UserLoginView, bolim, bolimcha, home, logout_view, register_view, savol

urlpatterns = [
    path('', home, name='home'),
    path('kabinet/', portal_views.dashboard, name='kabinet'),
    path('kabinet/guruh/yangi/', portal_views.group_edit, name='guruh_yangi'),
    path('kabinet/guruh/<int:pk>/tahrirlash/', portal_views.group_edit, name='guruh_edit'),
    path('kabinet/guruh/<int:pk>/ochirish/', portal_views.group_delete, name='guruh_delete'),
    path('kabinet/guruh/<int:pk>/oquvchi/', portal_views.student_add, name='oquvchi_add'),
    path('kabinet/oquvchilar/', portal_views.student_list, name='oquvchilar'),
    path('kabinet/oquvchi/<int:pk>/', portal_views.student_detail, name='oquvchi_detail'),
    path('kabinet/oquvchi/<int:pk>/tahrirlash/', portal_views.student_edit, name='oquvchi_edit'),
    path('kabinet/tarbiyachilar/', portal_views.teacher_list, name='tarbiyachilar'),
    path('kabinet/tarbiyachi/<int:pk>/tasdiq/', portal_views.teacher_approval, name='tarbiyachi_approval'),
    path('kabinet/ovozlar/', portal_views.voice_list, name='ovozlar'),
    path('kabinet/ovoz/<int:pk>/', portal_views.voice_review, name='ovoz_review'),
    path('ovoz/<int:pk>/tinglash/', portal_views.voice_file, name='ovoz_fayl'),
    path('sinov/', portal_views.preview_catalog, name='sinov'),
    path('sinov/<int:pk>/', portal_views.preview_question, name='sinov_savol'),
    path('natijalarim/', portal_views.my_results, name='natijalarim'),
    path('kutubxona/', book_views.kutubxona, name='kutubxona'),
    path('kutubxona/<int:pk>/', book_views.kitob_oqish, name='kitob_oqish'),
    path('kutubxona/<int:pk>/muqova/', book_views.kitob_muqova, name='kitob_muqova'),
    path('kutubxona/<int:pk>/sahifa/<int:number>/', book_views.kitob_sahifa, name='kitob_sahifa'),
    path('bolim/<int:num>/', bolim, name='bolim'),
    path('bolimcha/<int:pk>/', bolimcha, name='bolimcha'),
    path('savol/<int:pk>/', savol, name='savol'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
]
