from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    users = User.query.all()
    for user in users:
        user.set_password('password')
    db.session.commit()
    print("All passwords reset to 'password'")
