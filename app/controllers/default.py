from app import app, db, lm
from flask import render_template, flash, redirect, url_for
from flask_login import login_user, logout_user
from app.models.forms import LoginForm
from app.models.tables import User

@lm.user_loader
def user_loader(id):
    return User.query.get(id)

@app.route("/index")
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            flash("Successful login")
            redirect(url_for('index'))
        else:
            flash("Invalid login")
    return render_template('login.html', form=form)

@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/teste/")
def teste():
    #u = User('lucascb', '1234', 'Lucas Bernardes', 'lucascbernardes@live.com')
    #db.session.add(u)
    #db.session.commit()

    user = User.query.filter_by(username='lucascb').first()
    users = User.query.filter_by(username='lucascb').all()

    db.session.delete(user)
    db.session.commit()
    print(user, users)
    return "OK"
