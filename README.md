# Smart Library Manager
A containerized web application for library management.

## Features
* Automated Data Fetching - Automatically retrieves book details like author, description, page count, cover image and more using Google Books API.
* Dual Search Mode - Add books by entering 10/13 digits ISBN or by using the title of the book.
* Duplicate Prevention - Checks if a book already exists in the library based on a unique combination of the title and the ISBN. 
* Responsive UI - Styled with Bootstrap for a clean and modern look. 

## Technologies
* Backend: Python & Django 5.0+  
* Frontend: Bootstrap & Django Template Engine
* Database: PostgreSQL 15
* APIs: Google Books API
* Containerization: Docker & Docker Compose

## Getting Started
1. Prerequisites
    * Docker 
    * A Google Books API key
2. Environment Configuration
    * Create a `.env` file in the root directory (or delete the `.example` suffix in the `.env.example` file) and fill in the following:
    ```
    # Django settings
    DEBUG=True
    SECRET_KEY=django-secret-key-here

    # Postgres settings
    DB_NAME=db-name
    DB_USER=db-user
    DB_PASSWORD=db-password
    DB_HOST=db
    DB_PORT=5432

    # Google Books API
    GOOGLE_BOOKS_API_KEY=Google-Books-API-key
    ```
   
> [!TIP]  
> You can keep the `DB` variables the same, you only need to update the `SECRET_KEY` and the `GOOGLE_BOOKS_API_KEY`.

> [!NOTE]  
> The `SECRET_KEY` is required for security purposes (sessions, CSRF tokens, etc).  
> Since it is excluded from the version control for safety, you must generate your own.  
> You can do this by running `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`.   
> This will print the new secret key, copy it and paste in the `.env` file as the value of `SECRET_KEY`.  
> You can instead just write a random string as the value of `SECRET_KEY`, although this approach is less recommended.

> [!IMPORTANT]  
> You have to create an API key for Google Books if you don't have one already.  
> To create a new API key, you can check [here](https://console.cloud.google.com/apis/credentials) and then do the following:
> 1. Create a new project or use existing one if you have already.
> 2. In the project, press on `Create credentials` and then `API key`.
> 3. Give the API key a name and create it (you can also restrict it to be used only for Books API).
> 4. Copy the key and paste it in `.env` file as the value of `GOOGLE_BOOKS_API_KEY`.
> 5. Go to `Enabled APIs & Services` on the left, press the `Books API` and enable it. 

3. Run with Docker  
* From the root directory do the following. If this is the first time:
   * Run `docker-compose up --build` to build the image.
   * Run `docker-compose exec web python manage.py migrate`in order to set up the DB.  
* For every other time:   
   * Run `docker-compose up`. 
    
The app will be accessible at `localhost:8000` in the browser. 






