from abc import ABC, abstractmethod
from datetime import datetime, date
from Country import Country
from AirlineCompany import AirlineCompany
from datetime import datetime
import params
from Flights import Flights
from MyLogger import Logger
from User import User
from DbRepoPool import DbRepoPool

class FacadeBase(ABC):

    @abstractmethod
    def __init__(self, repo, config):
        self.logger = Logger.get_instance()
        self.repool = DbRepoPool.get_instance()
        self.repo = self.repool.get_connections()
        self.config = config

    def get_all_flights(self):
        self.logger.logger.info(f'getting all flights from db')
        return self.repo.get_all(Flights)

    def get_flight_by_id(self, id):
        self.logger.logger.info(f'gets flight by id')
        if type(id) != int:
            self.logger.logger.error(f'Invalid input, the input need to be type int')
            raise Exception('InvalidInput')
        elif id < 1:
            self.logger.logger.error(f'flight id need to be more then 0')
            raise Exception('NegativeInput')
        else:
            self.logger.logger.info(f'get flight by id {id}')
            return self.repo.get_by_column_value(Flights, Flights.id, id)[0]

    def get_landing_flights_delta(self, hoursNum):
        self.logger.logger.info(f'gets flights by dekta time')
        if type(hoursNum) != int:
            self.logger.logger.error(f'the delta need to be number')
            raise Exception('InvalidInput')
        elif hoursNum < 0:
            self.logger.logger.error(f'the delta need to be more then 0')
            raise Exception('NegativeInput')
        else:
            try:
                self.logger.logger.info(f'gets all flights in {hoursNum}')
                return self.repo.getLandingFlightsByDelta(hoursNum)
            except:
                self.logger.logger.error(f'unknow error')
                raise Exception('AnError')     
        
    def get_departure_flights_delta(self, hoursNum):
        self.logger.logger.info(f'gets all flights in delta time')
        if type(hoursNum) != int:
            self.logger.logger.error(f'the delta need to be number')
            raise Exception('InvalidInput')
        elif hoursNum < 0:
            self.logger.logger.error(f'the delta need to be more the 1')
            raise Exception('NegativeInput')
        else:
            try:
                self.logger.logger.info(f'gets all flights in dellta time {hoursNum}')
                return self.repo.getDepartureFlightsByDelta(hoursNum)
            except:
                self.logger.logger.error(f'UnknowError')
                raise Exception('AnError')  
        
    def get_flights_by_parameters(self, origin_country_id, destination_country_id, date):
        self.logger.logger.info(f'gets flights by params')
        return self.repo.get_by_condition(Flights,
                                          lambda query: query.filter
                                          (Flights.origin_country_id == origin_country_id and
                                           Flights.destination_country_id == destination_country_id and
                                           Flights.departure_time == date))

    def get_flights_by_destination_country(self, countryId):
        self.logger.logger.info(f'gets flights by destination country')
        if type(countryId) != int:
            self.logger.logger.error(f'country id need to be number')
            raise Exception('InvalidInput')
        elif countryId < 1:
            self.logger.logger.error(f'country id need to be bigger then 0')
            raise Exception('NegativeInput')
        else:
            self.logger.logger.info(f'gets all flights of destination country {countryId}')
            return self.repo.getFLightsByDestinationCountryId(countryId)
        
    def get_flights_by_origin_country(self, countryId):
        self.logger.logger.info(f'gets all flights by origin country id')
        if type(countryId) != int:
            self.logger.logger.error(f'the country id need to be number')
            raise Exception('InvalidData')
        elif countryId < 1:
            self.logger.logger.error(f'country id need to be more then 0')
            raise Exception('NegativeData')
        else:
            self.logger.logger.info(f'gets all flights by origin country id {countryId}')
            return self.repo.getFlightsByOriginCountryId(countryId)
        
    def get_flights_by_landing_date(self, lanYear, lanMonth, lanDay):
        # 2022-10-11 17:23:04.601053
        if type(lanYear) != int or type(lanMonth) != int or type(lanDay) != int :
            raise Exception('InvalidInput')
        elif lanDay < 1 or lanDay > 31:
            raise Exception('DayNeedToBeBetween 1 to 31')
        elif lanMonth < 1 or lanMonth > 12:
            raise Exception('MonthNeedToBeBetween 1 to 12')
        elif lanYear < 2021 or lanYear > 2024:
            raise Exception('YearNeedToBeBetween 2022 to 2023')
        else:
            lanDay_ = str(lanDay)
            lanMonth_ = str(lanMonth)
            lanYear_ = str(lanYear)
            dateString = str(lanYear_+'-'+lanMonth_+'-'+lanDay_)
            date = date.fromisoformat(dateString)
            return self.repo.getFlightsByLandingDate(date)
        
    def get_flights_by_departure_date(self, lanYear, lanMonth, lanDay):
        if type(lanYear) != int or type(lanMonth) != int or type(lanDay) != int:
            raise Exception('InvalidInput')
        elif lanDay < 1 or lanDay > 31:
            raise Exception('DayNeedToBeBetween 1 to 31')
        elif lanMonth < 1 or lanMonth > 12:
            raise Exception('MonthNeedToBeBetween 1 to 12')
        elif lanYear < 2021 or lanYear > 2024:
            raise Exception('YearNeedToBeBetween 2022 to 2023')
        else:
            lanDay_ = str(lanDay)
            lanMonth_ = str(lanMonth)
            lanYear_ = str(lanYear)
            dateString = str(lanYear_+'-'+lanMonth_+'-'+lanDay_)
            date = date.fromisoformat(dateString)
            return self.repo.getFlightsByDepartureDate(date)
        
    def get_flights_by_customer(self, customerId):
        if type(customerId) != int:
            raise Exception('InvalidInput')
        elif customerId < 1:
            raise Exception('NegativeData')
        else:
            return self.repo.getFlightsByCustomer(customerId)

    def get_airline_by_country(self, countryId):
        if type(countryId) != int:
            raise Exception('InvalidData')
        elif countryId < 1 :
            raise Exception('NegativeData')
        else:
            return self.repo.getFlightsByCustomer(countryId)
        
    def get_all_airlines(self):
        return self.repo.get_all(AirlineCompany)

    def get_airline_by_id(self, id):
        return self.repo.get_by_column_value(AirlineCompany, AirlineCompany.id, id)[0]

    def add_airline(self, airline):
        self.repo.add(airline)

    def get_all_countries(self):
        return self.repo.get_all(Country)

    def get_country_by_id(self, id):
        return self.repo.get_by_column_value(Country, Country.id, id)[0]

    def add_user(self, user):
        my_user = self.repo.get_by_column_value(User, User.user_name, user.user_name)[0]
        if my_user:
            self.logger.error(f'User {user.user_name} already exist')
            raise Exception('UserAlreadyExistException')
        elif len(user.password) <= params.len1:
            self.logger.error(f'user password must be longer that 4 char')
            raise Exception('PasswordTooShortException')
        try:
            self.repo.add(user)
            self.logger.logger.info(f'adding user {user.user_name} successes')
            return user
        except:
            self.logger.logger.error(f'adding user {user.user_name} to the db failed')
            print('failed to add customer')
            raise Exception('UnknownError')
    
    def check_roll_is_correct(self):
        if self._login_token.role != self.role_name:
            self.logger.logger.error(f'The login token is not correct for this function,'
                                     f' the login token is "{self._login_token}"')
            return False
        else:
            return True