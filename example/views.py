from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from example.models import *
from example.serializers import *


class FindExamples(APIView):
    """
    Find examples by word.

    maximum parameter limits the size of a returned array, defaults to 5.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, word=None):
        if not word:
            return Response(data='{"detail": "Word not given"}', status=400, content_type='application/json')
        examples = Example.objects.filter(string__icontains=word)
        if 'maximum' in request.query_params:
            maximum = request.query_params['maximum']
        else:
            maximum = 5
        examples = examples[:maximum]
        examples_serializer = ExamplesSerializer(examples, many=True)
        examples_json = JSONRenderer().render(examples_serializer.data)
        return Response(data=examples_json, status=200, content_type='application/json')