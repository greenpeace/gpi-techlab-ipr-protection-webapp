# Install Google Libraries
from google.cloud import secretmanager
import os


def check_environ_and_set_vars(path: str = "/Users/rich/greenpeace_workspace/gcp_key/techlab-coding-team-e231abddafaf.json"):
    if "GOOGLE_APPLICATION_CREDENTIALS" not in list(os.environ.keys()):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path

# Setup the Secret manager Client
check_environ_and_set_vars()
client = secretmanager.SecretManagerServiceClient()


def getsecrets(secret_name, project_id):
    resource_name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
    try:
        response = client.access_secret_version(request={"name": resource_name})
        return response.payload.data.decode('UTF-8')
    except:
        return False