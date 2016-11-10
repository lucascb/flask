from app import app, db, lm
from flask import render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app.models.forms  import LoginForm, RegisterForm, TwitForm
from app.models.tables import User, Post, Follow

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

@app.route("/profile/<username>")
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    twits = Post.query.filter_by(user_id=user.id).all()
    if current_user.id != user.id:
        following = Follow.query.filter_by(user_id=user.id,
                                           follower_id=current_user.id
                                          ).first()
    else:
        following = None
    return render_template('profile.html', user=user,
                                           twits=twits,
                                           following=following)

@app.route("/follow/<int:id>")
@login_required
def follow(id):
    u = User.query.get(id)
    f = Follow(id, current_user.id)
    db.session.add(f)
    db.session.commit()
    return redirect(url_for('profile', username=u.username))

@app.route("/unfollow/<int:id>")
@login_required
def unfollow(id):
    u = User.query.get(id)
    f = Follow.query.filter_by(user_id=u.id, follower_id=current_user.id).first()
    db.session.delete(f)
    db.session.commit()
    return redirect(url_for('profile', username=u.username))

@app.route("/dashboard/", methods=["GET", "POST"])
@login_required
def dashboard():
    form = TwitForm()
    if form.validate_on_submit():
        new_twit = Post(content=form.content.data, user_id=current_user.id)
        db.session.add(new_twit)
        db.session.commit()


    following = Follow.query.filter_by(follower_id=current_user.id).all()
    twits = []
    for follow in following:
        t = Post.query.filter_by(user_id=follow.user.id).all()
        twits.extend(t)
    my_twits = Post.query.filter_by(user_id=current_user.id).all()
    twits.extend(my_twits)
    return render_template('dashboard.html', twits=twits, form=form)

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
