from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from apps.tasks.models import Task

User = get_user_model()

class TaskReorderAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='juliana', email='juliana@example.com', password='123456')
        self.client.force_authenticate(self.user)
        self.reorder_url = reverse('task-reorder')

        # criadas pela API para receber as posições como no app: a mais nova fica no topo
        for title in ['A', 'B', 'C', 'D']:
            self.client.post('/api/tasks/', {'title': title})

    def titles(self):
        return [t['title'] for t in self.client.get('/api/tasks/').data]

    def ids(self, *titles):
        return [Task.objects.get(owner=self.user, title=t).id for t in titles]

    def test_new_task_goes_to_top(self):
        self.assertEqual(self.titles(), ['D', 'C', 'B', 'A'])

    def test_reorder_all_tasks(self):
        response = self.client.post(self.reorder_url, {'ids': self.ids('A', 'C', 'D', 'B')}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([t['title'] for t in response.data], ['A', 'C', 'D', 'B'])
        self.assertEqual(self.titles(), ['A', 'C', 'D', 'B'])

    def test_reorder_subset_keeps_other_tasks_in_place(self):
        # lista atual: D, C, B, A -> troca só C e A (ex.: as pendentes num filtro)
        response = self.client.post(self.reorder_url, {'ids': self.ids('A', 'C')}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.titles(), ['D', 'A', 'B', 'C'])

    def test_new_task_after_reorder_still_goes_to_top(self):
        self.client.post(self.reorder_url, {'ids': self.ids('A', 'B', 'C', 'D')}, format='json')
        self.client.post('/api/tasks/', {'title': 'E'})
        self.assertEqual(self.titles(), ['E', 'A', 'B', 'C', 'D'])

    def test_position_is_read_only_on_update(self):
        task_id = self.ids('A')[0]
        self.client.patch(f'/api/tasks/{task_id}/', {'position': -100})
        self.assertEqual(self.titles()[0], 'D')

    def test_reorder_rejects_other_users_task(self):
        other = User.objects.create_user(username='outra', email='outra@example.com', password='123456')
        other_task = Task.objects.create(owner=other, title='Da outra', position=0)

        response = self.client.post(self.reorder_url, {'ids': self.ids('A') + [other_task.id]}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        other_task.refresh_from_db()
        self.assertEqual(other_task.position, 0)

    def test_reorder_rejects_invalid_payload(self):
        for payload in [{}, {'ids': []}, {'ids': self.ids('A', 'A')}, {'ids': [999999]}]:
            response = self.client.post(self.reorder_url, payload, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, payload)

    def test_reorder_requires_authentication(self):
        self.client.force_authenticate(None)
        response = self.client.post(self.reorder_url, {'ids': self.ids('A')}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
