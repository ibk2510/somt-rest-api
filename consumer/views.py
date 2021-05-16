from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import viewsets
from .serializers import ConsumerSerializer, SubscriptionSerializer, UserLoginSerializer
from .models import Consumer, Subscription
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class UserRegistrationView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ConsumerSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # print(serializer.validated_data)
        # payload = JWT_PAYLOAD_HANDLER(serializer.validated_data.user)
        # jwt_token = JWT_ENCODE_HANDLER(payload)
        status_code = status.HTTP_201_CREATED
        response = {
            'success': 'True',
            'status code': status_code,
            'message': 'User registered  successfully',
            # 'token' : jwt_token
        }

        return Response(response, status=status_code)


class SubscriptionViewset(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer


# @api_view(['GET'])
# def getConsumers(request):
#     queryset = Consumer.objects.all()
#     serializer = ConsumerSerializer(queryset , many= True)
#     return Response(serializer.data)


class UserLoginView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer
    queryset = User.objects.filter(consumer__isnull=False)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        print(request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'success': 'True',
            'status code': status.HTTP_200_OK,
            'message': 'User logged in  successfully',
            'token': serializer.data['token'],
        }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)


class UserProfileView(RetrieveAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        try:
            user_profile = Consumer.objects.get(user=request.user)
            status_code = status.HTTP_200_OK
            response = {
                'success': 'true',
                'status code': status_code,
                'message': 'User profile fetched successfully',
                'data': [{
                    'first_name': user_profile.user.first_name,
                    'last_name': user_profile.user.last_name,
                    'phone_number': user_profile.phone,
                    'username': user_profile.user.username,
                    # 'gender': user_profile.gender,
                    }]
                }

        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'User does not exists',
                'error': str(e)
                }
        return Response(response, status=status_code)


# @csrf_exempt
# def user_login(request):
#     if request.method == "POST":
#         body = json.loads(request.body)
#         email = body['email']
#         pwd = body['password']
#         user = authenticate(username=email, password=pwd)
#         if user is None:
#             return JsonResponse({"success": False, "message": "Invalid Credentials"}, status=400)
#         payload = api_settings.JWT_PAYLOAD_HANDLER(user)
#         jwt_token = api_settings.JWT_ENCODE_HANDLER(payload)
#         return JsonResponse({"success": True, "token": jwt_token, "email": email}, status=200)


# def consumer_details(request):
#     if request.method == 'GET':
#         # data = Consumer.objects.first()
#         json_data = serializers.serialize("json", Consumer.objects.all())
#         t_data = {"data": json_data}
#         print(data.first().phone)
#         return JsonResponse(t_data)
