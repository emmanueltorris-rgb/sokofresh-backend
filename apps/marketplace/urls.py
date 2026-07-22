from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProduceViewSet, CategoryListView, MyProduceView, FarmerAnalyticsView, OrderListView, OrderDetailView

router = DefaultRouter()
router.register(r'produce', ProduceViewSet)

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('analytics/farmer/', FarmerAnalyticsView.as_view(), name='farmer-analytics'),
    path('my-produce/', MyProduceView.as_view(), name='my-produce'),
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('', include(router.urls)),
]
