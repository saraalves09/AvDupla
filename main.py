"""
pip install..
flask
flask_login
flask_wtf
email_validator
flask_bcrypt
flask_sqlalchemy

"""
from instagram import app
from instagram import database, app
from instagram.models import User, Posts, Like, Comment

with app.app_context():
    database.create_all()

if __name__ == '__main__':
    app.run(debug=True)


