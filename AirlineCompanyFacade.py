from AirlineCompany import AirlineCompany
from Exceptions import FlightDoesNotExistException, AirlineDoesNotExist, \
    UnknownError, FlightAlreadyExistException, FlightAlreadyExistException, NegativeDataError
from FacadeBase import FacadeBase
from Flights import Flights


class AirlineCompanyFacade(FacadeBase):
    def __init__(self, login_token, repo, config):
        super().__init__(repo, config)
        self.role_name = 'AirlineCompany'
        self._login_token = login_token

    def add_flight(self, flight):
        self.logger.logger.info(f'AirlineCompanyFacade: adding {flight}')
        if not self.check_roll_is_correct():
            return
        my_flight = self.repo.get_by_column_value(Flights, Flights.id, flight.id)
        if my_flight:
            self.logger.logger.error(f'AirlineCompanyFacade: {flight.id} already exist')
            raise Exception('FlightAlreadyExistException')
        try:
            self.repo.add(flight)
            self.logger.logger.info(f'AirlineCompanyFacade: adding flight {flight.id} successes')
        except:
            self.logger.logger.error(f'AirlineCompanyFacade: adding flight {flight.id} to the db failed')
            raise Exception('UnknownError')

    def remove_flight(self, flight):
        self.logger.logger.info(f'AirlineCompanyFacade: removing flight by id {flight.id}')
        if not self.check_roll_is_correct():
            return
        my_flight = self.repo.get_by_column_value(Flights, Flights.id, flight.id)
        if my_flight is None:
            print('airline does not exist')
            self.logger.logger.error(f'AirlineCompanyFacade: flight {flight.id} does not exist')
            raise Exception('FlightDoesNotExistException')
        elif my_flight:
            try:
                self.repo.delete_by_id(Flights, Flights.id, flight.id)
                self.logger.logger.info(f'AirlineCompanyFacade: flight deleted successfully')
            except:
                print("An unexpected Error occurred")
                self.logger.logger.error(f'AirlineCompanyFacade: something went wrong')
                raise Exception('UnknownError')
        my_flight = self.repo.get_by_column_value(AirlineCompany, AirlineCompany.id, flight.id)
        self.logger.logger.info(f'AirlineCompanyFacade: checking for flight removal by id {flight.id}')
        if my_flight is None:
            print('airline removed successfully')
            self.logger.logger.info(f'AirlineCompanyFacade: flight removed')

    def get_flights_by_airline(self, airline):
        self.logger.logger.info(f'AirlineCompanyFacade: getting flight by id {airline.id}')
        if not self.check_roll_is_correct():
            return
        my_airline = self.repo.get_by_column_value(AirlineCompany, AirlineCompany.id, airline.id)
        if my_airline:
            try:
                return self.repo.get_by_column_value(Flights, Flights.airline_company_id, airline.id)
            except:
                self.logger.logger.error(f'airline {airline} does not exist')
                print("airline does not exist")
                raise Exception('AirlineDoesNotExist') 
            
    def updateAirlineById (self, airlineId, airline):
        self.logger.logger.info(f'AirlineCompanyFacade: updating airline {airline.id}')
        self.logger.logger.info(f'AirlineCompanyFacade: getting airline by id {airline.id}')
        if not self.check_roll_is_correct():
            return
        checkAirline = self.repo.get_by_column_value(AirlineCompany, AirlineCompany.id, airlineId)
        if checkAirline == None:
            raise Exception('AirlineDoesNotExist')
        else:
            self.repo.update_by_column_value(AirlineCompany, AirlineCompany.id, airlineId, airline)
        
    def update_airline(self, airline):
        self.logger.logger.info(f'AirlineCompanyFacade: updating airline {airline.id}')
        self.logger.logger.info(f'AirlineCompanyFacade: getting airline by id {airline.id}')
        if not self.check_roll_is_correct():
            return
        my_old_airline_id = self.repo.get_by_column_value(AirlineCompany, AirlineCompany.id, airline.id)[0]
        if airline.user_id < 1:
            self.logger.logger.error(f'AirlineCompanyFacade: could not update air cause negative user id')
            raise Exception('NegativeAirlineIdException')
        elif airline.country_id < 1:
            self.logger.logger.error(f'AirlineCompanyFacade: could not update air cause negative country id')
            raise Exception('NegativeCountryIdException')
        elif my_old_airline_id is not None:
            try:
                self.repo.update_by_column_value(AirlineCompany,AirlineCompany.id, airline.id, airline)
                #self.repo.update_by_id(AirlineCompany, airline, airline.id)
            except:
                self.logger.logger.error(f'AirlineCompanyFacade: could not update airline')
                print("An exception occurred when we try update customer")
                raise Exception('UnknownError')
        else:
            print("airline does not exist")
            self.logger.logger.error(f'AirlineCompanyFacade: airline does not exist')
            raise Exception('AirlineDoesNotExist') 
                       

    def update_flight(self, flights):
        self.logger.logger.info(f'AirlineCompanyFacade: updating flight')
        if not self.check_roll_is_correct():
            return
        my_old_flight_id = self.repo.get_by_column_value(Flights, Flights.id, flights.id)[0]
        if flights.id < 1:
            self.logger.logger.error(f'AirlineCompanyFacade: could not update flight because negative flight id')
            raise Exception('NegativeAirlineIdException')
        elif flights.airline_company_id < 1:
            self.logger.logger.error(f'AirlineCompanyFacade: could not update flight because negative company id')
            raise Exception('NegativeAirlineCompanyIdException')
        elif my_old_flight_id is not None:
            try:
                self.repo.update_by_id(Flights, flights, flights.id)
                self.logger.logger.info(f'AirlineCompanyFacade: updating flight by id')
            except:
                if my_old_flight_id is None:
                    print('flight does not exist')
                    raise Exception('FlightDoesNotExistException')
                else:
                    print("An exception occurred when we try update customer")
                    raise Exception('UnknownError')
