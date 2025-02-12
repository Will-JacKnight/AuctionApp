from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/users')
def get_users():
    return jsonify({"message": "User service operational"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001) 