import json
from AdministratorFacade import AdministratorFacade
from Country import Country, ACountry
from DbRepo import DbRepo
from AirlineCompany import AirlineCompany
from Customer import Customer
from Administrator import Administrator
from Flights import Flights
from Ticket import Ticket
from User import User
from db2_config import config, local_session2
#from db_config import config, local_session
from UserRole import UserRole
from AnonymousFacade import AnonymousFacade
from AirlineCompanyFacade import AirlineCompanyFacade
from CustomerFacade import CustomerFacade
from DbRepoPool import DbRepoPool
import random
import datetime

class loader:
    def __init__(self):
        self.repool = DbRepoPool.get_instance()
        self.dbRepo = self.repool.get_connections()
        self.anonymous_facade = AnonymousFacade(self.dbRepo, config)
        #self.db_reset()
        #self.generate_user_role()
        admin_user = User(user_name='roy_admins', password='Aa12', email='a2421@gmail.com', user_role=1)
        self.anonymous_facade.add_user(admin_user)
        admin_token = self.anonymous_facade.login('roy_admins', 'Aa12')
        customer_user = User(user_name='roy_customers', password='Aa12', email='a5432522@gmail.com', user_role=2)
        self.anonymous_facade.add_user(customer_user)
        customer_token = self.anonymous_facade.login('roy_customers', 'Aa12')
        airline_user = User(user_name='roy_airlines', password='Aa12', email='a432343@gmail.com', user_role=3)
        self.anonymous_facade.add_user(airline_user)
        airline_token = self.anonymous_facade.login('roy_airlines', 'Aa12')
        self.customer_facade = CustomerFacade(customer_token, self.dbRepo, config)
        self.airline_facade = AirlineCompanyFacade(airline_token, self.dbRepo, config)
        self.administrator_facade = AdministratorFacade(admin_token, self.dbRepo, config)

    def db_reset(self):
        self.dbRepo.delete_all(Ticket)
        self.dbRepo.delete_all(Customer)
        self.dbRepo.delete_all(Flights)
        self.dbRepo.delete_all(AirlineCompany)
        self.dbRepo.delete_all(Administrator)
        self.dbRepo.delete_all(Country)
        self.dbRepo.delete_all(User)
        self.dbRepo.delete_all(UserRole)
        

    def generate_user_role(self):
        self.dbRepo.add(UserRole(id=1, role_name='Administrator'))
        print("at")
        self.dbRepo.add(UserRole(id=2, role_name='Customer'))
        print("at")
        self.dbRepo.add(UserRole(id=3, role_name='AirlineCompany'))
        print("at")
        self.dbRepo.add(UserRole(id=4, role_name='Anonymous'))
        print("at")

    def user_loader(self, number):
        f = open('user.json')
        j = json.load(f)
        num = 1
        for user in j:
            if number >= num:
                user1 = User(user_name=user['user_name'], password=user['password'], email=user['email'],
                            user_role=4)
                self.anonymous_facade.add_user(user1)
                num += 1
            else:
                break

    def customer_loader(self, number):
        f = open('customer.json')
        j = json.load(f)
        num = 1
        for customer in j:
            if number >= num:
                customer1 = Customer(first_name=customer['first_name'], last_name=customer['last_name'],
                                     address=customer['address'], phone_no=customer['phone_no'],
                                     credit_card_no=customer['credit_card_no'])
                user_name = customer['first_name'] + '_' + customer['last_name']
                print(user_name)
                password = 'Aa123456'
                email = customer['first_name'] + '_' + customer['last_name'] + '@gmail.com'
                user1 = User(user_name=user_name, password=password, email=email, user_role=2)
                self.anonymous_facade.add_customer(user1, customer1)
                num += 1
            else:
                break

    def administrator_loader(self, number):
        f = open('administrator.json')
        j = json.load(f)
        num = 1
        for admin in j:
            if number >= num:
                admin1 = Administrator(first_name=admin['first_name'], last_name=admin['last_name'])
                user_name = admin['first_name'] + '_' + admin['last_name']
                print(user_name)
                password = 'Aa123456'
                email = admin['first_name'] + '_' + admin['last_name'] + '@gmail.com'
                user1 = User(user_name=user_name, password=password, email=email, user_role=1)
                self.anonymous_facade.add_user(user1)
                admin1.user_id = user1.id
                self.administrator_facade.add_administrator(admin1)
                num += 1
            else:
                break

    def country_loader(self, number):
        num = 1
        file = open('countries.json')
        j = json.load(file)
        for country in j:
            if number >= num:
                add_country = ACountry(name=country['name'])
                print(country['name'])
                print(add_country)
                self.dbRepo.add(add_country)
                num += 1
            else:
                break

    def airline_loader(self, number):
        f = open('airline_companies.json')
        j = json.load(f)
        num = 1
        countries = self.dbRepo.get_all(Country)
        print(countries)
        size = len(list(countries))
        print(size)
        for airline in j:
            if number >= num:
                print(size)
                randi = (random.randint(1, (size - 1)))
                print(randi)
                p = countries[randi]
                country_id = p.id
                print(country_id)
                airline1 = AirlineCompany(name=airline['name'], country_id=country_id)
                user_name = airline['name'] + '01'
                print(user_name)
                password = 'Aa123456'
                email = airline['name'] + '@gmail.com'
                user1 = User(user_name=user_name, password=password, email=email, user_role=3)
                self.anonymous_facade.add_user(user1)
                airline1.user_id = user1.id
                self.administrator_facade.add_airline(airline1)
                num += 1
            else:
                break

    def flights_loader(self, number):
        countries = self.dbRepo.get_all(Country)
        print(countries)
        airline_companys = self.dbRepo.get_all(AirlineCompany)
        print(airline_companys)
        size_co = len(list(countries))
        for airline in airline_companys:
            airline_id = airline.id
            print(airline_id)
            for x in range(0, number):
                print(x)
                randi_1 = (random.randint(0, (size_co - 1)))
                randi_2 = (random.randint(0, (size_co - 1)))
                print(randi_2, randi_1)
                origin_country = countries[randi_1]
                origin_id = origin_country.id
                while randi_2 == randi_1:
                    randi_2 = (random.randint(1, (size_co - 1)))
                destination_country = countries[randi_2]
                dest_id = destination_country.id
                day_random = random.randint(1, 27)
                month_random = random.randint(1, 11)
                print(day_random)
                print(month_random)
                if day_random <= 27:
                    departure_time = datetime.date(2022, month_random, day_random)
                    day_random += 1
                    landing_time = datetime.datetime(2022, month_random, day_random)
                else:
                    landing_time = datetime.datetime(2022, month_random, day_random)
                    day_random -= 1
                    departure_time = datetime.datetime(2022, month_random, day_random)
                flight = Flights(airline_company_id=airline_id, origin_country_id=origin_id,
                                 destination_country_id=dest_id, departure_time=departure_time,
                                 landing_time=landing_time,
                                 remaining_tickets=0)
                self.airline_facade.add_flight(flight)
                print(f'this is the flights: {flight}')

    def tickets_loader(self, number):
        flights = self.dbRepo.get_all(Flights)
        print(flights)
        customers = self.dbRepo.get_all(Customer)
        print(customers)
        size_co = len(list(flights))
        for i in customers:
            customer_id = i.id
            print(customer_id)
            for x in range(0, number):
                print(x)
                randi_1 = (random.randint(0, (size_co - 1)))
                print(randi_1)
                flight_place = flights[randi_1]
                flight_id = flight_place.id
                print(flight_place)
                print(flight_id)
                ticket = Ticket(flight_id=flight_id, customer_id=customer_id)
                print(ticket)
                self.customer_facade.add_ticket(ticket)
                print(f'this is the tickets: {ticket}')
