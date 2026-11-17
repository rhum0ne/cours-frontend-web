from database import get_connection

def get_quiz_size():
	db_connection = get_connection()
	cur = db_connection.cursor()
	cur.execute("select count(*) from Question")
	result = cur.fetchone()
	return result[0]

def get_scores():
	db_connection = get_connection()
	cur = db_connection.cursor()
	cur.execute("select name, score from Participation")
	result = cur.fetchall()
	return [{"playerName": row[0], "score": row[1]} for row in result]