from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    farmer_name = serializers.ReadOnlyField(source='farmer.username')

    class Meta:
        model = Product
        fields = ('id', 'farmer', 'farmer_name', 'name', 'description', 'price_per_half_kg', 'stock_quantity', 'product_image', 'category', 'created_at', 'updated_at')
        read_only_fields = ('farmer',)

    def create(self, validated_data):
        # Automatically assign the request user as the farmer
        request = self.context.get('request')
        validated_data['farmer'] = request.user
        return super().create(validated_data)
