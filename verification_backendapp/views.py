from django.shortcuts import render
# user_management/views.py
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from .models import User,LogEntry,IcgSaleTransactions,Warehouse
from .serializers import UserSerializer,WarehouseSerializer,ReconcileSaleTransactionsSerializer,UserListWarehouseSerializer
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny
from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from django.utils.encoding import force_bytes
# user_management/views.py
from django.conf import settings
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from rest_framework import status
import hashlib
from rest_framework.response import Response
from .msal_utils import validate_token
from .tasks import my_task
from .models import User_Warehouse
from django.http import JsonResponse
from django.shortcuts import redirect
from django.conf import settings
from requests_oauthlib import OAuth2Session
import requests
from django.db import transaction

# Create your views here.


#result = my_task.delay(4, 4)  # Schedule the task to run asynchronously


def login(request):
    print(request)
    ms_graph = OAuth2Session(settings.MSAL_CLIENT_ID, redirect_uri=settings.MSAL_REDIRECT_URI)
    authorization_url, _ = ms_graph.authorization_url(settings.MSAL_AUTHORITY, prompt='login')
    print(authorization_url)
    return JsonResponse({'message': authorization_url})
    #authorization_url, _ = ms_graph.authorization_url(settings.MS_AUTHORIZATION_BASE_URL, prompt='login')
    #return redirect(authorization_url)
 
