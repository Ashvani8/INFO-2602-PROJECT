import csv
import os
from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from App.models.routines import Routine   
from App.models.user import User   
from App.views.user import *
from App.controllers.auth import *
from App.database import db

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')

csv_file_path = os.path.join(os.path.dirname(__file__), 'megaGymDataset.csv')

def get_exercises_from_csv(body_part=None, difficulty_level=None):
    exercises = []
    try:
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if (body_part is None or row['BodyPart'].lower() == body_part.lower()) and \
                   (difficulty_level is None or row['Level'].lower() == difficulty_level.lower()):
                    exercises.append(row)
    except FileNotFoundError:
        print(f"File '{csv_file_path}' not found.")
    return exercises


'''
Page/Action Routes
'''    
@auth_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@auth_views.route('/identify', methods=['GET'])
@jwt_required()
def identify_page():
    return render_template('message.html', title="Identify", message=f"You are logged in as {current_user.id} - {current_user.username}")

@auth_views.route('/signup', methods=['GET'])
def signup_page():
    return render_template('signup.html', title="Sign Up") 

@auth_views.route('/homepage')
def homepage():
    return render_template('homepage.html', title="Home Page")

@auth_views.route('/login', methods=['POST'])
def login_action():
    data = request.form
    token = login(data['username'], data['password'])
    if not token:
        flash('Bad username or password given'), 401
        return redirect(url_for('auth_views.login_page'))  
    else:
        flash('Login Successful')
        response = redirect(url_for('auth_views.homepage'))  
        set_access_cookies(response, token)
        return response
    
@auth_views.route('/create_routine', methods=['GET', 'POST'])
@jwt_required()  # Protect this route with JWT authentication
def create_routine():
    if request.method == 'POST':
        # Parse form data
        title = request.form.get('title')
        desc = request.form.get('desc')
        exercise_type = request.form.get('exercise_type')
        body_part = request.form.get('body_part')
        equipment = request.form.get('equipment')
        level = request.form.get('level')
        rating = request.form.get('rating')
        rating_desc = request.form.get('rating_desc')

        # Basic validation
        if not title or not desc or not exercise_type or not body_part or not equipment or not level or not rating or not rating_desc:
            flash('Please fill out all fields.', 'error')
        else:
            flash('Routine created successfully!', 'success')

    return render_template('create_routine.html')

@auth_views.route('/browse_routines', methods=['GET'])
@jwt_required()
def browse_routines():
    try:
        # Fetch routines from the database
        routines = Routine.query.all()
        
        # Render the template with fetched routines
        return render_template('browse_routines.html', routines=routines)
    except Exception as e:
        # Handle any exceptions
        flash(f'Error fetching routines: {e}', 'error')
        return redirect(url_for('auth_views.homepage'))

@auth_views.route('/browse_workouts', methods=['GET'])
@jwt_required()  # Protect this route with JWT authentication
def browse_workouts():
    exercises = get_exercises_from_csv()
    return render_template('browse_workouts.html', exercises=exercises)
    
@auth_views.route('/logout', methods=['GET'])
def logout_action():
    response = redirect(request.referrer) 
    flash("Logged Out!")
    unset_jwt_cookies(response)
    return response

'''
API Routes
'''

@auth_views.route('/api/login', methods=['POST'])
def user_login_api():
  data = request.json
  token = login(data['username'], data['password'])
  if not token:
    return jsonify(message='bad username or password given'), 401
  response = jsonify(access_token=token) 
  set_access_cookies(response, token)
  return response

@auth_views.route('/api/identify', methods=['GET'])
@jwt_required()
def identify_user():
    return jsonify({'message': f"username: {current_user.username}, id : {current_user.id}"})

@auth_views.route('/api/logout', methods=['GET'])
def logout_api():
    response = jsonify(message="Logged Out!")
    unset_jwt_cookies(response)
    return response
