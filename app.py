from flask_babel import Babel
import requests
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import CSRFProtect
from wtforms import StringField, PasswordField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email
import json

app = Flask(__name__)
# Set the secret key for your Flask app (required for CSRF and session management)
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Enable CSRF protection for all forms in the app
csrf = CSRFProtect(app)
babel = Babel(app)

# Define the languages you want to support
LANGUAGES = ['en', 'fr']
app.config['LANGUAGES'] = LANGUAGES
csrf = CSRFProtect(app)

# @babel.localeselector
# def get_locale():
#     # Use language from session, or default to 'en'
#     return session.get('language', 'en')

# --------------------------------------------------------------------------------

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User model

class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    profile_picture = db.Column(db.String(255), nullable=True)  # Path to the profile picture
    telephone = db.Column(db.String(15), nullable=False)
    location = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    user = db.relationship('User', backref=db.backref('profile', uselist=False, lazy=True))

    def __repr__(self):
        return f'<UserProfile user_id={self.user_id}>'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

# Create the database
with app.app_context():
    db.create_all()

# --------------------------------------------------------------------------------
  
@app.route('/')
def indi():
    if 'username' in session:
        # Pass the username to the welcome.html template
        return render_template('welcome.html', username=session['username'])
    else:
        # Render the welcome.html template without user details
        return render_template('welcome.html', username=None)

# --------------------------------------------------------------------------------
# registration route

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()  # Use the form for validation
    if form.validate_on_submit():  # Check if form submission is valid (with CSRF protection)
        username = form.username.data
        email = form.email.data
        password = form.password.data
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Check if the user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose another one.', 'error')
            return redirect(url_for('register'))

        # Create and save the new user
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    # If GET request or form validation fails
    return render_template('register.html', form=form)


# --------------------------------------------------------------------------------
# Login route

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():  # Check if the form is submitted and valid
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['username'] = user.username
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password. Please try again.', 'error')

    return render_template('login.html', form=form)

# --------------------------------------------------------------------------------
# Logout route

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('indi'))


# ----------------------------------------------------------------------------------


@app.route('/crop_recommendations')
def crop_recommendations():
    # Define hardcoded data for cities and their best crops to grow
    crop_recommendations = [
        {'city': 'City1', 'best_crop': 'Wheat'},
        {'city': 'City2', 'best_crop': 'Rice'},
        {'city': 'City3', 'best_crop': 'Corn'},
        # Add more data as needed
    ]
    return render_template('crop_recommendations.html', crop_recommendations=crop_recommendations)

# ---------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------

@app.route('/soil_profile')
def soil_profile():
    return render_template('soil_profile.html')

# ---------------------------------------------------------------------------------------

@app.route('/my_Profile')
def my_Profile():
    if 'username' in session:
        username = session['username']
        # Retrieve user information from the database
        user = User.query.filter_by(username=username).first()
        if user:
            return render_template('my_Profile.html', user=user)
    flash('Please log in to view your profile.', 'error')
    return redirect(url_for('login'))


@app.route('/update_profile', methods=['POST'])
def update_profile():
    if 'username' in session:
        username = session['username']
        
        # Handle file upload
        profile_picture = request.files['profile_picture']
        if profile_picture:
            profile_picture.save(f'static/uploads/{profile_picture.filename}')  # Save the file to the uploads folder

        telephone = request.form['telephone']
        email = request.form['email']
        location = request.form['location']

        # Update the user's profile in the database
        user = User.query.filter_by(username=username).first()
        user.telephone = telephone
        user.email = email
        user.location = location
        user.profile_picture = profile_picture.filename if profile_picture else user.profile_picture
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('my_Profile'))

    flash('Please log in to update your profile.', 'error')
    return redirect(url_for('login'))

# ---------------------------------------------------------------------------------------

@csrf.exempt
  
@app.route('/show_weather')
def show_weather():
    # Add the logic to display weather information
    return render_template('indi.html')
# ---------------------------------------------------------------------------------------


# @app.route('/soil_profile')
# def soil_profile():
#     # Add the logic to display soil profile information
#     return render_template('soil_profile.html')
# ---------------------------------------------------------------------------------------


@app.route('/government_schemes')
def government_schemes():
    return render_template('government_schemes.html')
  
# -------------------------------------------------------------------------------------

@app.route('/set_language', methods=['GET'])
def set_language():
    language = request.args.get('language', 'en')
    session['language'] = language  # Store the selected language in the session
    return jsonify({'status': 'success', 'language': language})
