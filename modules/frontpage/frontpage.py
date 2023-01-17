# Get the Flask Files Required
from flask import Blueprint, g, request, url_for, redirect, render_template
import logging

# Carbon tracking
# from codecarbon import track_emissions

# Set Blueprint’s name https://realpython.com/flask-blueprint/
frontpageblue = Blueprint("frontpageblue", __name__)
#
# API Route Default displays a webpage
#
@frontpageblue.route("/")
# @track_emissions
def index():
    return render_template("login.html", **locals())
