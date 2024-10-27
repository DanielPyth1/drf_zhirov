from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Course(models.Model):
    title = models.CharField(max_length=200)
    preview = models.ImageField(upload_to='course_previews/')
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')  # Исправлено на единый related_name

    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    preview = models.ImageField(upload_to='lesson_previews/')
    description = models.TextField()
    video_url = models.URLField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lessons')  # Исправлено на единый related_name

    def __str__(self):
        return self.title
