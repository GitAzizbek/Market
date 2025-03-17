from rest_framework import serializers, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from .models import *
from .serializers import *
from rest_framework.views import APIView

from rest_framework.parsers import MultiPartParser, FormParser

class OrderViewSet(viewsets.ModelViewSet):
    queryset = OrderModel.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)  # Fayl yuklashni qo‘llab-quvvatlash uchun

    def get_queryset(self):
        return OrderModel.objects.filter(user=self.request.user)
    
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

    @action(detail=True, methods=['patch'])
    def upload_payment_check(self, request, pk=None):
        """To‘lov chekini yuklash uchun API"""
        order = self.get_object()
        file = request.FILES.get('payment_check')

        if not file:
            return Response({'error': 'Fayl yuborilmadi'}, status=400)

        order.payment_check = file
        order.save()
        return Response({'status': 'To‘lov cheki yuklandi', 'file_url': order.payment_check.url})


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