# ---------------------------------------------------------------------------------------
@csrf.exempt

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form['city']
        current_weather, forecast_weather, error_message = get_weather_data(city)
        return render_template('indi.html', current_weather=current_weather, forecast_weather=forecast_weather, error_message=error_message)

    return render_template('indi.html', current_weather=None, forecast_weather=None, error_message=None)
# ---------------------------------------------------------------------------------------
# Notification route
@csrf.exempt
def reverse_geocode(lat, lon):
    api_key = '750ab95c3ef50eac94338c123603f273'
    geocode_url = f'http://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={lon}&limit=1&appid={api_key}'
    
    response = requests.get(geocode_url)
    data = response.json()

    if response.status_code == 200 and data:
        return data[0]['name']  # Extract city name
    else:
        return None
@csrf.exempt
# Route to receive user coordinates and set the city in session
@app.route('/update_user_location', methods=['POST'])
def update_user_location():
    if 'username' in session:
        data = request.json
        lat = data.get('latitude')
        lon = data.get('longitude')

        city = reverse_geocode(lat, lon)
        if city:
            session['user_city'] = city
            return jsonify({'success': True, 'city': city})
        else:
            return jsonify({'success': False, 'error': 'Failed to get city from coordinates'}), 500
    return jsonify({'success': False, 'error': 'User not logged in'}), 401

# Modify the weather notifications route to use the city in session
@csrf.exempt
@app.route('/get_weather_notifications')
def get_weather_notifications():
    if 'username' in session:
        city = session.get('user_city', 'indore')  # Use city from session or default city
        current_weather, _, error = get_weather_data(city)

        if error:
            return jsonify({
                'has_new_update': False,
                'notification_message': 'Failed to fetch weather data.',
                'current_weather':'Weather data unavailable'
            })

        # Check for weather conditions to generate an alert
        if current_weather:
            if current_weather['temperature'] < 10:
                return jsonify({
                    'has_new_update': True,
                    'notification_message': f"Weather Alert: It's cold in {current_weather['city']}! Current temp: {current_weather['temperature']}°C"
                })
            elif 'rain' in current_weather['description'].lower():
                return jsonify({
                    'has_new_update': True,
                    'notification_message': f"Weather Alert: It's raining in {current_weather['city']}!"
                })
            else:
                # No alerts but show the current weather
                return jsonify({
                    'has_new_update': False,
                    'notification_message': f"The current weather in {current_weather['city']} is {current_weather['temperature']}°C with {current_weather['description']}."
                })

        return jsonify({
            'has_new_update': False,
            'notification_message': 'No weather data available.'
        })
    return jsonify({
        'has_new_update': False,
        'notification_message': 'Please log in to receive notifications.'
    })

# ------------------------------------------------------------------------------------------
@csrf.exempt
def get_weather_data(city):
    api_key = '750ab95c3ef50eac94338c123603f273'
    current_url = 'http://api.openweathermap.org/data/2.5/weather'
    forecast_url = 'http://api.openweathermap.org/data/2.5/forecast'
    
    # Current weather data
    current_params = {'q': city, 'appid': api_key, 'units': 'metric'}
    current_response = requests.get(current_url, params=current_params)
    current_data = current_response.json()

    # Forecast data
    forecast_params = {'q': city, 'appid': api_key, 'units': 'metric'}
    forecast_response = requests.get(forecast_url, params=forecast_params)
    forecast_data = forecast_response.json()

    if current_response.status_code == 200 and forecast_response.status_code == 200:
        current_weather_info = {
            'city': current_data['name'],
            'temperature': current_data['main']['temp'],
            'description': current_data['weather'][0]['description'],
            'icon': current_data['weather'][0]['icon'],
        }

        forecast_weather_info = []
        for forecast in forecast_data['list']:
            forecast_info = {
                'datetime': forecast['dt_txt'],
                'temperature': forecast['main']['temp'],
                'description': forecast['weather'][0]['description'],
                'icon': forecast['weather'][0]['icon'],
            }
            forecast_weather_info.append(forecast_info)

        return current_weather_info, forecast_weather_info, None  # No error

    # Handle errors
    error_message = f"Error: {current_response.status_code} - {current_data.get('message', 'Unknown error')}"
    return None, None, error_message

if __name__ == '__main__':
    # app.secret_key = 'your_secret_key'  # Set a secret key for session management
    

    app.run(debug=True) 


  