def callback(request):
    
    if 'code' in request.GET:  # Ensure 'code' parameter is present in the request
        ms_graph = OAuth2Session(settings.MSAL_CLIENT_ID, redirect_uri=settings.MSAL_REDIRECT_URI)
        token = ms_graph.fetch_token(
            settings.MS_TOKEN_URL,
            code=request.GET['code'],  # Get the 'code' parameter from the request
            client_secret=settings.MSAL_CLIENT_SECRET
        )
        print(token)
        access_token=token['access_token']
        #access_token='eyJ0eXAiOiJKV1QiLCJub25jZSI6IkxhYTdQQU5BZnFyMllSVjA1VUhsa04tNnhMV04tUVFNdWZ5bzNSSXJfZ2ciLCJhbGciOiJSUzI1NiIsIng1dCI6IlhSdmtvOFA3QTNVYVdTblU3Yk05blQwTWpoQSIsImtpZCI6IlhSdmtvOFA3QTNVYVdTblU3Yk05blQwTWpoQSJ9.eyJhdWQiOiJodHRwczovL2dyYXBoLm1pY3Jvc29mdC5jb20iLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC84OTAwYzVlMi0yNzBmLTRjYTAtOWEyYy04NTg4OTcyMGQxOTgvIiwiaWF0IjoxNzExNTg0NDEyLCJuYmYiOjE3MTE1ODQ0MTIsImV4cCI6MTcxMTU4OTE1MywiYWNjdCI6MCwiYWNyIjoiMSIsImFpbyI6IkFWUUFxLzhXQUFBQVBsZWxtdHM5RUxjejFkUUJScnFuS1BoQlJ5Q2tSU0p2ckhBWnFnOHJySFZOOEpROVBFMjBPVUZsTlhBVnliRmtzcVlHcFI5ZE5ZWElmRGxIaEs2MkV6dkxoWVpHZTNRREhVWUNTOXlaMU1zPSIsImFtciI6WyJwd2QiLCJyc2EiLCJtZmEiXSwiYXBwX2Rpc3BsYXluYW1lIjoiRm9vZENvbmNlcHQiLCJhcHBpZCI6IjRmNmM1NmEyLTE4NjQtNDU0NC1iMDJkLTAyOWU1NDM4OTY1NyIsImFwcGlkYWNyIjoiMSIsImRldmljZWlkIjoiYzFiMjAxMWYtYTA3OC00OTU4LWE3NWQtMzZlNmZlOTJiOWJlIiwiZmFtaWx5X25hbWUiOiJPemlnYm8iLCJnaXZlbl9uYW1lIjoiQ2hpZG96aWUiLCJpZHR5cCI6InVzZXIiLCJpcGFkZHIiOiIyNjAzOjcwODE6NjNiOmM3ODphYzA5OjdkMGY6MzBlYTpiZmE4IiwibmFtZSI6IkNoaWRvemllIE96aWdibyIsIm9pZCI6IjQyOWYxMGY5LWE2YWEtNGVhMy1hMDRhLWY4MzRmM2Y3ZWNlNCIsInBsYXRmIjoiMyIsInB1aWQiOiIxMDAzMjAwMDQ3OTcyMkMwIiwicmgiOiIwLkFUd0E0c1VBaVE4bm9FeWFMSVdJbHlEUm1BTUFBQUFBQUFBQXdBQUFBQUFBQUFBOEFCcy4iLCJzY3AiOiJVc2VyLlJlYWQgcHJvZmlsZSBvcGVuaWQgZW1haWwiLCJzaWduaW5fc3RhdGUiOlsia21zaSJdLCJzdWIiOiIxelJHR05XS0dLd3lnTEdWYS05dDJ2aFE4U3JtU29aZ2NpOGI1SEFjQ05zIiwidGVuYW50X3JlZ2lvbl9zY29wZSI6IkFGIiwidGlkIjoiODkwMGM1ZTItMjcwZi00Y2EwLTlhMmMtODU4ODk3MjBkMTk4IiwidW5pcXVlX25hbWUiOiJjb3ppZ2JvQHdhamVzbWFydC5jb20iLCJ1cG4iOiJjb3ppZ2JvQHdhamVzbWFydC5jb20iLCJ1dGkiOiJZdnpySVNIQ3YwcVFjWkQxLTZ2bkFBIiwidmVyIjoiMS4wIiwid2lkcyI6WyJiNzlmYmY0ZC0zZWY5LTQ2ODktODE0My03NmIxOTRlODU1MDkiXSwieG1zX3N0Ijp7InN1YiI6IlVjbVhRSGF4ZjBDUjFKNmFRNll4QTV4aWxzUG9zMFRzOHZqMWRWY1hVdEUifSwieG1zX3RjZHQiOjE1NTczMjE1MTl9.rGIT7zK7qXEv-jCsqXUuPCvAU4lsxGOkn4aG098u4yrKr19Dkpl9jFhWQ6hG0ALd1sJmRXOK9dWZWbmwDmLj1P1DAtdBvI9jtjXgxoONqO8qkTAqflZEUP54xmcm5zkxofSKmZFNeGsXACG2lrYONcSa-sOQpEMbBHlQbkZwg2kmmiUfGCyEAgNDApvWXPEqpX7thWauF9GVPKS_7lyn-TrjCSI-tHWgjnWVX8owuN05naVVoe5tha0Vd6RMAoFIcGjuTmhfak1S5YKJj6OGme5x2XJhJcuBl7CKHzeqPl0rqecXu0vR8Sa8l0jkY_4WQVKU-s0181xwcm-0EOd7qA'
        #token['access_token']
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        response = requests.get('https://graph.microsoft.com/v1.0/me', headers=headers)
        #print(response.json())
        if response.status_code == 200:
            profile_data = response.json()
            return JsonResponse({'message': profile_data})



