import os, time
from util import run_cmd

def setup_queue():
    run_cmd('kubectl delete service scm-queue', False)
    run_cmd('kubectl delete deployment scm-queue', False)
    run_cmd('kubectl create -f scm_queue.yml', 'queue')

def setup_api():
    run_cmd('kubectl delete service scm-api', fail_on_error = False)
    run_cmd('kubectl delete deployment scm-api', fail_on_error = False)
    run_cmd('docker build -f Dockerfile.api -t scm-api . --no-cache')
    run_cmd('kubectl create -f scm_api.yml', 'api')
    time.sleep(10)
    run_cmd('kubectl port-forward service/scm-api 8080:5000')

def setup_app():
    setup_queue()
    setup_api()

if __name__ == '__main__':
    setup_app()