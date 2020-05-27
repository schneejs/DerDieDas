from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.forms.models import model_to_dict
from example.models import *


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
        examples_dict = [model_to_dict(example) for example in examples]
        return Response(data=examples_dict, status=200, content_type='application/json')