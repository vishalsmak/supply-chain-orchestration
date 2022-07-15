import platform, os, subprocess

def run_cmd(cmd):
    print(f'\n\n{cmd}')
    print('--------------------------------------------------------')
    subprocess.Popen(cmd, shell=True).communicate()

if __name__ == '__main__':
    # start docker if not running
    if (platform.system() == 'Windows'):
        run_cmd('powershell -ExecutionPolicy bypass "if (!(Get-Process \'Docker Desktop\' -ErrorAction SilentlyContinue)) {& \'C:\Program Files\Docker\Docker\Docker Desktop.exe\'}"')
    elif (os.system('service docker status') != 0):
            run_cmd('sudo service docker start')
    # start the kubernetes instance
    run_cmd('minikube start')
    # navigate to setup directory
    os.chdir(os.path.join(os.path.dirname(__file__), 'setup'))
    # set the environment variables for docker env in shell and setup SCM application 
    if (platform.system() == 'Windows'):
        run_cmd('powershell -ExecutionPolicy bypass "& minikube -p minikube docker-env --shell powershell | Invoke-Expression; python setup.py"')
    else:
        run_cmd('eval $(minikube docker-env) && python setup.py')