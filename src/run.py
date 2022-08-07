import platform, os, subprocess, shutil, argparse

def run_cmd(cmd):
    print(f'\n\n{cmd}')
    print('--------------------------------------------------------')
    subprocess.Popen(cmd, shell=True).communicate()

parser = argparse.ArgumentParser(description='args to Run SCM app')
parser.add_argument('--fresh_db', dest='fresh_db', type=bool, help='run app with fresh DB', default=False)
args = parser.parse_args()

if __name__ == '__main__':
    try:
        src_dir = os.path.dirname(__file__)
        data_dir = os.path.join(src_dir,'storage')
        if (args.fresh_db):
            run_cmd('minikube delete')
            # cleanup and fresh create the database folder
            shutil.rmtree(data_dir, ignore_errors=True)
            os.makedirs(data_dir)
            run_cmd(f'minikube start --mount-string "{data_dir}:/scm-storage" --mount')
        else:
            run_cmd(f'minikube start')
        # navigate to setup directory
        os.chdir(os.path.join(src_dir, 'setup'))
        # set the environment variables for docker env in shell and setup SCM application 
        if (platform.system() == 'Windows'):
            run_cmd(f'powershell -ExecutionPolicy bypass "& minikube -p minikube docker-env --shell powershell | Invoke-Expression; python setup.py --fresh_db={args.fresh_db}"')
        else:
            run_cmd(f'eval $(minikube docker-env) && python setup.py --fresh_db={args.fresh_db}')
    except KeyboardInterrupt:
        print('!!!!!!script run terminated from keyboard!!!!!!')
        exit()