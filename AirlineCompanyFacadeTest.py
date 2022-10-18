import pytest
from AdministratorFacade import AdministratorFacade
from AirlineCompany import AirlineCompany
from AirlineCompanyFacade import AirlineCompanyFacade
from AnonymousFacade import AnonymousFacade
from DbRepo import DbRepo
from Flights import Flights
from LoginToken import LoginToken
from db2_config import config
from User import User
from DbRepoPool import DbRepoPool

repoPool = DbRepoPool.get_instance()
repo = repoPool.get_connections()
repo.reset_db()
#anonymous_facade = AnonymousFacade(repo, config)
#airline_company_facade = AirlineCompanyFacade(LoginToken(13, 'el al', 'AirlineCompany'), repo, config)
#administrator_facade = AdministratorFacade(LoginToken(15, 'admin', 'Administrator'),repo, config)


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

#scope='function',
@pytest.fixture(scope='function',autouse=True)
def reset_db():
    repo.reset_db()

def test_login_success(anonymous_facade_object):
    user = User(user_name= 'roy_admin1', password= 'Aa1222', email= 'duv', user_role= 1)
    user_name1 = 'roy_admin1'
    password = 'Aa1222'
    anonymous_facade_object.add_user(user)
    token = anonymous_facade_object.login(user_name1, password)
    assert  token != None

def test_update_airline_success_test(airlinecompany_facade_object):
    airline = repo.get_by_column_value(AirlineCompany, AirlineCompany.name, 'Private flight')[0]
    id_ = airline.id
    airline2 = AirlineCompany(id= id_ , name= 'el al', country_id= 4, user_id= 3) 
    airlinecompany_facade_object.update_airline(airline2)
    check_airline = repo.get_by_column_value(AirlineCompany, AirlineCompany.id, airline2.id)[0]
    originAirline = str(airline2)
    newAirline = str(check_airline)
    assert originAirline == newAirline

def test_update_flight_success_test(airlinecompany_facade_object, administrator_facade_object):
    airline = AirlineCompany(name= 'airline1',country_id= 2, user_id= 1)
    administrator_facade_object.add_airline(airline)
    airlineId = repo.get_by_column_value(AirlineCompany, AirlineCompany.name, 'airline1')[0]
    flight = Flights(id= 5,airline_company_id=airlineId.id , origin_country_id= 3, destination_country_id= 2,
                    departure_time= '2022-03-21 00:00:00', landing_time= '2022-07-08 00:00:00', remaining_tickets= 9)
    airlinecompany_facade_object.add_flight(flight)
    flight2 = Flights(id= 5, airline_company_id=airlineId.id, origin_country_id= 4, destination_country_id= 2,
                      departure_time= '2022-03-21 00:00:00', landing_time= '2022-07-08 00:00:00', remaining_tickets= 9)
    airlinecompany_facade_object.update_flight(flight2)
    check_flight = repo.get_by_column_value(Flights, Flights.id, flight2.id)[0]
    originFlight = str(flight2)
    newFlight = str(check_flight)
    assert originFlight == newFlight

def test_update_airline_negative_country_id_test(administrator_facade_object, airlinecompany_facade_object):
    airline1 =AirlineCompany(name= 'roy_airline',country_id= 3, user_id= 1)
    administrator_facade_object.add_airline(airline1)
    airlineId = repo.get_by_column_value(AirlineCompany, AirlineCompany.name, 'roy_airline')[0]
    airline = AirlineCompany(id=airlineId.id,name= 'roy_airline',country_id= -3, user_id= 1)
    with pytest.raises(Exception):
        assert airlinecompany_facade_object.update_airline(airline)

def test_update_flight_DoesNotExist_test(airlinecompany_facade_object):
    flight = Flights(airline_company_id= 6, origin_country_id= 5, destination_country_id= 5,
              departure_time= 7, landing_time= 3, remaining_tickets= 9)
    airlinecompany_facade_object.remove_flight(flight)
    with pytest.raises(Exception):
        airlinecompany_facade_object.update_flight(flight)
        assert airlinecompany_facade_object.update_flight(flight)

def test_update_airline_negative_user_id_test(airlinecompany_facade_object, administrator_facade_object):
    airline1 =AirlineCompany(name= 'el roy',country_id= 2, user_id= 1)
    administrator_facade_object.add_airline(airline1)
    airlineId = repo.get_by_column_value(AirlineCompany, AirlineCompany.name, 'el roy')[0]
    airline = AirlineCompany(id=airlineId.id, name= 'el roy',country_id= 2, user_id= -1)
    with pytest.raises(Exception):
        assert airlinecompany_facade_object.update_airline(airline)

def test_update_flight_Negative_id_test(airlinecompany_facade_object):
    flight_test = airlinecompany_facade_object.get_all_flights()
    print(flight_test)
    flight1 = repo.get_by_column_value(Flights, Flights.id, 1)[0]
    print(flight1)
    flight = Flights(id= -11, airline_company_id= flight1.airline_company_id, origin_country_id= flight1.origin_country_id, 
                     destination_country_id= flight1.destination_country_id,
              departure_time=flight1.departure_time, landing_time= flight1.landing_time, remaining_tickets= flight1.remaining_tickets)
    with pytest.raises(Exception):
        assert airlinecompany_facade_object.update_flight(flight)

def test_update_airline_DoesNotExist_test(administrator_facade_object, airlinecompany_facade_object):
    airline = AirlineCompany(name='test_update', country_id=1, user_id=1)
    administrator_facade_object.add_airline(airline)
    airlineId = repo.get_by_column_value(AirlineCompany, AirlineCompany.name, 'test_update')[0]
    administrator_facade_object.remove_airline(airlineId)
    with pytest.raises(Exception):
        assert airlinecompany_facade_object.update_airline(airlineId)
