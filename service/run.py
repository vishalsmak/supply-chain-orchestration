import os, subprocess, time

if __name__ == '__main__':
    dir = os.path.join(os.path.dirname(__file__), 'Data_Intake_Api')
    os.chdir(dir)
    subprocess.Popen('kubectl delete service intake-api', shell=False).communicate()
    subprocess.Popen('kubectl delete deployment intake-api', shell=False).communicate()

    subprocess.Popen('docker build . -t intake-api --no-cache', shell=False).communicate()

    subprocess.Popen('kubectl create -f .\intake_api_deployment.yml', shell=False).communicate()
    subprocess.Popen('kubectl create -f .\intake_api_service.yml', shell=False).communicate()
    time.sleep(10)
    subprocess.Popen('kubectl port-forward service/intake-api 8080:5000', shell=False).communicate()
