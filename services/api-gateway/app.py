from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)
CORS(app)
# Microservices URLs
USER_SERVICE_URL = "http://user-service:8080"
AUCTION_SERVICE_URL = "http://auction-service:7070"

# Configure Upload Folder
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# App route
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

@app.route('/listing', methods=['POST'])
def listing():
    """ Handle auction upload and forward request to Auction Service """
    if "productImage" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["productImage"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)
        
        data = {key: request.form[key] for key in request.form}
        data["image_url"] = f"/uploads/{filename}"
        response = requests.post(f"{AUCTION_SERVICE_URL}/upload-auction", json=data)
        return jsonify(response.json()), response.status_code

    return jsonify({"error": "Invalid file type"}), 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000, debug=True)
