from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import status, request
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from crud.serializers import RegisterSerializer


class RegisterView(APIView):

    def get(self, request, format=None):
        register_user_list = User.objects.all()
        serializer = RegisterSerializer(register_user_list, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            checkuser = User.objects.filter(email=serializer.validated_data['email'])
            if checkuser:
                return Response({"error": "This Email Is already Register"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"error": "User name Exists"}, status=status.HTTP_400_BAD_REQUEST)


class Home(APIView):
    permission_classes = [IsAuthenticated]
    print("hii")

    def get_object(self):
        try:
            print("hiii")
            user = request.user
            return user
        except User.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        return Response({"msg": f"Welcome {request.user}"})
