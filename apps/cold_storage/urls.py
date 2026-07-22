from django.urls import path
from .views import ColdRoomListView, ColdRoomCreateView, ColdRoomDetailView, ColdRoomUpdateView, BookingCreateView, BookingListView, BookingApprovalView

urlpatterns = [
    path('rooms/', ColdRoomListView.as_view(), name='cold-room-list'),
    path('rooms/create/', ColdRoomCreateView.as_view(), name='cold-room-create'),
    path('rooms/<int:pk>/', ColdRoomDetailView.as_view(), name='cold-room-detail'),
    path('rooms/<int:pk>/update/', ColdRoomUpdateView.as_view(), name='cold-room-update'),
    path('bookings/', BookingListView.as_view(), name='booking-list'),
    path('bookings/create/', BookingCreateView.as_view(), name='booking-create'),
    path('bookings/<int:pk>/approve/', BookingApprovalView.as_view(), name='booking-approve'),
]