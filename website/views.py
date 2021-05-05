from __future__ import print_function
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, VolunteerGroup, Organization ,User
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
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("note.html", user=current_user)


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


@views.route('/', methods=['GET', 'POST'])
def home():
    org_list = []
    org = Organization.query.all()
    for ob in org:
        org_list.append(ob)
    if request.method == 'POST':
        org_id = request.form.get('org_id')
        value = User.query.filter_by(id=1).first()
        value.organization_id = int(org_id)
        db.session.commit()
        flash("Done!", category='success')

    return render_template("volunteering-catalog.html", org=org_list, user=current_user)


# Admin pages
@views.route('/Admin', methods=['GET', 'POST'])
def admin_panel():
    return render_template("admin-page.html", user=current_user)
