from flask import Flask, flash, render_template, request, redirect, url_for 
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, logout_user


from admin import admin
from config import Config
from extensions import db, login_manager
from forms import LoginForm, RegistrationForm
from models import db, University, User
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config.from_object(Config)


db.init_app(app)
admin.init_app(app)
login_manager.init_app(app)


with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def index():
    universities = University.query.all()
    return render_template("index.html", universities=universities)

@app.route("/university/<int:university_id>")
def university(university_id):
    university = University.query.get(university_id)
    return render_template("university.html", university=university)

@app.route("/creator")
def creator():
    return render_template("creator.html")

@app.route("/create", methods=["POST", "GET"])
def create():
    name = request.form.get("name")
    location = request.form.get("location")
    tuition_fee = request.form.get("tuition_fee")
    language_requirement = request.form.get("language_requirement")
    faculty = request.form.get("faculty")

    university = University(
        name=name,
        location=location,
        tuition_fee=tuition_fee,
        language_requirement=language_requirement,
        faculty=faculty
    )

    db.session.add(university)
    db.session.commit()

    return redirect("/")

@app.route("/editor/<int:university_id>", methods=["GET"])
def editor(university_id):
    university = University.query.get(university_id)
    return render_template("editor.html", university=university)

@app.route("/edit/<int:university_id>", methods=["POST", "GET"])
def edit(university_id):
    university = University.query.get(university_id)

    university.name = request.form.get("name")
    university.location = request.form.get("location")
    university.tuition_fee = request.form.get("tuition_fee")
    university.language_requirement = request.form.get("language_requirement")
    university.faculty = request.form.get("faculty")

    db.session.commit()

    return redirect(f"/university/{university_id}")

@app.route("/delete/<int:university_id>")
def delete(university_id):
    university = University.query.get(university_id)
    db.session.delete(university)

    db.session.commit()

    return redirect("/")



@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        # Перевіряємо, чи існує користувач з таким логіном
        existing_user = User.query.filter_by(
            username=form.username.data
        ).first()
        if existing_user:
            flash("Користувач з таким ім'ям вже існує!", "danger")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, password=hashed_password)

        db.session.add(user)
        db.session.commit()

        flash("Реєстрація пройшла успішно!", "success")
        login_user(user)
        return redirect(url_for("admin.index"))

    return render_template("register.html", form=form)



@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Успішний вхід!", "success")
            return redirect(url_for("admin.index"))

        flash("Невірний логін або пароль", "danger")

    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/")
def home():
    return "Hello, this is the home page!"


if __name__ == "__main__":
    app.run(debug=True)
