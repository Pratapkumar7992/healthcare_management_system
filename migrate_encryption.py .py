from app.utils import fernet, encrypt_patient_data  # Import new key and encryption function
from cryptography.fernet import Fernet
from app import db  # MongoDB connection

# Old key (replace this with your actual old key)
old_key = b"your-old-key-here"  # Example: b'wK7ZJ7Uq7ELyzszLX7E7oRDkAgRk_VxCTUrXZcfK98Q='
old_fernet = Fernet(old_key)

# Fetch all patient records from the database
patients = db.patients.find()

for patient in patients:
    try:
        # Decrypt each field with the old key
        decrypted_data = {
            "name": old_fernet.decrypt(patient["name"].encode()).decode(),
            "email": old_fernet.decrypt(patient["email"].encode()).decode(),
            "dob": old_fernet.decrypt(patient["dob"].encode()).decode(),
            "contact": old_fernet.decrypt(patient["contact"].encode()).decode(),
            "aadhar": old_fernet.decrypt(patient["aadhar"].encode()).decode(),
            "address": old_fernet.decrypt(patient["address"].encode()).decode(),
            "age": patient["age"],  # Not encrypted, copy as-is
            "gender": patient["gender"],  # Not encrypted, copy as-is
            "disease": patient["disease"]  # Not encrypted, copy as-is
        }

        # Re-encrypt all data with the new key
        encrypted_data = encrypt_patient_data(decrypted_data)

        # Update the database with the new encrypted data
        db.patients.update_one({"_id": patient["_id"]}, {"$set": encrypted_data})
        print(f"Successfully migrated patient {patient['_id']}")

    except Exception as e:
        print(f"Failed to migrate patient {patient['_id']}: {e}")
