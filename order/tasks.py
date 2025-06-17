from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Order

import logging
logger = logging.getLogger(__name__)


# celery -A OrderTrack worker -l info --pool=solo        ## run celery command
#  celery -A OrderTrack beat -l info                  ## run celery beat command



@shared_task
def send_warehouse_notification_email(order_id):
    """
    Send email notification to warehouse for order confirmation
    """
    logger.info(f"📦 Task started: Preparing email for order ID {order_id}")
    try:
        order = Order.objects.get(id=order_id)
        logger.info(f" Order found: {order}")
        
        subject = f"New Order  - Order #{order.id}"
        
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
                            NEW ORDER
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
        
        
        """
        logger.info(f"Sending email to warehouse for order #{order.id}")
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.WARE_HOUSE_EMAIL],
            html_message=html_message,
            fail_silently=False
        )
        logger.info(f"Email sent successfully for order #{order.id}")
        return f"Email sent successfully for order {order_id}"
        
    except Order.DoesNotExist:
        logger.error(f"Order with ID {order_id} does not exist.")
        return f"Order {order_id} not found"
    except Exception as e:
        logger.exception(f"Error sending email for order {order_id}: {str(e)}")
        return f"Error sending email: {str(e)}"
    






import imaplib
import email
from email.header import decode_header
import re
from celery import shared_task
from django.conf import settings
from .models import Order
import openai  




@shared_task
def send_dispatch_notification_email(order_id):
    """
    Send email notification to customer when order is dispatched
    """
    try:
        order = Order.objects.get(id=order_id)
        
        subject = f"Your Order #{order.id} is Ready for Dispatch!"
        
        # Create HTML email content for customer
        html_message = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #28a745; padding: 15px; text-align: center; color: white; }}
                .order-details {{ background-color: #fff; padding: 20px; border: 1px solid #ddd; }}
                .success-message {{ 
                    background-color: #d4edda; 
                    color: #155724; 
                    padding: 15px; 
                    border-radius: 5px; 
                    margin: 20px 0; 
                    text-align: center;
                }}
                .detail-row {{ margin: 10px 0; }}
                .footer {{ background-color: #f8f9fa; padding: 15px; text-align: center; color: #6c757d; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>🎉 Great News!</h2>
                    <p>Your order is ready for dispatch</p>
                </div>
                
                <div class="success-message">
                    <h3>Order #{order.id} Confirmed & Ready!</h3>
                    <p>Your order has been confirmed by our warehouse and will be dispatched soon.</p>
                </div>
                
                <div class="order-details">
                    <h3>Order Summary:</h3>
                    <div class="detail-row"><strong>Customer Name:</strong> {order.customer_name}</div>
                    <div class="detail-row"><strong>Product:</strong> {order.product.name}</div>
                    <div class="detail-row"><strong>Quantity:</strong> {order.quantity}</div>
                    <div class="detail-row"><strong>Total Cost:</strong> ₹{order.product_cost}</div>
                    <div class="detail-row"><strong>Order Status:</strong> <span style="color: #28a745; font-weight: bold;">Confirmed - Ready for Dispatch</span></div>
                    <div class="detail-row"><strong>Order Date:</strong> {order.created_at.strftime('%Y-%m-%d %H:%M:%S')}</div>
                </div>
                
                <div class="footer">
                    <p>Thank you for your order! We'll send you tracking information once your order is shipped.</p>
                    <p>If you have any questions, please contact our customer support.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Plain text version for customer
        plain_message = f"""
        Great News! Your Order #{order.id} is Ready for Dispatch!
        
        Your order has been confirmed by our warehouse and will be dispatched soon.
        
        Order Summary:
        Customer Name: {order.customer_name}
        Product: {order.product.name}
        Quantity: {order.quantity}
        Total Cost: ₹{order.product_cost}
        Order Status: Confirmed - Ready for Dispatch
        Order Date: {order.created_at.strftime('%Y-%m-%d %H:%M:%S')}
        
        Thank you for your order! We'll send you tracking information once your order is shipped.
        If you have any questions, please contact our customer support.
        """
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[order.user_email],  # Send to customer email
            html_message=html_message,
            fail_silently=False
        )
        
        return f"Dispatch notification email sent successfully to {order.user_email} for order {order_id}"
        
    except Order.DoesNotExist:
        return f"Order {order_id} not found"
    except Exception as e:
        return f"Error sending dispatch notification email: {str(e)}"



@shared_task
def process_warehouse_confirmation_emails():
    """
    Check for warehouse confirmation emails and update order status
    """
    try:
        # Connect to email server
        logger.info("Connecting to email server...")
        mail = imaplib.IMAP4_SSL(settings.IMAP_EMAIL_HOST)
        mail.login(settings.WARE_HOUSE_EMAIL, settings.WARE_HOUSE_EMAIL_PASSWORD)
        logger.info("Logged into email server.")

        
        # Select inbox
        mail.select('inbox')
        
        # Search for unread emails
        status, messages = mail.search(None, 'UNSEEN')
        logger.info(f"Search status: {status}")
        
        if status == 'OK':
            email_ids = messages[0].split()
            logger.info(f"Found {len(email_ids)} unread emails.")

            
            for email_id in email_ids:
                # Fetch email
                logger.info(f"Processing email ID: {email_id}")
                status, msg_data = mail.fetch(email_id, '(RFC822)')
                
                if status == 'OK':
                    email_body = msg_data[0][1]
                    email_message = email.message_from_bytes(email_body)
                    
                    # Get email subject and body
                    subject = decode_header(email_message["Subject"])[0][0]
                    if isinstance(subject, bytes):
                        subject = subject.decode()
                    logger.info(f"Email subject: {subject}")    
                    
                    # Get email body
                    body = get_email_body(email_message)
                    logger.debug(f"Email body: {body[:100]}...")  # Logging only first 100 chars for brevity
                    
                    # Process the email content with LLM
                    order_id, is_confirmation = analyze_email_with_llm(subject, body)
                    logger.info(f"LLM extracted - Order ID: {order_id}, Is Confirmation: {is_confirmation}")
                    
                    if is_confirmation and order_id:
                        # Update order status
                        try:
                            order = Order.objects.get(id=order_id)
                            order.status = 'Ready to Dispatch'
                            order.save()
                            logger.info(f"Order {order_id} status updated to 'Confirmed'.")

                            send_dispatch_notification_email.delay(order.id)
                            logger.info(f"Dispatch notification email task triggered for Order {order_id}.")
                            
                            # Mark email as read
                            mail.store(email_id, '+FLAGS', '\\Seen')
                            logger.info(f"Email {email_id} marked as read.")

                            
                            print(f"Order {order_id} status updated to Confirmed")
                            
                        except Order.DoesNotExist:
                            logger.warning(f"Order with ID {order_id} does not exist.")
        
        mail.close()
        mail.logout()
        logger.info("Email connection closed.")
        
        return "Email processing completed successfully"
        
    except Exception as e:
        logger.error(f"Error processing emails: {str(e)}", exc_info=True)
        return f"Error processing emails: {str(e)}"


def get_email_body(email_message):
    """
    Extract email body content
    """
    logger.info("Extracting email body...")
    body = ""

    if email_message.is_multipart():
        logger.debug("Email is multipart")
        for part in email_message.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            logger.debug(f"Checking part: content_type={content_type}, content_disposition={content_disposition}")

            if content_type == "text/plain" and "attachment" not in content_disposition:
                logger.info("Found plain text part")
                body = part.get_payload(decode=True).decode()
                break
            elif content_type == "text/html" and "attachment" not in content_disposition:
                logger.info("Found HTML part (fallback)")
                body = part.get_payload(decode=True).decode()
    else:
        logger.debug("Email is not multipart")
        body = email_message.get_payload(decode=True).decode()

    logger.debug(f"Extracted body: {body[:100]}...")  # log first 100 chars for preview
    return body



import requests

def analyze_email_with_llm(subject, body):
   
    try:
        logger.info("Starting LLM analysis...")
        logger.debug(f"Subject: {subject}")
        logger.debug(f"Body (first 100 chars): {body[:100]}")


        prompt = f"""
        Analyze the following email to extract order information.

        Subject: {subject}
        Body: {body}

        Instructions:
        1. Find the Order ID from the subject or body using formats like "Order #123", "Order 123", "#123".
        2. Check if the order status is exactly "Order Placed".
           - Match lines like "Status: Order Placed" (case-insensitive).
           - If status is "Order Placed", set IS_ORDER_PLACED to True. Otherwise, False.

        Respond ONLY in this exact format:
        ORDER_ID: [number only, or "None"]
        IS_ORDER_PLACED: [True/False]
        """

        headers = {
            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "mistralai/mistral-7b-instruct",  # or openchat/openchat-7b, meta-llama/llama-3-8b-instruct
            "messages": [
                {"role": "system", "content": "You are a precise email analyzer that extracts order information. Follow the format exactly."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.0,
            "max_tokens": 100
        }

        logger.debug("Sending request to OpenRouter...")
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

        if response.status_code != 200:
            logger.error(f"OpenRouter error {response.status_code}: {response.text}")
            return None, False

        result = response.json()['choices'][0]['message']['content'].strip()
        logger.debug(f"Raw LLM Response: {result}")


        # Parse the response
        order_id = None
        is_order_placed = False
        lines = result.split('\n')

        for line in lines:
            line = line.strip()
            if line.startswith('ORDER_ID:'):
                order_id_str = line.split(':', 1)[1].strip()
                if order_id_str.lower() != "none":
                    order_match = re.search(r'\d+', order_id_str)
                    if order_match:
                        try:
                            order_id = int(order_match.group())
                            logger.info(f"Parsed Order ID: {order_id}")
                        except ValueError:
                            logger.warning("Failed to convert order ID to integer")

            elif line.startswith('IS_ORDER_PLACED:'):
                status_str = line.split(':', 1)[1].strip().lower()
                is_order_placed = status_str == 'true'
                logger.info(f"Parsed IS_ORDER_PLACED: {is_order_placed}")

        return order_id, is_order_placed

    except Exception as e:
        logger.error(f"Error analyzing email with LLM: {str(e)}")
        return None, False




