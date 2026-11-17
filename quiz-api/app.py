import hashlib

from flask_cors import CORS
from flask import Flask, request, make_response
import hashlib
from jwt_utils import build_token
from entities.question import Question
from database import reset_database
from Participation import Participation
from quiz import get_quiz_size, get_scores

from repositories.questionRepository import QuestionRepository
from database import get_connection


app = Flask(__name__)
CORS(app)

question_repository = QuestionRepository()

password = b"_M\xcc;Z\xa7e\xd6\x1d\x83'\xde\xb8\x82\xcf\x99"

@app.route('/')
def hello_world():
	x = 'world'
	return f"Hello, {x}"

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
	return {"size": get_quiz_size(), "scores": get_scores()}, 200

@app.route('/questions/<int:id>', methods=['GET'])
def GetQuestion(id):
	auth = request.headers.get('Authorization')
	 
	if not auth:
		return {"message": "Unauthorized"}, 401

	question = question_repository.find_by_id(id)

	if not question:
		return {"message": "Question not found"}, 404
	
	data = {
		"id": question.id,
		"title": question.title,
		"position": question.position,
		"text": question.text,
		"image": question.image,
		"possibleAnswers": question.answers
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
 
 
	question = question_repository.save(question)

	print(f"Question created with id: {question.id}")
	return {
		"id": question.id
		}, 200

@app.route('/questions/<int:question_id>', methods=['PUT'])
def update_question(question_id):
	auth = request.headers.get('Authorization')
 
	if not auth:
		return {"message": "Unauthorized"}, 401
 
	return {"message": "Not implemented"}, 501

@app.route('/questions/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
	auth = request.headers.get('Authorization')
 
	if not auth:
		return {"message": "Unauthorized"}, 401
 
	return {"message": "Not implemented"}, 501

@app.route('/questions/all', methods=['DELETE'])
def delete_all_questions():
	auth = request.headers.get('Authorization')
 
	if not auth:
		return {"message": "Unauthorized"}, 401
 
	return {"message": "Not implemented"}, 501

@app.route('/participations/all', methods=['DELETE'])
def delete_all_participations():
	auth = request.headers.get('Authorization')
 
	if not auth:
		return {"message": "Unauthorized"}, 401
 
	return {"message": "Not implemented"}, 501


@app.route('/participations', methods=['POST'])
def create_participation():
	json = request.get_json()
 
	name = json['playerName']
	responses = json['answers']
 
	participation = Participation(name=name, responses=responses)
 
	if not participation.is_valid():
		return {"message": "Invalid answers size"}, 400
 
	participation.save_to_db()
 
	return {"message": "Participation created successfully"}, 201

@app.route('/rebuild-db', methods=['POST'])
def RebuildDB():
	auth = request.headers.get('Authorization')
 
	if not auth:
		return {"message": "Unauthorized"}, 401
    
	reset_database()
	return {"message": "Database rebuilt successfully"}, 200

if __name__ == "__main__":
    app.run()