from __future__ import print_function
from flask import jsonify
from flask_login import current_user
from .models import Note, Organization, User
from flask import request, flash
from . import db
import os
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from flask import Blueprint, render_template, request, flash, redirect, url_for




def add_note():
    note = request.form.get('note')
    if len(note) < 1:
        flash('Note is too short!', category='error')
    else:
        new_note = Note(data=note, user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()
        flash('Note added, please refresh the page!', category='success')
        return redirect(url_for("views.note"))


def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    username = User.query.filter_by(id=note.user_id).first()
    if note:
        if note.user_id == current_user.id or current_user.id == 0:
            db.session.delete(note)
            db.session.commit()
        else:
            flash(f'this is {username.first_name}\'s note, so you cant delete it', category='success')
        return jsonify({})


def volunteer_registration():
    if current_user.organization_id == None and current_user.id != 0:
        org_id = request.form.get('org_id')
        value = User.query.filter_by(id=current_user.id).first()
        value.organization_id = int(org_id)
        db.session.commit()
        flash("Done!", category='success')
        google_calender()
    elif current_user.id == 0:
        flash("אתה המנהל, אתה לא יכול להרשם להתנדבות", category='error')
    else:
        flash("אתה כבר רשום להתנדבות, אם ברצונך להחליף התנבות בטל קודם את ההתנדבות הנוכחית", category='error')


def organization_rating():
    org = Organization.query.filter_by(id=current_user.organization_id).first()
    if request.method == 'POST':
        if current_user.organization_id != None:
            if not org.raters.__contains__(' ' + str(current_user.id) + ' '):
                if 'submit_but' in request.form:
                    ans = request.form['rating']
                    org.votersNumber += 1
                    cur_rating = (1 / (org.votersNumber) * int(ans)) + (
                            ((org.votersNumber - 1) / org.votersNumber) * org.rating)
                    org.rating = cur_rating
                    org.raters = org.raters + ' ' + str(current_user.id) + ' '
                    db.session.commit()
                    flash("הדירוג התקבל בהצלחה! תודה על הביקורת", category='success')
            else:
                flash("כבר דירגת ארגון זה בעבר, אין באפשרותך לדרג אותו ארגון פעמיים", category='error')
        else:
            flash("!אתה לא רשום לאף קבוצת התנדבות, ולכן אין באפשרותך לדרג", category='error')
    return org


def stop_volunteering():
    if current_user.type in (0, 2):
        user_id = request.form.get('user_id')
        user = User.query.filter_by(id=user_id).first()
    else:
        user_in = json.loads(request.data)
        user_id = user_in['userId']
        user = User.query.filter_by(id=user_id).first()
    user.organization_id = None
    db.session.commit()
    if current_user.id == 0:
        flash(f" {user.first_name} הפסקת את ההתנדבות למשתמש ", category='success')
    else:
        flash("ההרשמה להתנדבות בוטלה בהצלחה ", category='success')


def google_calender():
    # API-GOOGLE
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
            creds = flow.run_local_server(port=8888)
    # Save the credentials for the next run
    # with open('token.json', 'w') as token:
    #     token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    # email = request.form.get('email')
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
