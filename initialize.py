from models import UserProfile, db
from datetime import datetime
from werkzeug.security import generate_password_hash
import uuid
from app import app

with app.app_context():
    db.create_all()

    print('database dibuat')
    hashed_password = generate_password_hash('admin', method='sha256')

    new_user = UserProfile(publik_id=str(uuid.uuid4()), username='admin', password=hashed_password, active=True)
    db.session.add(new_user)
    db.session.commit()