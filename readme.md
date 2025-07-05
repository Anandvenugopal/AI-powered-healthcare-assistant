# Patient Registration and QR Code Generator

This is a Flask-based web application for hospital patient registration. The application allows users to register patients, generate QR codes linking to their records, and update patient information using a database with SQLAlchemy.

---

## Features

- 📋 **Patient Registration Form**: Collects patient details including personal information, medical history, and lifestyle habits.
- 🏥 **Database Management**: Uses SQLAlchemy ORM for handling patient data.
- 🔗 **QR Code Generation**: Creates QR codes that link to patient records.
- 🔄 **Data Update Functionality**: Allows modification of patient details.
- 📊 **Flask-Migrate Support**: Handles database schema updates efficiently.

---

## Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### 2️⃣ Create a Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
source venv/bin/activate   # On Windows use: venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```



### 5️⃣ Run the Application
```bash
flask run
```
The application will be available at: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---


## Technologies Used

- **Flask** - Web framework
- **Flask-SQLAlchemy** - ORM for database management
- **Flask-Migrate** - Database migration tool
- **SQLite** - Database
- **Bootstrap** - Frontend styling
- **qrcode** - QR code generation

---

## License
This project is licensed under the MIT License.

---

## Future Enhancements
✅ Add authentication for access control
✅ Implement an admin dashboard
✅ Generate PDF reports for patient records

---

### 👨‍💻 Developed by: *Abin Varghese, Hafis Ahammed, Aquib ahammed, Anand Venugopal*

