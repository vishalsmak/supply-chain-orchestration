from flask import Flask, jsonify, request, make_response
from flask_restful import Resource, Api
import os, sys

# import file from sibling directory
api_dir = os.path.dirname(os.path.realpath(__file__))
app_dir = os.path.dirname(api_dir)
queue_dir = os.path.join(app_dir, 'scm-queue')
ent_dir = os.path.join(app_dir, 'scm-entities')
sys.path.append(queue_dir)
from EventQueue import EventQueue

app = Flask(__name__)
api = Api(app)
event_queue = EventQueue()

class Health(Resource):
    def get(self):
        if (event_queue.is_connected()):
            return make_response(jsonify({'Status': 'Healthy'}), 200)
        return make_response(jsonify({'Status': 'QueueConnectionFailed'}), 503)
  
class Intake(Resource):
    def post(self):
        event_queue.publish(request.get_data())
        return make_response(jsonify({'Success': 'True'}), 201)

api.add_resource(Health, '/')
api.add_resource(Intake, '/intake')

if __name__ == '__main__':
    print('Starting SCM API')
    app.run(debug = True)