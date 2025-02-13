from flask import Flask, request, jsonify
import requests
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
# Microservices URLs
USER_SERVICE_URL = "http://user-service:8080"

@app.route('/signup', methods=['POST'])
def register():
    """ Forward registration request to User Service """
    response = requests.post(f"{USER_SERVICE_URL}/signup", json=request.json)
    return jsonify(response.json()), response.status_code

@app.route('/login', methods=['POST'])
def login():
    """ Forward login request to User Service """
    response = requests.post(f"{USER_SERVICE_URL}/login", json=request.json)
    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000, debug=True)
