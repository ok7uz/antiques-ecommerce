from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.order.serializers import OrderSerializer


class OrderView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=OrderSerializer(),
        responses={200: 'Order saved!'},
        tags=['Order'],
    )
    def post(self, request):
        serializer = OrderSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'message': 'Order saved!'}, status=status.HTTP_200_OK)
        return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
