from rest_framework import serializers
from .models import Produce, Order


class ProduceSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='name', read_only=True)
    price_per_kg = serializers.DecimalField(source='price', max_digits=10, decimal_places=2, read_only=True)
    quantity_available_kg = serializers.IntegerField(read_only=True)
    grade = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    image_url = serializers.URLField(allow_blank=True, required=False, read_only=True)
    farmer = serializers.SerializerMethodField()
    farmer_location = serializers.SerializerMethodField()
    location = serializers.CharField(read_only=True)

    class Meta:
        model = Produce
        fields = [
            'id',
            'title',
            'description',
            'price_per_kg',
            'quantity_available_kg',
            'grade',
            'is_active',
            'image_url',
            'farmer',
            'farmer_location',
            'location',
        ]

    def get_farmer(self, obj):
        if obj.farmer:
            return {
                'id': obj.farmer.id,
                'username': getattr(obj.farmer, 'username', None),
                'email': getattr(obj.farmer, 'email', None),
            }
        return None

    def get_farmer_location(self, obj):
        # Prefer explicit produce.location, otherwise try to read farmer profile
        if obj.location:
            return obj.location
        farmer = getattr(obj, 'farmer', None)
        if farmer is None:
            return None
        # Try common profile attribute names
        profile = getattr(farmer, 'profile', None)
        if profile is not None:
            return getattr(profile, 'location_name', None) or getattr(profile, 'location', None)
        # fallback to farmer attribute if present
        return getattr(farmer, 'location', None)


class OrderSerializer(serializers.ModelSerializer):
    status_display = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id',
            'order_number',
            'created_at',
            'status',
            'status_display',
            'total_amount',
            'delivery_address',
            'delivery_notes',
            'items',
        ]

    def get_status_display(self, obj):
        mapping = {
            'PENDING': 'Pending',
            'PAID_ESCROW': 'Paid Escrow',
            'SHIPPED': 'Shipped',
            'DELIVERED': 'Delivered',
            'CANCELLED': 'Cancelled',
        }
        return mapping.get(obj.status, obj.status)

    def get_items(self, obj):
        return []
