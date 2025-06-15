from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.mail import send_mail
from django.conf import settings
from .models import Order, Product
from .serializers import OrderSerializer, ProductSerializer



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

            # Email content
            subject = f"New Order Placed: Order #{order.id}"
            message = f"""
Order Details:
Customer Name: {order.customer_name}
Customer ID: {order.customer_id}
Product: {order.product.name}
Quantity: {order.quantity}
Cost: ₹{order.product_cost}
Email: {order.user_email}
Status: {order.status}

To confirm this order, click the link below:
http://your-frontend-url.com/confirm-order/{order.id}
"""
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],  # warehouse email (for now same as sender)
                fail_silently=False
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)