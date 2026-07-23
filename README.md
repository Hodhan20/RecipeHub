# RecipeHub

RecipeHub is a web application where users can discover, create, edit, manage and favourite recipes. It provides a simple way for people to browse community recipes and organize their own culinary content.

## Project Overview

The project is a full-stack web application built with Django. It allows users to register for an account, share their own recipes with titles, descriptions, ingredients and instructions, and browse recipes shared by other users. Logged-in users can mark recipes as favourites, edit their own recipes, and manage their profiles. The interface supports light and dark mode.

## Features

- User registration and login (via django-allauth)
- User profile with avatar upload
- Browse all recipes on a public landing page
- Search recipes by title
- Filter recipes by category
- View individual recipe details
- Create new recipes (logged-in users)
- Edit own recipes
- Delete own recipes
- Favourite / unfavourite recipes
- View personal favourite recipes
- User dashboard with stats and recent recipes
- Admin dashboard with platform overview
- Light and dark mode toggle
- Responsive layout for mobile, tablet and desktop
- Public API with OpenAPI documentation

## Technologies Used

- Python 3.14
- Django
- Django REST Framework
- django-allauth
- SQLite (local development)
- Tailwind CSS v4
- DaisyUI
- Alpine.js
- HTMX
- JavaScript (ES6+)
- Vite
- Celery
- Redis (production / optional locally)

## Installation

Clone the repository and navigate into the project folder:

```bash
git clone <your-repo-url>
cd django-starter
```

Install Python dependencies and front-end dependencies, then apply database migrations:

```bash
make init
```

Or manually:

```bash
uv sync
npm install
python manage.py migrate
```

## Running the Application

Local development needs two terminals running at the same time.

**Terminal 1 — Django backend:**

```bash
make start
```

**Terminal 2 — Vite front end:**

```bash
make npm-dev
```

Open [http://localhost:8000](http://localhost:8000) in your browser.

The Django admin is available at [http://localhost:8000/admin/](http://localhost:8000/admin/).

## Everyday Commands

| Command | Description |
|---------|-------------|
| `make start` | Run the Django development server |
| `make npm-dev` | Run the Vite dev server |
| `make test` | Run the test suite |
| `make migrations` | Create new database migrations |
| `make migrate` | Apply migrations |
| `make shell` | Open a Django shell |
| `make manage ARGS='createsuperuser'` | Run any Django management command |
| `make ruff` | Format and lint Python code |

Run `make` with no arguments to see all available targets.

## Project Structure

```
django-starter/
├── apps/
│   ├── recipes/       # Recipe models, forms, views, URLs and templates
│   ├── users/         # Custom user model, profile views, avatar upload
│   └── web/           # Landing page, dashboards, base templates
├── assets/            # Front-end JavaScript, CSS and Vite config
├── static/            # Collected static files and uploaded media
├── templates/         # Django HTML templates
├── config/            # Django settings and URL configuration
├── media/             # User-uploaded files (profile pictures, recipe images)
├── api-client/        # Auto-generated TypeScript API client
└── manage.py          # Django management script
```

## Future Improvements

These are ideas that are not currently implemented:

- Advanced recipe search with multiple filters
- Recipe ratings and reviews
- Comments on recipes
- User-to-user messaging or following
- Meal planning and shopping lists
- Recipe collections or cookbooks
- Email notifications
- Social media sharing for recipes
- Mobile application

## Author

Hodhan Omar
