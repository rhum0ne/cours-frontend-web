from flask_cors import CORS
from flask import Flask, request
import hashlib
from jwt_utils import build_token

app = Flask(__name__)
CORS(app)

password = b"_M\xcc;Z\xa7e\xd6\x1d\x83'\xde\xb8\x82\xcf\x99"

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
    
    tried_password = payload['password'].encode('utf-8')
    hashed_tried_password = hashlib.md5(tried_password).digest()
    
    if hashed_tried_password != password:
        return {"message": "Unauthorized"}, 401
    
    return {"token": build_token()}, 200

if __name__ == "__main__":
    app.run()