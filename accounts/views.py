from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer, LoginSerializer, RefreshTokenSerializer
from .jwt import generate_tokens


class RegisterView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            return Response(
                {
                    "message": "User registered successfully",
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "username": user.username,
                    }
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data["user"]

            tokens = generate_tokens(user)

            return Response(
                {
                    "message": "Login successful",
                    "tokens": tokens,
                },
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class MeView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {
                "id": request.user.id,
                "email": request.user.email,
                "username": request.user.username,
            }
        )    

class RefreshTokenView(APIView):

    def post(self, request):
        serializer = RefreshTokenSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data["user"]

            tokens = generate_tokens(user)

            return Response(
                {
                    "access": tokens["access"]
                },
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )