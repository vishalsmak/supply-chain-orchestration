from flask import Flask, jsonify, request, make_response
from flask_restful import Resource, Api
import os, sys

# import file from sibling directory
api_dir = os.path.dirname(os.path.realpath(__file__))
app_dir = os.path.dirname(api_dir)
queue_dir = os.path.join(app_dir, 'scm-queue')
sys.path.append(queue_dir)
from EventQueue import EventQueue

app = Flask(__name__)
api = Api(app)
event_queue = EventQueue()

class Health(Resource):
    def get(self):
        return make_response(jsonify({'Status': 'Healthy'}), 200)
  
class Intake(Resource):
    def get(self):
        return make_response(jsonify({'Count': 0, 'comment':'work in progress will include more data' }), 200)
    def post(self):
        event_queue.publish(request.get_data())
        return make_response(jsonify({'Success': 'True'}), 201)

api.add_resource(Health, '/')
api.add_resource(Intake, '/intake')

if __name__ == '__main__':
    print('Startting SCM API')
    app.run(debug = True)