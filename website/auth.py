from flask import (
    Blueprint, flash, render_template, request, url_for, redirect
)
import os
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from werkzeug.security import generate_password_hash, check_password_hash
from .models import *
from .forms import LoginForm, RegisterForm
from flask_login import login_user, login_required, logout_user
from . import db


# create a blueprint
authBP = Blueprint('auth', __name__, url_prefix='/auth')


@authBP.route('/login', methods=['GET', 'POST'])
@authBP.route('/register', methods=['GET', 'POST'])
def loginRegister():

    #  Init form and assign to either be register or login
    form = None
    if request.path == '/auth/login':
        form = LoginForm()
    elif request.path == '/auth/register':
        form = RegisterForm()

    # Check submission and resulting function it based onrequest path (login or register)
    if form.is_submitted():
        if request.path == '/auth/register':

            # Assign form details to new user fields
            newUser = user()
            newUser.user_name = form.user_name.data
            newUser.email_id = form.email_id.data
            newUser.password_hash = form.confirm.data

            # Check user doesn't already exist and proceed
            if checkExists(newUser.user_name, user) == False:
                print(newUser.user_name)
                db.session.add(newUser)
                db.session.commit()
                flash("You've successfully registered!",
                      'list-group-item-success')
            # Return error
            elif checkExists(newUser.user_name, user) == True:
                print(True)
                error = 'Username already exists'
                flash(error, 'list-group-item-danger')

        elif request.path == '/auth/login':
            print('In Login View function')
            error = None
            if(form.validate_on_submit() == True):
                user_name = form.user_name.data
                password = form.password.data
                u1 = user.query.filter_by(name=user_name).first()
                if u1 is None:
                    error = 'Incorrect user name'
                # takes the hash and password
                elif not check_password_hash(u1.password_hash, password):
                    error = 'Incorrect password'
                if error is None:
                    login_user(u1)
                    # this gives the url from where the login page was accessed
                    nextp = request.args.get('next')
                    print(nextp)
                    if next is None or not nextp.startswith('/'):
                        return redirect(url_for('index'))
                    return redirect(nextp)
                else:
                    flash(error)
            return render_template('loginSignUp.html', form=form, pageType=request.path)

    return render_template('loginSignUp.html', form=form, pageType=request.path)


@authBP.route('/accountInformation')
def accountInformation():

    return render_template('accountInformation.html')
# this is the hint for a login function


# @authBP.route('/login', methods=['GET', 'POST'])
# def authenticate():  # view function
#     print('In Login View function')
#     login_form = LoginForm()
#     error = None
#     if(login_form.validate_on_submit() == True):
#         user_name = login_form.user_name.data
#         password = login_form.password.data
#         u1 = user.query.filter_by(name=user_name).first()
#         if u1 is None:
#             error = 'Incorrect user name'
#         # takes the hash and password
#         elif not check_password_hash(u1.password_hash, password):
#             error = 'Incorrect password'
#         if error is None:
#             login_user(u1)
#             # this gives the url from where the login page was accessed
#             nextp = request.args.get('next')
#             print(nextp)
#             if next is None or not nextp.startswith('/'):
#                 return redirect(url_for('index'))
#             return redirect(nextp)
#         else:
#             flash(error)
#     return render_template('user.html', form=login_form, heading='Login')
# Create image authentication function


def checkFile(form):
    print("test")
    # Get uploaded image from form
    img = form.image.data

    # Pull filename to check
    filename = img.filename

    # Get base file path (this files location)
    Base = os.path.dirname(__file__)

    # Join this files location with the image file and the location to store it
    uploadPath = os.path.join(Base, 'static/img', secure_filename(filename))

    img.save(uploadPath)


def checkExists(nameToCheck, table):
    test2 = table.query.all()
    test = None
    if table == user:
        for users in test2:
            if users.user_name == nameToCheck:
                return True
            else:
                test = False
        if test == False:
            return test
    elif table == event:
        for events in test2:
            if events.eventName == nameToCheck:
                return True
            else:
                test = False
        if test == False:
            return test
