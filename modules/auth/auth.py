# Get the Flask Files Required
import os
from flask import (
    Blueprint,
    g,
    session,
    request,
    url_for,
    redirect,
    render_template,
    abort,
    flash,
)
import pathlib
import requests

# Get Google Login with oauth
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
import google.auth.transport.requests
from pip._vendor import cachecontrol

from system.getsecret import getsecrets

# Import project id
from system.setenv import project_id

# Carbon tracking
# from codecarbon import track_emissions

authsblue = Blueprint("authsblue", __name__)

# Get the secret for Service Account
client_id = getsecrets("client_id", project_id)
app_secret_key = getsecrets("app_secret_key", project_id)
restrciteddomain = getsecrets("restrciteddomain", project_id)

# this is to set our environment to https because OAuth 2.0 only supports https environments
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
# enter your client id you got from Google console
GOOGLE_CLIENT_ID = client_id
# set the path to where the .json file you got Google console is
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")
# Flow is OAuth 2.0 a class that stores all the information on how we want to authorize our users
flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=[
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
        "openid",
    ],
    # and the redirect URI is the point where the user will end up after the authorization
    redirect_uri="http://127.0.0.1:8080/callback"
    # redirect_uri="https://iprprotection-gfwyo3nbea-lz.a.run.app/callback"
)

#
# API Route Default displays a webpage
#
@authsblue.route("/login")
def login():
    return render_template("login.html", **locals())


#
# the logout page and function
#
@authsblue.route("/logout")
def logout():
    session.clear()
    return redirect("/")


#
# API Route Default displays a webpage
#
@authsblue.route("/loginseq")  # the page where the user can login
def loginseq():
    # asking the flow class for the authorization (login) url
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


# this is the page that will handle the callback process meaning process after the authorization
@authsblue.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    # if not session["state"] == request.args["state"]:
    #     abort(500)  #state does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    # the final page where the authorized users will end up
    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token, request=token_request, audience=GOOGLE_CLIENT_ID
    )

    #
    # This code is to limit the login to a specific domain
    #
    email = id_info.get("email")
    if email.split("@")[1] != restrciteddomain:
        flash("You are not allowed to login to this site!")
        return redirect(url_for("frontpageblue.index"))

    # defing the results to show on the page
    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    session["photo"] = id_info.get("picture")
    return redirect(url_for("dashboardblue.main"))


# a function to check if the user is authorized or not
def login_is_required(function):
    def wrapper(*args, **kwargs):
        # authorization required
        if "google_id" not in session:
            return abort(401)
        else:
            return function()

    # Renaming the function name:
    # wrapper.__name__ = function.__name__
    return wrapper


#
# APP Pagenation
#
@authsblue.route("/api/data", methods=["POST"])
# @track_emissions
def data():
    total_filtered = 10

    # sorting
    order = []
    i = 0
    while True:
        col_index = request.args.get(f"order[{i}][column]")
        if col_index is None:
            break
        col_name = request.args.get(f"columns[{col_index}][data]")
        if col_name not in ["username", "age", "email"]:
            col_name = "username"
        descending = request.args.get(f"order[{i}][dir]") == "desc"
        col = getattr(User, col_name)
        if descending:
            col = col.desc()
        order.append(col)
        i += 1

    # Set the pagination configuration
    page = request.args.get("page", 1, type=int)
    start = request.args.get("start", 1, type=int)
    length = request.args.get("length", 5, type=int)
    pagination = User.objects.paginate(page=start, per_page=length)
    data = {
        "data": [user.to_dict() for user in pagination.items],
        "recordsFiltered": 10,
        "recordsTotal": 100,
        "draw": 1,
    }
    return data
