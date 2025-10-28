from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from apps.tasks.models import Task

User = get_user_model()

class TaskInvalidAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='juliana', email='juliana@example.com', password='123456')
        login_response = self.client.post(reverse('token_obtain_pair'), {
            'email': 'juliana@example.com',
            'password': '123456'
        })
        self.token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_create_task_missing_fields(self):
        # 'title' é obrigatório
        data = {
            'description': 'Faltando título',
            'is_completed': False
        }
        response = self.client.post('/api/tasks/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)

    def test_create_task_invalid_type(self):
        # 'is_completed' deve ser booleano
        data = {
            'title': 'Teste inválido',
            'description': 'Tipo errado',
            'is_completed': 'não'
        }
        response = self.client.post('/api/tasks/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('is_completed', response.data)

    def test_access_without_authentication(self):
        self.client.credentials()  # remove token
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_nonexistent_task(self):
        response = self.client.put('/api/tasks/9999/', {
            'title': 'Atualização inválida',
            'description': 'Tarefa não existe',
            'is_completed': True
        })
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_nonexistent_task(self):
        response = self.client.delete('/api/tasks/9999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
