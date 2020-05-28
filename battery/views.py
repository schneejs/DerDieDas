from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from django.forms.models import model_to_dict
from battery.models import *
from battery.serializers import *


class BatteryView(APIView):
    """
    Get user's batteries. Add lesson_id parameter for lesson specific batteries.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        params = request.query_params
        if 'lesson_id' in params:
            id = int(params['lesson_id'])
            batteries = Battery.objects.filter(user=request.user, card__lesson=id)
        else:
            batteries = Battery.objects.filter(user=request.user)
        batteries_serializer = UserBatteriesSerializer(batteries, many=True)
        batteries_json = JSONRenderer().render(batteries_serializer.data)
        return Response(data=batteries_json)