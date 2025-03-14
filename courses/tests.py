from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from courses.models import Course, Lesson
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@courses.com')
        self.course = Course.objects.create(name='Test Course', description='Test Course Description', owner=self.user)
        self.lesson = Lesson.objects.create(name='Test Lesson', course=self.course,
                                            description='Test Lesson Description',
                                            video_url='https://www.youtube.com/1', owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_list(self):
        url = reverse('courses:lesson_list')
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "video_url": "https://www.youtube.com/1",
                    "name": "Test Lesson",
                    "preview": None,
                    "description": "Test Lesson Description",
                    "course": self.course.pk,
                    "owner": self.user.pk,
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_lesson_retrieve(self):
        url = reverse('courses:lesson_detail', args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('name'), self.lesson.name)

    def test_lesson_create(self):
        url = reverse('courses:lesson_create')
        data = {'name': 'Test Lesson1', 'video_url': 'https://www.youtube.com/2', 'owner': self.user.pk}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        url = reverse('courses:lesson_update', args=(self.lesson.pk,))
        data = {'name': 'Test Lesson2'}
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('name'), 'Test Lesson2')

    def test_lesson_delete(self):
        url = reverse('courses:lesson_delete', args=(self.lesson.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)
