from rest_framework import viewsets,status
from rest_framework.response import Response
from .models import Order, Product
from .serializers import OrderSerializer, ProductSerializer
from .tasks import send_warehouse_notification_email



class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            
            # Send email to warehouse using Celery
            send_warehouse_notification_email.delay(order.id)
            
            return Response({
                'message': 'Order created successfully and warehouse has been notified',
                'order': serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
