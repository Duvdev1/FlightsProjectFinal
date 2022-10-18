from Administrator import Administrator
from AirlineCompany import AirlineCompany
from Customer import Customer
from Exceptions import CustomerDoesNotExist, UnknownError, \
    NegativeDataError, AdministratorAlreadyExist, AirlineDoesNotExist, AdministratorDoesNotExist
from FacadeBase import FacadeBase
from Country import Country



class AdministratorFacade(FacadeBase):
    def __init__(self, login_token, repo, config):
        super().__init__(repo, config)
        self.role_name= 'Administrator'
        self._login_token = login_token

    def get_all_customers(self):
        self.logger.logger.info(f'AdministratorFacade: getting all customers')
        if not self.check_roll_is_correct():
            return
        customers = self.repo.get_all(Customer)
        if customers is None:
            print('there are no customers')
            self.logger.logger.error(f'AdministratorFacade: there are no customers')
            raise CustomerDoesNotExist
        else:
            try:
                return self.repo.get_all(Customer)
            except:
                self.logger.logger.error(f'AdministratorFacade: could not get customers')
                print("An unexpected Error occurred")
                raise UnknownError

    def add_airline(self, airline):
        self.logger.logger.info(f'AdministratorFacade: adding airline by id {airline.id}')
        if not self.check_roll_is_correct():
            return
        if airline.user_id is None or airline.country_id is None:
            raise Exception('UserId or CountryId can not be none')
        elif airline is not None:
            try:
                self.repo.add(airline)
                self.logger.logger.info(f'AdministratorFacade: airline add successfully')
            except:
                self.logger.logger.error(f'AdministratorFacade: Failed to add airline')
                print("An Error occurred")
                raise Exception('UnknownError')
        else:
            self.logger.logger.error(f'AdministratorFacade: airline id {airline.id} already exist')
            raise Exception('AirlineAlreadyExist')

    def add_administrator(self, administrator):
        self.logger.logger.info(f'AdministratorFacade: adding administrator by id {administrator.id}')
        if not self.check_roll_is_correct():
            return
        if administrator.first_name is None or administrator.user_id is None:
            raise Exception('FirstName or UserId can not be None!')
        elif administrator is not None:
            try:
                self.repo.add(administrator)
                self.logger.logger.info(f'AdministratorFacade: admin {administrator.id} add successfully')
            except:
                print("An Error occurred")
                self.logger.logger.error(f'AdmimistratorFacade: Failed to add administrator')
                raise Exception('UnknownError')
        else:
            self.logger.logger.error(f'AdministratorFacde: administrator id {administrator.id} already exist')
        
    def remove_airline_by_id(self, airlineID):
        self.logger.logger.info(f'AdministratorFacade: removing airline by id {airlineID}')
        if not self.check_roll_is_correct():
            return
        my_airlines = self.repo.get_by_column_value(AirlineCompany,AirlineCompany.id, airlineID)
        if len(my_airlines) == 0:
            print('airline does not exist')
            self.logger.logger.error(f'AdministratorFacade: airline {airlineID} does not exist')
            raise AirlineDoesNotExist
        else:
            my_airline = my_airlines[0]
            try:
                self.repo.delete()
                self.repo.delete_by_id(AirlineCompany, AirlineCompany.id, airlineID)
                self.logger.logger.info(f'AdministratorFacade: airline deleted successfully')
            except:
                print("An unexpected Error occurred")
                self.logger.logger.error(f'something went wrong')
                raise Exception('UnknownError')
        my_airline = self.repo.get_by_column_value(AirlineCompany,AirlineCompany.id, airlineID)[0]
        self.logger.logger.info(f'AirlineCompanyFacade: checking for airline removal by id {airlineID}')
        if my_airline is None:
            print('airline removed successfully')
            self.logger.logger.info(f'AirlineCompanyFacade: airline removed')
        
    def remove_airline(self, airline):
        self.logger.logger.info(f'AdministratorFacade: removing airline by id {airline.id}')
        if not self.check_roll_is_correct():
            return
        if (type(airline) != AirlineCompany):
            raise Exception('InvalidData')
        my_airline = self.repo.get_by_column_value(AirlineCompany,AirlineCompany.name, airline.name)[0]
        if my_airline is None:
            print('airline does not exist')
            self.logger.logger.error(f'AdministratorFacade: airline {airline.id} does not exist')
            raise Exception('AirlineDoesNotExist')
        elif my_airline:
            try:
                self.repo.delete_by_id(AirlineCompany, AirlineCompany.id, airline.id)
                self.logger.logger.info(f'AdministratorFacade: airline deleted successfully')
            except:
                print("An unexpected Error occurred")
                self.logger.logger.error(f'something went wrong')
                raise Exception('UnknownError')
        my_airline = self.repo.get_by_column_value(AirlineCompany,AirlineCompany.id, airline.id)
        self.logger.logger.info(f'AirlineCompanyFacade: checking for airline removal by id {airline.id}')
        if my_airline is None:
            print('airline removed successfully')
            self.logger.logger.info(f'AirlineCompanyFacade: airline removed')
        return True
            
    def remove_airline_name(self, airlineName):
        airline = self.repo.get_by_column_value(AirlineCompany,AirlineCompany.name, airlineName)[0]
        self.logger.logger.info(f'AdministratorFacade: removing airline by id {airline.id}')
        if not self.check_roll_is_correct():
            return
        if airline is None:
            print('airline does not exist')
            self.logger.logger.error(f'AdministratorFacade: airline {airline.id} does not exist')
            raise Exception('AirlineDoesNotExist')
        else:
            try:
                self.repo.delete_by_id(AirlineCompany, AirlineCompany.id, airline.id)
                self.logger.logger.info(f'AdministratorFacade: airline deleted successfully')
            except:
                print("An unexpected Error occurred")
                self.logger.logger.error(f'something went wrong')
                raise Exception('UnknownError')  
        print('airline removed successfully')
        self.logger.logger.info(f'AirlineCompanyFacade: airline removed')
        return True

    def remove_customer(self, customer):
        self.logger.logger.info(f'AdministratorFacade: removing customer by id {customer.id}')
        if not self.check_roll_is_correct():
            return
        if (type(customer) != Customer):
            raise Exception('InvalidData')
        my_customer = self.repo.get_by_column_value(Customer,Customer.id, customer.id)
        if my_customer is None:
            print('customer does not exist')
            self.logger.logger.error(f'customer {customer.id} does not exist')
            raise CustomerDoesNotExist
        elif my_customer:
            try:
                self.repo.delete_by_id(Customer, Customer.id, customer.id)
                self.logger.logger.info(f'AdministratorFacade: customer {Customer.id} deleted successfully')
            except:
                self.logger.logger.error(f'AdministratorFacade: could not remove customer')
                print("An unexpected Error occurred")
                raise UnknownError
        return True

    def remove_administrator(self, administrator):
        self.logger.logger.info(f'AdministratorFacade: removing administrator by id {administrator.id}')
        if not self.check_roll_is_correct():
            return
        if (type(administrator) != Administrator):
            raise Exception('InvalidData')
        my_administrator = self.repo.get_by_column_value(Administrator, Administrator.id, administrator.id)[0]
        if administrator.id < 0:
            print('admin id cannot be negative')
            self.logger.logger.error(f'AdministratorFacade: admin id cannot be negative')
            raise Exception('NegativeDataError')
        elif my_administrator is None:
            print('admin id does not exist')
            self.logger.logger.error(f'AdministratorFacade: admin id {administrator.id} does not exist')
            raise Exception('AdministratorDoesNotExist')
        elif my_administrator:
            try:
                self.repo.delete_by_id(Administrator, Administrator.id, administrator.id)
                self.logger.logger.info(
                    f'AdministratorFacade: administrator {Administrator.id} removed successfully')
            except:
                print("An unexpected Error occurred")
                self.logger.logger.error(f'AdministratorFacade: an error occurred')
                raise Exception('UnknownError')
        return True

    def add_country(self, name):
        self.logger.logger.info(f'AdministratorFacade: adding country by name {name}')
        if self._login_token.role != 'Administrator':
            self.logger.logger.error(f'The login token is not correct for this function,'
                                     f' the login token is "{self._login_token}"')
            return
        my_country = self.repo.get_by_column_value(Country, Country.name, name)
        print(my_country)
        self.repo.add_co(Country, name)
        if not my_country:
            try:
                self.repo.add_co(Country, name)
                self.repo.add(name)
                self.logger.logger.info(f'AdministratorFacade: country add successfully')
            except:
                self.logger.logger.error(f'AdministratorFacade: Failed to add country')
                print("An Error occurred")
                raise UnknownError
        else:
            self.logger.logger.error(f'AdministratorFacade: airline id {AirlineCompany.id} already exist')
            return "a"
    
