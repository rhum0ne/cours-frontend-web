from database import get_connection
from quiz import get_quiz_size

class Participation():
    
    def __init__(self, name:str, responses: list):
        self.name = name
        self.responses = responses
        
    def is_valid(self) -> bool:
        return len(self.responses) == get_quiz_size()
    
    def calculate_score(self):
        return 0
    
    def save_to_db(self):
        db_connection = get_connection()
        cur = db_connection.cursor()

        # start transaction
        cur.execute("begin")

        # save the participation to db
        insertion_result = cur.execute(
            f"insert into Participation (name, score) values (?, ?)", (self.name, self.calculate_score()))
        
        # send the request
        cur.execute("commit")