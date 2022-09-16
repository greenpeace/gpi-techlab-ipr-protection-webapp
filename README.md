# TechLab IPR Protection

This is the IPR Protection web application


# How it works

# AI Blog Writer with OpenAI GPT-3



# Build and launch to Cloud Run

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
git push origin master
git push copy master
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
