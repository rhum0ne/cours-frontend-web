import hashlib

from flask_cors import CORS
from flask import Flask, request

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
	x = 'world'
	return f"Hello, {x}"

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
	return {"size": 0, "scores": []}, 200

@app.route('/login', methods=['POST'])
def Login():
	payload = request.get_json()
	tried_pwd = payload['password'].encode('UTF-8')
	hashed = hashlib.md5(tried_pwd).digest()
	if hashed == b'c\xa9\xf0\xea{\xb9\x80Pykd\x9e\x85H\x18E':
		return {"status": "success"}, 200
	else:
		return {"status": "failure"}, 401

if __name__ == "__main__":
    app.run()