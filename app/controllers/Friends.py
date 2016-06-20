from system.core.controller import *

class Friends(Controller):
    def __init__(self, action):
        super(Friends, self).__init__(action)
        self.load_model('Friend')
        self.__db = self.models['Friend']

    def home(self):
        if session['user_id']:
            session['friends'] = self.__db.get_friends(session['user_id'])
            session['others'] = self.__db.get_others(session['user_id'])
            return self.load_view('friends.html')
        else:
            return redirect('/')

    def add(self, id):
        self.__db.add_friend(session['user_id'], id)
        return redirect('/friends')

    def remove(self, id):
        self.__db.remove_friend(session['user_id'], id)
        return redirect('/friends')

    def profile(self, id):
        session['profile'] = self.__db.get_detail(id)
        return self.load_view('profile.html')
