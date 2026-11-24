from database import get_connection
from entities.question import Question


class QuestionRepository:
    def __init__(self):
        pass
        # self.connection = connection

    def save(self, question) -> Question:
        cn = get_connection()
        cur = cn.cursor()

        # start transaction
        cur.execute("begin")

        # save the question to db
        insertion_result = cur.execute(
            f"insert into Question (title, position, text, image) values (?, ?, ?, ?)", (question.title, question.position, question.text, question.image))
        
        id = cur.lastrowid
        question.id = id
        
        for answer in question.answers:
            cur.execute(
                f"insert into QuestionAnswer (question, text, is_correct) values (?, ?, ?)", (id, answer['text'], answer['isCorrect']))

        # send the request
        cur.execute("commit")

        # in case of exception, rollback the transaction
        #cur.execute('rollback')
        return question
    
    def find_by_id(self, id: int) -> Question:
        cn = get_connection()
        cur = cn.cursor()

        # get the question from db
        cur.execute(
            f"select * from Question where id = ?", (id,))
        
        question_row = cur.fetchone()
        
        if not question_row:
            return None
        
        question = Question(title=question_row[1], text=question_row[2], position=question_row[3], image=question_row[4], id=id)
        
        # get the answers for the question
        cur.execute(
            f"select * from QuestionAnswer where question = ?", (id,))
        
        answer_rows = cur.fetchall()
        
        for answer_row in answer_rows:
            question.add_answer(answer_row[2], answer_row[3])
        
        return question

    def delete_all(self):
        cn = get_connection()
        cur = cn.cursor()

        cur.execute("DELETE FROM Questions")
        cn.commit()