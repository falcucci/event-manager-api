from datetime import datetime, timedelta

from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

from authentication.serializers import UserRegisterSerializer, UserSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = CustomTokenObtainPairSerializer

@swagger_auto_schema(method='post', request_body=UserRegisterSerializer)
@api_view(http_method_names=['POST'])
@permission_classes(permission_classes=(AllowAny, ))
def register(request):
    user_serialized = UserRegisterSerializer(data=request.data)
    user_serialized.is_valid(raise_exception=True)
    user = user_serialized.save()
    print(user.username, user.email, user.first_name)

    return Response(
        status=status.HTTP_201_CREATED,
        data=UserSerializer(user).data
    )


