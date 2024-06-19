from smtplib import SMTPDataError
from django.core.mail import EmailMultiAlternatives

from django.core.mail import send_mail
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.order.serializers import OrderSerializer, CallbackSerializer
from config.settings.base import EMAIL_HOST_USER, RECIPIENT_EMAIL


class OrderView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=OrderSerializer(),
        responses={200: 'Order saved!', 400: 'Errors'},
        tags=['Order'],
    )
    def post(self, request):
        serializer = OrderSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'success': True, 'message': 'Order saved!'}, status=status.HTTP_200_OK)
        return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CallbackView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=CallbackSerializer(),
        responses={200: 'Callback data saved!', 400: 'Errors'},
        tags=['Order'],
    )
    def post(self, request):
        serializer = CallbackSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            applicant_name = serializer.data.get('applicant_name')
            applicant_email = serializer.data.get('applicant_email')
            message = 'Имя: ' + applicant_name + '\n' + 'Email: ' + applicant_email
            try:
                applicant_name = serializer.data.get('applicant_name')
                applicant_email = serializer.data.get('applicant_email')
                text_content = 'Имя: ' + applicant_name + '\n' + 'Email: ' + applicant_email
                html_content = '<b>Имя:</b>  ' + applicant_name + '<br>' + '<b>Email:</b>  ' + applicant_email
                subject, from_email, to = 'ОБРАТНАЯ СВЯЗЬ', EMAIL_HOST_USER, RECIPIENT_EMAIL
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
            except SMTPDataError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'success': True, 'message': 'Callback data saved!'}, status=status.HTTP_200_OK)
        return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
