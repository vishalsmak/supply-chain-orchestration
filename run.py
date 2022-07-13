import platform
from util import run_cmd

if __name__ == '__main__':
    # start the kubernetes instance
    run_cmd('minikube start')

    # set the environment variables for docker env in shell and setup SCM application 
    if (platform.system() == 'Windows'):
        run_cmd('powershell -ExecutionPolicy bypass "& minikube -p minikube docker-env --shell powershell | Invoke-Expression; python setup.py"')
    else:
        run_cmd('eval $(minikube docker-env) && python setup.py')