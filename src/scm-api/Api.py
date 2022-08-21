from flask import Flask, Blueprint, jsonify, make_response
from flask_restx import Resource, Api, Namespace, reqparse
import werkzeug
from werkzeug.utils import secure_filename
import os, sys, argparse

# import file from sibling directory
api_dir = os.path.dirname(os.path.realpath(__file__))
app_dir = os.path.dirname(api_dir)
queue_dir = os.path.join(app_dir, 'scm-queue')
cmn_dir = os.path.join(app_dir, 'scm-common')
sys.path.append(queue_dir)
sys.path.append(cmn_dir)
from EventQueue import EventQueue
from PortAction import PortAction
from UploadDir import get_upload_dir

parser = argparse.ArgumentParser(description='Starting SCM API')
parser = PortAction.Add_Port_Param(parser, 'port_number', 'Port number to start API on')
args = parser.parse_args()

app = Flask(__name__)
api = Api(app=app, version='1.0', title='SCM API', description='Supply Chain Management APIs')
blueprint = Blueprint('intake', __name__, url_prefix='/')
api.init_app(blueprint)
name_space_intake = Namespace('intake', description='SCM Intake APIs')
api.add_namespace(name_space_intake)
app.register_blueprint(blueprint)
event_queue = None
upload_folder = get_upload_dir()
upload_file_name = 'csv_file'
file_upload = reqparse.RequestParser()
file_upload.add_argument(upload_file_name,
                         type=werkzeug.datastructures.FileStorage, 
                         location='files', 
                         required=True, 
                         help='SCM data csv file')

@name_space_intake.route("/healthcheck")
class Health(Resource):
    def get(self):
        if (event_queue.is_connected()):
            return make_response(jsonify({'Status': 'Healthy'}), 200)
        return make_response(jsonify({'Status': 'QueueConnectionFailed'}), 503)

@name_space_intake.route("/file-upload")
class FileIntake(Resource):
    @api.expect(file_upload)
    def post(self):
        args = file_upload.parse_args()
        file = args[upload_file_name]
        save_name = secure_filename(file.filename)
        file.save(os.path.join(upload_folder, save_name))
        event_queue.publish(save_name)
        resp = jsonify({'message' : 'File successfully uploaded'})
        resp.status_code = 201
        return resp

if __name__ == '__main__':
    event_queue = EventQueue()
    print(f'Starting SCM API on port {args.port_number}')
    app.run(debug = True, port=args.port_number)