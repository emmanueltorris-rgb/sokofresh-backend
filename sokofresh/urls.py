from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from apps.accounts.views import EmailTokenObtainPairView
from apps.marketplace.views import RevenueReportView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/marketplace/', include('apps.marketplace.urls')),
    path('api/accounts/', include('apps.accounts.urls')),
    path('api/payments/', include('apps.payments.urls')),
    path('api/auth/login/', EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/reports/revenue/', RevenueReportView.as_view(), name='revenue-report'),
    path('api-auth/', include('rest_framework.urls')),
]
