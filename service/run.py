import os, subprocess, time, platform

def run_cmd(cmd, fail_on_error = True):
    try:
        print('--------------------------------------------------------')
        print(cmd)
        print('--------------------------------------------------------')
        subprocess.Popen(cmd, shell=True).communicate()
        print('\n\n')
    except:
        if (fail_on_error):
            raise
        else:
            print('!!!!above error ignored!!!!')

def init_kube():
    run_cmd('minikube start')
    if (platform.system() == 'Windows'):
        run_cmd('powershell -ExecutionPolicy bypass "& minikube docker-env | Invoke-Expression"')
    else:
        run_cmd('eval $(minikube docker-env)')

def setup_app():
    os.chdir(os.path.join(os.path.dirname(__file__), 'Data_Intake_Api'))
    run_cmd('kubectl delete service intake-api', False)
    run_cmd('kubectl delete deployment intake-api', False)
    run_cmd('docker build . -t intake-api --no-cache')
    run_cmd('kubectl create -f intake_api_deployment.yml')
    run_cmd('kubectl create -f intake_api_service.yml')
    time.sleep(10)
    run_cmd('kubectl port-forward service/intake-api 8080:5000')

if __name__ == '__main__':
    init_kube()
    setup_app()
