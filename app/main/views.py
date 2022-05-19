from . import main_blueprint
from flask import render_template, url_for, redirect, flash, request, abort
from .forms import Blog, LogIn, Signup
from ..model import Blogs, User
from flask_login import login_user, logout_user, login_required
from app import db
from ..request import get_quotes

@main_blueprint.route('/home')
@main_blueprint.route('/')
def index():
    return render_template('index.html')

@main_blueprint.route('/blogs', methods=['POST', 'GET'])
def blogs():
    form = Blog()
    if form.validate_on_submit():
        post = Blogs(title=form.title.data, content=form.content.data, author=form.author.data)
        # Clear the form
        form.title.data=''
        form.content.data=''
        form.author.data=''
        # Add post to database
        db.session.add(post)
        db.session.commit()

        flash('Post submitted successfully')

    return render_template('blog.html', form=form) 

@main_blueprint.route('/about')
def about():
    return render_template('about.html')       

@main_blueprint.route('/quotes')
def quotes():
    quotes=get_quotes()
    return render_template('quotes.html', quotes=quotes) 

@main_blueprint.route('/login', methods=['GET', 'POST'] )
def login():
    form=LogIn()
    if form.validate_on_submit():
        user=User.query.filter_by(username = form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember.data)
            return redirect(request.args.get('next') or url_for('main_blueprint.blogs'))  

        flash('Invalid username or Password')
        
    return render_template('login.html', form=form)

@main_blueprint.route("/signup", methods=['POST', 'GET'])
def sign_up():
    signup_form = Signup()
    if signup_form.validate_on_submit():
        user = User(email = signup_form.email.data, username = signup_form.username.data,password = signup_form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Successfully signed in for {signup_form.username.data}', category='success')
        return redirect(url_for('main_blueprint.login'))   
    return render_template("signup.html", form=signup_form)      

@main_blueprint.route('/profile/<uname>')
def profile(uname):
    user = User.query.filter_by(username=uname).first()
    if user is None:
        abort(404)
    return render_template('profile.html', user=user) 

@main_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main_blueprint.index"))
