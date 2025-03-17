from rest_framework import serializers, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from .models import *
from .serializers import *
from rest_framework.views import APIView

class OrderViewSet(viewsets.ModelViewSet):
    queryset = OrderModel.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return OrderModel.objects.filter(user=self.request.user).order_by('-created_at')
    
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        order = self.get_object()
        order.payment_status = 'confirmed'
        order.save()
        return Response({'status': 'Buyurtma tasdiqlandi'})
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        order.payment_status = 'canceled'
        order.save()
        return Response({'status': 'Buyurtma bekor qilindi'})

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError

class UploadCheck(APIView):
    def post(self, request, order_id):
        # Buyurtmani topamiz
        order = OrderModel.objects.filter(pk=order_id).first()
        if not order:
            return Response({"message": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        # Faylni olish
        checkfile = request.FILES.get('file')
        if not checkfile:
            return Response({"message": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        # Fayl turini tekshirish (faqat rasm yoki PDF)
        valid_mime_types = ["image/png", "image/jpeg", "image/jpg", "application/pdf"]
        if checkfile.content_type not in valid_mime_types:
            return Response(
                {"message": "Invalid file format. Only PNG, JPG, JPEG, and PDF allowed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Faylni saqlash
        order.payment_check = checkfile
        order.save()

        return Response({"message": "Success"}, status=status.HTTP_200_OK)

class CashboxView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        cashbox, _ = CashboxModel.objects.get_or_create(id=1)
        return Response({"total_income": cashbox.total_income})

    def post(self, request):
        cashbox = CashboxModel.objects.get(id=1)
        cashbox.total_income = 0
        cashbox.save()
        return Response({"message": "Kassa nolga tushirildi!"})