"""Interactive recovery using the configured database. Requires access to the deployment environment."""
from getpass import getpass
from werkzeug.security import generate_password_hash
from app import app
from models import db, Admin

with app.app_context():
    admin = Admin.query.first()
    if not admin:
        raise SystemExit('No admin exists. Configure ADMIN_PASSWORD and start the app first.')
    username = input('New admin username (3+ characters): ').strip()
    if len(username) < 3 or not all(c.isalnum() or c in '_.-' for c in username):
        raise SystemExit('Invalid username')
    password = getpass('New password (12+ characters): ')
    if len(password) < 12:
        raise SystemExit('Password too short')
    admin.username = username
    admin.password_hash = generate_password_hash(password)
    db.session.commit()
    print('Admin credentials updated.')
