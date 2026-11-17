class Question():
    
    def __init__(self, title: str):
        self.title = title
        
    def save_to_db(self):
        import sqlite3
        # create a connection
        path = "database.db"
        db_connection = sqlite3.connect(path)

        # set the sqlite connection in "manual transaction mode"
        # (by default, all execute calls are performed in their own transactions, not what we want)
        db_connection.isolation_level = None
        cur = db_connection.cursor()

        # start transaction
        cur.execute("begin")

        # save the question to db
        insertion_result = cur.execute(
            f"insert into Question (title) values (?)", (self.title,))

        # send the request
        cur.execute("commit")

        # in case of exception, rollback the transaction
        #cur.execute('rollback')