from market import app
from flask import render_template, redirect, url_for, flash
from market.models import Item, User
from market.forms import RegisterForm, LoginForm
from market import db
from flask_login import login_user

def flash_errors(form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'error')

@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")

@app.route("/order")
def order_page():
    items = Item.query.all()
    return render_template("order.html",items =items)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    error =  None;  
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password_hash=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('order_page'))
    else:
        flash_errors(form)

    return render_template('register.html', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user.check_password_correction(attempted_password=form.password.data):
             #login_user(attempted_user)
             flash('Success! You are logged in as: ')
             flash(attempted_user.username, category='success')
             #flash(form.password.data, category='success')
             #flash(attempted_user.password_hash, category='success')
             return redirect(url_for('home_page'))
        else:
             flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)