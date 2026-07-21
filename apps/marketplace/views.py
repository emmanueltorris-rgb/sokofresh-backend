from datetime import timedelta
from django.db.models import Sum
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.accounts.models import User
from apps.accounts.permissions import IsFarmerOrAdmin
from .models import Produce, Order
from .serializers import ProduceSerializer, OrderSerializer


class ProduceViewSet(viewsets.ModelViewSet):
    queryset = Produce.objects.all()
    serializer_class = ProduceSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsFarmerOrAdmin()]
        return [AllowAny()]


class CategoryListView(APIView):
    def get(self, request):
        categories = [
            {'id': 1, 'name': 'Fruits'},
            {'id': 2, 'name': 'Vegetables'},
            {'id': 3, 'name': 'Grains'},
            {'id': 4, 'name': 'Dairy'},
            {'id': 5, 'name': 'Pulses'},
        ]
        return Response(categories)


class MyProduceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        produce = Produce.objects.filter(farmer=request.user)
        serializer = ProduceSerializer(produce, many=True)
        return Response(serializer.data)


class FarmerAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = timezone.now().date()
        weekly = []
        for i in range(5):
            day = today - timedelta(days=7 * (4 - i))
            weekly.append({'date': day.isoformat(), 'revenue': 1500 + i * 1200})

        return Response({
            'monthly_revenue': weekly,
            'category_distribution': [
                {'category': 'Fruits', 'value': 40},
                {'category': 'Vegetables', 'value': 35},
                {'category': 'Grains', 'value': 25},
            ],
        })


class RevenueReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        time_frame = request.query_params.get('time_frame', 'monthly').lower()
        now = timezone.now()

        if time_frame == 'daily':
            since = now - timedelta(days=1)
        elif time_frame == 'weekly':
            since = now - timedelta(weeks=1)
        elif time_frame == 'yearly':
            since = now - timedelta(days=365)
        else:
            time_frame = 'monthly'
            since = now - timedelta(days=30)

        if user.role == User.FARMER and not (user.is_superuser or user.is_staff):
            orders = Order.objects.all()
        elif user.role == User.ADMIN or user.is_superuser or user.is_staff:
            orders = Order.objects.all()
        else:
            orders = Order.objects.filter(buyer=user)

        orders = orders.filter(created_at__gte=since)
        total_revenue = orders.aggregate(sum=Sum('total_amount'))['sum'] or 0

        return Response({
            'time_frame': time_frame,
            'total_revenue': total_revenue,
            'order_count': orders.count(),
        })


class OrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role == User.ADMIN or user.is_superuser or user.is_staff:
            orders = Order.objects.all()
        elif user.role == User.FARMER:
            orders = Order.objects.all()
        else:
            orders = Order.objects.filter(buyer=user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        user = request.user
        if user.role == User.ADMIN or user.is_superuser or user.is_staff:
            order = get_object_or_404(Order, pk=pk)
        elif user.role == User.FARMER:
            order = get_object_or_404(Order, pk=pk)
        else:
            order = get_object_or_404(Order, pk=pk, buyer=request.user)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
