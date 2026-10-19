from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from django.utils.dateparse import parse_datetime
from apps.tasks.models import Task

User = get_user_model()

class TaskAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='juliana', email='juliana@example.com', password='123456')

        login_response = self.client.post(reverse('token_obtain_pair'), {
            'email': 'juliana@example.com',
            'password': '123456'
        })
        self.token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        self.task = Task.objects.create(
            owner=self.user,
            title='Comprar ingredientes',
            description='Ir ao mercado comprar ovos e farinha',
            is_completed=False
        )

    def test_list_tasks(self):
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_task(self):
        data = {
            'title': 'Estudar Django',
            'description': 'Revisar testes com APITestCase',
            'is_completed': False
        }
        response = self.client.post('/api/tasks/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], data['title'])
        self.assertEqual(response.data['owner'], self.user.id)

    def test_retrieve_task(self):
        response = self.client.get(f'/api/tasks/{self.task.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.task.title)

    def test_update_task(self):
        updated_data = {
            'title': 'Comprar ingredientes atualizados',
            'description': 'Ir ao mercado e padaria',
            'is_completed': True
        }
        response = self.client.put(f'/api/tasks/{self.task.id}/', updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_completed'], True)

    def test_partial_update_task(self):
        response = self.client.patch(f'/api/tasks/{self.task.id}/', {'is_completed': True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_completed'], True)

    def test_delete_task(self):
        response = self.client.delete(f'/api/tasks/{self.task.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_create_task_with_due_date(self):
        response = self.client.post('/api/tasks/', {'title': 'Com prazo', 'due_date': '2026-10-20T14:30:00-03:00'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # compara como datetime: a API pode devolver o mesmo instante em outro fuso
        self.assertEqual(parse_datetime(response.data['due_date']), parse_datetime('2026-10-20T14:30:00-03:00'))

    def test_create_task_with_utc_due_date(self):
        # o app envia em UTC (Date.toISOString(), com "Z"); 17:30 UTC = 14:30 em Brasília
        response = self.client.post('/api/tasks/', {'title': 'Com prazo', 'due_date': '2026-10-20T17:30:00.000Z'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(parse_datetime(response.data['due_date']), parse_datetime('2026-10-20T14:30:00-03:00'))

    def test_create_task_without_due_date(self):
        response = self.client.post('/api/tasks/', {'title': 'Sem prazo'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(response.data['due_date'])

    def test_update_task_due_date(self):
        response = self.client.patch(f'/api/tasks/{self.task.id}/', {'due_date': '2026-10-25T09:00:00-03:00'}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(parse_datetime(response.data['due_date']), parse_datetime('2026-10-25T09:00:00-03:00'))

    def test_remove_task_due_date(self):
        task = Task.objects.create(owner=self.user, title='Com prazo', due_date=parse_datetime('2026-10-20T14:30:00-03:00'))

        response = self.client.patch(f'/api/tasks/{task.id}/', {'due_date': None}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.data['due_date'])
        task.refresh_from_db()
        self.assertIsNone(task.due_date)

    def test_create_task_with_invalid_due_date(self):
        for invalid in ['2026-13-01T10:00:00', '20/10/2026 14:30', 'amanhã']:
            response = self.client.post('/api/tasks/', {'title': 'Data inválida', 'due_date': invalid})
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, invalid)
            self.assertIn('due_date', response.data)

    def test_create_task_with_null_due_date(self):
        response = self.client.post('/api/tasks/', {'title': 'Sem prazo', 'due_date': None}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(response.data['due_date'])
