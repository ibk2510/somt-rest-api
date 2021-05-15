from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import viewsets
from .serializers import ConsumerSerializer, SubscriptionSerializer, UserLoginSerializer
from .models import Consumer, Subscription
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.permissions import AllowAny


class UserRegistrationView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ConsumerSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        status_code = status.HTTP_201_CREATED
        response = {
            'success': 'True',
            'status code': status_code,
            'message': 'User registered  successfully',
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
