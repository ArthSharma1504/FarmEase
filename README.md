# Farmer Profile Management System

## Description
This project is a web application that allows farmers to manage their profiles, including updating personal information, uploading profile pictures, and maintaining contact details. It is built using Flask as the backend framework and a SQLite database for storage.

## Features
- User registration and authentication
- Profile management for updating personal information
- File upload for profile pictures
- Responsive design for mobile and desktop

## Technologies Used
- Python
- Flask
- SQLAlchemy
- SQLite
- HTML/CSS
- JavaScript

## Prerequisites
Make sure you have the following installed on your system:
- Python 3.x
- pip (Python package installer)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/arthsharma1504/farmer-profile-management.git
2. **Navigate to the project directory:**
   cd farmer-profile-management
   
3. Install the required packages:
   pip install -r requirements.txt

4. Set up the database
   flask db init
   flask db migrate -m "Initial migration."
   flask db upgrade

5. Create a .env file (optional): If you're using environment variables for sensitive information (like database URIs or secret keys), create a .env file in the root directory and add your configurations.

## To run the Application

To set the Flask environment variable, use export FLASK_APP=app.py and export FLASK_ENV=development for development mode on Unix-based systems. For Windows, use set FLASK_APP=app.py and set FLASK_ENV=development. To run the application, execute the command flask run, and then access the application by opening your web browser and navigating to http://127.0.0.1:5000/.

## Usage

Register a new account: Navigate to the registration page and fill out the form.
Login: Use your credentials to log in.
Manage your profile: After logging in, you can view and edit your profile information and upload a profile picture.

## Folder Structure

farmer-profile-management/
│
├── app.py                 # Main application file
├── models.py              # Database models
├── forms.py               # Forms for user input
├── static/                # Static files (CSS, JS, images)
│   └── uploads/           # Uploaded profile pictures
├── templates/             # HTML templates
│   ├── my_Profile.html    # Profile management page
│   └── other templates...
├── requirements.txt       # Python packages required for the project
└── .env                   # Environment variables (if used)

Contributing
If you would like to contribute to this project, please fork the repository and submit a pull request.
