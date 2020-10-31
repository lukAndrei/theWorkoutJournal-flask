from application.models import User, Workout, Exercise, Set
from flask import render_template, url_for, flash, redirect, request, jsonify
from application.forms import RegistrationForm, LoginForm, UpdateAccount, WorkoutForm
from application import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import secrets, os
from PIL import Image

@app.route('/')
@app.route('/home')
def home():
    users = User.query.all()
    workouts = Workout.query.all()
    return render_template('home.html', users=users, workouts=workouts)
@app.route('/api/workouts',methods=['GET', 'POST'])
def api_workouts():
    users = User.query.all()
    workouts = Workout.query.all()
    workouts_serial = []
    for workout in workouts:
        workouts_serial.append(workout.serialize())
    return jsonify({"workouts": workouts_serial})
    
@app.route('/create-workout',methods=['GET', 'POST'])
def create_workout():
    form = WorkoutForm()
    if form.validate_on_submit():
        workout = Workout(name = form.name.data,  date = form.date.data, author=current_user)
        db.session.add(workout)
        db.session.commit()
        flash('Workout has been created','success')
        return redirect(url_for('home'))
    return render_template('create-workout.html',form=form)
@app.route('/api/add-workout', methods=['POST'])
def add_workout():
    name = request.json['name']
    date = request.json['date']
    user = request.json['user_id']

    new_workout = Workout(name=name,date=date,author=current_user)

    db.session.add(new_workout)
    db.session.commit()

    return workout_schema.jsonify(new_workout)

@app.route("/create-workout/<int:workout_id>",methods=['GET', 'POST'])
def workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    return render_template('workout.html',workout=workout)
@app.route('/api/workout/<int:workout_id>',methods=['GET', 'POST'])
def api_workout_id(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    workout_JSON = workout.serialize()
    return jsonify(workout_JSON)


@app.route("/update-workout/<int:workout_id>",methods=['GET', 'POST'])
@login_required
def update_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    if workout.author != current_user:
        abort(403)
    form = WorkoutForm()
    if form.validate_on_submit():
        workout.name = form.name.data
        db.session.commit()
        flash('Workout has been updated','success')
        return redirect(url_for('workout', workout_id = workout.id))
    elif request.method == "GET":
        form.name.data = workout.name
    return render_template('create-workout.html', form=form)

@app.route("/delete-workout/<int:workout_id>",methods=['POST'])
@login_required
def delete_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    if workout.author != current_user:
        abort(403)
    db.session.delete(workout)
    db.session.commit()
    flash('Your post has been deleted','success')
    return redirect(url_for('home'))

@app.route('/user-workouts')
@login_required
def user_workouts():
    return render_template('user-workouts.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created','success')
        return redirect(url_for('home'))
    return render_template('register.html',title="Register", form=form);

@app.route('/login',methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            flash('Logged in', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccesfull, please check email and password', 'danger')
    return render_template('login.html',title="Login", form=form);

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn=random_hex+f_ext
    picture_path = os.path.join(app.root_path,'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route('/user-account', methods=["GET", "POST"])
def account():
    form = UpdateAccount()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.profile_pic = picture_file

        db.session.commit()
        flash("Your account has been updated",'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/'+current_user.profile_pic)
    return render_template('user-account.html', image_file = image_file,form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
