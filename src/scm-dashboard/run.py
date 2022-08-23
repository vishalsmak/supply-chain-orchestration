import os, sys, argparse
from dashboard import app

# import file from sibling directory
api_dir = os.path.dirname(os.path.realpath(__file__))
app_dir = os.path.dirname(api_dir)
cmn_dir = os.path.join(app_dir, 'scm-common')
sys.path.append(cmn_dir)
from PortAction import PortAction

parser = argparse.ArgumentParser(description='Starting SCM Dashboard')
parser = PortAction.Add_Port_Param(parser, 'port_number', 'Port number to start dashboard on')
args = parser.parse_args()

if __name__ == "__main__":
    print(f'Starting SCM Dashboard on port {args.port_number}')
    app.run_server(debug=True, port=args.port_number)
