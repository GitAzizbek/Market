from rest_framework.views import APIView
from .models import UserModel
from .serializers import *
from main.responses import SuccessResponse, ErrorResponse
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import IsSuperUser, IsOwner


class UserLoginView(APIView):
    def post(self, request):
        data = request.data

        try:
            serializer = UserLoginSerializer(data=data)

            if not serializer.is_valid():
                return ErrorResponse(
                    error=str(serializer.errors),
                    message="Telefon raqam to'g'ri ekanligiga ishonch hosil qiling",
                    status=400,
                    path=request.path,
                    method=request.method
                )

            user = UserModel.objects.filter(phone=serializer.validated_data['phone']).first()
            
            if user:
                user.telegram_id = serializer.validated_data['telegram_id']
                user.save()
                is_new_user = False
            else:
                user = UserModel.objects.create(
                    phone=serializer.validated_data['phone'],
                    telegram_id=serializer.validated_data['telegram_id']
                )
                is_new_user = True

            refresh = RefreshToken.for_user(user)

            data = {
                "token": str(refresh.access_token),
                "user": UserMeSerializer(user).data,
                "is_new_user": is_new_user
            }

            return SuccessResponse(
                data=data,
                message="Muvaffaqiyatli",
                status=200
            )

        except Exception as e:
            return ErrorResponse(
                error=str(e),
                message="Nimadir muammo paydo bo'ldi",
                status=400,
                path=request.path,
                method=request.method
            )


class UserUpdateAPIView(APIView):
    permission_classes = [IsOwner]
    
    def patch(self, request):
        try:
            user = request.user  
            serializer = UserUpdateSerializer(user, data=request.data, partial=True)

            if not serializer.is_valid():
                return ErrorResponse(
                    error=serializer.errors,
                    message="Kiritilgan ma'lumotlarni tekshiring",
                    status=400,
                    path=request.path,
                    method=request.method
                )

            serializer.save()

            return SuccessResponse(
                data=serializer.data,
                message="Ma'lumotlar muvaffaqiyatli yangilandi!",
                status=200
            )

        except Exception as e:
            return ErrorResponse(
                error=str(e),
                message="Foydalanuvchi ma'lumotlarini yangilashda xatolik yuz berdi",
                status=500,
                path=request.path,
                method=request.method
            )

class ProfileView(APIView):
    def get(self,request):
        user = {
            "id": request.user.pk,
            "phone": request.user.phone,
            "telegram_id": request.user.telegram_id,
            "avatar": request.user.avatar,
            "first_name": request.user.first_name,
            "address": request.user.address,
        },

        return SuccessResponse(
            data=ProfileSerializer(user).data,
            status=200,
            message="Success"
        )
