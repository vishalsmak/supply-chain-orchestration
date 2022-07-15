import os, time, subprocess
from kubernetes import client, config, utils
import docker

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
        resp = apps_v1.delete_namespaced_deployment(name=deployment_name, namespace=namespace)
        print(f'deployment "{deployment_name}" deleted')
    except Exception as e:
        print (f"Failed to delete k8 deployment : {str(e)}")

def del_k8_service(service_name):
    try:
        core_V1.delete_namespaced_service(name=service_name, namespace=namespace)
        print(f'service "{service_name}" deleted')
    except Exception as e:
        print (f"Failed to delete k8 service : {str(e)}")

def setup_component(component, cleanup_k8_service = True, docker_image_build = True):
    print(f'\n\n----------------------------------setting up {component}----------------------------------\n')
    print(f'deleting exisiting pods on k8')
    del_k8_deployment(component)
    if (cleanup_k8_service):
        del_k8_service(component)
    if (docker_image_build):
        print(f'building docker image {component}:latest')
        docker_client.images.build(path = src_dir, dockerfile = f'{component}/Dockerfile', tag = f'{component}:latest', nocache = True, rm = True)
    print(f'creating new k8 deployment for {component}')
    yml = os.path.join(src_dir, f'{component}', f'{component}.yml')
    utils.create_from_yaml(k8s_client, yml)
    print(f'{component} setup complete')    

if __name__ == '__main__':
    try:
        setup_component('scm-queue', docker_image_build=False)
        print('waiting for 5 secs for scm-queue pod to startup')
        time.sleep(5)
        setup_component('scm-service', cleanup_k8_service=False)
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