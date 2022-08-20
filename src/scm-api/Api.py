from flask import Flask, Blueprint, jsonify, request, make_response
from flask_restx import Resource, Api, Namespace
import os, sys, argparse

# import file from sibling directory
api_dir = os.path.dirname(os.path.realpath(__file__))
app_dir = os.path.dirname(api_dir)
queue_dir = os.path.join(app_dir, 'scm-queue')
ent_dir = os.path.join(app_dir, 'scm-entities')
sys.path.append(queue_dir)
from EventQueue import EventQueue
from PortAction import PortAction

parser = argparse.ArgumentParser(description='Starting SCM API')
parser = PortAction.Add_Port_Param(parser, 'port_number', 'Port number to start API on')
args = parser.parse_args()

app = Flask(__name__)
api = Api(version='1.0', title='SCM API', description='Supply Chain Management APIs')
blueprint = Blueprint('intake', __name__, url_prefix='/')
api.init_app(blueprint)
name_space_intake = Namespace('intake', description='SCM Intake APIs')
api.add_namespace(name_space_intake)
app.register_blueprint(blueprint)
event_queue = None

@name_space_intake.route("/healthcheck")
class Health(Resource):
    def get(self):
        if (event_queue.is_connected()):
            return make_response(jsonify({'Status': 'Healthy'}), 200)
        return make_response(jsonify({'Status': 'QueueConnectionFailed'}), 503)

@name_space_intake.route("/")
class Intake(Resource):
    def post(self):
        event_queue.publish(request.get_data())
        return make_response(jsonify({'Success': 'True'}), 201)

if __name__ == '__main__':
    event_queue = EventQueue()
    print(f'Starting SCM API on port {args.port_number}')
    app.run(debug = True, port=args.port_number)