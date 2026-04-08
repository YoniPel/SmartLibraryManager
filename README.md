# Smart Library Manager 📚 [![GitHub Actions CI](https://github.com/YoniPel/SmartLibraryManager/actions/workflows/ci.yaml/badge.svg)](https://github.com/YoniPel/SmartLibraryManager/actions/workflows/ci.yaml)
A full-stack, containerized web application for managing your personal library with automated book data retrieval.

## Features
* Automated Data Fetching - Automatically retrieves book details like author, description, page count, cover image and more using Google Books API
* Dual Search Mode - Add books by entering 10/13 digits ISBN, the title of the book or manually filling in the details
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
│   ├── tests/                  # Unit tests and intergration tests
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
    * Docker and Docker Compose
    * A Google Books API key 

> [!NOTE]  
> A Google Books API key is required to fetch book details from the Google Books API.  
> You can use an existing API key if you have one, or create a new one if you don't have it yet.  
> To create a new API key, you can check [here](https://console.cloud.google.com/apis/credentials) and then do the following:
> * Create a new project or use existing one if you have already
> * In the project, press on `Create credentials` and then `API key`
> * Give the API key a name and create it (you can also restrict it to be used only for Books API)
> * Go to `Enabled APIs & Services` on the left, press the `Books API` and enable it



2. Environment Configuration
   * Create a `.env` file in the root directory (or delete the `.example` suffix in the `.env.example` file) and fill in the following:  
     
       ```
       # Django settings
       DEBUG=True
       SECRET_KEY=django-secret-key-here
       ALLOWED_HOSTS=localhost

       # Postgres settings
       DB_NAME=db-name
       DB_USER=db-user
       DB_PASSWORD=db-password
       DB_HOST=db
       DB_PORT=5432
  
       DATABASE_URL=postgres://db-user:db-password@db:5432/db-name

       # Google Books API key 
       GOOGLE_BOOKS_API_KEY=Google-Books-API-key
 
> [!TIP]  
> For a minimal setup, you only need to update `GOOGLE_BOOKS_API_KEY`.  
> If you're only planning on adding books manually, you can also ignore that as well. The only required field for adding a book manually is the title of the book.  

3. Run with Docker  
* If this is the first time you are running the project:
   * Run `docker-compose up --build` to build the image
   * Run `docker-compose exec web python manage.py migrate`in order to set up the DB  
* For every other time:  
   * Run `docker-compose up` 
    
The app will be accessible at `localhost:8000` in the browser. 

## Deployment
As mentioned above, this project is configured primarily for development use.  
However, it uses a single `setting.py` file that dynamically adjusts its configuration based on the environment variables,
so it can be easily adapted for production with the following deployment setup:
* Hosting - Render Web Service
* Database - Render PostgreSQL
* Static Files - Served via Whitenoise
* Media Files - Stored and Served via AWS S3
* WSGI Server - Gunicorn

With that being said, that is by no means the only way to deploy the project, and you can choose any hosting provider and deployment setup that suits your needs.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details