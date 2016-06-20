from system.core.model import Model

class Friend(Model):
    def __init__(self):
        super(Friend, self).__init__()
        self.__query = ''
        self.__data = {}

    def run_query(self, query, data={}):
        return self.db.query_db(query, data)

    def get_friends(self, id):
        self.__query = 'SELECT u.name, u.alias, u.email, u.id FROM friends f, users u WHERE f.user_id = :id and f.friend_id = u.id'
        self.__data = {
            'id': id
        }
        return self.run_query(self.__query, self.__data)

    def get_others(self, id):
        self.__query = 'SELECT u.name, u.alias, u.email, u.id FROM users u WHERE u.id <> :id AND u.id NOT IN (SELECT friend_id FROM friends WHERE user_id = :id)'
        self.__data = {
            'id': id
        }
        return self.run_query(self.__query, self.__data)

    def remove_friend(self, u_id, f_id):
        self.__query = 'DELETE FROM friends WHERE (friend_id = :f_id and user_id = :u_id) or (friend_id = :u_id and user_id = :f_id)'
        self.__data = {
            'u_id': u_id,
            'f_id': f_id
        }
        return self.run_query(self.__query, self.__data)

    def add_friend(self, u_id, f_id):
        self.__query = 'INSERT into friends (user_id, friend_id, created_at, modified_at) VALUES (:user_id, :friend_id, NOW(), NOW()), (:friend_id, :user_id, NOW(), NOW())'
        self.__data = {
            'user_id': u_id,
            'friend_id': f_id
        }
        return self.run_query(self.__query, self.__data)

    def get_detail(self, id):
        self.__query = 'SELECT u.name, u.alias, u.email, u.id FROM users u WHERE u.id = :id'
        self.__data = {
            'id': id
        }
        return self.run_query(self.__query, self.__data)[0]
