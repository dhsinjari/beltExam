from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Thought:
    db_name='userThoughts' # Our database name in the workbench
    def __init__(self,data):
        self.id = data['id'],
        self.description = data['description'],
        self.user_id = data['user_id'],
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']    

    @classmethod
    def getAllThoughts(cls):
        query= 'SELECT thoughts.id as id , description as description , COUNT(likes.id) as likesNr, thoughts.user_id as creator_id, email, firstname, lastname FROM thoughts LEFT JOIN users on thoughts.user_id = users.id LEFT JOIN likes on likes.thought_id = thoughts.id GROUP BY thoughts.id;'
        results =  connectToMySQL(cls.db_name).query_db(query)
        thoughts = []
        if results:
            for row in results:
                thoughts.append(row)
            return thoughts
        return thoughts
        
    @classmethod
    def getThoughtsLikes(cls,data):
        query= 'SELECT COUNT(likes.id) as nrLikes FROM likes WHERE likes.thought_id=%(thought_id)s GROUP BY likes.thought_id;'
        results =  connectToMySQL(cls.db_name).query_db(query,data)
        if results:
            return results[0]
        return False

    @classmethod
    def create_thought(cls,data):
        query = 'INSERT INTO thoughts ( description, user_id) VALUES ( %(description)s, %(user_id)s);'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def update_thought(cls,data):
        query = 'UPDATE thoughts SET description=%(description)s, user_id=%(user_id)s WHERE thoughts.id=%(thought_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_thought_by_id(cls, data):
        query= 'SELECT * FROM thoughts LEFT JOIN users on thoughts.user_id=users.id WHERE thoughts.id = %(thought_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results[0]

    @classmethod
    def get_user_thoughts(cls, data):
        query= 'SELECT * FROM users LEFT JOIN thoughts on thoughts.user_id = users.id WHERE users.id = %(user_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        thoughts = []
        for row in results:
            thoughts.append(row)
        return thoughts

    @classmethod
    def like(cls, data):
        query= 'INSERT INTO likes (thought_id, user_id) VALUES ( %(thought_id)s, %(user_id)s );'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def unlike(cls, data):
        query= 'DELETE FROM likes WHERE thought_id = %(thought_id)s and user_id = %(user_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def deleteThought(cls, data):
        query= 'DELETE FROM thoughts WHERE thoughts.id = %(thought_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)
    @classmethod
    def removeAllLikes(cls, data):
        query= 'DELETE FROM likes WHERE likes.thought_id = %(thought_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @staticmethod
    def validate_thought(thought):
        is_valid = True
        if len(thought['description']) < 5:
            flash("Thought must not be empty!", 'description')
            is_valid = False
        return is_valid