from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import PredictionRequest
from .serializers import PredictionRequestSerializer

class PredictView(APIView):
    def post(self, request):
        serializer = PredictionRequestSerializer(data=request.data)
        if serializer.is_valid():
            prediction_request = serializer.save()

            # Dummy prediction (replace with your ML model later)
            prediction_request.prediction_result = {"result": "success"}
            prediction_request.save()

            return Response(PredictionRequestSerializer(prediction_request).data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
