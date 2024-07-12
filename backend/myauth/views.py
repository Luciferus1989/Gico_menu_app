import json
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from serializers import UserSerializer, AvatarSerializer, ChangePasswordSerializer
from models import CustomUser
from django.contrib.auth.models import Group


class LoginApiView(APIView):
    def post(self, request, *args, **kwargs):
        data = json.loads(list(request.data.keys())[0])
        user = authenticate(request, username=data.get('username'), password=data.get('password'))
        if user is not None:
            login(request, user)
            return Response({'status': 'success'}, status=200)
        else:
            return Response({'status': 'failure'}, status=500)


class LogoutApiView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            logout(request)
            return Response({'status': 'success', 'message': 'User logged out successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 'failure', 'error': 'Internal Server Error', 'details': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RegisterApiView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(list(request.data.keys())[0])
            first_name = data.get('name')
            username = data.get('username')
            password = data.get('password')
            user = CustomUser.objects.create_user(username=username, password=password, first_name=first_name)
            group, created = Group.objects.get_or_create(name='Users')
            user.groups.add(group)
            return Response({'status': 'success', 'message': 'User registered successfully'},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'status': 'failure', 'error': 'Internal Server Error', 'details': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProfileAPIView(APIView):
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.request.user)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data

        if 'avatar' in data and len(data) == 1:
            user = request.user
            data = request.data
            serializer = AvatarSerializer(user, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif 'currentPassword' in data:
            serializer = ChangePasswordSerializer(data=data)
            if serializer.is_valid():
                if not user.check_password(serializer.validated_data.get("currentPassword")):
                    return Response({"currentPassword": ["Current password is not correct"]},

                                    status=status.HTTP_400_BAD_REQUEST)
                user.set_password(serializer.validated_data.get("newPassword"))
                user.save()
                return Response({"detail": "Password has been successfully changed"}, status=status.HTTP_200_OK)

            else:
                print(serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif 'fullName' in data:
            full_name_parts = data['fullName'].split()
            first_name = full_name_parts[0] if full_name_parts else ''
            last_name = ' '.join(full_name_parts[1:]) if len(full_name_parts) > 1 else ''
            user.first_name = first_name
            user.last_name = last_name
            serializer = UserSerializer(user, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"detail": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)