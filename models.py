# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()

# class Patient(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     age = db.Column(db.Integer, nullable=False)
#     gender = db.Column(db.String(10), nullable=False)
#     phone = db.Column(db.String(15), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=True)
#     address = db.Column(db.Text, nullable=False)
#     disease = db.Column(db.String(200), nullable=True)
#     created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

#     def __repr__(self):
#         return f'<Patient {self.name}>'


from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Patients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    address = db.Column(db.Text, nullable=False)
    disease = db.Column(db.String(200), nullable=True)
    chronic_diseases = db.Column(db.Text, nullable=True)
    surgeries = db.Column(db.Text, nullable=True)
    medications = db.Column(db.Text, nullable=True)
    allergies = db.Column(db.Text, nullable=True)
    smoking = db.Column(db.String(10), nullable=True)  
    alcohol = db.Column(db.String(10), nullable=True)  
    exercise = db.Column(db.String(20), nullable=True)  
    sleep = db.Column(db.String(20), nullable=True)  

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<Patient {self.name}>'

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)  # Store the full path to the file
    file_type = db.Column(db.String(50), nullable=False)
    tag = db.Column(db.String(100))
    comment = db.Column(db.Text)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)  
    source = db.Column(db.String(50), nullable=False, default='index')  # 'index' or 'patient_form'
    
    def __repr__(self):
        return f'<Document {self.original_filename}>'
