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
            print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
            send_warehouse_notification_email.delay(order.id)
            
            return Response({
                'message': 'Order created successfully and warehouse has been notified',
                'order': serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

from rest_framework.views import APIView

class ConfirmOrderDispatchView(APIView):
    def patch(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)

            if order.status == 'Order Placed':
                order.status = 'Ready to Dispatch'
                order.save()
                return Response(
                    {'message': f'Order #{order.id} status updated to Ready to Dispatch'},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'message': 'Order already confirmed or dispatched'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)