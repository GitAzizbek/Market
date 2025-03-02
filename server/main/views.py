from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import ProductModel
from .serializers import ProductSerializer, ProductCreateSerializer
from main.responses import SuccessResponse, ErrorResponse

class ProductViewSet(viewsets.ModelViewSet):
    queryset = ProductModel.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProductCreateSerializer
        return ProductSerializer

    def list(self, request, *args, **kwargs):
        """Mahsulotlar ro'yxatini chiqarish"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(
            data=serializer.data,
            message="Mahsulotlar muvaffaqiyatli olindi",
            status=200
        )

    def retrieve(self, request, *args, **kwargs):
        """Bitta mahsulot tafsilotlarini chiqarish"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return SuccessResponse(
            data=serializer.data,
            message="Mahsulot tafsilotlari muvaffaqiyatli olindi",
            status=200
        )

    def create(self, request, *args, **kwargs):
        """Yangi mahsulot qo'shish"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            return SuccessResponse(
                data=ProductSerializer(product).data,
                message="Mahsulot muvaffaqiyatli qo'shildi",
                status=201
            )
        return ErrorResponse(
            error=serializer.errors,
            message="Mahsulot qo'shishda xatolik yuz berdi",
            status=400,
            path=request.path,
            method=request.method
        )

    def destroy(self, request, *args, **kwargs):
        """Mahsulotni o‘chirish"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return SuccessResponse(
            data=[],
            message="Mahsulot muvaffaqiyatli o'chirildi",
            status=204
        )
