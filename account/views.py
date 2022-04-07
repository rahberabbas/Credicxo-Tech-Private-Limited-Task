from django.shortcuts import get_object_or_404
from account.models import User
from rest_framework import status, viewsets, permissions, generics
from .permissions import IsAdminUser, IsStudentUser, IsTeacherUser
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import TeacherSignupSerializer, StudentSignupSerializer, UserSerializer, UserLoginSerializer, AdminSignupSerializer, SendPasswordResetEmailSerializer, UserPasswordResetSerializer
from .renders import UserRenderer

# Token Generate
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Admin SignUp Api
class AdminSignupView(generics.GenericAPIView):
    serializer_class = AdminSignupSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token,
            "message": "Account Created Successfully"
        })

# Teacher SignUp Api
class TeacherSignupView(generics.GenericAPIView):
    serializer_class = TeacherSignupSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token,
            "message": "Account Created Successfully"
        })

# Student SignUp API
class StudentSignupView(generics.GenericAPIView):
    serializer_class = StudentSignupSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token,
            "message": "Account Created Successfully"
        })

# Login API
class UserLoginView(APIView):
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token': token, 'msg': 'Login Successful', 'is_student': user.is_student}, status=status.HTTP_200_OK)
            else:
                return Response({'errors': {'non_field_error': ['Email or Password is not valid']}}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Logout API
class Logout(APIView):
    def post(self, request, format=None):
        request.auth.delete()
        return Response(status=status.HTTP_200_OK)

# Student Information API
class StudentOnlyView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated&IsStudentUser]
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user

# Admin See User API
class AdminOnlyView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser&IsAdminUser]
    serializer_class = UserSerializer
    
    def get(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

# Teacher See Users API
class TeacherOnlyView(generics.RetrieveAPIView):
    queryset = User.objects.filter(is_student=True)
    permission_classes = [IsTeacherUser]
    serializer_class = UserSerializer
    
    def get(self, request):
        queryset = User.objects.filter(is_student=True)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

# Admin Add Teacher
class AdminAddTeacher(generics.GenericAPIView):
    serializer_class = TeacherSignupSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token,
            "message": "Teacher Account Added Successfully"
        })

# Admin Add Student
class AdminAddStudent(generics.GenericAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = StudentSignupSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token,
            "message": "Student Account Added Successfully"
        })

# Teacher Add Student
class TeacherAddStudent(generics.GenericAPIView):
    permission_classes = [IsTeacherUser]
    serializer_class = StudentSignupSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token,
            "message": "Student Account Added Successfully"
        })

# Send Reset Password Email API
class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)

# Send Password Resets API
class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)
