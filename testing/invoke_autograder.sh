#!/usr/bin/env bash

LINK="https://autograder-service-ece440spring2024.apps.shift.nerc.mghpcc.org"
USERNAME="uname"
PASSWORD="pwd"
ASSIGNMENT_NAME=challenge-synchronization
SUBMISSION_PATH=$1

curl --user "$USERNAME:$PASSWORD" -X POST -F "submission.zip=@$SUBMISSION_PATH" -F "assignment_name=$ASSIGNMENT_NAME" $LINK
