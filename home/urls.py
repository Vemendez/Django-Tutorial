from django.urls import path, reverse_lazy
from home.views import HomeView
from . import views
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordResetView, TemplateView
, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('connect/(?P<operation>.+)/(?P<pk>\d+)', views.change_friends, name='change_friends')
]
app_name = 'home'