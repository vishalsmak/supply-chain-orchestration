from flask import Flask, jsonify, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Health(Resource):
    def get(self):
        return jsonify({'Status': 'Healthy'})
  
class Intake(Resource):
    def get(self):
        return jsonify({'Count': 0, 'comment':'work in progress will include more data' })
    def post(self):  
        data = request.get_json()
        return data, 201

api.add_resource(Health, '/')
api.add_resource(Intake, '/intake')

if __name__ == '__main__':
    app.run(debug = True)