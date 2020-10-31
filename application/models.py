
from application import db, login_manager, ma
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    profile_pic = db.Column(db.String(120), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    workouts = db.relationship('Workout',backref='author', lazy=True)


    def __repr__(self):
        return f"User('{self.username}','{self.email}', '{self.profile_pic}')"

class Workout(db.Model):
    __tablename__='workouts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True, default="")
    date = db.Column(db.DateTime, nullable=False, default  = datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "date": self.date,
            "user_id": self.user_id
        }
    def __repr__(self):
        return f"Workout('{self.name}','{self.id}', '{self.date}')"

class WorkoutSchema(ma.Schema):
    class Meta:
        fields=('id', 'name', 'date', 'user_id')

class Exercise(db.Model):
    __tablename__="exercises"
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(2), nullable=False)
    workout_id = db.Column(db.Integer,db.ForeignKey("workouts.id"), nullable=False)

    def __repr__(self):
        return f"Exercise('{self.name}','{self.sets}')"

class Set(db.Model):
    __tablename__="sets"
    id=db.Column(db.Integer,primary_key=True)
    set_number = db.Column(db.Integer, nullable=False, default=1)
    set_reps = db.Column(db.Integer, nullable=False, default=1)
    exercise_id = db.Column(db.Integer,db.ForeignKey('exercises.id'), nullable=False)

    def __repr__(self):
        return f"Set '{ set_number }', reps '{ set.reps }'"
