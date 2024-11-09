from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Course(models.Model):
    title = models.CharField(max_length=200)
    preview = models.ImageField(upload_to='course_previews/')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='courses')

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    preview = models.ImageField(upload_to='lesson_previews/')
    description = models.TextField()
    video_url = models.URLField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='lessons')

    def __str__(self):
        return self.title


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subscriptions')

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f'{self.user} подписан на {self.course}'


class Payment(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lms_payments',  # Уникальное related_name
    )
    price_id = models.CharField(max_length=255)
    session_id = models.CharField(max_length=255)
    checkout_url = models.URLField()
