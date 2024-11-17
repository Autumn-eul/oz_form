from app import create_app
from config import db
from app.models import User, Question, Choice, Answer
from app.routes import survey

application = create_app()

if __name__ == "__main__":
    application.run(debug=True)