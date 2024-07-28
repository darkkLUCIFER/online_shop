from django.urls import path

from apps.accounts import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('verify/', views.UserVerifyOtpView.as_view(), name='verify_otp_code'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('logout/', views.UserLogOutView.as_view(), name='user_logout'),
]