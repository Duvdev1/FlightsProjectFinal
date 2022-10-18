from datetime import datetime, timedelta
from Country import Country
from sqlalchemy import asc
from sqlalchemy import *
from sqlalchemy.orm import *
from User import User
from UserRole import UserRole
from AirlineCompany import AirlineCompany
from Customer import Customer
from Flights import Flights
from Administrator import Administrator
from Ticket import Ticket



def get_update_fields(table_name, data):
    return {column: getattr(data, column) for column in table_name.__table__.columns.keys()}


class DbRepo:

    def __init__(self, local_session):
        self.local_session = local_session

    def create_procedure(self, procedure_name):
        self.local_session.execute(f'CREATE or replace function {procedure_name}')
        self.local_session.expunge_all()
        self.local_session.close()

    def delete_procedure(self, procedure_name):
        self.local_session.execute(f'DROP PROCEDURE {procedure_name}')
        self.local_session.expunge_all()
        self.local_session.close()

    def reset_auto_inc(self, table_class):
        #ALTER SEQUENCE product_id_seq RESTART WITH 1453
        self.local_session.execute(f'TRUNCATE TABLE {table_class.__tablename__} RESTART IDENTITY CASCADE')
        #self.local_session.execute(f'ALTER SEQUENCE {table_class.__tablename__}_id_seq RESTART WITH 1')
        self.local_session.commit()
        self.local_session.expunge_all()
        self.local_session.close()
        
    
    # for get by name/id/value use get_by_column_value():
    def get_by_column_value(self, table_class, column_name, value):
        result = self.local_session.query(table_class).filter(column_name == value).all()
        self.local_session.expunge_all()
        self.local_session.close()
        return result
    
    def get_all(self, table_class):
        result = self.local_session.query(table_class).all()
        self.local_session.expunge_all()
        self.local_session.close()
        return result

    def get_all_limit(self, table_class, limit_num):
        result = self.local_session.query(table_class).limit(limit_num).all()
        self.local_session.expunge_all()
        self.local_session.close()
        return result

    def get_all_order_by(self, table_class, column_name, direction=asc):
        result = self.local_session.query(table_class).order_by(direction(column_name)).all()
        self.local_session.expunge_all()
        self.local_session.close()
        return result

    def get_by_condition(self, table_class, cond):
        query_result = self.local_session.query(table_class)
        result = cond(query_result)
        self.local_session.expunge_all()
        self.local_session.close()
        return result
    
    def get_by_condition_lm(self, table_class, cond):
        return cond(self.local_session.query(table_class))

    def add(self, one_row):
        self.local_session.add(one_row)
        self.local_session.commit()
        self.local_session.refresh(one_row)
        self.local_session.expunge_all()
        self.local_session.close()

    def add_co(self, table_class, name):
        self.local_session.insert(table_class).values(name=name)
        self.local_session.commit()
        self.local_session.refresh(name)
        self.local_session.expunge_all()
        self.local_session.close()

    def add_all(self, rows_list):
        self.local_session.add_all(rows_list)
        self.local_session.commit()
        self.local_session.refresh(rows_list)
        self.local_session.expunge_all()
        self.local_session.close()

    def delete_by_id(self, table_class, id_column_name, id):
        self.local_session.query(table_class).filter(id_column_name == id).delete(synchronize_session=False)
        self.local_session.commit()
        self.local_session.expunge_all()
        self.local_session.close()

    def delete_by_name(self, table_class, id_column_name, name):
        self.local_session.query(table_class).filter(id_column_name == name).delete(synchronize_session=False)
        self.local_session.commit()
        self.local_session.expunge_all()
        self.local_session.close()

    def delete_all(self, table_class):
        #ALTER SEQUENCE product_id_seq RESTART WITH 1453
        #self.local_session.execute(f'drop TABLE {table_class} cascade')
        self.local_session.delete(table_class)
        #self.local_session.query(table_class).delete()
        self.local_session.commit()
        self.reset_auto_inc(table_class)
        self.local_session.close()
        
    # data is json object, which all what i want to update will be included in.
    def update_by_id(self, table_class, data, id_):
        self.local_session.query(table_class).filter_by(id=id_).update(get_update_fields(table_class, data))
        self.local_session.commit()
        self.local_session.expunge_all()
        self.local_session.close()

    def update_by_column_value(self, table_class, column_name, value, data):
        self.local_session.query(table_class).filter(column_name == value).update(get_update_fields(table_class, data))
        self.local_session.commit()
        self.local_session.expunge_all()
        self.local_session.close()

    def get_by_ilike(self, table_class, column_name, exp):
        result = self.local_session.query(table_class).filter(column_name.ilike(exp)).all()
        self.local_session.expunge_all()
        self.local_session.close()
        return result
    
    def delete_all_tables(self):
        self.local_session.execute('DROP TABLE tickets CASCADE')
        self.local_session.execute('DROP TABLE customers CASCADE')
        self.local_session.execute('DROP TABLE flights CASCADE')
        self.local_session.execute('DROP TABLE airline_companies CASCADE')
        self.local_session.execute('DROP TABLE administrators CASCADE')
        self.local_session.execute('DROP TABLE countries CASCADE')
        self.local_session.execute('DROP TABLE users CASCADE')
        self.local_session.execute('DROP TABLE user_roles CASCADE')
        
    def reset_db(self):
        self.reset_auto_inc(Ticket)
        self.reset_auto_inc(Customer)
        self.reset_auto_inc(Flights)
        self.reset_auto_inc(AirlineCompany)
        self.reset_auto_inc(Administrator)
        self.reset_auto_inc(Country)
        self.reset_auto_inc(User)
        self.reset_auto_inc(UserRole)
        
        Afghanistan = Country(name='Afghanistan')
        Albania = Country(name='Albania')
        duv = Country(name='duvdev second land')
        duv2 = Country(name='duvdev land')
        Algeria = Country(name='Algeria')
        
        self.add(Afghanistan)
        self.add(Albania)
        self.add(duv)
        self.add(duv2)
        self.add(Algeria)
        
        self.add(UserRole(id=1, role_name='Administrator'))
        self.add(UserRole(id=2, role_name='Customer'))
        self.add(UserRole(id=3, role_name='AirlineCompany'))
        self.add(UserRole(id=4, role_name='Anonymous'))
        
        admin_user = User(user_name='roy_admins', password='Aa12', email='a2421@gmail.com', user_role=1)
        self.add(admin_user)
        customer_user = User(user_name='roy_customers', password='Aa12', email='a5432522@gmail.com', user_role=2)
        self.add(customer_user)
        airline_user = User(user_name='roy_airlines', password='Aa12', email='a432343@gmail.com', user_role=3)
        self.add(airline_user)
        airline_user2 = User(user_name='test', password='Aa12', email='a432343@gmail.com', user_role=3)
        self.add(airline_user2)
        
        customer1 = Customer(first_name='roy', last_name='duv',address='Hilll, Mayert and Wolf', phone_no='2014-12-25T04:06:27.981Z',
                             credit_card_no='Switzerland',user_id=2)
        self.add(customer1)
        admin1 = Administrator(first_name='dean', last_name='dean',user_id=1)
        self.add(admin1)
        airline1 = AirlineCompany(name='Private flight',country_id='2',user_id=3)
        airline2 = AirlineCompany(name='test',country_id='1',user_id=4)
        self.add(airline1)
        self.add(airline2)
        departureTime_1 = datetime.now() + timedelta(hours=2)
        landingTime_1 = datetime.now() + timedelta(hours=6)
        flight1 = Flights(airline_company_id=2, origin_country_id=5, destination_country_id= 5, departure_time= departureTime_1, 
                          landing_time= landingTime_1, remaining_tickets= 1) 
        self.add(flight1)
        departureTime_2 = datetime.now() + timedelta(hours=1)
        landingTime_2 = datetime.now() + timedelta(hours=3)
        flight2 = Flights(airline_company_id=1, origin_country_id=3, destination_country_id= 2, departure_time= departureTime_2, 
                          landing_time= landingTime_2, remaining_tickets= 5)
        self.add(flight2)
        departureTime_3 = datetime.now() + timedelta(hours=10)
        landingTime_3 = datetime.now() + timedelta(hours=24)
        flight3 = Flights(airline_company_id=1, origin_country_id=2, destination_country_id= 1, departure_time= departureTime_3, 
                          landing_time= landingTime_3, remaining_tickets= 5)
        self.add(flight3)

        self.local_session.close()
        
    def getFLightsByDestinationCountryId(self,countryId):
        result = self.local_session.query(Flights).filter(Flights.destination_country_id == countryId).all()
        self.local_session.expunge_all()
        self.local_session.close()
        return result
        
    def getFlightsByOriginCountryId(self, countryId):
        result = self.local_session.query(Flights).filter(Flights.origin_country_id == countryId).all()
        self.local_session.expunge_all()
        self.local_session.close()
        return result
    
    def getFlightsByLandingDate(self, landingDate):
        result = self.local_session.query(Flights).filter(extract('day', Flights.landing_time) == landingDate.day,
                                                          extract('month', Flights.landing_time) == landingDate.month, 
                                                          extract('year', Flights.landing_time) == landingDate.year).all()
        self.local_session.expunge_all()
        self.local_session.close()
        return result
    
    def getFlightsByDepartureDate(self, departureDate):
        result = self.local_session.query(Flights).filter(extract('day', Flights.departure_time) == departureDate.day,
                                                          extract('month', Flights.departure_time) == departureDate.month,
                                                          extract('year', Flights.departure_time) == departureDate.year).all() 
        self.local_session.expunge_all()
        self.local_session.close()
        return result
    
    def getDepartureFlightsByDelta(self, numHours : int):
        newTime = datetime.now() + timedelta(hours=numHours)
        result = self.local_session.query(Flights).filter(datetime.now() <= Flights.departure_time, Flights.departure_time <= newTime).all()
        self.local_session.expunge_all()
        self.local_session.close()
        return result
    
    def getLandingFlightsByDelta(self, numHours : int):
        newTime = datetime.now() + timedelta(hours=numHours)
        result = self.local_session.query(Flights).filter(datetime.now() <= Flights.landing_time ,Flights.landing_time <= newTime).all()
        self.local_session.expunge_all()
        self.local_session.close()
        return result
    
    def airlineByCountry(self, countryId):
        result = self.local_session.query(AirlineCompany).filter(AirlineCompany.country_id == countryId).all()
        self.local_session.expunge_all()
        self.local_session.close()
        return result
    
    def getFlightsByCustomer(self, customerId):
        flights = []
        tickets = self.local_session.query(Ticket).filter(Ticket.customer_id == customerId)
        for ticket in tickets:
            flights.append(ticket.flight)
        return flights