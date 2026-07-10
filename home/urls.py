from django.urls import path

from .views import UserLoginView, bolim, bolimcha, home, logout_view, register_view, savol

urlpatterns = [
    path('', home, name='home'),
    path('bolim/<int:num>/', bolim, name='bolim'),
    path('bolimcha/<int:pk>/', bolimcha, name='bolimcha'),
    path('savol/<int:pk>/', savol, name='savol'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
]
