from FacadeBase import FacadeBase
from LoginToken import LoginToken
from User import User

class AnonymousFacade(FacadeBase):

    def __init__(self, repo, config):
        super().__init__(repo, config)
        self.role_name = 'Anonymous'

    def login(self, username1, password1):
        user1 = self.repo.get_by_condition_lm(User, lambda query: query.filter(User.user_name == username1).first())
        self.logger.logger.error(user1)
        if username1 is None or password1 is None or user1 is None:
            raise Exception('Username or Password needed!')
        elif user1 is None:
            raise Exception('UserDoseNotExist')
        else:
            user = self.repo.get_by_condition_lm(User, lambda query: query.filter(User.user_name == username1).first())
            print(user)
            self.logger.logger.error(user)
            if user.password != password1:
                self.logger.logger.info(f'Wrong username {username1} '
                                        f'or password {password1} has been entered to the login function.')
                raise Exception('username or password are worng!')
            logged_in_user = user
            if logged_in_user.user_role == 1:
                print("f")
                token_dic = {'id': logged_in_user.id, 'name': username1, 'role': 'Administrator'}
            elif logged_in_user.user_role == 2:
                token_dic = {'id': logged_in_user.id, 'name': username1, 'role': 'Customer'}
            elif logged_in_user.user_role == 3:
                token_dic = {'id': logged_in_user.id, 'name': username1, 'role': 'AirlineCompany'}
            else:
                self.logger.logger.info(f'User Roles table contains more than 3 user roles. Please check it ASAP.')
                raise Exception('UserRoleTableError')
            login_token = LoginToken(token_dic['id'], token_dic['name'],
                                    token_dic['role'])
            self.logger.logger.info(f'{login_token} logged in to the system.')
            print(login_token)
            return login_token

    def add_customer(self,user,customer):
        self.logger.logger.info(f'AnonymousFacade: adding customer by id {customer.id}')
        if customer is not None:
            try:
                self.logger.logger.info(f'AnonymousFacade: adding user by id {user}')
                self.add_user(user)
                self.logger.logger.info(f'AnonymousFacade: adding customer by id {customer}')
                user_name = user.user_name
                user_id = self.repo.get_by_column_value(User, User.user_name, user_name)[0]
                customer.user_id = user_id.id
                self.repo.add(customer)
                self.logger.logger.info(f'AnonymousFacade: customer add successfully')
            except:
                print("An Error occurred")
                raise Exception('UnknownError')
        else:
            print('customer object error')
            self.logger.logger.error(f'AnonymousFacade: customer {customer.id} already exist')
            raise Exception('CustomerAlreadyExist')
       
    def add_customer_without_add_user(self,customer):
        self.logger.logger.info(f'AnonymousFacade: adding customer by id {customer.id}')
        if customer is not None:
            try:
                self.repo.add(customer)
                self.logger.logger.info(f'AnonymousFacade: customer add successfully')
            except:
                print("An Error occurred")
                raise Exception('UnknowError')
        else:
            print('customer object error')
            raise Exception('CustomerObjectE')

    def add_user(self, user):
        user1 = self.repo.get_by_condition_lm(User, lambda query: query.filter(User.user_name == user.user_name).first())
        if user1 is not None:
            self.logger.logger.error(f'AnonymousFacade: UserName already exist!')
            raise Exception('UserNameAlreadyExist')
        elif user.user_name is None or user.password is None:
            self.logger.logger.error(f'AnonymousFacade: userName or password can not be none!')
            raise Exception('InvalidData')
        elif len(user.password) < 4:
            self.logger.logger.error(f'AnonymousFacade: password len need to be more then 4 letters!')
            raise Exception('PasswordShortError')
        else:
            try:
                self.repo.add(user)
                self.logger.logger.info(f'AnonymousFacade: user add sucessfuly!')
            except:
                self.logger.logger.error(f'AnonymousFacade: An Error Occurred!')
                raise Exception('UnkownError')
        


