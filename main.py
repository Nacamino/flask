from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from bson import json_util

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost/pruebamongodb'
mongo = PyMongo(app)


@app.route('/users', methods=['GET'])
def get_users():
    users = mongo.db.users.find()
    response = json_util.dumps(users)
    return Response(response, mimetype='application/json ')


@app.route('/users', methods=['POST'])
def create_user():
    """crear nuevo usuario"""
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    if first_name and last_name:

        id = mongo.db.users.insert(
            {'first_name': first_name, 'last_name': last_name})
        response = {
            'id': str(id),
            'first_name': first_name,
            'last_name': last_name

        }
        return response
    else:
        return not_found()

    return {"message": "received"}


@app.errorhandler(404)
def not_found(error=None):
    message = jsonify({'message': 'Resource Not Found:' + request.url,
                       'status': 404})
    return message


if __name__ == "__main__":
    app.run(debug=True)
