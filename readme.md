# MyProject

## Note

The credentials of SMTP are not mentioned in the project. You can create a `.env` file and enter your credentials to generate OTP emails:

- `EMAIL_HOST_USER=your_email@example.com`
- `EMAIL_HOST_PASSWORD=your_app_password`
- `SECRET_KEY=your_django_secret_key`

## Description
A Django-based authentication system featuring user registration, OTP verification, and login/logout functionality. This project uses Django Rest Framework for API endpoints and a simple frontend interface.

## Features
- Custom user model with unique email login
- OTP-based verification
- Session and token-based authentication
- Simple frontend for demonstration

## Requirements
- Python 3.9+
- Django 5.1.7
- djangorestframework 3.14.0
- drf-yasg 1.21.4
- django-cors-headers 3.13.0

## Installation
1. Clone the repository or download the source code.
2. Create and activate a virtual environment (optional but recommended).
3. Install dependencies:  
   ```
   pip install -r requirements.txt
   ```

## Usage
1. Start the development server:
   ```
   python manage.py runserver
   ```
2. Visit http://127.0.0.1:8000/ in your browser to access the frontend.

## Configuration
- `settings.py` contains all configuration, including database, authentication classes, and installed apps.
- Update your SMTP settings in `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` for OTP emails.

## Project Structure
```
myproject/
├── authentication/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── authentication.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── myproject/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── templates/
│   └── index.html
├── manage.py
├── requirements.txt
└── db.sqlite3
```
## API Endpoints
The project provides the following API endpoints:

- `POST /api/register/` - Register a new user
- `POST /api/login/` - Login with email and password
- `POST /api/register/verify/` - Verify OTP for user authentication
- `POST /api/logout/` - Logout the current user
- `GET /api/me/` - Retrieve the authenticated user's details

## API Documentation
The project uses Swagger for API documentation. To access the Swagger UI, follow these steps:

1. Ensure the development server is running:
   ``` 
   python manage.py runserver
   ```
2. Visit http://127.0.0.1:8000/swagger/ in your browser to view the API documentation.

Swagger provides an interactive interface to test the API endpoints and view the request/response formats.
