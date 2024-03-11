# OPE Autograder

This is a flask application that receives homework submissions via a `POST` request, runs some tests, and sends the results back to the client. It is generic and easily adaptable to the gradescope framework. The service is coupled loosely such that you only need to run the build configuration once. If you change tests to your autograder, simply [restart the rollout](#restart-rollout) and the initContainer will pull the newest version of the tests from your GitHub repo.

## Getting Started
Fork this repository and place all of your gradescope autograders inside [`nerc/assignments`](nerc/assignments).

## Configuration
The application requires the following environmental variables in [`manifests/autograder.env`](manifests/autograder.env):

- `USERNAME` -- custom username for to autograder API
- `PASSOWRD` -- custom password authenticating to autograder API
- `ASSIGNMENT_NAME` -- name of autograder to use from repo for this assignment
- `autograderv2_REPO_SSH_URL` -- git URL of your autograding tests
- `REPO_PATH_TOASSIGNMENTS` -- path within your GitHub repo which contains the assignments in the format `repo_name/path_to_assignments` where each assignment has the format provided in this repo of `assignment_name/autograder`

Also, you need to generate a [deploy key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/managing-deploy-keys) for your fork of this repository and paste its value in [`manifests/ssh-privatekey`](manifests/ssh-privatekey).

Finally, change the GitHub URL in [`manifests/build-config.yaml`](manifests/buildconfig.yaml) to match the ssh URL of your fork of this repository containing your autograding tests. 

## Deploying the application
After following the configuration steps, you can deploy the manifests into your current namespace by running:

```
kubectl apply -k manifests
oc start-build autograder-bc
```

#### Restart Rollout
Then after the build finishes, reapply the deployment with the new image:

```
kubectl delete -f manifests/deployment.yaml
kubectl apply -f manifests/deployment.yaml
```

If you want to see what the manifests look like -- including the generated Secret -- without deploying the, you can run:

```
kubectl kustomize manifests
```

# Gradescope Autograder
Follow the steps provided in [`gradescope/README.md`](gradescope/README.md) to set up the gradescope autograder which invokes your OpenShift autograder API.
