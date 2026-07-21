from django.db.models import Sum
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User
from .serializers import RegisterSerializer, UserSerializer


class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role == User.FARMER:
            active_listings = user.produce.filter(is_active=True).count()
            # Placeholder values until order item tracking is implemented
            total_orders = 0
            total_revenue = 0
            pending_orders = 0
            return Response({
                'active_listings': active_listings,
                'total_orders': total_orders,
                'total_revenue': total_revenue,
                'pending_orders': pending_orders,
            })

        if user.role == User.BUYER:
            from apps.marketplace.models import Order

            orders = Order.objects.filter(buyer=user)
            total_spent = orders.aggregate(sum=Sum('total_amount'))['sum'] or 0
            pending_orders = orders.filter(status='PENDING').count()
            completed_orders = orders.filter(status='DELIVERED').count()
            return Response({
                'total_orders': orders.count(),
                'total_spent': total_spent,
                'pending_orders': pending_orders,
                'completed_orders': completed_orders,
            })

        # Operator or other roles
        return Response({
            'active_listings': 0,
            'total_orders': 0,
            'total_revenue': 0,
            'pending_orders': 0,
            'completed_orders': 0,
        })


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = User.EMAIL_FIELD

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        token['role'] = user.role
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({
            'user': {
                'id': self.user.id,
                'username': self.user.username,
                'email': self.user.email,
                'role': self.user.role,
            }
        })
        return data


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer
