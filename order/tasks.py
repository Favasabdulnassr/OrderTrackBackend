from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Order

# celery -A OrderTrack worker -l info --pool=solo        ## run celery command

@shared_task
def send_warehouse_notification_email(order_id):
    """
    Send email notification to warehouse for order confirmation
    """
    try:
        order = Order.objects.get(id=order_id)
        
        subject = f"New Order Confirmation Required - Order #{order.id}"
        
        # Create HTML email content
        html_message = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #f4f4f4; padding: 15px; text-align: center; }}
                .order-details {{ background-color: #fff; padding: 20px; border: 1px solid #ddd; }}
                .confirm-button {{ 
                    display: inline-block; 
                    padding: 12px 24px; 
                    background-color: #28a745; 
                    color: white; 
                    text-decoration: none; 
                    border-radius: 5px; 
                    margin: 20px 0; 
                }}
                .detail-row {{ margin: 10px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>New Order Received</h2>
                    <p>Order #{order.id} requires confirmation</p>
                </div>
                
                <div class="order-details">
                    <h3>Order Details:</h3>
                    <div class="detail-row"><strong>Customer Name:</strong> {order.customer_name}</div>
                    <div class="detail-row"><strong>Customer ID:</strong> {order.customer_id}</div>
                    <div class="detail-row"><strong>Product:</strong> {order.product.name}</div>
                    <div class="detail-row"><strong>Quantity:</strong> {order.quantity}</div>
                    <div class="detail-row"><strong>Product Cost:</strong> ₹{order.product_cost}</div>
                    <div class="detail-row"><strong>Customer Email:</strong> {order.user_email}</div>
                    <div class="detail-row"><strong>Status:</strong> {order.status}</div>
                    <div class="detail-row"><strong>Order Date:</strong> {order.created_at.strftime('%Y-%m-%d %H:%M:%S')}</div>
                    
                    <div style="text-align: center; margin-top: 30px;">
                        <a href="http://your-frontend-url.com/confirm-order/{order.id}" class="confirm-button">
                            CONFIRM ORDER
                        </a>
                    </div>
                    
                    <p style="margin-top: 20px; font-size: 12px; color: #666;">
                        Click the button above to confirm this order. Once confirmed, the customer will be notified.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Plain text version
        plain_message = f"""
        New Order Confirmation Required - Order #{order.id}
        
        Order Details:
        Customer Name: {order.customer_name}
        Customer ID: {order.customer_id}
        Product: {order.product.name}
        Quantity: {order.quantity}
        Product Cost: ₹{order.product_cost}
        Customer Email: {order.user_email}
        Status: {order.status}
        Order Date: {order.created_at.strftime('%Y-%m-%d %H:%M:%S')}
        
        To confirm this order, visit:
        http://your-frontend-url.com/confirm-order/{order.id}
        """
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.WAREHOUSE_EMAIL],
            html_message=html_message,
            fail_silently=False
        )
        
        return f"Email sent successfully for order {order_id}"
        
    except Order.DoesNotExist:
        return f"Order {order_id} not found"
    except Exception as e:
        return f"Error sending email: {str(e)}"