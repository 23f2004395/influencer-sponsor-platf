# importing Flask
import os
from flask import Flask
from backend.database import db

# current directory path
curr_dir = os.path.abspath(os.getcwd())
# initialising my_app to none
my_app = None


def init_app():
    """function to create an application instance"""
    # creating sponsorship platform my_app
    sponsor_app = Flask(__name__, template_folder='templates', static_folder='static')

    # connecting sponsor my_app to local directory's database
    sponsor_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(curr_dir + 'sponsors_app.db')
    sponsor_app.app_context().push()

    # connecting SQLAlchemy database with sponsor my_app's database
    db.init_app(sponsor_app)

    return sponsor_app


my_app = init_app()

# importing controllers from backend folder
from backend.controllers import *

# running the my_app
my_app.run(debug=True)