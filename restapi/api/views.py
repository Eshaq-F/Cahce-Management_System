from logging import getLogger

from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.openapi import Parameter, IN_HEADER, TYPE_STRING

from api.serializers import TransactionSerializer, UserSerializer
from api.utils import get_tokens_for_user, blacklist_token
from api.filters import TransactionFilter
from api.models import User

logger = getLogger(__name__)


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = ()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        if user := serializer.validated_data.get('user'):
            return Response({'message': 'Login successful.'} | get_tokens_for_user(user))

        self.perform_create(serializer)
        return Response({'message': 'User registered successfully.'})


class UserLogoutView(generics.RetrieveAPIView):
    refresh_token = Parameter('refresh_token', IN_HEADER, type=TYPE_STRING, required=True,
                              description="Your current refresh token")

    @swagger_auto_schema(manual_parameters=[refresh_token])
    def get(self, request, *args, **kwargs):
        try:
            blacklist_token(request.headers.get('refresh_token'))
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': str(e)})


class TransactionListCreateView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = TransactionFilter
    ordering_fields = '__all__'

    def perform_create(self, serializer):
        serializer.validate_cache(user=self.request.user)
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.request.user.transactions.all()


class TransactionRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        logger.info(f' user: {self.request.user.username}')
        return self.request.user.transactions.all()
