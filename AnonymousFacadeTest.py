import pytest
from User import User
from AdministratorFacade import AdministratorFacade
from AnonymousFacade import AnonymousFacade
from DbRepoPool import DbRepoPool
from db2_config import config
from LoginToken import LoginToken

repoPool = DbRepoPool.get_instance()
repo = repoPool.get_connections()
repo.reset_db()

@pytest.fixture(scope='session')
def anonymous_facade_object():
    anonymous_facade = AnonymousFacade(repo, config)
    return anonymous_facade

@pytest.fixture(scope='session')
def administrator_facade_object():
    administrator_facade = AdministratorFacade(LoginToken(15, 'admin', 'Administrator'),repo, config)
    return administrator_facade

@pytest.fixture(scope='function',autouse=True)
def reset_db():
   repo.reset_db()


def test_login_success_test(anonymous_facade_object):
    user = User(user_name= 'roy_1212', password= '6555', email= 'duv', user_role= 3)
    user_name1 = 'roy_1212'
    password = '6555'
    anonymous_facade_object.add_user(user)
    token = anonymous_facade_object.login(user_name1, password)
    assert token != None


def test_login_user_DoesNotExist_test(anonymous_facade_object):
    user_name1 = 'lolo'
    password = '121'
    with pytest.raises(Exception):
        assert anonymous_facade_object.login(user_name1, password)

def test_login_wrong_password_test(anonymous_facade_object):
    user = User(user_name= 'roy', password= '6555', email= 'duv', user_role= 1)
    anonymous_facade_object.add_user(user)
    password = '65224'
    user_name = 'roy'
    with pytest.raises(Exception):
        assert anonymous_facade_object.login(user_name, password)

def test_add_user_success_test(anonymous_facade_object):
    user = User(user_name= 'roy_test', password= '6555', email= 'duv', user_role= 2)
    anonymous_facade_object.add_user(user)
    my_user = repo.get_by_column_value(User, User.user_name, user.user_name)[0]
    assert str(user) == str(my_user)

def add_user_passwordTooShort_test(anonymous_facade_object):
    user = User(user_name= 'roy', password= '6', email= 'duv', user_role= 2)
    with pytest.raises(Exception):
        assert anonymous_facade_object.add_user(user)


def test_add_user_AlreadyExist_test(anonymous_facade_object):
    user = User (user_name= 'roy_exist', password= '3443344', email= 'duv', user_role= 2)
    anonymous_facade_object.add_user(user)
    with pytest.raises(Exception):
        assert anonymous_facade_object.add_user(user)
        
