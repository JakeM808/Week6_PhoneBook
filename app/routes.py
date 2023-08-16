from app import app, db
from flask import render_template, redirect, url_for
from app.forms import AddContactForm
from app.models import Contact

@app.route('/')
def index():
    return render_template('index.html')

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
       

        # Check User table to see if there are any users with username or email
        # check_user = db.session.execute(db.select(User).where( (User.username==username) | (User.email==email) )).scalar()
        # if check_user:
        #     print('A user with that username/password already exists')
        #     return redirect(url_for('signup'))
        # Create a new instance of the User class with data from form
        # new_user = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password)

        new_contact = Contact(first_name=first_name, last_name=last_name, email=email, address=address, phone=phone_number)
        # Add the new_user object to the database
        db.session.add(new_contact)
        db.session.commit()
        # redirect back to the home page
        return redirect(url_for('index'))
    
    return render_template('add_contact.html', form=form)