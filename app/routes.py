from flask import request, redirect, url_for, flash, render_template
from app.models import User
from app.utils import decrypt_password
from app import app

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get user input from the login form
        email = request.form.get('email')
        provided_password = request.form.get('password')
        
        # Fetch the user from MongoDB database
        patient = User.objects(email=email).first()

        if patient:
            stored_password = patient.password  # The encrypted password from the database
            
            # Correctly call decrypt_password with both arguments
            if decrypt_password(stored_password, provided_password):
                # Password matches, log the user in
                return redirect(url_for('dashboard'))  # Redirect to some dashboard or homepage
            else:
                flash('Invalid password, please try again.')
        else:
            flash('No account found with that email.')

    return render_template('login.html')  # Render the login form on GET request




# @app.route('/register', methods=['POST'])
# def register_user():
#     password = request.form['password']
    
#     # Encrypt the password
#     encrypted_password = encrypt_password(password)
    
#     # Save the encrypted password to the database
#     # save_to_database(username, encrypted_password)
    
#     return "User registered!"

