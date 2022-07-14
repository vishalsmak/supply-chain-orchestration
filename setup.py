from util import run_cmd, wait

def setup_queue():
    run_cmd('kubectl delete service scm-queue', False)
    run_cmd('kubectl delete deployment scm-queue', False)
    run_cmd('kubectl create -f scm_queue.yml', 'queue')
    wait(10)

def setup_service():
    run_cmd('kubectl delete service scm-service', fail_on_error = False)
    run_cmd('docker build -f service/Dockerfile.service -t scm-service . --no-cache')
    run_cmd('kubectl create -f scm_service.yml', 'service')

def setup_api():
    run_cmd('kubectl delete service scm-api', fail_on_error = False)
    run_cmd('kubectl delete deployment scm-api', fail_on_error = False)
    run_cmd('docker build -f api/Dockerfile.api -t scm-api . --no-cache')
    run_cmd('kubectl create -f scm_api.yml', 'api')

def expose_api(port):
    wait(10)
    run_cmd(f'kubectl port-forward service/scm-api {port}:5000')

if __name__ == '__main__':
    setup_queue()
    setup_service()
    setup_api()
    expose_api(8080)