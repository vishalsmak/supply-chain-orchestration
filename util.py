import os, subprocess

def run_cmd(cmd, dir = '', fail_on_error = True):
    try:
        set_dir(dir)
        print('--------------------------------------------------------')
        print(cmd)
        print('--------------------------------------------------------')
        subprocess.Popen(cmd, shell=True).communicate()
        print('\n\n')
    except KeyboardInterrupt:
        print('!!!!Terminating script due to canceled!!!!')
        raise
    except:
        if (fail_on_error):
            raise
        else:
            print('!!!!above error ignored!!!!')

def wait(seconds):
    run_cmd(f"python -c \"__import__('time').sleep({seconds})\"")

def set_dir(dir):
    if (not dir):
        dir = os.path.dirname(__file__)
    if (os.getcwd() != dir):
        os.chdir(os.path.join(os.path.dirname(__file__), dir))