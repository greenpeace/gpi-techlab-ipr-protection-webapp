import os
# configure local or cloud
try:
    from system.config import BUCKET # only cloud
    # Get the sites environment credentials
    project_id = os.environ["GCP_PROJECT"]
except:
    # Set Local Environment Variables (Local)
    os.environ['GCP_PROJECT'] = 'torbjorn-zetterlund'    
    # Get project id to intiate
    project_id = os.environ["GCP_PROJECT"]