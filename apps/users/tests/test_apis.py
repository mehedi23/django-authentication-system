from django.test import TestCase

# Create your tests here. 
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from apps.users.models import User
from rest_framework_simplejwt.tokens import RefreshToken
import uuid

class TestUserAPI(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('users:register')
        self.login_url = reverse('users:login')
        self.login_refresh_url = reverse('users:login-refresh')
        self.user_me_url = reverse('users:self-me')
        self.change_password_url = reverse('users:change-password')

        # Test user data
        self.user_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'phone_number': '1234567890',
            'password': 'StrongPass123!'
        }

        # Create an existing user
        self.user = User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='StrongPass123!'
        )

        # Custom making verify - for test
        self.user.is_email_verify = True
        self.user.save()

        # Generate token for existing user
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

    # --------------------------
    # Registration tests
    # --------------------------
    def test_user_registration(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data) 

    def test_duplicate_email_registration(self):
        User.objects.create_user(username='duplicate',email=self.user_data['email'],password='StrongPass123!')
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    # --------------------------
    # Login tests
    # --------------------------
    def test_user_login(self):
        login_data = {'username': self.user.username, 'password': 'StrongPass123!'}
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_invalid_credentials(self):
        login_data = {'username': self.user.username, 'password': 'WrongPass!'}
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # --------------------------
    # Token refresh test
    # --------------------------
    def test_jwt_refresh(self):
        refresh = RefreshToken.for_user(self.user)
        response = self.client.post(self.login_refresh_url, {'refresh': str(refresh)}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    # --------------------------
    # Self profile tests
    # --------------------------
    def test_get_self_profile(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get(self.user_me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)

    def test_update_self_profile_put(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        update_data = {'username':'username','first_name': 'Updated', 'last_name': 'User', 'email': 'newemail@example.com'}
        response = self.client.put(self.user_me_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(User.objects.get(id=self.user.id).is_email_verify)  # email changed - is_email_verify=False

    def test_update_self_profile_patch(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.patch(self.user_me_url, {'first_name': 'Patched'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(id=self.user.id).first_name, 'Patched')

    def test_delete_self_profile(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.delete(self.user_me_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=self.user.id).exists())

    def test_post_self_profile_not_allowed(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.post(self.user_me_url, {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # --------------------------
    # Change password tests
    # --------------------------
    def test_change_password_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        data = {'old_password': 'StrongPass123!', 'new_password': 'NewStrongPass123!'}
        response = self.client.post(self.change_password_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh user instance from DB
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NewStrongPass123!'))

    def test_change_password_wrong_old_password(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        data = {'old_password': 'WrongOldPass', 'new_password': 'NewStrongPass123!'}
        response = self.client.post(self.change_password_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('old_password', response.data)
