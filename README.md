# Blog Platform

A complete blog platform built with Flask, featuring user authentication, post management, commenting, and an admin dashboard.

## Description

This project provides a fully functional blogging system where users can register, log in, create posts, comment on posts, and interact with content. The admin dashboard allows administrators to manage users, posts, and comments. The application is containerized with Docker for easy deployment.

## Features

- User registration and login/logout (password hashing)
- Create, edit, and delete posts (CRUD)
- Comment on posts (create, delete for authors/admins)
- Admin dashboard to manage all users, posts, and comments
- Responsive HTML/CSS design with custom styling
- Form validation and CSRF protection
- SQLite database (development) – easily switchable to PostgreSQL/MySQL
- Docker support for containerized deployment

## Tech Stack

- **Backend:** Flask (Python), SQLAlchemy (ORM), Flask-WTF (forms), Flask-Login (authentication)
- **Frontend:** HTML5, CSS3, JavaScript (vanilla)
- **Database:** SQLite (default) – can be swapped for PostgreSQL/MySQL
- **Containerization:** Docker, Docker Compose
- **Testing:** pytest (see `tests/`)

## Installation

### Prerequisites

- Python 3.9+
- pip
- (Optional) Docker and Docker Compose

### Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/blog-platform.git
   cd blog-platform
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   If no `requirements.txt` exists, create one with:
   ```
   Flask
   Flask-SQLAlchemy
   Flask-WTF
   Flask-Login
   ```
   Or install manually:
   ```bash
   pip install Flask Flask-SQLAlchemy Flask-WTF Flask-Login
   ```

4. Set up the database:
   ```bash
   flask shell
   >>> from app import db
   >>> db.create_all()
   >>> exit()
   ```

5. Run the development server:
   ```bash
   flask run
   ```

The application will be available at `http://127.0.0.1:5000`.

### Docker Deployment

1. Make sure Docker and Docker Compose are installed.

2. Build and start the services:
   ```bash
   docker-compose up --build
   ```

3. Access the application at `http://localhost:5000`.

## Usage

1. **Register a new account** at `/register`.
2. **Log in** at `/login`.
3. **Create a post** via the “New Post” link on the dashboard.
4. **View and comment** on posts.
5. **Admin access**: The first registered user is automatically an admin (or seed an admin account). Navigate to `/admin` to manage content.

## Project Structure

```
blog-platform/
├── app/
│   ├── __init__.py           # Flask app factory
│   ├── models.py             # SQLAlchemy models (User, Post, Comment)
│   ├── forms.py              # WTForms definitions
│   ├── routes/
│   │   ├── auth.py           # Login/logout/register routes
│   │   ├── posts.py          # Post CRUD routes
│   │   ├── comments.py       # Comment routes
│   │   └── admin.py          # Admin dashboard routes
│   ├── templates/
│   │   ├── base.html         # Base template with navigation
│   │   ├── index.html        # Home page (list of posts)
│   │   ├── login.html        # Login form
│   │   ├── register.html     # Registration form
│   │   ├── post.html         # Single post with comments
│   │   ├── create_post.html  # New/edit post form
│   │   └── admin.html        # Admin panel
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css     # Custom styles
│   │   └── js/
│   │       └── main.js       # Client-side scripts
├── tests/
│   ├── test_auth.py          # Authentication tests
│   └── test_posts.py         # Post route tests
├── Dockerfile                # Docker image definition
├── docker-compose.yml        # Docker Compose configuration
└── README.md                 # This file
```

## Testing

Run tests using pytest:
```bash
pip install pytest
pytest tests/
```

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.