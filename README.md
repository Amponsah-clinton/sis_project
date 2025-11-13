# SIS - ScholarIndex System

Django project for scholarly research indexing platform.

## Project Structure

```
sis/
├── app/                    # Main application
│   ├── forms.py           # Django forms
│   ├── urls.py            # App URL configuration
│   ├── views.py           # View functions
│   ├── models.py          # Database models
│   └── templates/
│       └── app/
│           └── landing.html
├── sis/                    # Project settings
│   ├── settings.py        # Django settings
│   └── urls.py            # Main URL configuration
├── static/                 # Static files directory
├── manage.py              # Django management script
└── requirements.txt        # Python dependencies
```

## Setup Instructions

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

3. Create superuser (optional):
```bash
python manage.py createsuperuser
```

4. Run development server:
```bash
python manage.py runserver
```

5. Access the application:
- Landing page: http://127.0.0.1:8000/
- Admin panel: http://127.0.0.1:8000/admin/

## URLs

- `/` - Landing page
- `/browse/` - Browse articles
- `/submit/` - Submit research
- `/about/` - About page
- `/admin/` - Django admin panel

## Features

- Modern responsive landing page with hero carousel
- Search functionality
- Dark/light theme toggle
- Contact form for submissions
- Fully configured Django project structure

