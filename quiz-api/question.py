from database import get_connection

class Question():
    
    def __init__(self, title: str, position: int):
        self.title = title
        self.position = position
        self.answers = []
        
    def add_answer(self, text: str, is_correct: bool):
        self.answers.append({"text": text, "isCorrect": is_correct})
        
    def save_to_db(self):
        db_connection = get_connection()
        cur = db_connection.cursor()

        # start transaction
        cur.execute("begin")

        # save the question to db
        insertion_result = cur.execute(
            f"insert into Question (title, position) values (?, ?)", (self.title, self.position))
        
        id = cur.lastrowid
        
        for answer in self.answers:
            cur.execute(
                f"insert into QuestionAnswer (question, text, is_correct) values (?, ?, ?)", (id, answer['text'], answer['isCorrect']))

        # send the request
        cur.execute("commit")

        # in case of exception, rollback the transaction
        #cur.execute('rollback')