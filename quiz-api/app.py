import hashlib

from flask_cors import CORS
from flask import Flask, request, make_response
import hashlib
from jwt_utils import build_token
from question import Question
from database import reset_database

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

@app.route('/questions/<int:id>', methods=['GET'])
def GetQuestion(id):

	question = Question.get_by_id(id)
	data = {
		"id": 0 if not question else id,
		"title": "" if not question else question.title,
		"position": 0 if not question else question.position,
		"text": "" if not question else question.text,
		"image": "" if not question else question.image, # TODO: add image support
		"possibleAnswers": [] if not question else question.answers
	}

	return data, 200

@app.route('/login', methods=['POST'])
def Login():
    payload = request.get_json()
    
    tried_password = payload['password'].encode('utf-8')
    hashed_tried_password = hashlib.md5(tried_password).digest()
    
    if hashed_tried_password != password:
        return {"message": "Unauthorized"}, 401
    
    return {"token": build_token()}, 200

@app.route('/questions', methods=['POST'])
def create_question():
	auth = request.headers.get('Authorization')
 
	if not auth:
		return {"message": "Unauthorized"}, 401

	json = request.get_json()
 
	question = Question(title=json['title'], position=json['position'], text=json['text'], image=json['image'])
	for answer in json['possibleAnswers']:
		question.add_answer(answer['text'], answer['isCorrect'])
 
 
	question.save_to_db()
 
	return {"message": "Question created successfully"}, 201

@app.route('/rebuild-db', methods=['POST'])
def RebuildDB():
	auth = request.headers.get('Authorization')
 
	if not auth:
		return {"message": "Unauthorized"}, 401
    
	reset_database()
	return {"message": "Database rebuilt successfully"}, 200

if __name__ == "__main__":
    app.run()