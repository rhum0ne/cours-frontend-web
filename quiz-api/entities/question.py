from database import get_connection

class Question():
    
    def __init__(self, title: str, position: int, text: str, image: str, answers: list = [], id: int = None):
        self.id = id
        self.title = title
        self.position = position
        self.answers = answers
        self.text = text
        self.image = image
        
    def add_answer(self, text: str, is_correct: bool):
        self.answers.append({"text": text, "isCorrect": is_correct})