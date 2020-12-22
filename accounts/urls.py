from django.urls import path, reverse_lazy
from accounts import views
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordResetView
, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
)

urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/(?P<pk>\d+)?', views.profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('reset-password/', PasswordResetView.as_view(template_name='accounts/reset_password.html'
                                                      , success_url=reverse_lazy('accounts:password_reset_done')
                                                      , email_template_name='accounts/reset_password_email.html')
         , name='reset_password'),

    path('reset-password/done/'
         , PasswordResetDoneView.as_view(template_name='accounts/reset_password_done.html')
         , name='password_reset_done'),

    path('reset-password/confirm/<uidb64>/<token>/'
         , PasswordResetConfirmView.as_view(template_name='accounts/reset_password_confirm.html'
                                            , success_url=reverse_lazy('accounts:password_reset_complete'))
         , name='password_reset_confirm'),

    path('reset-password/complete/'
         , PasswordResetCompleteView.as_view(template_name='accounts/reset_password_complete.html')
         , name='password_reset_complete')
]
app_name = 'accounts'
