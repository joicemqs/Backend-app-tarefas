from rest_framework.test import APITestCase
from django.core import mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()

class AccountsAPITestCase(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('token_obtain_pair')
        self.token_refresh_url = reverse('token_refresh')
        self.me_url = reverse('user_me')
        self.password_reset_request_url = reverse('password_reset_request')
        self.password_reset_confirm_url = reverse('password_reset_confirm')

        self.user_data = {
            'username': 'juliana',
            'email': 'juliana@example.com',
            'password': '123456'
        }

        self.user = User.objects.create_user(**self.user_data)

    def test_register_user(self):
        data = {
            'username': 'nova_juliana',
            'email': 'nova_juliana@example.com',
            'password': 'SenhaForte#2025'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_user(self):
        response = self.client.post(self.login_url, {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.token = response.data['access']

    def test_token_refresh(self):
        login_response = self.client.post(self.login_url, {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        })
        refresh_token = login_response.data['refresh']
        response = self.client.post(self.token_refresh_url, {'refresh': refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_me_requires_authentication(self):
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_me_returns_only_authenticated_user(self):
        User.objects.create_user(username='outra', email='outra@example.com', password='123456')
        login_response = self.client.post(self.login_url, {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        })
        token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user_data['email'])
        self.assertNotIn('outra@example.com', str(response.data))

    def test_password_reset_request(self):
        response = self.client.post(self.password_reset_request_url, {'email': self.user_data['email']})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.user_data['email']])

    def test_password_reset_request_does_not_reveal_unknown_email(self):
        known = self.client.post(self.password_reset_request_url, {'email': self.user_data['email']})
        unknown = self.client.post(self.password_reset_request_url, {'email': 'naoexiste@example.com'})
        self.assertEqual(unknown.status_code, status.HTTP_200_OK)
        self.assertEqual(unknown.data, known.data)
        self.assertEqual(len(mail.outbox), 1)  # só o e-mail cadastrado recebeu

    def test_password_reset_confirm_valid_token(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        response = self.client.post(self.password_reset_confirm_url, {
            'uid': uid,
            'token': token,
            'new_password': 'NovaSenha#2025'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NovaSenha#2025'))

    def test_password_reset_confirm_invalid_token(self):
        data = {
            'token': 'token_invalido',
            'uid': 'uid_invalido',
            'new_password': 'nova_senha123'
        }
        response = self.client.post(self.password_reset_confirm_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
