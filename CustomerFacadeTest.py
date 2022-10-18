import pytest
from AdministratorFacade import AdministratorFacade
from AirlineCompanyFacade import AirlineCompanyFacade
from AnonymousFacade import AnonymousFacade
from Customer import Customer
from CustomerFacade import CustomerFacade
from Ticket import Ticket
from db2_config import config
from DbRepoPool import DbRepoPool
from LoginToken import LoginToken
from User import User

repoPool = DbRepoPool.get_instance()
repo = repoPool.get_connections()
repo.reset_db()
anonymous_facade = AnonymousFacade(repo, config)
customer_facade = CustomerFacade(LoginToken(11, 'customer', 'Customer'), repo, config)
ticket =Ticket (flight_id= 1, customer_id= 1)
customer_facade.add_ticket(ticket)
ticketR = repo.get_by_column_value(Ticket, Ticket.flight_id, 1)[0]
checkTicket = customer_facade.remove_ticket(ticketR)

@pytest.fixture(scope='session')
def anonymous_facade_object():
    anonymous_facade = AnonymousFacade(repo, config)
    return anonymous_facade

@pytest.fixture(scope='session')
def airlinecompany_facade_object():
    airline_company_facade = AirlineCompanyFacade(LoginToken(13, 'el al', 'AirlineCompany'), repo, config)
    return airline_company_facade

@pytest.fixture(scope='session')
def administrator_facade_object():
    administrator_facade = AdministratorFacade(LoginToken(15, 'admin', 'Administrator'),repo, config)
    return administrator_facade

@pytest.fixture(scope='session')
def customer_facade_object():
    customer_facade = CustomerFacade(LoginToken(11, 'customer', 'Customer'), repo, config)
    return customer_facade

@pytest.fixture(scope='function',autouse=True)
def reset_db():
   repo.reset_db()

#the test doesn't work!!
def test_update_customer_success_test(customer_facade_object, anonymous_facade_object):
    user = User(user_name='customerTest', password='121212', email='email', user_role=2)
    anonymous_facade_object.add_user(user)
    userId = repo.get_by_column_value(User, User.user_name, 'customerTest')[0]
    customer = Customer(first_name= 'royy', last_name= 'duvdev', address= 'tel aviv', phone_no= 235,
                        credit_card_no= 152, user_id= userId.id)
    anonymous_facade_object.add_customer_without_add_user(customer)
    t = repo.get_by_column_value(Customer, Customer.first_name, 'royy')[0]
    customer2 = Customer(id = t.id,first_name= 'roy1', last_name= 'duvdev1', address= 'tel avivs', phone_no= 2354,
                        credit_card_no= 1521, user_id= userId.id)
    customer2_name = 'roy1'
    customer_facade_object.update_customer(customer2)
    update_customer = repo.get_by_column_value(Customer, Customer.first_name, customer2_name)[0]
    assert str(update_customer) == str(customer2)

def test_update_customer_not_exist_test(customer_facade_object):
    customer = Customer(first_name= 'roy12121', last_name= 'duvdev1', address= 'tel avivs', phone_no= 2354,
                credit_card_no= 1521, user_id= 1)
    with pytest.raises(Exception):
        assert customer_facade_object.update_customer(customer)


def test_update_customer_negative_user_id_test(customer_facade_object):
    customer1 = Customer(first_name= 'roy1', last_name= 'duvdev1', address= 'tel avivs', phone_no= 2354,
                credit_card_no= 1521, user_id= -1)
    with pytest.raises(Exception):
        assert customer_facade_object.update_customer(customer1)

def test_add_ticket_success_test(customer_facade_object, anonymous_facade_object, airlinecompany_facade_object):
    customer = Customer(first_name= 'royFl', last_name= 'duvdev1', address= 'tel avivs', phone_no= 2354,
                        credit_card_no= 1521, user_id= 1)
    anonymous_facade.add_customer_without_add_user(customer)
    customerId = repo.get_by_column_value(Customer, Customer.first_name, 'royFl')[0]
    ticket = Ticket(flight_id= 1, customer_id = customerId.id)
    customer_facade.add_ticket(ticket)
    tickets = customer_facade.get_tickets_by_customer(customer)
    assert str(ticket) == str(tickets)

def test_add_ticket_flightNotExist_test(customer_facade_object):
    ticket = Ticket(flight_id = 5, customer_id = 2)
    with pytest.raises(Exception):
        assert customer_facade_object.add_ticket(ticket)

def test_add_ticket_negative_customer_Id_test(customer_facade_object):
    ticket = Ticket(flight_id= 5, customer_id= -1)
    with pytest.raises(Exception):
        assert customer_facade_object.add_ticket(ticket)


def test_add_ticket_negative_flight_id_test(customer_facade_object):
    ticket = Ticket(flight_id= -1, customer_id= 2)
    with pytest.raises(Exception):
        assert customer_facade_object.add_ticket(ticket)

def test_remove_ticket_success_test(customer_facade_object):
    ticket =Ticket (flight_id= 1, customer_id= 1)
    customer_facade_object.add_ticket(ticket)
    ticketR = repo.get_by_column_value(Ticket, Ticket.flight_id, 1)[0]
    checkTicket = customer_facade_object.remove_ticket(ticketR)    
    assert checkTicket == True

def test_remove_ticket_negative_customer_id_test(customer_facade_object):
    ticket = Ticket(flight_id= 1, customer_id= -1)
    with pytest.raises(Exception):
        assert customer_facade_object.remove_ticket(ticket)

def test_remove_ticket_negative_flight_id_test(customer_facade_object):
    ticket =Ticket (flight_id= -1, customer_id= 1)
    with pytest.raises(Exception):
        assert customer_facade_object.remove_ticket(ticket)

def test_remove_ticket_DoesNotExist_test(customer_facade_object):
    ticket = Ticket(flight_id= 1, customer_id= 1)
    with pytest.raises(Exception):
        assert customer_facade_object.remove_ticket(ticket)