from flask import Flask, redirect, url_for, render_template, request, flash
import csv
import os
from your_auth_module import authenticate  # Import the authenticate function from your authentication module
from App.views.auth import auth_views  # Import the auth_views blueprint from auth.py
from App.models.routines import Routine

# Create a Flask app
app = Flask(__name__)

# Register the auth_views blueprint for authentication
app.register_blueprint(auth_views)

# Define the routines list
routines = []

# Define the CSV file path
csv_file_path = os.path.join(os.path.dirname(__file__), 'megaGymDataset.csv')

# Render the homepage template
@app.route('/homepage')
def homepage():
    return render_template('homepage.html')

# Route for the home page
@app.route('/')
def index():
    return redirect(url_for('homepage'))  # Redirect the root URL to the homepage

# Handle login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(f"Received username: {username}, password: {password}")  # Debugging print statement
        if authenticate(username, password):  # Call the authenticate function
            flash('Login successful!', 'success')
            return redirect(url_for('homepage'))  # Redirect to the homepage after successful login
        else:
            flash('Invalid username or password. Please try again.', 'error')
            print("Login failed.")  # Debugging print statement
    return render_template('login.html')

@app.route('/create_routine', methods=['GET', 'POST'])
def create_routine():
    if request.method == 'POST':
        # Parse form data
        name = request.form.get('name')
        exercise_type = request.form.get('exercise_type')
        muscle_group = request.form.get('muscle_group')
        difficulty_level = request.form.get('difficulty_level')

        # Basic validation
        if not name or not exercise_type or not muscle_group or not difficulty_level:
            flash('Please fill out all fields.', 'error')
        else:
            # Fetch exercises from the CSV file based on the selected muscle group and difficulty level
            exercises = get_exercises_from_csv(muscle_group, difficulty_level)

            # Store routine (mock)
            routine = {
                'name': name,
                'exercise_type': exercise_type,
                'muscle_group': muscle_group,
                'difficulty_level': difficulty_level,
                'exercises': exercises  # Add exercises to the routine
            }
            routines.append(routine)
            flash('Routine created successfully!', 'success')

    return render_template('create_routine.html', routines=routines)

@auth_views.route('/browse_routines', methods=['GET'])
def browse_routines():
    # Fetch routines from the database
    routines = Routine.query.all()

    # Render the template with the fetched routines
    return render_template('browse_routines.html', routines=routines)

def get_exercises_from_csv():
    exercises = []
    csv_file_path = os.path.join(os.path.dirname(__file__), 'megaGymDataset.csv')
    try:
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                exercise = {
                    'title': row['title'],
                    'desc': row['desc'],
                    'exercise_type': row['exercise_type'],
                    'body_part': row['body_part'],
                    'equipment': row['equipment'],
                    'level': row['level'],
                    'rating': row['rating'],
                    'rating_desc': row['rating_desc']
                }
                exercises.append(exercise)
    except FileNotFoundError:
        print(f"File '{csv_file_path}' not found.")
    except Exception as e:
        print(f"Error reading CSV file: {e}")
    return exercises

# Function to filter exercises based on body part and difficulty level
def filter_exercises(body_part, difficulty_level):
    filtered_exercises = []
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['BodyPart'].lower() == body_part.lower() and row['Level'].lower() == difficulty_level.lower():
                filtered_exercises.append(row)
    return filtered_exercises

# Route to handle the form submission
@app.route('/search', methods=['POST'])
def search():
    body_part = request.form.get('body_part')
    difficulty_level = request.form.get('difficulty_level')
    if body_part and difficulty_level:
        exercises = filter_exercises(body_part, difficulty_level)
        return render_template('results.html', exercises=exercises)
    else:
        flash('Please select both body part and difficulty level.', 'error')
        return redirect(url_for('create_routine'))

if __name__ == '__main__':
    app.secret_key = 'your_secret_key'
    app.run(debug=True)
