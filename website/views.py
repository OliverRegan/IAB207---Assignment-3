from flask import Blueprint, render_template, redirect, url_for, request
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
    if form.is_submitted():
        print('hello')
        print(form.name.data)
        print(form.gameType.data)
        name = form.name.data
        type = form.gameType.data
        for events in all_events:
            # Search by just category
            if type != 'All' and name == '':
                print('test1')
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
def createEvent():

    # Check user is signed in here to proceed
    # TBD

    # Create form
    from .forms import EventForm
    form = EventForm()

    # Check form submission
    if form.validate_on_submit():
        checkFile(form)
        # get data
        newEvent = event()
        newEvent.imagePath = form.image.data.filename
        form.populate_obj(newEvent)
        # newEvent = event(name=form.eventName._value, gameType=form.gameType.data, price=form.price._value, date=form.date._value, location=form.location._value, startTime=form.startTime._value, endTime=form.endTime._value,
        #                  blurb=form.blurb._value, requirements=form.requirements._value, description=form.description._value, tickets=form.tickets._value, creator='test@test.com', status='testStatus')
        db.session.add(newEvent)
        db.session.commit()
        # Return template
        return redirect(url_for('main.createEvent'))
    return render_template('eventCreation.html', form=form)


@main.route('/events/<id>', methods=['GET'])
def events(id):

    return render_template('eventDetails.html')
