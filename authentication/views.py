from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer, VerifyOTPSerializer, UserSerializer
from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from django.contrib.auth import get_user_model
import random
from django.core.mail import send_mail
from drf_yasg.utils import swagger_auto_schema
from django.middleware.csrf import get_token
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(["GET"])
def get_csrf_token(request):
    return Response({"csrfToken": get_token(request)})


User = get_user_model()

@swagger_auto_schema(method='post', request_body=RegisterSerializer, responses={201: 'OTP sent to email', 400: 'Bad Request'})
@api_view(["POST"])
@permission_classes([AllowAny]) 
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        otp = str(random.randint(100000, 999999))
        user.otp = otp
        user.save()
        send_mail("Your OTP Code", f"Your OTP code is {otp}", "youremail@gmail.com", [user.email])
        return Response({"message": "OTP sent to email"}, status=200)
    return Response(serializer.errors, status=400)

@swagger_auto_schema(method='post', request_body=VerifyOTPSerializer, responses={200: 'Account verified', 400: 'Invalid OTP'})
@api_view(["POST"])
@permission_classes([AllowAny])
def verify_otp(request):
    serializer = VerifyOTPSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data["email"]
        otp = serializer.validated_data["otp"]
        try:
            user = User.objects.get(email=email, otp=otp)
            user.is_verified = True
            user.otp = None
            user.save()
            return Response({"message": "Account verified"}, status=200)
        except User.DoesNotExist:
            return Response({"error": "Invalid OTP"}, status=400)
    return Response(serializer.errors, status=400)

@swagger_auto_schema(method='post', request_body=LoginSerializer, responses={200: 'Login successful', 400: 'Invalid credentials or unverified account'})
@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    if request.user.is_authenticated:
        return Response({"message": "Already logged in"}, status=200)
    
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = authenticate(email=serializer.validated_data["email"], password=serializer.validated_data["password"])
        if user and user.is_verified:
            login(request, user)
            response = Response({"message": "Login successful"}, status=200)
            response.set_cookie("auth_token", user.id, httponly=True, secure=True, samesite="Strict")
            response["X-CSRFToken"] = get_token(request)
            return response
        return Response({"error": "Invalid credentials or unverified account"}, status=400)
    return Response(serializer.errors, status=400)

@swagger_auto_schema(method='get', responses={200: UserSerializer})
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_details(request):
    auth_token = request.COOKIES.get("auth_token")
    
    if not auth_token:
        return Response({"error": "Authentication token missing"}, status=400)

    try:
        user = User.objects.get(id=auth_token)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)
    except User.DoesNotExist:
        return Response({"error": "Invalid authentication token"}, status=400)


@swagger_auto_schema(method='post', responses={200: 'Logged out'})
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_user(request):
    logout(request)
    response = Response({"message": "Logged out"}, status=200)
    response.delete_cookie("auth_token")
    response["X-CSRFToken"] = get_token(request)
    return response
