import logging
import json
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView


class LoginApiView(APIView):
    def post(self, request, *args, **kwargs):
        data = json.loads(list(request.data.keys())[0])
        user = authenticate(request, username=data.get('username'), password=data.get('password'))

        if user is not None:
            login(request, user)
            return Response({'status': 'success'}, status=200)
        else:
            return Response({'status': 'failure'}, status=500)
