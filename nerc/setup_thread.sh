#!/bin/bash

THREAD_NAME=$1
ASSIGNMENT_NAME=$2
THREAD_DIR=/app/${THREAD_NAME}

rm -rf ${THREAD_DIR}		# do this to ensure new env for each run
mkdir -p $THREAD_DIR/autograder/{source,submission,results}

cd ${THREAD_DIR}/autograder/source
cp -r /app/assignments/${REPO_PATH_TO_ASSIGNMENTS}/${ASSIGNMENT_NAME}/autograder/* .
rm -rf tests
cp -r /app/assignments/${REPO_PATH_TO_ASSIGNMENTS}/${ASSIGNMENT_NAME}/tests .
chmod +x run_autograder

find . -type f -exec sed -i "s#/autograder#${THREAD_DIR}/autograder#g" {} +
