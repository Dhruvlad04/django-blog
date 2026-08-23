# django-blog

A Blog Post Management REST API built with Django and Django REST Framework.

## Features
- CRUD for blog posts
- Token/session authentication
- Custom permission: only a post's author can edit or delete it
- Filtering by `status`, `author`, `created_after`, `created_before`
- Full-text search on `title` and `content` (`?search=`)
- Ordering (`?ordering=created_at` or `-created_at`, `title`)
- Pagination (5 per page, `?page=`, `?page_size=`)

## Setup

```bash
python -m venv venv
source venv/bin/activate      # venv\Scripts\activate on Windows
pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

python manage.py runserver
```

## API endpoints

| Method | Endpoint             | Auth required | Description             |
|--------|-----------------------|---------------|--------------------------|
| GET    | `/api/posts/`          | No            | List posts (paginated)  |
| POST   | `/api/posts/`          | Yes           | Create a post            |
| GET    | `/api/posts/{id}/`     | No            | Retrieve a post          |
| PUT    | `/api/posts/{id}/`     | Yes (author)  | Update a post            |
| PATCH  | `/api/posts/{id}/`     | Yes (author)  | Partially update a post  |
| DELETE | `/api/posts/{id}/`     | Yes (author)  | Delete a post             |
| POST   | `/api/token/`          | No            | Get auth token (username/password) |

Example filter/search/order query:
```
GET /api/posts/?status=published&search=django&ordering=-created_at
```

## Running tests
```bash
python manage.py test
```

## Notes / things to change before you submit or deploy this
- `SECRET_KEY` in `blog/settings.py` has an insecure fallback — set `DJANGO_SECRET_KEY` as an environment variable instead of leaving the default.
- `DEBUG = True` and `ALLOWED_HOSTS = ["*"]` are dev-only settings, not production-safe.
- `db.sqlite3` is gitignored on purpose — don't commit a database with test data if you're submitting this as coursework; migrations are enough to reconstruct the schema.
