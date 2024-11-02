from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Course, Lesson, Subscription
from rest_framework.test import APIClient
from django.core.files import File

User = get_user_model()


class LessonCourseTests(APITestCase):
    def setUp(self):
        User.objects.all().delete()
        self.user1 = User.objects.create_user(username="user1", email="user1@example.com", password="password123")
        self.user2 = User.objects.create_user(username="user2", email="user2@example.com", password="password123")
        self.course = Course.objects.create(title="Test Course", description="Description", owner=self.user1)
        self.lesson = Lesson.objects.create(
            title="Test Lesson",
            description="Lesson Description",
            video_url="https://www.youtube.com/watch?v=example",
            course=self.course,
            owner=self.user1,
            preview=SimpleUploadedFile("preview.jpg", b"file_content", content_type="image/jpeg")
        )
        self.client1 = APIClient()
        self.client1.force_authenticate(user=self.user1)
        self.client2 = APIClient()
        self.client2.force_authenticate(user=self.user2)

    def test_create_lesson(self):
        url = reverse('lesson-list-create')
        with open("C:\\Users\\mario\\OneDrive\\Рабочий стол\\РП\\clou.png", "rb") as img:
            data = {
                "title": "New Lesson",
                "description": "New Description",
                "course": self.course.id,
                "video_url": "https://www.youtube.com/watch?v=example2",
                "preview": SimpleUploadedFile(name='valid_image.jpg', content=img.read(), content_type='image/jpeg')
            }
        response = self.client1.post(url, data, format='multipart')
        print("Create Lesson Response Data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_read_lesson(self):
        url = reverse('lesson-detail', args=[self.lesson.id])
        response = self.client1.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.lesson.title)

    def test_update_lesson(self):
        url = reverse('lesson-detail', args=[self.lesson.id])

        with open("C:\\Users\\mario\\OneDrive\\Рабочий стол\\РП\\cloud2566.png", "rb") as img:
            data = {
                "title": "Updated Lesson",
                "description": "Updated Description",
                "video_url": "https://www.youtube.com/watch?v=example3",
                "course": self.course.id,
                "preview": File(img, name="cloud2566.png")
            }
            response = self.client1.put(url, data, format='multipart')

        print("Update Lesson Response Data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, "Updated Lesson")

    def test_delete_lesson(self):
        url = reverse('lesson-detail', args=[self.lesson.id])
        response = self.client1.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_create_subscription(self):
        url = reverse('subscription')
        data = {"course_id": self.course.id}
        response = self.client1.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Subscription.objects.filter(user=self.user1, course=self.course).exists())

    def test_delete_subscription(self):
        Subscription.objects.create(user=self.user1, course=self.course)

        url = reverse('subscription')
        data = {"course_id": self.course.id}
        response = self.client1.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Subscription.objects.filter(user=self.user1, course=self.course).exists())

    def test_subscription_status_in_course(self):
        Subscription.objects.create(user=self.user1, course=self.course)

        url = reverse('course-detail', args=[self.course.id])
        response = self.client1.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_subscribed'])

        response = self.client2.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['is_subscribed'])
