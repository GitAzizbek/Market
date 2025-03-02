from rest_framework import viewsets
from rest_framework.permissions import *
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *
from main.responses import SuccessResponse, ErrorResponse
from .filters import ProductFilter, ReviewFIlter
from rest_framework.decorators import action
from rest_framework.views import APIView

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = ProductReviewModel.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReviewFIlter  

    def list(self, request, *args, **kwargs):
        reviews = self.get_queryset()

        reviews = reviews.filter(user=request.user)

        filtered_data = self.filter_queryset(queryset=reviews)

        serializer = self.get_serializer(filtered_data, many=True)

        return SuccessResponse(
            data=serializer.data,
            status=200,
            message="Muvaffaqqiyatli"
        )


    @action(detail=True, methods=['get'])
    def reviews_for_product(self, request, pk=None):
        product_reviews = ProductReviewModel.objects.filter(product_id=pk)
        serializer = self.get_serializer(product_reviews, many=True)
        return SuccessResponse(data=serializer.data, message="Muvaffaqqiyatli", status=200)

    def create(self, request, *args, **kwargs):
        product_id = request.data.get('product')
        if not ProductModel.objects.filter(id=product_id).exists():
            return ErrorResponse(
                error="Bad request",
                message="Izoh yozishda nimadir xatolik bor",
                status=400,
                path=request.path,
                method=request.method
            )

        return super().create(request, *args, **kwargs)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = ProductModel.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter  # Make sure you're using the right filterset class
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProductCreateSerializer
        return ProductSerializer

    def list(self, request, *args, **kwargs):
        """Mahsulotlar ro'yxatini chiqarish"""
        queryset = self.get_queryset()
        filtered_data = self.filter_queryset(queryset=queryset)
        serializer = self.get_serializer(filtered_data, many=True)
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
    

class GetAnnounce(APIView):
    def get(self, request):
        announce = AnnounceModel.objects.all().order_by('-created_at')[:3]

        serializer = AnnounceSerializer(announce, many=True)

        return SuccessResponse(
            data=serializer.data,
            message="Muvaffaqqiyatli",
            status=200
        )