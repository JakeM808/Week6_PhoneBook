from app import app, db
from flask import render_template, redirect, url_for, flash
from app.forms import AddContactForm, SignUpForm, LoginForm
from app.models import User, Contact
from flask_login import login_user, logout_user, login_required, current_user 


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        # Get the data from the form
        first_name = form.first_name.data
        last_name = form.last_name.data
        username = form.username.data
        email = form.email.data
        password = form.password.data
        # print(first_name, last_name, username, email, password)

      
            # Check User table to see if there are any users with username or email
        check_user = db.session.execute(db.select(User).where( (User.username==username) | (User.email==email) )).scalar()
        if check_user:
            flash('A user with that username and/or email already exists')
            return redirect(url_for('signup'))
        # Create a new instance of the User class with data from form
        new_user = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
        # Add the new_user object to the database
        db.session.add(new_user)
        db.session.commit()
        flash(f'{new_user.username} has been created')
               # Log the user in
        login_user(new_user)
        # redirect back to the home page
        return redirect(url_for('index'))
    elif form.is_submitted():
        flash("Your passwords do not match", 'danger')
        return redirect(url_for('signup'))
    return render_template('signup.html', form=form)

@app.route('/add_contact', methods=["GET", "POST"])
def add_contact():
    form = AddContactForm()
    if form.validate_on_submit():
        # Get the data from the form
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        address = form.address.data
        phone_number = form.phone.data
       
        new_contact = Contact(first_name=first_name, last_name=last_name, email=email, address=address, phone=phone_number, user_id=current_user.id)
        # Add the new_user object to the database
        db.session.add(new_contact)
        db.session.commit()
        flash(f"{new_contact.first_name} has been created", 'primary')
        # redirect back to the home page
        return redirect(url_for('index'))
    
    return render_template('add_contact.html', form=form)

app.route('/logout')
def logout():
    logout_user()
    flash("You have successfully logged out", "danger")
    return redirect(url_for('index'))

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        # print(username, password)
        # Query the User table for a user with that username
        user = db.session.execute(db.select(User).where(User.username==username)).scalar()
        # If we have a user AND the password is correct for that user
        if user is not None and user.check_password(password):
            # log the user in via login_user function
            login_user(user)
            flash("You have successfully logged in", 'primary')
            return redirect(url_for('index'))
        else:
            flash('Invalid username and/or password', 'danger')
            return redirect(url_for('login'))    
            

    return render_template('login.html', form=form)
