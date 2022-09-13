# Get the Flask Files Required
from flask import Blueprint, g, request, render_template

# Fake News firestore collection
from firebase_admin import firestore

# Set Blueprint’s name https://realpython.com/flask-blueprint/
dashboardblue = Blueprint('dashboardblue', __name__)

from modules.auth.auth import login_is_required

# Main page dashboard
@dashboardblue.route("/main", endpoint='main')
@login_is_required
def main():
    return render_template('index.html', **locals())
