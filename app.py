# Python standard libraries
import os
import logging
import werkzeug

# Third-party libraries
from flask import Flask, request, render_template, session, flash
from flask_mail import Message, Mail

# Get Form
from forms import BrandForm

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

mail = Mail()

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

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'your_email@gmail.com'
app.config["MAIL_PASSWORD"] = '****************' # password generated in Google Account Settings under 'Security', 'App passwords',
                                                 # choose 'other' in the app menu, create a name (here: 'FlaskMail'),
                                                 # and generate password. The password has 16 characters. 
                                                 # Copy/paste it under app.config["MAIL_PASSWORD"].
                                                 # It will give you access to your gmail when you have two steps verification.
mail.init_app(app)

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

### Brand
###  Brand Section
@brandsblue.route('/brandcontact', methods=['GET', 'POST'], endpoint='brandcontact')
def brandcontact():
    form = BrandForm()

    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('contact.html', form=form)
        else:
            msg = Message(form.subject.data, sender='contact@example.com', recipients=['your_email@gmail.com'])
            msg.body = """
            From: %s <%s>
            %s
            """ % (form.name.data, form.email.data, form.message.data)
            mail.send(msg)
            return render_template('brandcontact.html', success=True)

    elif request.method == 'GET':
        return render_template('brandcontact.html', form=form)

#
# Setting up to serve on port 8080
#
port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=port)
