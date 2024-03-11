# OPE Autograder

This is a flask application that receives homework submissions via a `POST` request, runs some tests, and sends the results back to the client. It is generic and easily adaptable to the gradescope framework. 

The service is coupled loosely such that you only need to run the build configuration once. If you change tests to your autograder, simply [reapply the deployment](#reapply-deployment) and the initContainer will pull the newest version of the tests from your GitHub repo.

## Getting Started
Fork this repo. 

## Configuration
The application requires the following environmental variables in [`manifests/autograder.env`](manifests/autograder.env):

- `USERNAME` -- custom username for to autograder API (prevent unauthorized access)
- `PASSOWRD` -- custom password authenticating to autograder API (prevent unauthorized access)
- `autograderv2_REPO_SSH_URL` -- git URL of your autograding tests
- `REPO_PATH_TOASSIGNMENTS` -- path within your GitHub repo which contains the assignments in the format `repo_name/path_to_assignments` where each assignment has the format provided in this repo of `assignment_name/autograder`

Also, you need to generate a [deploy key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/managing-deploy-keys) for your repository with the autograder source code and paste its value in [`manifests/ssh-privatekey`](manifests/ssh-privatekey).

This is the directory structure of our tests in our private autograder repo, which is used in [`setup_thread.sh`](nerc/setup_thread.sh). You can use a different path, just make sure to configure it properly in the `setup_threads` shell script.

```
.
├── 2024
│   ├── {assignment_name}
│   │   ├── Makefile
│   │   ├── autograder
│   │   │   ├── Dockerfile
│   │   │   ├── README.md
│   │   │   ├── bundle.sh
│   │   │   ├── makefile
│   │   │   ├── run_autograder
│   │   │   ├── run_tests.py
│   │   │   ├── setup.sh
│   │   │   ├── test_bundle.sh
│   │   │   └── tests -> ../tests
│   │   └── tests
│   │       ├── README.md
│   │       ├── __init__.py
│   │       ├── test0.c
│   │       └── test1.c
```

## Deploying the application
After following the configuration steps, you can deploy the manifests into your current namespace by running:

```
kubectl apply -k manifests
oc start-build autograderv2-bc
```

#### Reapply Deployment
Then after the build finishes, reapply the deployment with the new image:

```
kubectl delete -f manifests/deployment.yaml
kubectl apply -f manifests/deployment.yaml
```

If you want to see what the manifests look like you can run:

```
kubectl kustomize manifests
```

# Gradescope Autograder
Follow the steps provided in [`gradescope/README.md`](gradescope/README.md) to set up the gradescope autograder which invokes your OpenShift autograder API. One of the arguments it passes is the assignment name, which allows the OpenShift service to grade multiple different assignments based on this form value in the curl request without needing to reapply the deployment.
