from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_datepicker import datepicker
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SECRET_KEY'] = '2ef194df1753af854e63dce644a11b47';
app.config['SQLALCHEMY_DATABASE_URI']="postgresql://luka:pierrebezuhov@localhost:5432/theworkoutjournal"

Bootstrap(app)
datepicker(app)
db=SQLAlchemy(app)
ma = Marshmallow(app)


bcrypt  = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='info'

from application.models import WorkoutSchema
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
from application import routes
