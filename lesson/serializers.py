from rest_framework.serializers import ModelSerializer

from lesson.models import Lesson


class LessonSerializer(ModelSerializer):
    """
    Serializer that should be used for listing lessons
    """
    class Meta:
        model = Lesson
        fields = ['id', 'name', 'difficulty']
