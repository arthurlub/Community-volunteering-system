from __future__ import print_function
from flask import jsonify
from flask_login import login_required, current_user
from .models import Note, VolunteerGroup, Organization, User
from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db
import json
from . import be
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
        be.add_note()
    return render_template("note.html", notes=notes_list, user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    be.delete_note()


# page to delete
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
    if current_user.is_authenticated:
        org_list = []
        org = Organization.query.all()
        for ob in org:
            org_list.append(ob)
        if request.method == 'POST':
            be.volunteer_registration()
        return render_template("volunteering-catalog.html", org=org_list, user=current_user)
    else:
        return redirect(url_for('auth.login'))


# Admin pages
@views.route('/Admin', methods=['GET', 'POST'])
def admin_page():
    if current_user.id == 0:
        users_list = User.query.all()
        users_organization_info = []
        for user in users_list:
            if user.id != 0 and user.organization_id != None:
                org = Organization.query.filter_by(id=user.organization_id).first()
                temp_dict = {'user':user, 'org':org}
                users_organization_info.append(temp_dict)
        if request.method == 'POST':
            be.stop_volunteering()
        return render_template("admin-page.html", users= users_organization_info, user=current_user)


# personal page
@views.route('/personal-page', methods=['GET', 'POST'])
def personalpage():
    org = be.organization_rating()
    return render_template("personal-page.html", user=current_user, org=org)

@views.route('/stop-vol', methods=['POST'])
def stop_vol():
    be.stop_volunteering()


# personal-recommendations
@views.route('/personal-recommendations', methods=['GET', 'POST'])
def personal_recommendations():
    org = be.organization_rating()
    return render_template("personal-recommendations.html", user=current_user, org=org)