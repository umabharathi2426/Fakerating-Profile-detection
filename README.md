# Fake Rating Detection System

This project is a Django-based web application designed to detect fake ratings using a K-Means clustering model. It provides a system for users to create accounts, view products, and for administrators to train a model and identify suspicious ratings.

## Features

- **User Authentication:** Sign up and log in functionality for users.
- **Product Ratings:** Users can view and rate products.
- **Fake Rating Detection:** Uses a K-Means clustering model to identify potentially fake ratings.
- **API for AI Model:** Endpoints to upload data, train the model, and get predictions.
- **Admin Interface:** Django admin for managing users and ratings.

## Prerequisites

Be sure you have the following installed on your development machine:

- Python >= 3.7
- Git
- pip
- virtualenv (or virtualenvwrapper)

## Project Installation

To set up a local development environment:

1.  **Create and activate a virtual environment:**

    ```bash
    # With virtualenv
    virtualenv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

2.  **Clone the project:**

    ```bash
    git clone <your-repository-url>
    cd FakeRatingDetection
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Migrate the database:**

    ```bash
    python manage.py migrate
    ```

5.  **Create a superuser:**

    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the development server:**

    ```bash
    python manage.py runserver
    ```

The application will be available at `http://127.0.0.1:8000`.

## How to Use the AI Model

The application provides a set of API endpoints to manage the machine learning model.

### 1. Upload Data

Upload your rating datasets (`user_rating.txt`, `mc.txt`, `rating.txt`) to the server.

-   **Endpoint:** `/api/detection/upload/`
-   **Method:** `POST`
-   **Body:** `multipart/form-data` with your files.

### 2. Train the Model

Train the K-Means clustering model with the uploaded data.

-   **Endpoint:** `/api/detection/train/`
-   **Method:** `POST`

### 3. Get Predictions

Get predictions on new rating data.

-   **Endpoint:** `/api/detection/predict/`
-   **Method:** `POST`
-   **Body:** JSON with a "RATING" key.

    Example:
    ```json
    {
        "RATING": 4
    }
    ```

## Technology Stack

-   **Backend:** Django, Django REST Framework
-   **Database:** SQLite3 (default)
-   **Machine Learning:** scikit-learn, pandas, joblib
-   **Frontend:** HTML, CSS, JavaScript (via Django Templates)
