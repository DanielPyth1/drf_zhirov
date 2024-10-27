from rest_framework import serializers
from .models import Course, Lesson

class LessonSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = Lesson
        fields = ['title', 'preview', 'description', 'video_url', 'course', 'owner']


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['title', 'description', 'preview', 'owner', 'lessons', 'lessons_count']  # добавьте необходимые поля
        read_only_fields = ['owner']

    def get_lessons_count(self, obj):
        return obj.lessons.count()
