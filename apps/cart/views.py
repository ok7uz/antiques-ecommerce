from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.cart.models import Cart
from apps.cart.serializers import CartSerializer, CartItemSerializer


class CartCreateView(APIView):
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
            return Response({
                "success": True,
                "cart": serializer.data['id'],
                "data": serializer.validated_data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartView(APIView):
    @swagger_auto_schema(
        operation_description="Cart Detail",
        tags=['Cart'],
        responses={201: CartSerializer(many=True)}
    )
    def get(self, request, id):
        try:
            instance = Cart.objects.get(id=id)
        except Cart.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CartSerializer(instance)
        items = instance.items.all()
        items_list = []

        for item in items:
            item_data = CartItemSerializer(item).data
            items_list.append(item_data)

        data = serializer.data
        data['items'] = items_list
        return Response(data, status=status.HTTP_200_OK)
