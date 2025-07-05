from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
from datetime import datetime
import qrcode
from io import BytesIO
import base64
import socket
import os

app = Flask(__name__)
app.secret_key = "secret123"  # Needed for flashing messages

# Ensure instance directory exists
instance_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
os.makedirs(instance_path, exist_ok=True)

# Configure Database
db_path = os.path.join(instance_path, 'hospital.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'  # Updated database path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure upload folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize Database and Migrations
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define models
class Patients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    blood_group = db.Column(db.String(5))
    phone = db.Column(db.String(15))
    email = db.Column(db.String(120))
    address = db.Column(db.Text)
    disease = db.Column(db.String(200))  # Current disease/condition
    
    # Medical History
    chronic_diseases = db.Column(db.Text)
    surgeries = db.Column(db.Text)
    medications = db.Column(db.Text)
    allergies = db.Column(db.Text)
    
    # Lifestyle Information
    smoking = db.Column(db.String(3), default='No')
    alcohol = db.Column(db.String(3), default='No')
    exercise = db.Column(db.String(10), default='Low')
    sleep = db.Column(db.String(10), default='<8 hours')
    
    # Relationships
    documents = db.relationship('Document', backref='patient', lazy=True)

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(10), nullable=False)
    uploaded_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    source = db.Column(db.String(20), default='index')
    tag = db.Column(db.String(50))
    comment = db.Column(db.Text)

# Create tables within application context
with app.app_context():
    try:
        db.create_all()
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Error creating database tables: {e}")

# Auto-upgrade database on startup
# with app.app_context():
#     try:
#         upgrade()
#         print("upgraded")
#     except Exception as e:
#         print(f"Database migration error: {e}")
# # 
# Redirect to registration page

ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return redirect('/register')

# Function to get device IP
def get_device_ip():
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        try:
            name = request.form['name']
            age = int(request.form['age'])
            gender = request.form['gender']
            phone = request.form['phone']
            email = request.form.get('email', '')  # Make email optional
            address = request.form['address']

            # Check if email already exists (if provided)
            if email:
                existing_patient = Patients.query.filter_by(email=email).first()
                if existing_patient:
                    flash('A patient with this email already exists. Please use a different email.', 'error')
                    return render_template('register.html')

            new_patient = Patients(
                name=name,
                age=age,
                gender=gender,
                phone=phone,
                email=email if email else None,  # Set to None if empty
                address=address,
            )
            
            db.session.add(new_patient)
            db.session.commit()
            
            # Get the patient ID for QR code generation
            patient_id = new_patient.id

            # Generate QR code URL using the local device IP
            device_ip = get_device_ip()
            qr_url = f"http://{device_ip}:5000/patient_form/{patient_id}"
            
            flash('Registration successful!', 'success')
            return render_template('registration_success.html', patient_id=patient_id, qr_url=qr_url)
            
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error in registration: {str(e)}")
            flash('An error occurred during registration. Please try again.', 'error')
            return render_template('register.html')
    
    return render_template('register.html')

@app.route('/qr_code/<int:patient_id>')
def generate_qr_code(patient_id):
    # Create QR code for the patient form URL
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    form_url = f"{request.host_url}patient_form/{patient_id}"
    qr.add_data(form_url)
    qr.make(fit=True)
    
    # Create QR code image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save QR code to bytes
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    
    return send_file(img_io, mimetype='image/png')

@app.route('/patient_form/<int:patient_id>', methods=['GET', 'POST'])
def patient_form(patient_id):
    patient = Patients.query.get_or_404(patient_id)  # Fetch patient or return 404 if not found

    if request.method == 'POST':
        try:
            # Update medical history & lifestyle
            patient.chronic_diseases = request.form.get('chronic_diseases', '')
            patient.surgeries = request.form.get('surgeries', '')
            patient.medications = request.form.get('medications', '')
            patient.allergies = request.form.get('allergies', '')
            
            patient.smoking = request.form.get('smoking', 'No')
            patient.alcohol = request.form.get('alcohol', 'No')
            patient.exercise = request.form.get('exercise', 'Low')
            patient.sleep = request.form.get('sleep', '<8 hours')

            # Handle file uploads
            if 'medical_files' in request.files:
                files = request.files.getlist('medical_files')
                for file in files:
                    if file and file.filename and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        unique_filename = f"{timestamp}_{filename}"
                        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                        
                        # Save the file
                        file.save(file_path)

                        # Create document record
                        document = Document(
                            filename=unique_filename,
                            original_filename=filename,
                            file_path=file_path,
                            file_type=filename.rsplit('.', 1)[1].lower(),
                            uploaded_at=datetime.utcnow(),
                            patient_id=patient.id,
                            source='patient_form'  # Mark as uploaded from patient form
                        )
                        db.session.add(document)

            db.session.commit()
            flash('Information updated successfully!', 'success')
            return redirect(url_for('patient_form', patient_id=patient_id))
            
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error in form submission: {str(e)}")
            flash('An error occurred while saving the form. Please try again.', 'error')
            return str(e), 500

    return render_template("patient_form.html", patient=patient)


@app.route('/search', methods=['GET', 'POST'])
def search_patient():
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        return redirect(f"/patient/{patient_id}")

    return render_template("search.html")

