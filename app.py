
from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import os
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "career-compass-development-key-change-before-deployment"
)

DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")


# Create database
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


init_db()


# Login protection decorator
def login_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in first.")
            return redirect(url_for("login"))
        return function(*args, **kwargs)
    return wrapper


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Learn More
@app.route("/learn-more")
def learn_more():
    return render_template("learn_more.html")


# Login
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, name, password FROM users WHERE email = ?",
            (email,)
        )

        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):

            session.clear()
            session["user_id"] = user[0]
            session["user_name"] = user[1]

            return redirect(url_for("dashboard"))

        flash("Invalid email or password. Please try again.")

    return render_template("login.html")


# Sign Up
@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not name or not email:
            flash("Please enter your name and email.")
            return render_template("signup.html")

        if len(password) < 8:
            flash("Password must contain at least 8 characters.")
            return render_template("signup.html")

        if password != confirm_password:
            flash("Passwords do not match.")
            return render_template("signup.html")

        hashed_password = generate_password_hash(password)

        conn = sqlite3.connect(DB_PATH)

        try:
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                (name, email, hashed_password)
            )

            conn.commit()
            flash("Account created successfully! Please log in.")
            return redirect(url_for("login"))

        except sqlite3.IntegrityError:
            flash("This email is already registered. Please log in.")
            return render_template("signup.html")

        finally:
            conn.close()

    return render_template("signup.html")


# Dashboard
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


# Logout
@app.route("/logout")
@login_required
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("login"))


# Career page
@app.route("/career")
@login_required
def career():
    return render_template("career.html")


# Skill Analysis page
@app.route("/skill")
@login_required
def skill():
    return render_template("skill.html")


# Career recommendation result
@app.route("/career-result", methods=["POST"])
@login_required
def career_result():

    name = request.form["name"]
    skills = request.form["skills"].lower()
    interests = request.form["interests"].lower()

    if "python" in skills and ("ai" in interests or "machine learning" in interests):
        career = "AI / Machine Learning Engineer"
        roadmap = "Python → Statistics → Machine Learning → Deep Learning"
        salary = "₹4 - ₹12 LPA (indicative)"
        learn = "Python, NumPy, Pandas, Scikit-learn, TensorFlow"

    elif "java" in skills and ("web" in interests or "software" in interests):
        career = "Software Developer"
        roadmap = "Java → OOP → Data Structures → Spring Boot"
        salary = "₹4 - ₹10 LPA (indicative)"
        learn = "Java, DSA, SQL, Spring Boot, Git"

    elif "sql" in skills and ("data" in interests or "analytics" in interests):
        career = "Data Analyst"
        roadmap = "SQL → Excel → Python → Data Visualization"
        salary = "₹3 - ₹8 LPA (indicative)"
        learn = "SQL, Python, Pandas, Power BI"

    elif "html" in skills or "css" in skills or "web" in interests:
        career = "Web Developer"
        roadmap = "HTML → CSS → JavaScript → React"
        salary = "₹3 - ₹8 LPA (indicative)"
        learn = "HTML, CSS, JavaScript, React"

    elif "python" in skills:
        career = "Python Developer"
        roadmap = "Python → OOP → APIs → Django"
        salary = "₹3 - ₹8 LPA (indicative)"
        learn = "Python, Django, Flask, SQL"

    else:
        career = "Software Developer"
        roadmap = "Programming Basics → DSA → Projects → Git"
        salary = "₹3 - ₹8 LPA (indicative)"
        learn = "Programming, DSA, SQL, Git"

    return render_template(
        "career_result.html",
        name=name,
        career=career,
        roadmap=roadmap,
        salary=salary,
        learn=learn
    )


# Skill Analysis result
@app.route("/skill-result", methods=["POST"])
@login_required
def skill_result():

    skills = request.form["skills"].lower()

    if "python" in skills:
        recommended = "Flask, Django, Machine Learning"

    elif "java" in skills:
        recommended = "Spring Boot, Hibernate"

    elif "sql" in skills:
        recommended = "MongoDB, Database Optimization"

    else:
        recommended = "Python, Git, HTML, CSS"

    return render_template(
        "skill_result.html",
        skills=skills,
        recommended=recommended
    )


# Roadmap
@app.route("/roadmap")
@login_required
def roadmap():
    return render_template("roadmap.html")


if __name__ == "__main__":
    app.run(debug=True)
