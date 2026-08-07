# MoviWeb App

A dynamic web application built with Flask that lets multiple users keep track of their favorite movies. It's the web evolution of a command-line movie app: users can be created and selected from the site, and each user can add, update, delete, and list their own movies. New movies are automatically enriched with data (director, year, poster) fetched from the [OMDb API](https://www.omdbapi.com/).

## Features

- **User management** — create new users and select an existing one from a list.
- **Movie management per user** — add, update, and delete movies from a personal favorites list.
- **OMDb integration** — adding a movie only requires a title; director, release year, and poster are fetched automatically.
- **Feedback messages** — success, warning, and error messages (via Flask's flash system) confirm what just happened.
- **Resilient error handling** — network timeouts, OMDb "not found" responses, and database errors are handled gracefully instead of crashing the app.
- **Custom error pages** — friendly 404 and 500 pages instead of Flask's default ones.

## Tech Stack

- [Python 3](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/) — web framework
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) — ORM for the SQLite database
- [Jinja2](https://jinja.palletsprojects.com/) — HTML templating (bundled with Flask)
- [Requests](https://requests.readthedocs.io/) — HTTP calls to the OMDb API
- [python-dotenv](https://pypi.org/project/python-dotenv/) — environment variable management
- SQLite — lightweight file-based database

## Project Structure

```
MoviWebApp/
├── app.py                 # Flask app, routes, and OMDb integration
├── models.py               # SQLAlchemy models (User, Movie)
├── data_manager.py         # DataManager class: all CRUD operations
├── data/
│   └── movies.db           # SQLite database (created automatically)
├── static/
│   └── style.css
├── templates/
│   ├── base.html            # Shared layout + flash messages
│   ├── index.html           # User list / create user form
│   ├── movies.html          # Movie list for a selected user
│   ├── 404.html             # Custom "page not found" page
│   └── 500.html             # Custom "server error" page
├── .env                    # Environment variables (not committed)
├── requirements.txt
└── README.md
```

## Data Model

**User**
| Field | Type | Description |
|---|---|---|
| id | Integer | Primary key |
| name | String | User's display name |

**Movie**
| Field | Type | Description |
|---|---|---|
| id | Integer | Primary key |
| name | String | Movie title |
| director | String | Fetched from OMDb (nullable) |
| year | Integer | Release year, fetched from OMDb (nullable) |
| poster_url | String | Poster image URL, fetched from OMDb (nullable) |
| user_id | Integer | Foreign key to `User.id` |

Each user can have many movies; deleting a user also deletes their movies (cascade).

## Getting Started

### Prerequisites

- Python 3.9+
- A free [OMDb API key](https://www.omdbapi.com/apikey.aspx)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd MoviWebApp
   ```

2. **Create and activate a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate      # on Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   Create a `.env` file in the project root:
   ```env
   OMDB_API_KEY=your_omdb_api_key_here
   SECRET_KEY=a_random_secret_string
   ```
   - `OMDB_API_KEY` is required to fetch movie details; without it, movies are still added but without director/year/poster info.
   - `SECRET_KEY` is used by Flask to sign session data (needed for flash messages). If it's missing, the app falls back to an insecure default and prints a warning — don't skip this in production.

5. **Run the app**
   ```bash
   python app.py
   ```
   The `data/` folder and the SQLite database are created automatically on first run. The app will be available at `http://localhost:5000`.

## Usage

1. Open the home page and create a user (or pick an existing one from the list).
2. On the user's movie page, add a movie by typing just its title — the app fetches the rest from OMDb.
3. Update a movie's title inline, or delete it, directly from its card.
4. Flash messages at the top of the page confirm whether each action succeeded, and explain what went wrong when it doesn't.

## Error Handling

- **OMDb lookups** use a 5-second timeout and check OMDb's own `Response: False` field, so a mistyped or unknown title doesn't silently store a movie with empty fields — the movie is still added with just the title the user typed, and a warning explains that no OMDb data was found.
- **Database writes** (`create_user`, `add_movie`, `update_movie`, `delete_movie`) are wrapped in error handling that rolls back the session on failure, so a failed operation never leaves the database session in a broken state.
- **404 / 500 pages** replace Flask's default error pages with ones that match the site's look and offer a way back to the home page.

## Possible Future Improvements

- User authentication (passwords/login) instead of simple user selection.
- CSRF protection on forms (e.g. via Flask-WTF).
- Prevent duplicate movies in the same user's list.
- Pagination or search/filter for large movie lists.