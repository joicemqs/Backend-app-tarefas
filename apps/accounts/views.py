from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, UserSerializer, CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PasswordResetRequestSerializer, PasswordResetConfirmSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema, OpenApiExample

User = get_user_model()

@extend_schema(
    summary="Registro de usuário",
    description="Faz o registro de um novo usuário.",
    examples=[
        OpenApiExample(
            name="Exemplo de criação de usuário",
            value={"nome": "Joice", "email": "joice@example.com", "senha": "12345678"},
            request_only=True,
        )
    ],
    responses={200: RegisterSerializer(many=True)}
)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

@extend_schema(
    summary="Lista de usuários",
    description="Retorna todos os usuários cadastrados. Requer autenticação JWT.",
    responses={200: UserSerializer(many=True)}
)

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

@extend_schema(
    summary="Obter token JWT",
    description="Obtém um token JWT para autenticação.",
    examples=[
        OpenApiExample(
            name="Exemplo de obtenção de token",
            value={"email": "joice@example.com", "senha": "12345678"},
            request_only=True,
        )
    ],
    responses={200: UserSerializer(many=True)}
)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

@extend_schema(
    summary="Solicitação de redefinição de senha",
    description="Envia um email com instruções para redefinir a senha.",
    examples=[
        OpenApiExample(
            name="Exemplo de criação de usuário",
            value={"email": "joice@example.com"},
            request_only=True,
        )
    ],
    responses={200: UserSerializer(many=True)}
)
class PasswordResetRequestView(GenericAPIView):
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Email enviado com instruções."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    summary="Confirmação de redefinição de senha",
    description="Redefine a senha do usuário usando o token enviado por email.",
    examples=[
        OpenApiExample(
            name="Exemplo de criação de usuário",
            value={"uid": "Ts", "token": "jlKkfyrwG...kjghHJDFA", "new_password": "87654321"},
            request_only=True,
        )
    ],
    responses={200: UserSerializer(many=True)}
)

class PasswordResetConfirmView(GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Senha redefinida com sucesso."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
