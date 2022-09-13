# Python standard libraries
import os
import logging
import werkzeug

# Third-party libraries
from flask import Flask, render_template, session, flash
# Get Babel

# Add Editor
from flask_ckeditor import CKEditor

# Internal imports
from system.getsecret import getsecrets

# Import Modules
# Import Authorization
from modules.auth.auth import authsblue
# Import Brand Module
from modules.brand.brand import brandsblue
# Import from Dashboard
from modules.dashboard.dashboard import dashboardblue
# Import Frontpage
from modules.frontpage.frontpage import frontpageblue

#from modules.multilingual.routes import multilingualblue

# Import project id
from system.setenv import project_id

# Install Google Libraries
import google.cloud.logging

## Logging Client
client = google.cloud.logging.Client()

# Get the secret for Service Account
app_secret_key = getsecrets("app_secret_key",project_id)

# Create the Flask application error handlers
def page_not_found(e):
  return render_template('systemmsg/404.html'), 404

def internal_server_error(e):
  return render_template('systemmsg/500.html'), 500

# Initialize Flask App
app = Flask(__name__)

# register frontpage
app.register_blueprint(frontpageblue)
# Register Module Brand
app.register_blueprint(brandsblue)
# Register AUTh Module
app.register_blueprint(authsblue)
# Dashboard
app.register_blueprint(dashboardblue)
#app.register_blueprint(multilingualblue)

#it is necessary to set a password when dealing with OAuth 2.0
app.secret_key = app_secret_key
# Intiate the editor
ckeditor = CKEditor(app)

# Possible
logging.info("Start processing Function")

# Register Error Handlers
app.register_error_handler(404, page_not_found)
app.register_error_handler(500, internal_server_error)

#
# 404 Page not found    
#
@app.errorhandler(404)
def not_found_error(error):
    logging.info(f'404 Page Not Found')
    return render_template('systemmsg/404.html'), 404

#
# 500 error trying to access the API endpoint
#
@app.errorhandler(werkzeug.exceptions.HTTPException)
def internal_error(error):
    logging.info(f'500 System Error')
    return render_template('systemmsg/500.html'), 500

#
# Setting up to serve on port 8080
#
port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=port)
