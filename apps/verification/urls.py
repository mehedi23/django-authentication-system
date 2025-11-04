from django.urls import path , include
from .views import SendOTPView,VerifyOTPView ,ForgotPasswordSendOTPView, ForgotPasswordVerifyOTPView,ResetPasswordView

urlpatterns = (
    [
        path('me/email/request-verify/',SendOTPView.as_view(),name='request-verify'),
        path('me/email/conform-verify/',VerifyOTPView.as_view(),name='conform-verify'),

        path("user/forgot-password/send-otp/", ForgotPasswordSendOTPView.as_view(),name='forgot-password-send-otp'),
        path("user/forgot-password/verify-otp/", ForgotPasswordVerifyOTPView.as_view(),name='forgot-password-verify-otp'),
        path("user/forgot-password/reset/", ResetPasswordView.as_view(),name='forgot-password-reset'),
    ]  
)