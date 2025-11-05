from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from apps.users.models import User
from apps.verification.models import EmailOTP

class TestEmailOTPAPI(APITestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='StrongPass123!'
        )
        self.user.is_email_verify = False
        self.user.save()

        # JWT token
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        # URLs
        self.send_otp_url = reverse('verification:request-verify')
        self.verify_otp_url = reverse('verification:conform-verify')
        self.forgot_send_otp_url = reverse('verification:forgot-password-send-otp')
        self.forgot_verify_otp_url = reverse('verification:forgot-password-verify-otp')
        self.reset_password_url = reverse('verification:forgot-password-reset')

    # --------------------------
    # Authenticated user OTP flow
    # --------------------------
    def test_send_otp_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.post(self.send_otp_url, {'email': self.user.email}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], "OTP sent successfully")

    def test_send_otp_wrong_email(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.post(self.send_otp_url, {'email': 'wrong@example.com'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_verify_otp_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        # Send OTP first
        self.client.post(self.send_otp_url, {'email': self.user.email}, format='json')
        otp_obj = EmailOTP.objects.filter(user=self.user).last()

        response = self.client.post(self.verify_otp_url, {'email': self.user.email, 'otp': otp_obj.otp}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], "OTP verified successfully")

    # --------------------------
    # Forgot password OTP flow for Anonymous user
    # ---------------------------
    def test_forgot_password_send_otp(self):
        response = self.client.post(self.forgot_send_otp_url, {'email': self.user.email}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], "OTP sent to email")

    def test_forgot_password_verify_otp(self):
        # Send OTP first
        self.client.post(self.forgot_send_otp_url, {'email': self.user.email}, format='json')
        otp_obj = EmailOTP.objects.filter(user=self.user).last()

        response = self.client.post(self.forgot_verify_otp_url, {'email': self.user.email, 'otp': otp_obj.otp}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], "OTP verified successfully")

    def test_forgot_password_reset(self):
        # Send and verify OTP first
        self.client.post(self.forgot_send_otp_url, {'email': self.user.email}, format='json')
        otp_obj = EmailOTP.objects.filter(user=self.user).last()
        otp_obj.is_verified = True
        otp_obj.save()

        new_password = "NewStrongPass123!"
        response = self.client.post(self.reset_password_url,{'email': self.user.email, 'otp': otp_obj.otp, 'new_password': new_password},format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], "Password reset successful")

        # Verify password updated
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(new_password))

    # --------------------------
    # Negative tests
    # --------------------------
    def test_forgot_password_send_otp_nonexistent_email(self):
        response = self.client.post(self.forgot_send_otp_url, {'email': 'nonexistent@example.com'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_forgot_password_reset_wrong_otp(self):
        # Send OTP
        self.client.post(self.forgot_send_otp_url, {'email': self.user.email}, format='json')
        otp_obj = EmailOTP.objects.filter(user=self.user).last()
        otp_obj.is_verified = True
        otp_obj.save()

        response = self.client.post(self.reset_password_url,{'email': self.user.email, 'otp': '000000', 'new_password': 'AnotherPass123!'},format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], "OTP not verified or expired")
