from system.core.model import Model
import re

class Login(Model):
    def __init__(self):
        super(Login, self).__init__()
        self.__query = ''
        self.__data = {}

    def run_query(self, query, data={}):
        return self.db.query_db(query, data)

    def get_user(self, email):
        self.__query = "SELECT id, name, alias, email, password FROM users WHERE email = :email"
        self.__data = {
            'email': email
        }
        return self.run_query(self.__query, self.__data)

    def register(self, form):
        user = {
            'name': form['name'],
            'alias': form['alias'],
            'email': form['email'],
            'pwd': self.bcrypt.generate_password_hash(form['pwd']),
            'dob': form['dob']
        }

        self.register_user(user)
        user = self.get_user(form['email'])[0]
        return user

    def register_user(self, user):
        self.__query = "INSERT INTO users (name, alias, email, password, dob, created_at, modified_at) VALUES(:name, :alias, :email, :password, :dob, NOW(), NOW())"

        self.__data = {
            'name': user['name'],
            'alias': user['alias'],
            'email': user['email'],
            'password': user['pwd'],
            'dob': user['dob']
        }
        return self.run_query(self.__query, self.__data)

    def name_validate(self, name):
        digit = re.compile('[0-9]')
        has_digit = digit.search(name)

        result = {
            'status': False,
            'msg': {}
        }

        if len(name) <= 2:
            result['msg']['name'] = '** must have more than 2 chars **'
        elif has_digit:
            result['msg']['name'] = '** must not have numbers **'
        else:
            result['status'] = True
            result['msg'] = {}

        return result

    def alias_validate(self, alias):
        result = {
            'status': False,
            'msg': {}
        }

        if len(alias) == 0:
            result['msg']['alias'] = '** alias cannot be empty **'
        else:
            result['status'] = True
            result['msg'] = {}

        return result

    def remail_validate(self, email):
        email_validity = self.__email_validate(email, 'r')
        if email_validity['status']:
            user = self.get_user(email)
            if user:
                email_validity['status'] = False
                email_validity['msg']['email'] = '** mail id already exists **'

        return email_validity

    def lemail_validate(self, email):
        return self.__email_validate(email, 'l')

    def __email_validate(self, email, which_email):
        mail = re.compile(r'^[a-zA-Z0-9\._-]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+$')
        is_email = mail.match(email)

        if which_email == 'r':
            msg_key = 'email'
        else:
            msg_key = 'lemail'

        result = {
            'status': False,
            'msg': {}
        }

        if is_email:
            result['status'] = True
            result['msg'] = {}
        else:
            result['msg'][msg_key] = '** Invalid Email **'

        return result

    def rpwd_validate(self, pwd, c_pwd=None):
        pwd_isValid = self.__pwd_validate(pwd, 'r')
        if pwd_isValid['status']:
            return self.__match_pwd(pwd, pwd_c=c_pwd)
        else:
            return pwd_isValid

    def lpwd_validate(self, pwd):
        return self.__pwd_validate(pwd, 'l')

    def __pwd_validate(self, pwd, which_pwd):
        digit = re.compile('[0-9]')
        cap = re.compile('[A-Z]')
        has_digit = digit.search(pwd)
        has_cap = cap.search(pwd)

        if which_pwd == 'r':
            msg_key = 'pwd'
        else:
            msg_key = 'lpwd'

        result = {
            'status': False,
            'msg': {}
        }

        if len(pwd) < 8:
            result['msg'][msg_key] = '** must be minimum 8 chars **'
        elif not has_cap:
            result['msg'][msg_key] = '** must have atleast 1 uppecase char **'
        elif not has_digit:
            result['msg'][msg_key] = '** must have atleast 1 digit **'
        else:
            result['status'] = True
            result['msg'] = {}

        return result

    def __match_pwd(self, pwd, **pwd_args):
        result = {
            'status': True,
            'msg': {}
        }

        if 'pwd_c' in pwd_args:
            if pwd != pwd_args['pwd_c']:
                result['status'] = False
                result['msg']['cpwd'] = "** confirmation password doesn't match **"
        elif 'pwd_hsh' in pwd_args:
            if not self.bcrypt.check_password_hash(pwd_args['pwd_hsh'], pwd):
                result['status'] = False
                result['msg']['lpwd'] = "** Password mismatch **"

        return result

    def login(self, form):
        isLogin = {
            'status': False,
            'msg': {}
        }

        user = self.get_user(form['email'])
        if user:
            pwd_validity = self.__match_pwd(form['pwd'], pwd_hsh = user[0]['password'])
            if pwd_validity['status']:
                pwd_validity['msg'] = user[0]
            return pwd_validity
        else:
            isLogin['status'] = False
            isLogin['msg']['lemail'] = '** email-id not found **'
            return isLogin
