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


@authBP.route('/login')
def login():
    form = LoginForm()
    return render_template('loginSignUp.html', form=form)


@authBP.route('/accountInformation')
def accountInformation():

    return render_template('accountInformation.html')
# this is the hint for a login function
# @bp.route('/login', methods=['GET', 'POST'])
# def authenticate(): #view function
#     print('In Login View function')
#     login_form = LoginForm()
#     error=None
#     if(login_form.validate_on_submit()==True):
#         user_name = login_form.user_name.data
#         password = login_form.password.data
#         u1 = User.query.filter_by(name=user_name).first()
#         if u1 is None:
#             error='Incorrect user name'
#         elif not check_password_hash(u1.password_hash, password): # takes the hash and password
#             error='Incorrect password'
#         if error is None:
#             login_user(u1)
#             nextp = request.args.get('next') #this gives the url from where the login page was accessed
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
    print(img)

    # Pull filename to check
    filename = img.filename

    # Get base file path (this files location)
    Base = os.path.dirname(__file__)

    # Join this files location with the image file and the location to store it
    uploadPath = os.path.join(Base, 'static/img', secure_filename(filename))

    img.save(uploadPath)
