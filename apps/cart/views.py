from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.cart.serializers import CartSerializer


class CartView(APIView):
    @swagger_auto_schema(
        request_body=CartSerializer,
        operation_description="Cart",
        tags=['Cart'],
        responses={201: CartSerializer(many=True)}
    )
    def post(self, request):
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
