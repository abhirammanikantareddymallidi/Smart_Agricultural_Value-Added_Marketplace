from rest_framework import viewsets, permissions
from .models import Order, Review
from .serializers import OrderSerializer, ReviewSerializer
from users.permissions import IsBuyer, IsFarmer, IsAdminRole

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_farmer():
            # Farmers see orders containing their products
            return Order.objects.filter(items__product__farmer=user).distinct()
        elif user.is_buyer():
            # Buyers see their own orders
            return Order.objects.filter(buyer=user)
        elif user.is_admin_role():
            return Order.objects.all()
        return Order.objects.none()

    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [permissions.IsAuthenticated, IsBuyer]
        elif self.action in ['update', 'partial_update']:
            # Either admin or farmer can update status
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, IsBuyer]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
