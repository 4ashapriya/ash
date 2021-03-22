from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.generics import GenericAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User

from .forms import StudentBulkUploadForm
from .serializers import RegisterSerializer, UpdateSerializer, New, PermissionSerializer, BulkSerializer
from rest_framework import viewsets, views, permissions, authentication, generics
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.http import Http404
from rest_framework import status
from rest_framework.authtoken.views import obtain_auth_token
from .models import User, BulkUser
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
from django.views import View
from datetime import datetime
import io, csv
import logging

logger = logging.getLogger(__name__)


# creating class for user registration
class RegisterAPIView(APIView):
    permission_class = (AllowAny,)

    @swagger_auto_schema(
        operation_description="apiview post description override",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
                'password2': openapi.Schema(type=openapi.TYPE_STRING)
            },
        ),
        security=[],
        # tags=['Login'],
    )
    def post(self, request, format=None):

        serializer = RegisterSerializer(data=request.data)

        data = {}  # create a null dictionary to return the data

        if serializer.is_valid():  # check the condition serializer is valid or not
            serializerData = serializer.save()
            data['id'] = serializerData.id
            data['response'] = 'registered'
            data['username'] = serializerData.username
            data['email'] = serializerData.email
            # token,create=Token.objects.get_or_create(user=account) # get or create a token
            # data['token']=token.key
        else:
            data = serializer.errors  # return error if serializer is not valid
        return Response(data)


# create a permission class
class PermissionAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'user': str(request.user), 'userid': str(request.user.id)}  # what all content must return
        return Response(content)


class UpdateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, format=None, *args, **kwargs):
        pk = self.kwargs.get('pk')

        serializer = UpdateSerializer(pk, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteAPIView(GenericAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]
    serializer_class = BulkSerializer
    queryset = User.objects.all()

    # authentication_class = [TokenAuthentication]
    # permission_class = (IsAuthenticated)
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, *args, **kwargs):
        user1 = self.get_object(pk)
        serializer = BulkSerializer(user1, many=True)
        return Response(serializer.data)

    def post(self, request):
        userobj = BulkSerializer(data=request.data)
        if userobj.is_valid():
            userobj.save()
            return Response(userobj.data, status=status.HTTP_201_CREATED)
        else:
            return Response( status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        usobj = self.get_object(pk)
        usobj.delete()
        return Response(status=status.HTTP_200_OK)

    def put(self, request, pk):
        emp= self.get_object(pk)
        serializer_class= BulkSerializer(emp,data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)


class BulkInsertView(View):

    def get(self, request):
        template_name = 'user.html'
        return render(request, template_name)

    def post(self, request):
        user = request.user  # get the current login user details
        paramFile = io.TextIOWrapper(request.FILES['employeefile'].file)
        portfolio1 = csv.DictReader(paramFile)
        list_of_dict = list(portfolio1)
        objs = [
            BulkUser(
                name=row['name'],
                email=row['email'],
                phone=row['number'],

            )
            for row in list_of_dict
        ]
        try:
            msg = BulkUser.objects.bulk_create(objs)
            returnmsg = {"status_code": 200}
            print('imported successfully')
        except Exception as e:
            print('Error While Importing Data: ', e)
            returnmsg = {"status_code": 500}

        return JsonResponse(returnmsg)

    def put(self, request):
        extra_content = {}
        if request.method == 'PUT':
            form = StudentBulkUploadForm(request.POST, request.FILES)

        user = request.user  # get the current login user details
        paramFile = io.TextIOWrapper(request.FILES['employeefile'].file)
        portfolio1 = csv.DictReader(paramFile)
        list_of_dict = list(portfolio1)
        objs = [
            BulkUser(
                name=row['name'],
                email=row['email'],
                phone=row['number'],

            )
            for row in list_of_dict
        ]
        try:
            msg = BulkUser.objects.bulk_update(objs)
            returnmsg = {"status_code": 200}
            print('imported successfully')
        except Exception as e:
            print('Error While Importing Data: ', e)
            returnmsg = {"status_code": 500}

        return JsonResponse(returnmsg)


#
# class Registerupdate(GenericAPIView):
#     serializer_class = New
#
#     def post(self, request, *args, **kwargs):
#
#         userobj = self.get_serializer(data=request.data)
#         if userobj.is_valid():
#             userobj.save()
#             return Response(userobj.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(userobj.error, status=status.HTTP_400_BAD_REQUEST)
#
#     def register(request):
#         if request.method =='GET':
#             reg = User.objects.all()
#             serializer = RegisterUpdateSerializer(reg,many=True)
#             return Response(serializer.data)
#         elif request.method =='POST':
#             serializer = RegisterUpdateSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data,status=status.HTTP_201_CREATED)
#             return Response(serializer.error,status=status.HTTP_400_BAD_REQUEST)
#
#
# # put update delete function
# class UpdateViewSet(viewsets.ModelViewSet):
#     serializer_class = UserUpdateSerializer
#     permission_classes_by_action = {
#         'list' :(permissions.AllowAny),
#         'update': (permissions.IsAuthenticated),
#         'destroy':(permissions.IsAuthenticated),
#     }
#     def get_object(self,pk):
#         try:
#             return User.objects.get(pk=pk)
#         except:
#             raise Http404
#
#     def list(self,request,pk,format=None):
#         userData = self.get_object(pk)
#         serializer = UserLoginSerializer(userData)
#         return Response(serializer.data)
#
