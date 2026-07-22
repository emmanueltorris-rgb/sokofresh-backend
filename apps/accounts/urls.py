from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CurrentUserView, RegisterView, UserViewSet, DashboardStatsView

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('me/', CurrentUserView.as_view(), name='current-user'),
    path('register/', RegisterView.as_view(), name='register'),
    path('dashboard-stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
]
