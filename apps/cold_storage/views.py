from rest_framework import generics, status, filters
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from .models import ColdRoom, ColdStorageBooking
from .serializers import ColdRoomSerializer, ColdRoomCreateSerializer, ColdStorageBookingSerializer, BookingApprovalSerializer
from apps.accounts.permissions import IsFarmer, IsOperator, IsAdmin

class ColdRoomListView(generics.ListAPIView):
    queryset = ColdRoom.objects.filter(is_active=True, is_verified=True)
    serializer_class = ColdRoomSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', 'location_name']

class ColdRoomCreateView(generics.CreateAPIView):
    serializer_class = ColdRoomCreateSerializer
    permission_classes = [IsOperator]

class ColdRoomDetailView(generics.RetrieveAPIView):
    queryset = ColdRoom.objects.filter(is_active=True)
    serializer_class = ColdRoomSerializer

class ColdRoomUpdateView(generics.UpdateAPIView):
    queryset = ColdRoom.objects.all()
    serializer_class = ColdRoomCreateSerializer
    permission_classes = [IsOperator]

class BookingCreateView(generics.CreateAPIView):
    serializer_class = ColdStorageBookingSerializer
    permission_classes = [IsFarmer]

class BookingListView(generics.ListAPIView):
    serializer_class = ColdStorageBookingSerializer
    def get_queryset(self):
        user = self.request.user
        if user.is_farmer:
            return ColdStorageBooking.objects.filter(farmer=user)
        elif user.is_operator:
            return ColdStorageBooking.objects.filter(cold_room__operator=user)
        return ColdStorageBooking.objects.none()

class BookingApprovalView(generics.UpdateAPIView):
    serializer_class = BookingApprovalSerializer
    permission_classes = [IsOperator]
    queryset = ColdStorageBooking.objects.all()