#@permission_classes([IsAuthenticated])
class UserViewSet(viewsets.ModelViewSet):
    #authentication_classes = [JWTAuthentication]
    #permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    print(queryset)
    serializer_class = UserSerializer
    # Add a custom list method for debugging
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'warehousecodes':openapi.Schema(type=openapi.TYPE_ARRAY,items=openapi.Schema(type=openapi.TYPE_STRING)),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                'role': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'is_active':openapi.Schema(type=openapi.TYPE_BOOLEAN),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                'username': openapi.Schema(type=openapi.TYPE_STRING)
                # Include other properties from your serializer if needed
            },
        ),
    )

    def create(self, request, *args, **kwargs):
        # Get the password from the request data
        password ='Admin$1234'
        # Hash the password using Django's make_password
        hashed_password = make_password(password)
        # Replace the plain password with the hashed one
        request.data['password'] = hashed_password
        warehousecodes = request.data.get('warehousecodes')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_instance = serializer.save(password=hashed_password)
        # Iterate through warehouse IDs and create User_Warehouse instances
        for warehousecode in warehousecodes:
            # Assuming warehouse_instance comes from somewhere like a database query
            warehouse_instance = Warehouse.objects.get(warehousecode=warehousecode)
            # Create a new User_Warehouse instance
            User_Warehouse.objects.create(
                user=user_instance,
                warehouse=warehouse_instance,
                # created_at and updated_at will be automatically set
            )

        return Response(status=status.HTTP_201_CREATED)
    
    def list(self, request, *args, **kwargs):
        #queryset = self.filter_queryset(self.get_queryset())
        #print(f"Number of users: {queryset.count()}")
        #serializer = self.get_serializer(queryset, many=True)

        #queryset = self.filter_queryset(self.get_queryset())
        queryset = User.objects.all()
        serializer = UserListWarehouseSerializer(queryset, many=True)
        print(serializer)
        serialized_data = serializer.data  # Serialize the queryset
        print(serialized_data)  # Print serialized data
        return Response(serialized_data, status=status.HTTP_200_OK) 
         
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'warehousecodes': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_STRING)
                ),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                'role': openapi.Schema(type=openapi.TYPE_STRING),
                'is_active': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING)
                # Include other properties from your serializer if needed
            },
        ),
    )
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        warehousecodes = request.data.get('warehousecodes')
        serializer.is_valid(raise_exception=True)
        user_instance = serializer.save()
        User_Warehouse.objects.filter(user=user_instance.id).delete()
        with transaction.atomic():
            for warehousecode in warehousecodes:
                # Assuming warehouse_instance comes from somewhere like a database query
                warehouse_instance = Warehouse.objects.get(warehousecode=warehousecode)
                # Create a new User_Warehouse instance
                User_Warehouse.objects.create(
                    user=user_instance,
                    warehouse=warehouse_instance
                )
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
      
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserLoginView(TokenObtainPairView):
    authentication_classes = []  # Set authentication classes to an empty list
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'code': openapi.Schema(type=openapi.TYPE_STRING),
            }
            
        ),
    )
    def post(self, request):
        #authentication_classes = [SessionAuthentication, TokenAuthentication]
        try:
            code = request.data.get('code')
            ms_graph = OAuth2Session(settings.MSAL_CLIENT_ID, redirect_uri=settings.MSAL_REDIRECT_URI)
            print(settings.MS_TOKEN_URL)
            print(settings.MSAL_CLIENT_SECRET)
            print(code)
            token = ms_graph.fetch_token(
                settings.MS_TOKEN_URL,
                code=code, # Get the 'code' parameter from the request
                client_secret=settings.MSAL_CLIENT_SECRET
            )
            print(token)
            access_token=token['access_token']
            print(access_token)
            #access_token='eyJ0eXAiOiJKV1QiLCJub25jZSI6InVSVEk5ejZ5M0o3V3pmZTMzSVlsbzFEWDd4V3IzcEdrQ1U3SmJKalNQalUiLCJhbGciOiJSUzI1NiIsIng1dCI6IlhSdmtvOFA3QTNVYVdTblU3Yk05blQwTWpoQSIsImtpZCI6IlhSdmtvOFA3QTNVYVdTblU3Yk05blQwTWpoQSJ9.eyJhdWQiOiJodHRwczovL2dyYXBoLm1pY3Jvc29mdC5jb20iLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC84OTAwYzVlMi0yNzBmLTRjYTAtOWEyYy04NTg4OTcyMGQxOTgvIiwiaWF0IjoxNzExNjI0MDIxLCJuYmYiOjE3MTE2MjQwMjEsImV4cCI6MTcxMTYyODEwOCwiYWNjdCI6MCwiYWNyIjoiMSIsImFpbyI6IkFWUUFxLzhXQUFBQU5KakQ4eHhrbkc5Z3hhYWxHdndETnJNSVFKUnhIM0VRS1VSYis1VWVKZ1R2aUpnbGxVRENwWER0eDlMbFNQVGo3b3lrWlB6YXpUeG4wMm4rRUkrQnMveGxXWUdaS1huS0JzUFpXelVTVEhVPSIsImFtciI6WyJwd2QiLCJyc2EiLCJtZmEiXSwiYXBwX2Rpc3BsYXluYW1lIjoiRm9vZENvbmNlcHQiLCJhcHBpZCI6IjRmNmM1NmEyLTE4NjQtNDU0NC1iMDJkLTAyOWU1NDM4OTY1NyIsImFwcGlkYWNyIjoiMSIsImRldmljZWlkIjoiYzFiMjAxMWYtYTA3OC00OTU4LWE3NWQtMzZlNmZlOTJiOWJlIiwiZmFtaWx5X25hbWUiOiJPemlnYm8iLCJnaXZlbl9uYW1lIjoiQ2hpZG96aWUiLCJpZHR5cCI6InVzZXIiLCJpcGFkZHIiOiIyNjAzOjcwODE6NjNiOmM3ODphYzA5OjdkMGY6MzBlYTpiZmE4IiwibmFtZSI6IkNoaWRvemllIE96aWdibyIsIm9pZCI6IjQyOWYxMGY5LWE2YWEtNGVhMy1hMDRhLWY4MzRmM2Y3ZWNlNCIsInBsYXRmIjoiMyIsInB1aWQiOiIxMDAzMjAwMDQ3OTcyMkMwIiwicmgiOiIwLkFUd0E0c1VBaVE4bm9FeWFMSVdJbHlEUm1BTUFBQUFBQUFBQXdBQUFBQUFBQUFBOEFCcy4iLCJzY3AiOiJVc2VyLlJlYWQgcHJvZmlsZSBvcGVuaWQgZW1haWwiLCJzaWduaW5fc3RhdGUiOlsia21zaSJdLCJzdWIiOiIxelJHR05XS0dLd3lnTEdWYS05dDJ2aFE4U3JtU29aZ2NpOGI1SEFjQ05zIiwidGVuYW50X3JlZ2lvbl9zY29wZSI6IkFGIiwidGlkIjoiODkwMGM1ZTItMjcwZi00Y2EwLTlhMmMtODU4ODk3MjBkMTk4IiwidW5pcXVlX25hbWUiOiJjb3ppZ2JvQHdhamVzbWFydC5jb20iLCJ1cG4iOiJjb3ppZ2JvQHdhamVzbWFydC5jb20iLCJ1dGkiOiJqY2p6TEhhMzVrVzdRQkRTX2JYM0FBIiwidmVyIjoiMS4wIiwid2lkcyI6WyJiNzlmYmY0ZC0zZWY5LTQ2ODktODE0My03NmIxOTRlODU1MDkiXSwieG1zX3N0Ijp7InN1YiI6IlVjbVhRSGF4ZjBDUjFKNmFRNll4QTV4aWxzUG9zMFRzOHZqMWRWY1hVdEUifSwieG1zX3RjZHQiOjE1NTczMjE1MTl9.V-_JQQxSIHtGJEwR5Oswsa7nbaDpN56_P0w-I7Gx5jgnPjZbIgBLHcp3ciDXabYybUzia8ZFATakrci4KcTxsV3wNU4pVWkrWFi5DJyJlehvXt8egoJeu9qh4ehJJO1AqfWh0Y7nfNaPsRNUKwYIDSqV8RN6ap6KkBzYr6BYY2_EAGec-pJlsNnZWeSRsTtpz-hSXveBEQo1Yv-vx6MX3lr3rAxerBoHSqs6F_J3WBaVredQ9ClxYIJnQip3rHCYoVi2aOI9OIAOoP57fhbReWPcYwj0EEQv2dDw2L5KRwKa9spBeffHL0BGdnOS-kSQXy93GVv0yp8vY8-ex9YwWA'
            headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
            }
            response = requests.get('https://graph.microsoft.com/v1.0/me', headers=headers)
            print(response.json())
            if response.status_code == 200:
                profile_data = response.json()
                user=User.objects.filter(email=profile_data['mail']).values_list('username','email','first_name','last_name','is_staff','date_joined','is_active','is_superuser','password','id').first()
                #user = authenticate(request,username=user[1], password=user[8])
                if user is not None:
                    #login(request, user)
                    # Retrieve the user's role (assuming a ForeignKey relationship)
                    request.data['username'] =user[0]
                    request.data['password']='Admin$1234'
                    print(request.data['password'])
                    print(request.data['username'])
                    token = super().post(request)
                    #token = super().post(request)
                    #queryset = user
                    queryset = User.objects.filter(id=user[9]).first()
                    serializer = UserListWarehouseSerializer(queryset, many=False)
                    serialized_data = serializer.data  # Serialize the queryset
                    #print(token)
                    '''
                    user_data = {
                        'id': user[9],
                        'username': user[0],
                        'email': user[1],
                        'first_name': user[2],
                        'last_name': user[3],
                        'is_staff': user[4],
                        'date_joined': user[5],
                        'is_active': user[6],
                        'is_superuser': user[7],
                        # Include other user data fields as needed
                    }
                    '''

                    response_data = {
                        'message': 'Login successful',
                        'user': serialized_data,
                        'token':token.data
                        # Include the role data in the response
                    }

                    return Response(response_data, status=status.HTTP_200_OK)
                else:    
                    return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'message': 'Invalid username and password'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            error_message = str(e)  # Get the error message as a string
            return Response({'error': error_message}, status=status.HTTP_401_UNAUTHORIZED)



