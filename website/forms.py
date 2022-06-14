
from tokenize import Number
from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, SelectField, IntegerField, TimeField
from wtforms.validators import InputRequired, Length, EqualTo, Email
from werkzeug.datastructures import *
from flask_wtf.file import FileRequired, FileField, FileAllowed


# creates the login information
class LoginForm(FlaskForm):
    user_name = StringField("User Name", validators=[
                            InputRequired('Enter user name')])
    password = PasswordField("Password", validators=[
                             InputRequired('Enter user password')])
    submit = SubmitField("Login")

 # this is the registration form


class RegisterForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[
                           Email("Please enter a valid email")])

    # add buyer/seller - check if it is a buyer or seller hint : Use RequiredIf field

    # linking two fields - password should be equal to data entered in confirm
    password = PasswordField("Password", validators=[InputRequired(),
                                                     EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")

    # submit button
    submit = SubmitField("Register")


# Create event search form
class searchForm(FlaskForm):
    # Create list of game types for the select field
    gameTypes = ["All", "Casino", "Dungeons and Dragons",
                 "Board Games", "Cards", "Magic the Gathering"]

    gameType = SelectField("Game Type", choices=gameTypes)
    name = StringField("Search through names of events")
    submit = SubmitField('Search')

# Create event form


class EventForm(FlaskForm):

    # Create list of game types for the select field
    gameTypes = ["Casino", "Dungeons and Dragons",
                 "Board Games", "Cards", "Magic the Gathering"]

    # Status types
    statusTypes = ["Upcoming", "Inactive", "Booked", "Cancelled"]

    # Allowed images
    ALLOWED_FILE = {'png', 'jpg', 'jpeg', 'JPG', 'PNG', 'bmp'}

    # Create fields
    eventName = StringField("Event Name", validators=[InputRequired()])
    gameType = SelectField("Game Type", choices=gameTypes,
                           validators=[InputRequired()])
    price = IntegerField("Price")
    date = StringField("Date", validators=[InputRequired()])
    startTime = StringField("Start Time", validators=[InputRequired()])
    endTime = StringField("End Time", validators=[InputRequired()])
    location = StringField("Location", validators=[InputRequired()])
    blurb = StringField("Brief Description")
    requirements = TextAreaField("Event Reqirements")
    description = TextAreaField("Event Description")
    tickets = IntegerField("Number of Tickets")
    status = SelectField("Status", choices=statusTypes,
                         validators=[InputRequired()])
    image = FileField('Upload Event Image...', validators=[FileRequired(message="Please enter a file"),
                                                           FileAllowed(ALLOWED_FILE, message="Only accepts png, jpg/jpeg and bmp")])
    # Creator not needed as that will be drawn from the session

    submit = SubmitField("Create Event")