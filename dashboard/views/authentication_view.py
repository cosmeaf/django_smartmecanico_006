from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.exceptions import NotFound
from dashboard.models.user_model import RecoverPassword
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from dashboard.serializers.authentication_serializers import (AuthUserRegisterSerializer, AuthUserSignInSerializer, 
AuthUserRecoverySerializer, AuthUserOtpSerializer, AuthUserResetPasswordSerializer )


class AuthUserRegisterView(generics.CreateAPIView):
    serializer_class = AuthUserRegisterSerializer
    permission_classes = [AllowAny]

class AuthUserSignInView(TokenObtainPairView):
    serializer_class = AuthUserSignInSerializer
    permission_classes = [AllowAny] 

    CACHE_KEY_PREFIX = "login"
    @method_decorator(cache_page(300, key_prefix=CACHE_KEY_PREFIX))
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        response_data = {
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'token': access_token,
            'refresh': refresh_token,
        }

        return Response(response_data, status=status.HTTP_200_OK)

class AuthUserRecoveryView(generics.CreateAPIView):
    serializer_class = AuthUserRecoverySerializer
    permission_classes = [AllowAny]

class AuthUserOtpView(generics.CreateAPIView):
    serializer_class = AuthUserOtpSerializer
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token_value = serializer.validated_data["token"]
        return Response({
            "message": "One-Time Password gerado com sucesso. Por favor, valide o OTP dentro de 1 hora.",
            "token": token_value
        })


class AuthUserResetPasswordView(generics.UpdateAPIView):
    serializer_class = AuthUserResetPasswordSerializer
    permission_classes = [AllowAny]

    def get_object(self, uuid, token):
        try:
            return get_object_or_404(RecoverPassword, id=uuid, token=token, is_used=False)
        except Http404:
            raise NotFound(detail="O link de redefinição de senha é inválido ou expirou.", code=404)

    def put(self, request, uuid, token):
        recover_data = self.get_object(uuid, token)

        serializer = self.get_serializer(recover_data, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()        
        return Response({"message": "Senha redefinida com sucesso."})