

# ORDERTRACK (Backend)

  **Overview**

        OrderTrack is a backend service built using Django REST Framework. It allows customers to place orders and automatically handles email communication with the warehouse.

        This project includes only the backend. The frontend is built with React (in a separate project).



## Order Flow Summary

    - Customer submits an order from the React frontend

    - Backend saves the order with status “Order Placed” and emails the warehouse

    - Celery + LLM check unread emails from the warehouse every minute

    - If the email says “Order Placed”:
        → Order status is updated to “Ready to Dispatch”
        → A confirmation email is sent to the customer



 ## How to Run

    1. Clone the Repository

        - git clone https://github.com/Favasabdulnassr/OrderTrackBackend.git

    2. Create & Activate Virtual Environment

        - For macOS / Linux:

            python3 -m venv venv
            source venv/bin/activate

        - For Windows:

            python -m venv venv
            venv\Scripts\activate

    3. Install Dependencies
        - pip install -r requirements.txt

    4. Setup Environment Variables
        - Create a .env file in the project root directory and add the following:


            SECRET_KEY=your_secret_key
            DEBUG=True

            # PostgreSQL
            DATABASE_NAME=your_db_name
            DATABASE_USER=your_db_user
            DATABASE_PASSWORD=your_db_pass
            DATABASE_HOST=localhost
            DATABASE_PORT=5432

            # Email
            EMAIL_HOST=smtp.gmail.com
            EMAIL_PORT=587
            EMAIL_HOST_USER=your_email@gmail.com
            EMAIL_HOST_PASSWORD=your_app_password

            # IMAP
            IMAP_EMAIL_HOST=imap.gmail.com
            IMAP_EMAIL_PORT=993
            WARE_HOUSE_EMAIL=warehouse_email@example.com
            WARE_HOUSE_EMAIL_PASSWORD=warehouse_email_password

            # Celery / Redis
            CELERY_BROKER_URL=redis://localhost:6379/0
            CELERY_RESULT_BACKEND=redis://localhost:6379/1

            # OpenRouter LLM API
            OPENROUTER_API_KEY=your_openrouter_api_key
            Note: Use an App Password for Gmail instead of your real password.

    5. Run Migrations
    
        - python manage.py migrate

    6. Start the Django Server

        - python manage.py runserver

    7. Start Celery
        - In two separate terminals (activate your virtual environment in both):

        - Terminal 1: Celery Worker
                celery -A OrderTrack worker -l info
                Terminal 2: Celery Beat Scheduler

