from flask import Flask, request, Response, send_file, after_this_request
import zipfile
import os
import shutil
import subprocess
import threading
import sys

lock = threading.Lock()
app = Flask(__name__)

# Required settings
USERNAME = os.environ.pop("AUTOGRADER_USERNAME")
PASSWORD = os.environ.pop("AUTOGRADER_PASSWORD")

# Optional settings
try:
    AUTOGRADER_TIMEOUT = int(os.environ.pop("AUTOGRADER_TIMEOUT", 0))
except ValueError:
    AUTOGRADER_TIMEOUT = None

def check_auth(username, password):
    return username == USERNAME and password == PASSWORD

@app.route('/', methods=['POST'])
def upload_file():
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return 'Incorrect credentials', 401

    file = request.files['submission.zip']
    assignment_name = request.form['assignment_name']
    
    if not file:
        return 'Missing submission.zip', 400

    if not assignment_name:
        return 'Missing assignment name', 400
    
    thread_id = threading.get_ident()
    
    # create new test env for each new submission
    subprocess.run(['bash', '/app/setup_thread.sh', f'{thread_id}', assignment_name])
    
    @after_this_request
    def remove_thread_id_dir(response):
        shutil.rmtree(f'/app/{thread_id}', ignore_errors=True)
        return response

    with lock:
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall(f'/app/{thread_id}/autograder/submission/')
            subprocess.run([f'/app/{thread_id}/autograder/source/run_autograder'],
                       timeout=AUTOGRADER_TIMEOUT)

        return send_file(f'/app/{thread_id}/autograder/results/results.json')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8080,ssl_context='adhoc')
