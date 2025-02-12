from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Microservices URLs
USER_SERVICE_URL = "http://user-service:6000"

@app.route('/api/register', methods=['POST'])
def register():
    """ Forward registration request to User Service """
    response = requests.post(f"{USER_SERVICE_URL}/register", json=request.json)
    return jsonify(response.json()), response.status_code

@app.route('/api/login', methods=['POST'])
def login():
    """ Forward login request to User Service """
    response = requests.post(f"{USER_SERVICE_URL}/login", json=request.json)
    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
