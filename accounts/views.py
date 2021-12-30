from django.db.models import Q
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import User, ConfirmEmailToken, Contact
from .serializers import UserRegisterSerializer, ContactsSerializer, UserSerializer


class RegisterUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def post(self, request, *args, **kwargs):
        if {'first_name', 'last_name', 'email', 'password', 'password2', 'company', 'position'}.issubset(request.data):
            serializer = UserRegisterSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return JsonResponse({'Status': 'Registered'}, status=status.HTTP_200_OK)
            else:
                data = serializer.errors
                return JsonResponse(data)
        else:
            return JsonResponse(
                {'Need all fields': 'first_name, last_name, email, password, password2, company, position'})

    def perform_create(self, serializer):
        serializer.save()


class ConfirmRegisterUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        if {'email', 'token'}.issubset(request.data):
            token = ConfirmEmailToken.objects.filter(
                Q(key=request.data['token']) & Q(user__email=request.data['email'])).select_related('user').first()
            if token:
                user = User.objects.filter(email=request.data['email']).first()
                user.is_active = True
                user.save()
                return JsonResponse({'Status': 'User confirmed'})
            else:
                return JsonResponse({'Status': 'User not confirmed'})
        else:
            return JsonResponse({'Need all fields': 'email, token'})


class UserLoginView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def post(self, request, *args, **kwargs):
        if {'email', 'password'}.issubset(request.data):
            password = request.data['password']
            user = User.objects.filter(email=request.data['email']).first()
            if user and user.check_password(password):
                token = Token.objects.create(user=user)
                return JsonResponse({'Status': f"{user.first_name} registered",
                                     'Authorization token': token.key})
            else:
                return JsonResponse({'Status': 'User not registered'})
        else:
            return JsonResponse({'Need all fields': 'email, password'})


class UserDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = Token.objects.get(key=request.auth.key).user_id
        user = User.objects.filter(id=user_id).first()
        response_data = UserSerializer(user)
        return JsonResponse({"data": response_data.data})

    def post(self, request, *args, **kwargs):
        user_id = Token.objects.get(key=request.auth.key).user_id
        user = User.objects.filter(id=user_id).first()
        serializer = UserSerializer(instance=user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            context = serializer.save()
            return JsonResponse({'Change info successfully': context.first_name}, status=status.HTTP_200_OK)


class ContactsView(ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactsSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['city']

    def get_queryset(self):
        user = self.request.user
        contacts = Contact.objects.filter(user=user)
        return contacts

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['put'])
    def contact_update(self, request, *args, **kwargs):
        if {'id'}.issubset(request.data):
            contact = Contact.objects.filter(id=request.data['id']).first()
            serializer = ContactsSerializer(instance=contact, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return JsonResponse({'Change info successfully': 'Ok'}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'Need all fields': 'id'})

    @action(detail=True, methods=['destroy'])
    def contact_delete(self, request, *args, **kwargs):
        for contact_id in request.data['items'].split(','):
            contact = Contact.objects.filter(id=int(contact_id)).first()
            self.perform_destroy(contact)
        return JsonResponse({'Deleted': f'Deleted {request.data["items"]}'}, status=status.HTTP_204_NO_CONTENT)
