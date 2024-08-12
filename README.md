# Credentials Management System

## Project Overview

The Credentials Management System is a Django-based web application designed to securely manage credentials for various services. It provides features for creating, updating, and managing credentials, services, and tags. The system ensures that only authenticated users can access and manage their credentials, with additional support for admin users to manage all credentials.

## Features

- User registration and authentication
- Create, update, and delete credentials
- Filter credentials by service and tag
- Secure password storage using encryption
- Rate limiting to prevent abuse
- Pagination for large datasets
- API documentation with Swagger (you can directly test the APIs from it)

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtualenv (optional but recommended)

### Step-by-Step Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/Manhalmaath/AswarBackEndTask.git
    cd credentials-management-system
    ```

2. **Create a virtual environment (optional but recommended):**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Set up the database:**

    ```sh
    python manage.py migrate
    ```

5. **Create a superuser (admin user):**

    ```sh
    python manage.py createsuperuser
    ```

6. **Run the development server:**

    ```sh
    python manage.py runserver
    ```

7. **Access the application:**

    Open your web browser and go to `http://127.0.0.1:8000/`.

## API Endpoints

### User Management

- **Register:** `POST /api/register/`
- **Login:** `POST /api/login/`

### Credential Management

- **List Credentials:** `GET /api/credentials/`
- **Create Credential:** `POST /api/credentials/create/`
- **Update Credential:** `PATCH /api/credentials/<id>/update/`
- **Grant Access:** `POST /api/credentials/<id>/grant-access/`

### Service Management

- **List/Create Services:** `GET/POST /api/services/`
- **Update/Delete Service:** `PATCH/DELETE /api/services/<id>/`

### Tag Management

- **List/Create Tags:** `GET/POST /api/tags/`
- **Update/Delete Tag:** `PATCH/DELETE /api/tags/<id>/`

## Configuration

### Environment Variables

- `SECRET_KEY`: Your Django secret key (set in `AswarBackEndTask/settings.py`).
- `DEBUG`: Set to `False` in production.
- `ALLOWED_HOSTS`: List of allowed hosts.

### Email Configuration

Set the following variables in `AswarBackEndTask/settings.py` for email functionality (temporary and will remove the Google app password after evaluation):

- `EMAIL_BACKEND`
- `EMAIL_HOST`
- `EMAIL_PORT`
- `EMAIL_USE_TLS`
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`

## Running Tests

To run the tests, use the following command:

```sh
python manage.py test