from flask import Flask, render_template,jsonify, request, redirect, url_for, flash, session
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from app.utils import encrypt_data, decrypt_data,encrypt_password,decrypt_password
import json
import bcrypt
import os
from collections import Counter
from bson.objectid import ObjectId
from datetime import datetime
from functools import wraps
import logging
import socket 
import bcrypt
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

YOUR_ENCRYPTION_KEY = os.urandom(16)  # Ensure this key is stored securely in production



PATIENT_DATA_FILE = 'patients.json'
DOCTOR_DATA_FILE = 'doctors.json'

#start of updated code

app.secret_key = 'supersecretkey'  # This is for Flask session security, not for encryption

# Load the encryption key from the 'secret.key' file
key_path = "secret.key"

# Ensure the file exists before loading
if not os.path.exists(key_path):
    raise ValueError(f"The key file '{key_path}' is missing. Please provide the 'secret.key' file.")

# Read the key from the 'secret.key' file
with open(key_path, "rb") as key_file:
    key = key_file.read()

# Initialize the Fernet cipher with the constant key


# Rest of your app code here...




# MongoDB configuration
MONGODB_URI = "mongodb+srv://healthsphere:Office9087@cluster0.lvgai.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"  # Replace with your MongoDB URI
client = MongoClient(MONGODB_URI)
db = client['Healthsphere']  # Replace with your database name
patients_collection = db['patients']  # Collection for storing patients
doctors_collection = db['doctors']
doctor_info_collection = db['doctor_info']
appointment_collection=db['appointments']
past_appointment_collection=db['past_appointment']
test_bills_collection = db['test_bills_collection']
authorize_collection=db['Authorized_person']
cancer_patients = db['cancer_patients']
dermatology_patients = db['dermatology_patients']
cardiology_patients = db['cardiology_patients']
general_patients = db['general_patients']

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def load_patients():
    if os.path.exists(PATIENT_DATA_FILE):
        with open(PATIENT_DATA_FILE, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    return {}

def save_patients(patients):
    with open(PATIENT_DATA_FILE, 'w') as file:
        json.dump(patients, file, indent=4)

def load_doctors():
    if os.path.exists(DOCTOR_DATA_FILE):
        with open(DOCTOR_DATA_FILE, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    return {}

def save_doctors(doctors):
    with open(DOCTOR_DATA_FILE, 'w') as file:
        json.dump(doctors, file, indent=4)

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/home')
def home():
    return render_template('home.html')

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        
        # Check if email already exists in the database
        if patients_collection.find_one({"email": email}):
            flash('Email already registered!')
            return redirect(url_for('register'))
        
        # Insert email into the collection
        patients_collection.insert_one({'email': email})
        
        # Set session after registration
        session['patient'] = email
        flash('Registration successful! Please fill out your information.')
        
        # Redirect to the patient information page
        return redirect(url_for('patient_info'))
    
    # Render the registration template
    return render_template('register.html')




# ... (rest of your existing code remains unchanged)


# new code for patient_info
@app.route('/submitPatientData', methods=['POST'])
def submit_patient_data():
    name = encrypt_data(request.form['name'], key)
    age = encrypt_data(request.form['age'], key)
    gender = encrypt_data(request.form['gender'], key)
    dob = encrypt_data(request.form['dob'], key)
    contact = encrypt_data(request.form['contact'], key)
    aadhar = encrypt_data(request.form['aadhar'], key)
    disease = encrypt_data(request.form['disease'], key)
    address = encrypt_data(request.form['address'], key)
    email = session.get('patient')
    if not email:
        return jsonify({'error': 'User not logged in!'}), 401
    
    patient_data = {
        'name': name,
        'age': age,
        'gender': gender,
        'dob': dob,
        'contact': contact,
        'aadhar': aadhar,
        'disease': disease,
        'address': address,
        'email': email
    }
    try:
        result = patients_collection.update_one({'email': email}, {'$set': patient_data}, upsert=True)
        print(f'MongoDB update result: {result.raw_result}')
        return jsonify({'status': 'success', 'message': 'Patient data submitted successfully!'})
    except Exception as e:
        print(f'Error saving data: {str(e)}')
        return jsonify({'error': str(e)}), 500






@app.route('/patient-info', methods=['GET', 'POST'])
def patient_info():
    if request.method == 'POST':
        name = encrypt_data(request.form['name'], key)
        age = encrypt_data(request.form['age'], key)
        gender = encrypt_data(request.form['gender'], key)
        dob = encrypt_data(request.form['dob'], key)
        contact = encrypt_data(request.form['contact'], key)
        aadhar = encrypt_data(request.form['aadhar'], key)
        disease = encrypt_data(request.form['disease'], key)
        address = encrypt_data(request.form['address'], key)
        email = session.get('patient')
        
        if not email:
            flash('You must be logged in to submit patient information.')
            return redirect(url_for('login'))
        
        patient_data = {
            'name': name,
            'age': age,
            'gender': gender,
            'dob': dob,
            'contact': contact,
            'aadhar': aadhar,
            'address': address,
            'email': email
        }
        
        if disease == 'Cancer':
            cancer_patients.update_one({'email': email}, {'$set': patient_data}, upsert=True)
        elif disease == 'Dermatology':
            dermatology_patients.update_one({'email': email}, {'$set': patient_data}, upsert=True)
        elif disease == 'Cardiology':
            cardiology_patients.update_one({'email': email}, {'$set': patient_data}, upsert=True)
        else:
            general_patients.update_one({'email': email}, {'$set': patient_data}, upsert=True)
        
        flash('Patient information submitted successfully!')
        return redirect(url_for('home'))
    
    return render_template('patient_info.html')


#PAU
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'doctor' not in session:
            flash('You need to be logged in as a doctor to view this page.', 'danger')
            return redirect(url_for('doctor_login'))  # Redirect to login page if not logged in
        return f(*args, **kwargs)
    return decorated_function

@app.route('/view_patients', methods=['GET'])
@login_required  # Ensure doctor is logged in
def view_patients():
    try:
        # Fetch all patients from MongoDB
        patients = patients_collection.find()

        # Decrypt patient data
        decrypted_patients = []
        for patient in patients:
            try:
                decrypted_patient = {
                    'email': patient.get('email', 'N/A'),
                    'name': decrypt_data(patient.get('name', ''), key),
                    'age': decrypt_data(patient.get('age', ''), key),
                    'gender': decrypt_data(patient.get('gender', ''), key),
                    'dob': decrypt_data(patient.get('dob', ''), key),  # Decrypt date of birth
                    'contact': decrypt_data(patient.get('contact', ''), key),  # Decrypt contact number
                    'aadhar': decrypt_data(patient.get('aadhar', ''), key),  # Decrypt Aadhar number
                    'disease': decrypt_data(patient.get('disease', ''), key),
                    'address': decrypt_data(patient.get('address', ''), key)
                }
                decrypted_patients.append(decrypted_patient)
            except Exception as decrypt_error:
                print(f"Decryption error for patient {patient.get('email')}: {decrypt_error}")
                continue  # Skip patient if decryption fails

        # Render the view_patients page with the decrypted patient data
        return render_template('view_patients.html', doctor=session['doctor'], patients=decrypted_patients)

    except Exception as e:
        print(f"Error fetching patient data: {str(e)}")
        flash('Error fetching patient data!', 'danger')
        return redirect(url_for('doctor_home'))


@app.route('/authenticate-user', methods=['GET', 'POST'])
def authenticate_user():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']

        # Find the doctor in MongoDB by name
        doctor = doctors_collection.find_one({'name': name})

        if doctor and decrypt_password(doctor['password'], password):
            session['doctor'] = name  # Store the doctor in the session
            
            # Redirect to the view_patients page after successful login
            return redirect(url_for('view_patients'))
        else:
            flash('Invalid name or password!', 'danger')
            return redirect(url_for('authenticate_user'))

    return render_template('authenticate_user.html')  # Correct template name

#schedule_appointment


def index():
    return render_template('index.html')  # Or your main page

@app.route('/schedule_appointment')
def schedule_appointment():
    return render_template('schedule_appointment.html')

@app.route('/api/doctors', methods=['GET'])
def get_doctors():
    disease = request.args.get('disease')
    
    if disease:
        # Find doctors based on disease (specialty)
        doctors = doctor_info_collection.find({"specialty": disease})
        doctor_list = [{"name": doctor['name']} for doctor in doctors]
        return jsonify(doctor_list)
    return jsonify([])

@app.route('/api/appointments', methods=['POST'])
def book_appointment():
    data = request.get_json()
    doctor = data['doctor']
    start_time = data['startTime']
    end_time = data['endTime']

    # Check for existing appointments with overlapping time slots
    conflict = appointment_collection.find_one({
        "doctor": doctor,
        "$or": [
            {"startTime": {"$lt": end_time, "$gt": start_time}},
            {"endTime": {"$gt": start_time, "$lt": end_time}},
            {"startTime": {"$lte": start_time}, "endTime": {"$gte": end_time}}
        ]
    })
    
    if conflict:
        return jsonify({"success": False, "message": "This time slot is already booked with Dr. " + doctor}), 400
    
    # If no conflict, save the new appointment
    try:
        appointment_collection.insert_one(data)
        return jsonify({"success": True, "message": "Appointment booked successfully!"}), 200
    except Exception as e:
        logging.debug(f"Error booking appointment: {str(e)}")
        return jsonify({"success": False, "message": "Error booking appointment"}), 500


#adding doctor_info


# @app.route('/add_doctor', methods=['GET', 'POST'])
# def add_doctor():
#     if request.method == 'POST':
#         name = request.form['name']
#         specialty = request.form['specialty']
#         email = request.form['email']

#         # Insert the doctor data into MongoDB
#         doctor_info_collection.insert_one({
#             'name': name,
#             'specialty': specialty,
#             'email': email
#         })
#         return redirect(url_for('add_doctor'))

#     return render_template('add_doctor.html')

#end doctor_info







#end schedule_appointment


#start fetch data from doctor_info
@app.route('/doctor_profiles')
def doctor_profiles():
    try:
        # Fetch all doctors from the collection
        doctors = list(doctor_info_collection.find({}))

        # Convert ObjectId to string for each doctor (if needed)
        for doctor in doctors:
            doctor['_id'] = str(doctor['_id'])
        
        return render_template('doctor_profiles.html', doctors=doctors)
    except Exception as e:
        print(f"Error fetching doctor profiles: {str(e)}")
        flash('An error occurred while fetching doctor profiles.', 'danger')
        return redirect(url_for('patient_dashboard'))



#end fetch data from doctor_info

#schedule management 

@app.route('/schedule_management', methods=['GET', 'POST'])
def schedule_management():
    appointments = []
    if request.method == 'POST':
        email = request.form.get('email')
        if email:
            # Fetch appointments for the given doctor email
            appointments = list(appointment_collection.find({'email': email}))
            for appointment in appointments:
                appointment['_id'] = str(appointment['_id'])  # Convert ObjectId to string for rendering

    return render_template('schedule_management.html', appointments=appointments)

@app.route('/update_schedule/<appointment_id>', methods=['POST'])
def update_schedule(appointment_id):
    try:
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')

        # Update the appointment in the database
        appointment_collection.update_one(
            {'_id': ObjectId(appointment_id)},
            {'$set': {'startTime': start_time, 'endTime': end_time}}
        )

        flash('Appointment updated successfully!', 'success')
    except Exception as e:
        print(f"Error updating appointment: {str(e)}")
        flash('An error occurred while updating the appointment.', 'danger')

    return redirect(url_for('schedule_management'))


#schedule_management

#analystic management

@app.route('/analytics', methods=['GET'])
def analytics():
    # Fetch and decrypt patient data
    patients = patients_collection.find()
    decrypted_patients = []
    for patient in patients:
        decrypted_patients.append({
            'age': int(decrypt_data(patient['age'], key)),
            'gender': decrypt_data(patient['gender'], key),
            'disease': decrypt_data(patient['disease'], key)
        })

    # Calculate total patients, age distribution, and gender distribution
    total_patients = len(decrypted_patients)
    age_distribution = Counter([patient['age'] for patient in decrypted_patients])
    gender_distribution = Counter([patient['gender'] for patient in decrypted_patients])

    # Fetch past appointment data (no decryption needed)
    past_appointments = past_appointment_collection.find()
    plain_past_appointments = []
    for appointment in past_appointments:
        plain_past_appointments.append({
            'email': appointment['email'],
            'doctor': appointment['doctor'],
            'disease': appointment['disease'],
            'startTime': appointment['startTime'],
            'endTime': appointment['endTime']
        })

    # Fetch current appointment data (no decryption needed)
    current_appointments = appointment_collection.find()
    plain_current_appointments = []
    for appointment in current_appointments:
        plain_current_appointments.append({
            'email': appointment['email'],
            'doctor': appointment['doctor'],
            'disease': appointment['disease'],
            'startTime': appointment['startTime'],
            'endTime': appointment['endTime']
        })

    # Trends for appointments
    appointment_trends = {
        'total_appointments': len(plain_current_appointments),
        'total_past_appointments': len(plain_past_appointments)
    }

    # Disease trends
    disease_trends_past = Counter([appointment['disease'] for appointment in plain_past_appointments])
    disease_trends_current = Counter([appointment['disease'] for appointment in plain_current_appointments])

    # Doctor appointment load
    doctor_appointments_past = Counter([appointment['doctor'] for appointment in plain_past_appointments])
    doctor_appointments_current = Counter([appointment['doctor'] for appointment in plain_current_appointments])

    # Pass the data to the analytics.html template
    return render_template(
        'analytics.html',
        patient_demographics={
            'total_patients': total_patients,
            'age_distribution': dict(age_distribution),
            'gender_distribution': dict(gender_distribution)
        },
        appointment_trends=appointment_trends,
        disease_trends_past=dict(disease_trends_past),
        disease_trends_current=dict(disease_trends_current),
        doctor_appointments_past=dict(doctor_appointments_past),
        doctor_appointments_current=dict(doctor_appointments_current)
    )


#end analystic management


#testing billing

@app.route('/check_email', methods=['POST'])
def check_email():
    email = request.form.get('email')
    if email:
        # Search for the email in the patients collection
        patient = patients_collection.find_one({'email': email})
        if patient:
            return jsonify({"found": True})
        else:
            return jsonify({"found": False})
    return jsonify({"found": False})

@app.route('/enter_test_details', methods=['GET', 'POST'])
def enter_test_details():
    if request.method == 'POST':
        email = request.form.get('email')
        test_name = request.form.get('test_name')
        amount = request.form.get('amount')
        timing = request.form.get('timing')
        test_date = request.form.get('test_date')

        if not email:
            return jsonify({"message": "Email is required"}), 400

        # Check if patient exists in the database by email
        patient = patients_collection.find_one({'email': email})
        if patient:
            # Save test details to the test_bills_collection
            test_bills_collection.insert_one({
                'email': email,
                'test_name': test_name,
                'amount': amount,
                'timing': timing,
                'test_date': test_date
            })

            # After successful insertion, reload the page with a success message
            return render_template('enter_test_details.html', success_message="Amount added successfully!")
        else:
            return jsonify({"message": "Patient email not found."}), 404

    # If the method is GET, just render the page
    return render_template('enter_test_details.html')


#end testing billing

#invoice management

@app.route('/validate_email', methods=['GET', 'POST'])
def validate_email():
    if request.method == 'POST':
        email = request.form['email']
        records = list(test_bills_collection.find({"email": email}))
        
        if records:
            return render_template('validate_email.html', email=email, records=records)
        else:
            error = "No records found for this email."
            return render_template('validate_email.html', error=error)

    return render_template('validate_email.html')

@app.route('/mark_paid/<record_id>', methods=['POST'])
def mark_paid(record_id):
    # Update the specific test record's payment status
    result = test_bills_collection.update_one({"_id": ObjectId(record_id)}, {"$set": {"paid_status": "Paid"}})

    if result.modified_count > 0:
        flash("Test marked as paid successfully.")
    else:
        flash("Failed to mark test as paid.")

    # Redirect back to the email validation page
    email = request.form['email']
    records = list(test_bills_collection.find({"email": email}))
    return render_template('validate_email.html', email=email, records=records)

@app.route('/print_invoice/<email>', methods=['GET'])
def print_invoice(email):
    # Fetch only the paid records for the invoice
    paid_records = list(test_bills_collection.find({"email": email, "paid_status": "Paid"}))
    
    if paid_records:
        total_amount = sum(float(record['amount']) for record in paid_records)
        return render_template('invoice.html', email=email, records=paid_records, total_amount=total_amount)
    else:
        flash("No paid records found for this email.")
        return redirect(url_for('validate_email'))


#end invoice management


#innovation_solution
@app.route('/innovative_solutions')
def innovative_solutions():
    # Render the 'innovative_solutions.html' template when the route is accessed
    return render_template('innovative_solutions.html')



#end_innovation solution


#PAU
# new code for login of patient

@app.route('/login', methods=['GET'])
def login_page():
    doctor_name = session.get('doctor')  # Get the doctor's name from session
    return render_template('login.html', doctor_name=doctor_name)


# @app.route('/login', methods=['GET'])
# def login_page():
#     return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        patient = patients_collection.find_one({'email': email})

        if patient:
            try:
                # Decrypt patient details (same as before)
                encrypted_name = patient.get('name', '')
                decrypted_name = decrypt_data(encrypted_name, key)

                encrypted_age = patient.get('age', '')
                decrypted_age = decrypt_data(encrypted_age, key)

                encrypted_gender = patient.get('gender', '')
                decrypted_gender = decrypt_data(encrypted_gender, key)

                encrypted_dob = patient.get('dob', '')
                decrypted_dob = decrypt_data(encrypted_dob, key)

                encrypted_contact = patient.get('contact', '')
                decrypted_contact = decrypt_data(encrypted_contact, key)

                encrypted_aadhar = patient.get('aadhar', '')
                decrypted_aadhar = decrypt_data(encrypted_aadhar, key)

                encrypted_disease = patient.get('disease', '')
                decrypted_disease = decrypt_data(encrypted_disease, key)

                encrypted_address = patient.get('address', '')
                decrypted_address = decrypt_data(encrypted_address, key)

                # Store decrypted patient details in session
                patient_details = {
                    'email': email,
                    'name': decrypted_name,
                    'age': decrypted_age,
                    'gender': decrypted_gender,
                    'dob': decrypted_dob,
                    'contact': decrypted_contact,
                    'aadhar': decrypted_aadhar,
                    'disease': decrypted_disease,
                    'address': decrypted_address
                }
                session['patient'] = patient_details

                # Fetch appointments for the patient and convert ObjectId to string
                appointments = list(appointment_collection.find({'email': email}))
                for appointment in appointments:
                    appointment['_id'] = str(appointment['_id'])  # Convert ObjectId to string

                session['appointments'] = appointments  # Store appointments in session

                return redirect(url_for('patient_dashboard'))

            except Exception as e:
                print(f"Decryption error: {str(e)}")
                flash('Data integrity check failed!', 'danger')
                return redirect(url_for('login'))
        else:
            flash('Invalid email!', 'danger')

    return render_template('login.html')




@app.route('/patient_dashboard')
def patient_dashboard():
    patient = session.get('patient')
    if not patient:
        flash('Please log in first.', 'danger')
        return redirect(url_for('login'))

    email = patient.get('email')

    # Fetch active appointments
    active_appointments = list(appointment_collection.find({'email': email}))
    for appointment in active_appointments:
        appointment['_id'] = str(appointment['_id'])  # Convert ObjectId to string

    # Fetch past appointments
    past_appointments = list(past_appointment_collection.find({'email': email}))
    for appointment in past_appointments:
        appointment['_id'] = str(appointment['_id'])  # Convert ObjectId to string

    return render_template(
        'patient_dashboard.html',
        patient=patient,
        active_appointments=active_appointments,
        past_appointments=past_appointments
    )



@app.route('/complete_appointment/<appointment_id>', methods=['POST'])
def complete_appointment(appointment_id):
    try:
        # Find the appointment by ID and remove it from appointment_collection
        appointment = appointment_collection.find_one({'_id': ObjectId(appointment_id)})
        if appointment:
            # Insert the appointment into past_appointment_collection
            past_appointment_collection.insert_one(appointment)
            # Remove it from the current appointment_collection
            appointment_collection.delete_one({'_id': ObjectId(appointment_id)})
            flash('Appointment marked as completed!', 'success')
        else:
            flash('Appointment not found!', 'danger')
    except Exception as e:
        print(f"Error: {str(e)}")
        flash('An error occurred while completing the appointment.', 'danger')

    return redirect(url_for('patient_dashboard'))






@app.route('/logout')
def logout():
    session.pop('patient', None)  # Remove patient from session
    return redirect(url_for('home'))  # Redirect to login page



@app.route('/doctor-login', methods=['GET', 'POST'])
def doctor_login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']

        # Find the doctor in MongoDB by name
        doctor = doctors_collection.find_one({'name': name})

        if doctor and decrypt_password(doctor['password'], password):
            session['doctor'] = name  # Store the doctor in the session
            flash('Login successful!', 'success')
            
            # Redirect to login.html after successful login
            return redirect(url_for('login_page'))
        else:
            flash('Invalid name or password!', 'danger')
            return redirect(url_for('doctor_login'))

    return render_template('doctor_login.html')




@app.route('/register_doctor', methods=['GET', 'POST'])
def register_doctor():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']

        # Check if the doctor already exists
        if doctors_collection.find_one({"name": name}):
            flash('Doctor already registered!', 'danger')
            return redirect(url_for('register_doctor'))

        # Encrypt the password before saving
        encrypted_password = encrypt_password(password)

        # Save the doctor data to MongoDB
        doctors_collection.insert_one({'name': name, 'password': encrypted_password})
        flash('Doctor registration successful!', 'success')
        return redirect(url_for('doctor_login'))

    return render_template('doctor_register.html')



@app.route('/doctor-home', methods=['GET', 'POST'])
def doctor_home():
    if 'doctor' not in session:
        flash('Please log in as a doctor first!', 'danger')
        return redirect(url_for('doctor_login'))

    if request.method == 'POST':
        patient_email = request.form['patient_email']
        # Search for the patient in the patients collection
        patient = patients_collection.find_one({'email': patient_email})

        if patient:
            # Redirect to a patient details page
            return render_template('patient_details.html', patient=patient)
        else:
            flash('Patient not found!', 'danger')

    return render_template('doctor_home.html', doctor=session['doctor'])

@app.route('/doctor-logout')
def doctor_logout():
    session.pop('doctor', None)
    flash('Logged out successfully!')
    return redirect(url_for('main'))


if __name__ == '__main__':
    app.run(debug=True)