from database import get_connection

class Question():
    
    def __init__(self, title: str, position: int):
        self.title = title
        self.position = position
        self.answers = []
        self.text = ""
        self.image = ""
        
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
    
    def get_by_id(id: int):
        db_connection = get_connection()
        cur = db_connection.cursor()

        # get the question from db
        cur.execute(
            f"select * from Question where id = ?", (id,))
        
        question_row = cur.fetchone()
        
        if not question_row:
            return None
        
        question = Question(title=question_row[1], position=question_row[2], text=question_row[3], image=question_row[4])
        
        # get the answers for the question
        cur.execute(
            f"select * from QuestionAnswer where question = ?", (id,))
        
        answer_rows = cur.fetchall()
        
        for answer_row in answer_rows:
            question.add_answer(answer_row[2], answer_row[3])
        
        return question