import subprocess
import time
import os
import concurrent.futures
import json
import sys

# request with correct solution
def make_req(submission_path):
    for http_retries in range(1):
        try:
            response = subprocess.run(["./invoke_autograder.sh", submission_path], capture_output=True, text=True)
            response_json = json.loads(response.stdout)
            score = response_json.get('score')
            print(score)
        except:
            print("0")

def main():
    number_of_requests = 100

    with concurrent.futures.ThreadPoolExecutor(max_workers=number_of_requests) as executor:
        # Create a list of futures
        futures = []
        for i in range(number_of_requests):
            if i % 10 == 0:
                time.sleep(2)
            if i % 2 == 0:  # Even step
                futures.append(executor.submit(make_req, "./bogus_solution/submission.zip"))
            else:  # Odd step
                futures.append(executor.submit(make_req, "./correct_solution/submission.zip"))        
        # Wait for the futures to complete and get the results
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
if __name__ == "__main__":
    main()
