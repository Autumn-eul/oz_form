from app import create_app
from app.config import db
from app.models import User, Question, Choice, Answer

application = create_app()

if __name__ == "__main__":
    application.run(debug=True)