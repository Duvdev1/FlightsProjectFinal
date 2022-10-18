import pytest
from Administrator import Administrator
from AdministratorFacade import AdministratorFacade
from AirlineCompany import AirlineCompany
from Customer import Customer
from User import User
from db2_config import config
from AnonymousFacade import AnonymousFacade
from LoginToken import LoginToken
from DbRepoPool import DbRepoPool

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
  

def test_get_all_customers(administrator_facade_object):
    customers = str(administrator_facade_object.get_all_customers())
    customersDb = str(repo.get_all(Customer))
    assert customers == customersDb
     
def test_add_airline_success_test(administrator_facade_object, anonymous_facade_object):
    user = User(user_name= 'jyg', password= '6777755', email= 'fff', user_role= 1)
    anonymous_facade_object.add_user(user)
    userID = repo.get_by_column_value(User, User.user_name, 'jyg')[0]
    airline = AirlineCompany(name= 'poplk', country_id= 2, user_id= 1)
    administrator_facade_object.add_airline(airline)
    check_airline = repo.get_by_column_value(AirlineCompany, AirlineCompany.name, airline. name)[0]
    assert str(check_airline) == str(airline)

def test_add_airline_failed_test(administrator_facade_object):
    with pytest.raises(Exception):
        airline = AirlineCompany(name='el al', country_id=2, user_id=None)
        assert administrator_facade_object.add_airline(airline)
    with pytest.raises(Exception):
        airline = None
        assert administrator_facade_object.add_airline(airline)
    with pytest.raises(Exception):
        airline = AirlineCompany(name= 'el al', country_id= 1, user_id= 1)
        assert administrator_facade_object.add_airline(airline)

def test_add_customer_success(anonymous_facade_object):
    user = User(user_name= 'testcu', password= '1529936', email= 'lolo@g.com', user_role= 1)
    anonymous_facade_object.add_user(user)
    UserID = repo.get_by_column_value(User, User.user_name, 'testcu')[0]
    customer = Customer(first_name= 'te',last_name= 'dg', address= 'tel aviv', phone_no= 12548,
                     credit_card_no= 646, user_id= UserID.id)
    anonymous_facade_object.add_customer_without_add_user(customer)
    check_customers = str(repo.get_by_column_value(Customer, Customer.phone_no, customer.phone_no)[0])
    assert check_customers == str(customer)

def test_add_customer_failed_test(administrator_facade_object):
    with pytest.raises(Exception):
        user = User(user_name= 'roy', password= '655999', email= 'duv', user_role= 6)
        customer = ""
        administrator_facade_object.add_customer(user, customer)
    with pytest.raises(Exception):
        user = ""
        customer = Customer(first_name= 'roy',last_name= 'duvdev', address= 'tel aviv', phone_no= 265,
                     credit_card_no= 646, user_id= 7)
        administrator_facade_object.add_customer(user, customer)
    with pytest.raises(Exception):
        user = User(user_name= 'roy', password= '0', email= 'duv', user_role= 6)
        customer = Customer(first_name= 'roy',last_name= 'duvdev', address= 'tel aviv', phone_no= 265,
                     credit_card_no= 646, user_id= 7)
        administrator_facade_object.add_customer(user, customer)
    with pytest.raises(Exception):
        user = User(user_name= 'roy', password= '0', email= 'duv', user_role= 6)
        customer = Customer(first_name= 'roy',last_name= 'duvdev', address= 'tel aviv', phone_no= 265,
                     credit_card_no= 646, user_id= 7)
        administrator_facade_object.add_user(user)
        administrator_facade_object.add_customer(user, customer)

def test_add_administrator_success_test(administrator_facade_object):
    admin = Administrator(first_name= 'roppppuy', last_name= 'duupppv', user_id= 2)
    administrator_facade_object.add_administrator(admin)
    check_admin = str(repo.get_by_column_value(Administrator, Administrator.id, admin.user_id)[0])
    assert check_admin == str(admin)

def test_add_administrator_failed_test(administrator_facade_object):
    with pytest.raises(Exception):
        admin = Administrator(first_name= None, last_name= 'druv', user_id= 2)
        administrator_facade_object.add_administrator(admin)
    with pytest.raises(Exception):
        admins = 'p'
        administrator_facade_object.add_administrator(admins)

def test_remove_airlineCompany_failed_test(administrator_facade_object):
    with pytest.raises(Exception):
        administrator_facade_object.remove_airline('a')
    with pytest.raises(Exception):
        administrator_facade_object.remove_airline(55)

def test_remove_customer_failed_test(administrator_facade_object):
     with pytest.raises(Exception):
        administrator_facade_object.remove_customer('a')
     with pytest.raises(Exception):
        administrator_facade_object.remove_customer(7)
        

def test_remove_administrator_failed_test(administrator_facade_object):
    with pytest.raises(Exception):
        administrator_facade_object.remove_administrator(1)
    with pytest.raises(Exception):
        admin = Administrator(id=-2, first_name='po', last_name='ll', user_id=2)
        administrator_facade_object.remove_administrator(admin)
           
def test_remove_customer_success_test(administrator_facade_object, anonymous_facade_object):
    customer = Customer(first_name= 'roooy',last_name='pp',address= 'tel aviv', phone_no= 265, credit_card_no= 646, user_id=4)
    anonymous_facade_object.add_customer_without_add_user(customer)
    check_customers = administrator_facade_object.remove_customer(customer)
    assert check_customers == True

def test_remove_administrator_success_test(administrator_facade_object):
    admin = Administrator(first_name= 'roiy', last_name= 'dukv', user_id= 4)
    administrator_facade_object.add_administrator(admin)
    check_admin = administrator_facade_object.remove_administrator(admin)
    assert check_admin == True


def test_remove_airlineCompany_success_test(administrator_facade_object):
    airline = AirlineCompany(name= 'el tel', country_id= 1, user_id= 1)
    administrator_facade_object.add_airline(airline)
    check_airline = administrator_facade_object.remove_airline_name('el tel')
    assert check_airline == True
