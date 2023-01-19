# TechLab IPR Protection

This is the IPR Protection web application


# How it works

# Build and launch to Cloud Run

# Local development

Before local development is possible, you'll need a couple of configuration files from a person with admin access
to GCP. Specfically, you'll need two `.json` files:

1. `client_secret.json`, which you'll need to move to `/modules/auth/`
2. `techlab-coding-team-XXXX.json`, which you'll need to set as an environment variable like so: `export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/key/key.json`. To avoid having to set this
environment variable each time you start a new terminal session, we recommend that you add it to your `.bash_profile`.

It goes without saying, but we'll repeat it anyway: don't commit these keys to github :)!

Finally, we make use of a pre-commit hook to maintain some (basic) code styling. If you're committing to the repo for the first time, please do the following:

```bash
pre-commit install
pre-commit run --all-files
```
Then, the next time you commit (particularly if you're working on a new branch), you might see an error like:

```bash
Check Yaml...............................................................Passed
Fix End of Files.........................................................Failed
```

In this case, simply `git add .; git commit -m "your message"; git push` once more to push the cleaned code.

# Deploy
Log in to gcloud as the user that will run Docker commands. To configure authentication with user credentials, run the following command:

```
gcloud auth login
```

To configure authentication with service account credentials, run the following command:

```
gcloud auth activate-service-account ACCOUNT --key-file=KEY-FILE
```

```
gcloud auth activate-service-account <ypur service account name>@<project-id>.iam.gserviceaccount.com --key-file=<location to your service account>
```

Where

ACCOUNT is the service account name in the format
```
[USERNAME]@[PROJECT-ID].iam.gserviceaccount.com.
```

You can view existing service accounts on the Service Accounts page of console or with the command gcloud iam service-accounts list

KEY-FILE is the service account key file. See the Identity and Access Management (IAM)

documentation for information about creating a key.

gcloud projects add-iam-policy-binding "${PROJECT_ID}" \
   --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
   --role="roles/run.admin"

Configure Docker with the following command:

```
gcloud auth configure-docker
```
<a href="https://cloud.google.com/compute/docs/regions-zones/#available">Regions and zones</a>

<a href="https://cloud.google.com/container-registry/docs/pushing-and-pulling">Pushing and pulling images</a>

Europe Docker is the Docker registry that is used for the Docker image.
```
$ docker build -t eu.gcr.io/<project-id>/iprprotection .
$ docker push eu.gcr.io/<project-id>/iprprotection
```

US
```
$ docker build -t us.gcr.io/<project-id>/iprprotection .
$ docker push us.gcr.io/<project-id>/iprprotection
```

#
# Building a docker image on a Apple M1 for Google Cloud linux/am64
#

Option A: buildx
Buildx is a Docker plugin that allows, amongst other features, to build multi-platform images.

We are developing on the Mac ARM architecture but we want to create a x86 compatible image. The solution is NOT to use the heroku:container push command but rather building the image locally with Docker buildx.

```
docker buildx build \
--platform linux/amd64 \
--push \
-t eu.gcr.io/<project-id>/iprprotection:v0.1 .
```

As you can see I am tagging for each new version with adding:v<number> like this iprprotection:v1

This allows me to modifying the image without having to rebuild it.

You would need to update the terraform main/tf file so the tag matches.


Option B: set DOCKER_DEFAULT_PLATFORM
The DOCKER_DEFAULT_PLATFORM environment variable permits to set the default platform for the commands that take the --platform flag.

```
export DOCKER_DEFAULT_PLATFORM=linux/amd64
```

## Deploy with Yaml - work in progress
```
gcloud builds submit --config cloudbuild.yaml .
```

# Push To Multiple Git Repositories

I use two git Repositories
    GitLab for internal Use and deployment
    GitHub for public open source code sharing

From the root folder of your project, add both repositories to the remotes:

```
git remote add origin <GitLab URL>
git remote add copy <GitHUb URL>

Run the git remote -v command to ensure that both remotes were successfully added

Now you are able to perform a push to the selected remote by specifying it in the git push command:

```
git push origin main
git push copy main
```

Create a new remote named "all", and add GitLab and GitHub URLs to it

```
git remote add all <GitLab URL>```
git remote set-url all --add --push <GitLab URL>
git remote set-url all --add --push <GitHub URL>
```

```
git push all main
```
