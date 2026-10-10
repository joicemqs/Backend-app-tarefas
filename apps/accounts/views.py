from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, OpenApiExample, inline_serializer
from rest_framework import generics, serializers, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (
    RegisterSerializer,
    UserSerializer,
    CustomTokenObtainPairSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
)

User = get_user_model()

DetailResponse = inline_serializer(
    name='DetailResponse',
    fields={'detail': serializers.CharField()},
)

@extend_schema(
    summary="Registro de usuário",
    description="Faz o registro de um novo usuário. A senha precisa passar pelos validadores do Django.",
    examples=[
        OpenApiExample(
            name="Exemplo de criação de usuário",
            value={"username": "joice", "email": "joice@example.com", "password": "MinhaSenha#2025"},
            request_only=True,
        )
    ],
    responses={201: RegisterSerializer}
)
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

@extend_schema(
    summary="Usuário autenticado",
    description="Retorna os dados do usuário dono do token JWT.",
    responses={200: UserSerializer}
)
class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

@extend_schema(
    summary="Obter token JWT",
    description="Faz login com e-mail e senha e retorna os tokens access e refresh.",
    examples=[
        OpenApiExample(
            name="Exemplo de login",
            value={"email": "joice@example.com", "password": "MinhaSenha#2025"},
            request_only=True,
        )
    ],
)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

@extend_schema(
    summary="Solicitação de redefinição de senha",
    description=(
        "Envia um e-mail com instruções para redefinir a senha. "
        "A resposta é sempre a mesma, exista ou não uma conta com o e-mail informado."
    ),
    examples=[
        OpenApiExample(
            name="Exemplo de solicitação",
            value={"email": "joice@example.com"},
            request_only=True,
        )
    ],
    responses={200: DetailResponse}
)
class PasswordResetRequestView(GenericAPIView):
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "Se existir uma conta com este e-mail, enviaremos as instruções para redefinir a senha."},
            status=status.HTTP_200_OK,
        )

@extend_schema(
    summary="Confirmação de redefinição de senha",
    description="Redefine a senha do usuário usando o uid e o token enviados por e-mail.",
    examples=[
        OpenApiExample(
            name="Exemplo de confirmação",
            value={"uid": "Mw", "token": "cy96u3-959143f2c3ec9cbab5f42f0d23080efc", "new_password": "NovaSenha#2025"},
            request_only=True,
        )
    ],
    responses={200: DetailResponse}
)
class PasswordResetConfirmView(GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Senha redefinida com sucesso."}, status=status.HTTP_200_OK)
