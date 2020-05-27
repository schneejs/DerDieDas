from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from django.forms.models import model_to_dict
from main.models import *
from main.serializers import *


class ListLessons(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        lessons = [model_to_dict(lesson) for lesson in Lesson.objects.all()]
        lessons_json = JSONRenderer().render(lessons)
        return Response(data=lessons_json, status=200, content_type='application/json')

    
class LoadLesson(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, lesson_id=None):
        if not lesson_id:
            return Response(data='{"detail": "Lesson not given"}', status=400, content_type='application/json')
        try:
            lesson = Lesson.objects.get(pk=lesson_id)
        except Lesson.DoesNotExist:
            return Response(data='{"detail": "Lesson not found"}', status=404, content_type='application/json')
        user = request.user
        lesson_serializer = LessonSerializer(instance=lesson)
        lesson_json = JSONRenderer().render(lesson_serializer.data)
        return Response(data=lesson_json, status=200, content_type='application/json')
