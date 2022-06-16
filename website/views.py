from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required
from .models import *
from .auth import checkFile
from . import db

main = Blueprint('main', __name__)


#  Home page route
@main.route('/', methods=['GET', 'POST'])
def index():

    # Import search form
    from .forms import searchForm
    form = searchForm()

    # Get events from database to pass data to the template
    all_events = event.query.all()

    # print(all_events[0].location)
    filtered_events = []
    print(form)

    # Deal with form submission
    if form.is_submitted():

        # Get name and type
        name = form.name.data

        # Test if an event with name
        type = form.gameType.data

        for events in all_events:
            # Search by just category
            if type != 'All' and name == '':
                if events.gameType == type:
                    filtered_events.append(events)
            # search by name
            if type == 'All' and name != '':
                if name.lower() in (events.eventName).lower():
                    filtered_events.append(events)
            # search by both
            if type != 'All' and name != '':
                if name.lower() in (events.eventName).lower() and events.gameType == type:
                    filtered_events.append(events)
            # default
            if type == 'All' and name == '':
                filtered_events = all_events
        return render_template("index.html", events=filtered_events, form=form, scroll=True)
    return render_template("index.html", events=all_events, form=form)


# Create event route
@main.route('/createEvent', methods=['GET', 'POST'])
@login_required
def createEvent():

    # Check user is signed in here to proceed
    # TBD

    # Create form
    from .forms import EventForm
    form = EventForm()

    # Check form submission
    if form.validate_on_submit():

        # Before proceeding check name hasnt been taken
        from .auth import checkExists
        if checkExists(form.eventName.data, event) == True:
            print('hello')
            error = 'Name has already been used'
            flash(error, 'list-group-item-danger')
        else:
            checkFile(form)
            # get data
            newEvent = event()
            newEvent.imagePath = form.image.data.filename
            form.populate_obj(newEvent)
            db.session.add(newEvent)
            db.session.commit()
            message = 'Event successfully created'
            flash(message, 'list-group-item-success')

    return render_template('eventCreation.html', form=form)


@main.route('/events/<id>', methods=['GET'])
def events(id):
    return render_template('eventDetails.html')


@main.route('/accountInformation')
@login_required
def accountInformation():

    return render_template('accountInformation.html')