class StoreListingsByWarehouseType(APIView):
    permission_classes = [AllowAny]
    #authentication_classes = [JWTAuthentication]
    #permission_classes = [IsAuthenticated]
    # Set permission classes to AllowAny
    @swagger_auto_schema(
        manual_parameters=[
    
            openapi.Parameter(
                'warehouse_type',
                openapi.IN_QUERY,
                description='The code for warehouse type',
                type=openapi.TYPE_STRING,
            ),
        ]
    )
    def get(self, request,format=None):
        try:
            # Get the warehouse type from query parameters
            warehouse_type = request.GET.get('warehouse_type')
            # Retrieve warehouses by warehouse type
            if warehouse_type:
                warehouses = Warehouse.objects.filter(warehousetype=warehouse_type)
            else:
                warehouses = Warehouse.objects.all()
            # Serialize the data
            serializer = WarehouseSerializer(warehouses, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Warehouse.DoesNotExist:
            return Response({'message': 'No warehouses found for the specified type'}, status=status.HTTP_404_NOT_FOUND)


class ReconcileDataViewSet(APIView):
    # Specify the serializer class to use
    serializer_class = ReconcileSaleTransactionsSerializer
    # Define the create method to handle POST requests
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                #'reconciletransactionscode': openapi.Schema(type=openapi.TYPE_STRING),
                'is_reconcile':openapi.Schema(type=openapi.TYPE_BOOLEAN),
                'paymenttype': openapi.Schema(type=openapi.TYPE_STRING),
                'settlement_amount': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT),
                'bank_amount': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT),
                'transactiondate': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
                # Include other properties from your serializer if needed
            },
        ),
    )
    def post(self, request, *args, **kwargs):
        # Validate the request data using the serializer
        concatenated_str = f"{request.GET.get('transactiondate')}-{request.GET.get('paymenttype')}"
        unique_value = hashlib.sha256(concatenated_str.encode()).hexdigest()
        print(unique_value)
        #serializer = self.get_serializer(data=request.data)
        # Add unique identifier to request data
        #request.GET.get('icgtransactionscode') = unique_value
        request.data['reconciletransactionscode'] = unique_value

        # Create serializer instance with request data
        serializer = self.serializer_class(data=request.data)
        
        # Validate serializer data
        serializer.is_valid(raise_exception=True)
        
        # Save the reconciled data
        serializer.save()
        
        # Prepare the response data
        response_data = serializer.data
        
        # Return a success response with the created data
        return Response(response_data, status=status.HTTP_201_CREATED)
