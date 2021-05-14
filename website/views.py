from __future__ import print_function
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, VolunteerGroup, Organization, User
from sqlalchemy import update
from . import db
import json
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

views = Blueprint('views', __name__)


@views.route('/notes', methods=['GET', 'POST'])
@login_required
def note():
    notes = Note.query.all()
    notes_list = []
    for note in notes:
        user1 = User.query.filter_by(id=note.user_id).first()
        temp_dict = {'user_name': user1.first_name, 'note': note}
        notes_list.append(temp_dict)

    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added, please refresh the page!', category='success')

    return render_template("note.html", notes=notes_list, user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    username = User.query.filter_by(id=note.user_id).first()
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
        else:
            flash(f'this is {username.first_name}\'s note, so you cant delete it', category='success')
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


@views.route('/', methods=['GET', 'POST'])
def home():
    org_list = []
    org = Organization.query.all()
    for ob in org:
        org_list.append(ob)
    if request.method == 'POST':
        org_id = request.form.get('org_id')
        value = User.query.filter_by(id=current_user.id).first()
        value.organization_id = int(org_id)
        db.session.commit()
        flash("Done!", category='success')

    return render_template("volunteering-catalog.html", org=org_list, user=current_user)


# Admin pages
@views.route('/Admin', methods=['GET', 'POST'])
def admin_panel():
    return render_template("admin-page.html", user=current_user)

# personal page
@views.route('/personal-page', methods=['GET', 'POST'])
def personalpage():
    org = Organization.query.filter_by(id=current_user.organization_id).first()
    if request.method == 'POST':
       if 'submit_but' in request.form:
           ans = request.form['rating']
           org.votersNumber += 1
           cur_rating = (1 / (org.votersNumber)*int(ans)) + (((org.votersNumber-1)/org.votersNumber)*org.rating)
           org.rating = cur_rating
           db.session.commit()
       flash(ans, category='success')
    return render_template("personal-page.html", user=current_user ,org = org)