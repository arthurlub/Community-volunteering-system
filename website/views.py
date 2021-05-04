from __future__ import print_function
import datetime
import os.path
import pickle

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, VolunteerGroup
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


# Neomis pages

@views.route('/company-registration', methods=['GET', 'POST'])
def company_registration():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('first_name')
        phone = request.form.get('phone')
        organization = request.form.get('company')
        description = request.form.get('desc')
        comp = VolunteerGroup(name=name, organization_name=organization, email=email, cellphone_number=phone,
                              description=description)
        db.session.add(comp)
        db.session.commit()

        flash('Done!', category='success')

    return render_template("company-registration.html", user=current_user)


@views.route('/volunteering-catalog', methods=['GET', 'POST'])
def volunteering_catalog():
    if request.method == 'POST':
        SCOPES = ['https://www.googleapis.com/auth/calendar']
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        service = build('calendar', 'v3', credentials=creds)
        #email = request.form.get('email')
        event = {
            'summary': 'Google I/O 2015',
            'location': '800 Howard St., San Francisco, CA 94103',
            'description': 'A chance to hear more about Google\'s developer products.',
            'start': {
                'dateTime': '2015-05-28T09:00:00-07:00',
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': '2015-05-28T17:00:00-07:00',
                'timeZone': 'America/Los_Angeles',
            },
            'recurrence': [
                'RRULE:FREQ=DAILY;COUNT=2'
            ],
            'attendees': [
                {'email': 'noamishraki2@gmail.com'}
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }

        event = service.events().insert(calendarId='primary', body=event).execute()
        flash('Done!', category='success')
    return render_template("volunteering-catalog.html", user=current_user)


# Admin pages
@views.route('/Admin', methods=['GET', 'POST'])
def admin_panel():
    return render_template("admin-page.html", user=current_user)