@app.route('/patient/<int:patient_id>')
def view_patient(patient_id):
    patient = Patients.query.get(patient_id)
    if patient:
        return render_template("patient.html", patient=patient)
    else:
        return "Patient not found", 404  # Error if no patient exists with the given ID

@app.route('/doctor_panel')
def doctor_panel():
    try:
        # Query patients using SQLAlchemy
        patients = Patients.query.with_entities(Patients.id, Patients.name, Patients.age).all()
        return render_template('index.html', patients=patients)
    except Exception as e:
        app.logger.error(f"Error in doctor_panel: {str(e)}")
        flash(f"Error accessing patient data: {str(e)}", "error")
        return redirect('/')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        
        # Basic analysis of patient data
        analysis = "Patient Analysis:\n\n"
        
        # Age-based analysis
        age = int(data.get('age', 0))
        if age < 18:
            analysis += "- Patient is in pediatric age group\n"
        elif age >= 65:
            analysis += "- Patient is in geriatric age group\n"
        else:
            analysis += "- Patient is in adult age group\n"
            
        # Medical condition analysis
        if data.get('disease'):
            analysis += f"- Current medical condition: {data['disease']}\n"
            analysis += "- Regular monitoring recommended\n"
        else:
            analysis += "- No current medical conditions reported\n"
            
        # Contact information check
        if data.get('email') and data.get('phone'):
            analysis += "- Multiple contact methods available\n"
        
        return jsonify({
            "status": "success",
            "analysis": analysis.replace('\n', '<br>')
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

# Function to get database connection
def get_db_connection():
    conn = sqlite3.connect("instance/hospital.db")
    return conn

# Route to get patient data
@app.route('/get_patient_data/<int:patient_id>')
def get_patient_data(patient_id):
    try:
        patient = Patients.query.get_or_404(patient_id)
        documents = Document.query.filter_by(patient_id=patient_id).all()
        
        doc_list = [{
            'id': doc.id,
            'filename': doc.original_filename,
            'tag': doc.tag,
            'comment': doc.comment,
            'uploaded_at': doc.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')
        } for doc in documents]
        
        return jsonify({
            'status': 'success',
            'patient': {
                'id': patient.id,
                'name': patient.name,
                'age': patient.age,
                'gender': patient.gender,
                'phone': patient.phone,
                'email': patient.email,
                'address': patient.address,
                'disease': patient.disease,
                'medical_history': {
                    'chronic_diseases': patient.chronic_diseases or '',
                    'surgeries': patient.surgeries or '',
                    'medications': patient.medications or '',
                    'allergies': patient.allergies or ''
                },
                'lifestyle': {
                    'smoking': patient.smoking or 'Not specified',
                    'alcohol': patient.alcohol or 'Not specified',
                    'exercise': patient.exercise or 'Not specified',
                    'sleep': patient.sleep or 'Not specified'
                }
            },
            'documents': doc_list
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/get_patient_documents/<int:patient_id>')
def get_patient_documents(patient_id):
    try:
        documents = Document.query.filter_by(patient_id=patient_id).all()
        return jsonify([{
            'id': doc.id,
            'filename': doc.filename,
            'original_filename': doc.original_filename,
            'file_type': doc.file_type,
            'uploaded_at': doc.uploaded_at.isoformat(),
            'source': doc.source
        } for doc in documents])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delete_document/<int:document_id>', methods=['DELETE'])
def delete_document(document_id):
    try:
        document = Document.query.get_or_404(document_id)
        
        # Delete the file from the filesystem
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], document.filename)
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Delete the database record
        db.session.delete(document)
        db.session.commit()
        
        return jsonify({'status': 'success', 'message': 'Document deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/archive-document/<int:document_id>', methods=['POST'])
def archive_document(document_id):
    try:
        document = Document.query.get_or_404(document_id)
        document.source = 'patient_form'  # Mark as archived/previous
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

# Route to handle file upload and tags
@app.route('/upload_file', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'status': 'error', 'message': 'No file part'}), 400
        
        file = request.files['file']
        patient_id = request.form.get('patient_id')
        tag = request.form.get('tag', '')
        comment = request.form.get('comment', '')
        
        if not patient_id:
            return jsonify({'status': 'error', 'message': 'Patient ID is required'}), 400
        
        if file.filename == '':
            return jsonify({'status': 'error', 'message': 'No selected file'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'status': 'error', 'message': 'File type not allowed'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Generate unique filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            unique_filename = f"{timestamp}_{filename}"
            
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)
            
            # Create document record
            new_doc = Document(
                filename=unique_filename,
                original_filename=filename,
                file_path=file_path,
                file_type=filename.rsplit('.', 1)[1].lower(),
                patient_id=patient_id,
                tag=tag,
                comment=comment
            )
            
            db.session.add(new_doc)
            db.session.commit()
            
            return jsonify({
                'status': 'success',
                'message': 'File uploaded successfully',
                'document': {
                    'id': new_doc.id,
                    'filename': new_doc.filename,
                    'original_filename': new_doc.original_filename,
                    'uploaded_at': new_doc.uploaded_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'tag': new_doc.tag,
                    'comment': new_doc.comment
                }
            })
            
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Run the Flask App
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
