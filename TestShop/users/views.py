from django.contrib.auth import get_user_model
from rest_framework import exceptions, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .utils import generate_access_token, generate_refresh_token, UserJSONRenderer

from .serializers import UserSerializer, LoginSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        User = get_user_model()
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        response = Response()
        if (username is None) or (password is None) or (email is None):
            raise exceptions.AuthenticationFailed(
                'username and password and email required')

        user = User.objects.filter(username=username).first()
        if user is None:
            raise exceptions.AuthenticationFailed('user not found')
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed('wrong password')

        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)
        response.data = {
            'access_token': access_token,
            'refresh_token': refresh_token
        }

        return response

#
# class LoginAPIView(APIView):
#     permission_classes = (AllowAny,)
#     renderer_classes = (UserJSONRenderer,)
#     serializer_class = LoginSerializer
#
#     def post(self, request):
#         # user = request.data.get()
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#         return Response(serializer.data, status=status.HTTP_200_OK)
