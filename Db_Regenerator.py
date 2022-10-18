from AdministratorFacade import AdministratorFacade
from AirlineCompanyFacade import AirlineCompanyFacade
from AnonymousFacade import AnonymousFacade
from CustomerFacade import CustomerFacade
from DbRepo import DbRepo
from db2_config import local_session2, config
from LoaderToApp import loader
from User import User
import json 
from Country import Country
from AirlineCompany import AirlineCompany
from DbRepoPool import DbRepoPool

repoPool = DbRepoPool.get_instance()
repo = repoPool.get_connections()
anonymous_facade = AnonymousFacade(repo, config)
Lo = loader()

class Db_Regenerator():
    
    @staticmethod
    def clean_and_load():   
        # @@ reset the db @@ :
        Lo.db_reset()

        # @@ loading data base @@:

        # generate user role:
        Lo.generate_user_role()

        # generate login_token
        admin_user = User(user_name='roy_admin1', password='Aa12', email='a43621@gmail.com', user_role=1)
        anonymous_facade.add_user(admin_user)
        customer_user = User(user_name='roy_customer1', password='Aa12', email='gdfga@gmail.com', user_role=2)
        anonymous_facade.add_user(customer_user)
        airline_user = User(user_name='roy_airline1', password='Aa12', email='ahfghe@gmail.com', user_role=3)
        anonymous_facade.add_user(airline_user)
        admin_token = anonymous_facade.login('roy_admin1', 'Aa12')
        customer_token = anonymous_facade.login('roy_customer1', 'Aa12')
        airline_token = anonymous_facade.login('roy_customer1', 'Aa12')
        customer_facade = CustomerFacade(customer_token, repo, config)
        airline_company_facade = AirlineCompanyFacade(airline_token, repo, config)
        administrator_facade = AdministratorFacade(admin_token, repo, config)
        test = AirlineCompany(name='test',country_id=1,user_id=1)
        
        # load your desired number of countries to be added from json file:
        Lo.country_loader(5)

        # load your desired number of countries to be added from json file:
        Lo.user_loader(2)

        # load your desired number of customers to be added from json file:
        Lo.customer_loader(5)

        # load your desired number of administrator to be added from json file:
        Lo.administrator_loader(2)

        # load your number of airlines to be added from json file:
        Lo.airline_loader(2)

        # load flights to be generated:
        Lo.flights_loader(2)

        # load tickets per customer to be generated:
        Lo.tickets_loader(2)
        administrator_facade.add_airline(test)
        
