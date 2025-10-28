from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()

class AccountsAPITestCase(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('token_obtain_pair')
        self.token_refresh_url = reverse('token_refresh')
        self.user_list_url = reverse('user_list')
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
            'password': 'senha123'
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

    def test_user_list_requires_authentication(self):
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_list_authenticated(self):
        login_response = self.client.post(self.login_url, {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        })
        token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_password_reset_request(self):
        response = self.client.post(self.password_reset_request_url, {'email': self.user_data['email']})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_password_reset_confirm_invalid_token(self):
        data = {
            'token': 'token_invalido',
            'uid': 'uid_invalido',
            'new_password': 'nova_senha123'
        }
        response = self.client.post(self.password_reset_confirm_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
