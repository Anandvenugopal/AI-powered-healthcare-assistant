
# AI-powered healthcare assistant(Flask + Gemini AI)

This is a Flask-based web application for hospital patient registration. It allows users to register patients, generate QR codes linking to their records, and update patient information using a SQLAlchemy database. It also integrates **Gemini API** for AI-powered features like automated data interpretation or report assistance.

---

## ✨ Features

- 📋 **Patient Registration Form**  
  Collects patient details including personal information, medical history, and lifestyle habits.

- 🏥 **Database Management**  
  Uses SQLAlchemy ORM for storing and retrieving patient data.

- 🔗 **QR Code Generation**  
  Automatically generates QR codes that link to each patient’s record.

- 🔄 **Update Functionality**  
  Modify and manage patient data in real time.

- 📊 **Flask-Migrate Support**  
  Handles database schema updates with version control.

- 🤖 **Gemini API Integration**  
  AI assistance for interpreting patient data, generating suggestions, and enhancing the overall workflow.

---

## 🚀 Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### 2️⃣ Create a Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Application
```bash
flask run
```

➡️ The application will be available at: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 📈 Future Enhancements

- ✅ Add login & authentication  
- ✅ Build an admin dashboard  
- ✅ Generate downloadable PDF reports

---

## 📄 License

This project is licensed under the **MIT License**.
