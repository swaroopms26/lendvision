from dotenv import load_dotenv
load_dotenv()

from app import create_app, db
from app.models import User, LoanApplication

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'LoanApplication': LoanApplication}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, use_reloader=False, port=5001)
