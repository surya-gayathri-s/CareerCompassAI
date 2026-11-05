
# 🚀 CareerCompass AI

A career guidance web application built using Flask and Python to help students explore career paths based on their skills and interests.

## ✨ Features

- **User Registration & Login** – Create an account and securely log in.
- **Career Recommendations** – Get rule-based career suggestions based on skills and interests.
- **Skill Analysis** – Explore recommended technologies and skills.
- **Learning Roadmaps** – View structured learning paths for different career roles.
- **User Dashboard** – Access career guidance features from one place.

## 🛠️ Technologies Used

- Python
- Flask
- SQLite
- HTML
- CSS
- Werkzeug Password Hashing

## 📁 Project Structure

CareerCompassAI/
│
├── app.py
├── static/
│   └── css/
│       └── style.css
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html
│   ├── career.html
│   ├── career_result.html
│   ├── skill.html
│   ├── skill_result.html
│   ├── roadmap.html
│   └── learn_more.html
├── .gitignore
├── requirements.txt
└── README.md

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Navigate to the project folder

```bash
cd CareerCompassAI
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the environment

Windows:

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

Navigate to the folder containing `app.py` and run:

```bash
python app.py
```

Open your browser and visit:

http://127.0.0.1:5000

## 🔐 Security

- Passwords are stored using Werkzeug password hashing.
- SQLite is used for user account storage.
- Login sessions protect application features.
- Local database files and environment secrets are excluded from Git.

## 👩‍💻 Author

Surya Gayathri S

Computer Science and Data Science Student
