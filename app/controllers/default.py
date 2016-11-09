from app import app, db, lm
from flask import render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required
from app.models.forms  import LoginForm, RegisterForm
from app.models.tables import User

@lm.user_loader
def user_loader(id):
    return User.query.get(id)

@app.route("/index/")
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register/", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    name=form.name.data)
        user.generate_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("User registered successfully")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)

@app.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash("Successful login")
            return redirect(url_for('index'))
        else:
            flash("Invalid login")
    elif form.errors:
        flash("Error in login")
    return render_template('login.html', form=form)

@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/dashboard/")
@login_required
def dashboard():
    return "OK"

@app.route("/teste/")
def teste():
    u = User('lucascb', '1234', 'Lucas Bernardes', 'lucascbernardes@live.com')
    db.session.add(u)
    db.session.commit()

    #user = User.query.filter_by(username='lucascb').first()
    #users = User.query.filter_by(username='lucascb').all()

    #db.session.delete(user)
    #db.session.commit()
    #print(user, users)
    return "OK"
