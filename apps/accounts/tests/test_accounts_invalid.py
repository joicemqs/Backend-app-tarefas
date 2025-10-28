from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()

class AccountsInvalidAPITestCase(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('token_obtain_pair')
        self.password_reset_request_url = reverse('password_reset_request')
        self.password_reset_confirm_url = reverse('password_reset_confirm')

        self.valid_user_data = {
            'username': 'juliana',
            'email': 'juliana@example.com',
            'password': '123456'
        }

        self.user = User.objects.create_user(**self.valid_user_data)

    def test_register_missing_fields(self):
        data = {
            'email': 'incompleto@example.com'
            # falta 'username' e 'password'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
        self.assertIn('password', response.data)

    def test_register_invalid_email(self):
        data = {
            'username': 'juliana2',
            'email': 'email-invalido',
            'password': '123456'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_login_wrong_password(self):
        response = self.client.post(self.login_url, {
            'email': self.valid_user_data['email'],
            'password': 'senhaerrada'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_nonexistent_user(self):
        response = self.client.post(self.login_url, {
            'email': 'naoexiste@example.com',
            'password': '123456'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_password_reset_request_invalid_email(self):
        response = self.client.post(self.password_reset_request_url, {'email': 'email@invalido'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_reset_confirm_invalid_token(self):
        data = {
            'token': 'token_invalido',
            'uid': 'uid_invalido',
            'new_password': 'nova_senha123'
        }
        response = self.client.post(self.password_reset_confirm_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
