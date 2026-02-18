# Backend

This is the backend for the full-stack project. It contains the Django application, including core, todo, and users apps.

## Structure
- core: Django project settings and configuration
- todo: To-do app
- users: User management app

## Setup
1. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```
2. Activate the virtual environment:
   - Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```
3. Install dependencies:
   ```bash
   pip install -r requirement.txt
   ```
4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. Start the server:
   ```bash
   python manage.py runserver
   ```

## Development
- Use `.venv` for your virtual environment.
- `db.sqlite3` is the default database (ignored in .gitignore).
- Add new apps as needed.
