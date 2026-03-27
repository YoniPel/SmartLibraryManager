# Smart Library Manager 📚
A full-stack, containerized web application for managing your personal library with automated book data retrieval.

## Features
* Automated Data Fetching - Automatically retrieves book details like author, description, page count, cover image and more using Google Books API
* Dual Search Mode - Add books by entering 10/13 digits ISBN or by using the title of the book
* Duplicate Prevention - Checks if a book already exists in the library based on a unique combination of the title and the ISBN
* Responsive UI - Styled with Bootstrap for a clean and modern look

## Technologies
* Backend: Python & Django 5.0+  
* Frontend: Bootstrap & Django Template Engine
* Database: PostgreSQL 15
* APIs: Google Books API
* Containerization: Docker & Docker Compose


> [!WARNING]  
> This project is configured primarily for development use.
> * The application runs using Django's built-in development server
> * The Docker setup is intended for local development and testing 
> * Production configuration (e.g., Nginx, Gunicorn, etc.) is not included
>
> While the project can be adapted for production use, it is recommended to implement additional security measures and optimizations before deploying it in a production environment.
> 
> More on that can be found in the Deployment section below.


## Project Structure
```
├── catalog/                    # Main Django app
│   ├── services.py             # Google Books API integration
│   ├── templates/              # HTML templates  
│   └── static/                 # The CSS, JS and static images 
├── smart_library/              # Project configuration 
├── media/                      # Uploaded book cover images 
├── Dockerfile                  # The dockerfile
├── docker-compose.yaml         # The docker-compose file 
├── requirements.txt            # The Python dependencies 
├── manage.py                   # manage.py by Django 
├── .env.example                # .env template file 
└── README.md                   # The README file 
```

## Getting Started
1. Prerequisites
    * Docker 
    * A Google Books API key
    
> [!IMPORTANT]  
> If you don't have a Google API key, you can create a new one.  
> To create a new API key, you can check [here](https://console.cloud.google.com/apis/credentials) and then do the following:
> 1. Create a new project or use existing one if you have already
> 2. In the project, press on `Create credentials` and then `API key`
> 3. Give the API key a name and create it (you can also restrict it to be used only for Books API)
> 4. Go to `Enabled APIs & Services` on the left, press the `Books API` and enable it
>

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

    # Google Books API key 
    GOOGLE_BOOKS_API_KEY=Google-Books-API-key
    ```
> [!TIP]  
> For a minimal setup, you only need to update the `SECRET_KEY` and the `GOOGLE_BOOKS_API_KEY`.


> [!NOTE]  
> The `SECRET_KEY` is required for security purposes (sessions, CSRF tokens, etc.).  
> Since it is excluded from the version control for safety, you must generate your own.  
> You can do this by running:   
> `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`.   
> This will print the new secret key, copy it and paste in the `.env` file as the value of `SECRET_KEY`.  
> You can instead just write a random string as the value of `SECRET_KEY`, although this approach is less recommended.


3. Run with Docker  
* If this is the first time:
   * Run `docker-compose up --build` to build the image
   * Run `docker-compose exec web python manage.py migrate`in order to set up the DB  
* For every other time:  
   * Run `docker-compose up` 
    
The app will be accessible at `localhost:8000` in the browser. 

## Common Problems
* If you get an error related to the database connection, make sure that the database container is running and that the environment variables in the `.env` file are correct. You can also check the logs of the database container for more details on the error
* Running `docker-compose` in Linux machines has to be used with `sudo`. Without it, you'll have permissions issues
   with docker
* If you try to add a new book to the DB, and it doesn't find any book, it is possible that the API key doesn't work.  
Please check that you copied the right API key, and that you did enable the Google Books API. Notice that as long as 
you didn't enable it, the API key won't work, even if it's valid
  

## Deployment
This repository is focused on local development.  

With that being said, the project was successfully deployed on Render as part of validating a real-world deployment flow.  
If you'd like to deploy the project on Render, you can:
* Use a WSGI server like Gunicorn
* Configure environment variables in Render's dashboard (e.g., `SECRET_KEY`, `GOOGLE_BOOKS_API_KEY`, and `DATABASE_URL` for PostgreSQL)
* Set up static/media handling (e.g., whitenoise for static files and a cloud storage service for media files)  

You are of course free to adapt the project for deployment on other platforms as well.