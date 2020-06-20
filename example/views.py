from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from example.models import *
from example.serializers import *
from userprofile.permissions import IsEditor


class FindExamples(APIView):
    """
    Find examples by word.
    maximum parameter limits the size of a returned array, defaults to 5.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, word=None):
        if not word:
            return Response({"detail": "Word not given"}, status=400)
        examples = Example.objects.filter(string__icontains=word)
        if 'maximum' in request.query_params:
            maximum = request.query_params['maximum']
        else:
            maximum = 5
        examples = examples[:maximum]
        examples_serializer = ExamplesSerializer(examples, many=True)
        return Response(examples_serializer.data)


class ExampleView(RetrieveUpdateDestroyAPIView):
    queryset = Example.objects.all()
    serializer_class = ExamplesSerializer
    permission_classes = [IsEditor]
