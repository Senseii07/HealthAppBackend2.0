# PCOS Companion - Backend API Service

This is the backend API service for **PCOS Companion**, a private wellness web application designed to help manage PCOS/PCOD through nutrition, hydration tracking, exercise, yoga, meditation, symptom logging, and cycle predictions.

It is built using **Django 5**, **Django REST Framework**, and supports both **PostgreSQL** (production) and **SQLite** (local fallback). It also integrates with **Google Gemini API** (`gemini-1.5-flash`) for the AI Wellness Assistant.

---

## Technical Stack

*   **Framework**: Django 5.0.x
*   **API Toolkit**: Django REST Framework (DRF)
*   **Database**: PostgreSQL (production) / SQLite (local dev fallback)
*   **WSGI Server**: Gunicorn (for production)
*   **Static Asset Management**: WhiteNoise
*   **AI Integration**: Google Generative AI (Gemini SDK)

---

## Local Setup & Installation

To run this backend locally on your Windows system:

### 1. Prerequisites
Ensure you have Python 3.12+ installed. You can verify this by running:
```powershell
python --version
```

### 2. Create and Activate Virtual Environment
Open your terminal (PowerShell), navigate to the `backend/` directory, and run:
```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies
Install all package requirements listed in `requirements.txt`:
```powershell
pip install -r requirements.txt
```

### 4. Create local environment settings
A `.env` file has been pre-configured with default development parameters. If you need to make changes, refer to `.env.example`.

To enable the AI assistant, add your Gemini API Key in the `.env` file:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 5. Run Database Migrations
Create and initialize your local SQLite database:
```powershell
python manage.py migrate
```

### 6. Seed the Database
Populate your database with anti-inflammatory meal plans (Week 1), exercise workouts, yoga routines, educational articles, and daily quotes:
```powershell
python manage.py seed_data
```

### 7. Run the Development Server
Launch the local Django server:
```powershell
python manage.py runserver
```
The API is now running locally at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

---

## Running Automated Tests

Run the test suite to verify endpoints and model calculations:
```powershell
python manage.py test apps
```

---

## Local Administrator Credentials

You can log in to the Django Admin console to manage meals, articles, and logs directly:
*   **URL**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
*   **Username**: `admin`
*   **Password**: `admin123`

---

## API Catalog Reference

All requests (except authentication) require a token header:
`Authorization: Token <your_token_key>`

### 1. Authentication
*   `POST /api/auth/login/`: Takes `username` and `password`. Returns auth `token`, profile completeness status.
*   `POST /api/auth/logout/`: Invalidates the authentication token.
*   `GET /api/auth/me/` / `PUT /api/auth/me/`: Retrieve or update the current user's profile information.

### 2. Consolidated Dashboard
*   `GET /api/wellness/dashboard/`: The main application dashboard. Consolidates:
    *   Today's habit checklist (water, sleep, exercise, yoga, meditation).
    *   Today's anti-inflammatory meals (breakfast, lunch, dinner, snack) matching the rotating week.
    *   Today's symptoms.
    *   Menstrual cycle progress details (active period day OR days until next predicted period).
    *   Today's recommended routine (rotating yoga, workouts, and meditations).
    *   Daily quote.

### 3. Wellness & Habits Tracker
*   `GET /api/wellness/habits/by_date/?date=YYYY-MM-DD`: Retrieve or initialize daily checklist values for a specific day.
*   `POST /api/wellness/habits/`: Create habit log entries.
*   `PATCH /api/wellness/habits/<id>/`: Update water intake, sleep, or checklist completions.
*   `GET /api/wellness/symptoms/` / `POST /api/wellness/symptoms/`: Fetch historical symptom logs or add new ones.
*   `GET /api/wellness/cycles/` / `POST /api/wellness/cycles/`: Fetch historical cycles or log a new period.
*   `GET /api/wellness/cycles/predictions/`: Calculates average cycle lengths and outputs predicted dates for the next 3 menstrual periods.

### 4. Content & Rotation
*   `GET /api/content/meals/today/`: Returns today's meals ( Breakfast, Lunch, Dinner, Snack) matching the current rotating week (determined by ISO week of the year).
*   `GET /api/content/meals/weekly_plan/?week=<num>`: Returns full weekly plans.
*   `GET /api/content/routines/?category=<category>`: Returns exercise, yoga, or meditation routines.
*   `GET /api/content/resources/`: Retrieves educational articles and news.
*   `GET /api/content/quotes/today/`: Returns the quote of the day.

### 5. Gemini AI Assistant Chat
*   `GET /api/chat/sessions/` / `POST /api/chat/sessions/`: Retrieve list of chat history or create a new conversation session.
*   `POST /api/chat/sessions/<uuid>/send_message/`: Sends a prompt to the AI wellness assistant. It maintains short-term memory of previous conversation messages and yields natural, PCOS-focused, empathetic recommendations.

---

## Render Production Deployment

To host this API backend on Render:
1.  Connect your GitHub repository to Render.
2.  Create a new **Web Service**.
3.  Set **Build Command** to: `./build.sh`
4.  Set **Start Command** to: `gunicorn pcos_backend.wsgi`
5.  Set the following **Environment Variables**:
    *   `SECRET_KEY`: A secure random secret key.
    *   `DEBUG`: `False`
    *   `ALLOWED_HOSTS`: `<your-subdomain>.onrender.com`
    *   `DATABASE_URL`: Add your Render PostgreSQL database connection string.
    *   `CORS_ALLOWED_ORIGINS`: Your frontend URL (e.g. `https://<username>.github.io`).
    *   `GEMINI_API_KEY`: Your Google Gemini API Key.
