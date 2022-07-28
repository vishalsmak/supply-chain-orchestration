import os, time, subprocess, argparse
from kubernetes import client, config, utils
import docker

parser = argparse.ArgumentParser(description='args to setup SCM app')
parser.add_argument('--fresh_db', dest='fresh_db', type=bool, help='start app with fresh DB', default=False)
args = parser.parse_args()
config.load_kube_config()
k8s_client = client.ApiClient()
apps_v1 = client.AppsV1Api()
core_V1 = client.CoreV1Api()
network_api = client.NetworkingV1Api()
docker_client = docker.from_env()
src_dir = os.path.dirname(os.path.dirname(__file__))
namespace = 'default'

def del_k8_deployment(deployment_name):
    try:
        apps_v1.delete_namespaced_deployment(name=deployment_name, namespace=namespace)
        print(f'deployment "{deployment_name}" deleted')
    except Exception as e:
        print (f"Failed to delete k8 deployment : {str(e)}")

def del_k8_pvc(pvc_name):
    try:
        core_V1.delete_namespaced_persistent_volume_claim(name=pvc_name, namespace=namespace)
        print(f'persistent volume claim "{pvc_name}" deleted')
    except Exception as e:
        print (f"Failed to delete k8 persistent volume claim : {str(e)}")

def del_k8_pv(pv_name):
    try:
        core_V1.delete_persistent_volume(name=pv_name)
        print(f'persistent volume "{pv_name}" deleted')
    except Exception as e:
        print (f"Failed to delete k8 persistent volume : {str(e)}")

def del_k8_service(service_name):
    try:
        core_V1.delete_namespaced_service(name=service_name, namespace=namespace)
        print(f'service "{service_name}" deleted')
    except Exception as e:
        print (f"Failed to delete k8 service : {str(e)}")

def create_from_yml(dir, yml_name):
    print(f'creating new k8 deployment from {yml_name}')
    yml = os.path.join(src_dir, dir, yml_name)
    utils.create_from_yaml(k8s_client, yml)

def setup_component(component, cleanup_k8_dep = True, cleanup_k8_service = True, docker_image_build = True):
    print(f'\n\n----------------------------------setting up {component}----------------------------------\n')
    if (cleanup_k8_dep):
        del_k8_deployment(component)
    if (cleanup_k8_service):
        del_k8_service(component)
    if (docker_image_build):
        print(f'building docker image {component}:latest')
        docker_client.images.build(path = src_dir, dockerfile = f'{component}/Dockerfile', tag = f'{component}:latest', nocache = True, rm = True)
    create_from_yml(f'{component}', f'{component}.yml')
    print(f'{component} setup complete')

def reset_pv():
    print(f'\n\n----------------------------------setting up persistent volume----------------------------------\n')
    del_k8_deployment('scm-db')
    del_k8_pv('scm-storage')
    del_k8_pvc('scm-storage-claim')
    time.sleep(5)
    create_from_yml('scm-db', 'scm-pv.yml')

if __name__ == '__main__':
    try:
        if (args.fresh_db):
            reset_pv()
        setup_component('scm-db', cleanup_k8_dep=not args.fresh_db, docker_image_build=False)
        setup_component('scm-queue', docker_image_build=False)
        print('waiting for 5 secs for scm-queue pod to startup')
        time.sleep(5)
        setup_component('scm-intake-service', cleanup_k8_service=False)
        setup_component('scm-analyze-service', cleanup_k8_service=False)
        setup_component('scm-api')
        print('\nwaiting for 10 secs for scm-api pod to startup')
        time.sleep(10)
        print('\n\n-----------------------------forwarding scm-api on localhost:8080')
        subprocess.Popen('kubectl port-forward service/scm-api 8080:5000').communicate()
    except KeyboardInterrupt:
        print('!!!!!!script run terminated from keyboard!!!!!!')
        exit()
    except Exception as e:
        print (f"Failed to setup scm : {str(e)}")