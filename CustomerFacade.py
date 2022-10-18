from User import User
from Customer import Customer
from Exceptions import TicketNotFoundException, UnknownError, \
    CustomerDoesNotExist, NegativeDataError, FlightDoesNotExistException
from FacadeBase import FacadeBase
from Ticket import Ticket
from Flights import Flights


class CustomerFacade(FacadeBase):

    def __init__(self, login_token, repo, config):
        super().__init__(repo, config)
        self.role_name= 'Customer'
        self._login_token = login_token

    def update_customer(self, customer):
        self.logger.logger.info(f'CustomerFacade: updating customer {customer}')
        if not self.check_roll_is_correct():
            return
        # here is the problem
        if customer.id < 0 or customer.user_id < 0:
            raise Exception('InvalidInput')
        my_customer = self.repo.get_by_column_value(Customer, Customer.id, customer.id)[0]
        if my_customer is None:
            self.logger.logger.error(f'CustomerFacade: Customer dose not exist!')
            raise Exception('CustomerDoseNotExist')
        else:
            try:
                self.repo.update_by_column_value(Customer,Customer.id , customer.id, customer)
            except:
                self.logger.logger.error(f'CustomerFacade: customer could not be updated')
                print("An exception occurred when we try update customer")
                raise Exception('UnkownError')
       

    def add_ticket(self, ticket):
        self.logger.logger.info(f'CustomerFacade: adding ticket {ticket}')
        if not self.check_roll_is_correct():
            return
        if ticket.customer_id < 0:
            self.logger.logger.error(f'CustomerFacade: customer id is negative')
            raise Exception('CustomerIdCanNotBeNegative')
        elif ticket.flight_id < 0:
            self.logger.logger.error(f'CustomerFacade: flight id is negative')
            raise Exception('FlightIdCanNotBeNegative')
        customer = self.repo.get_by_column_value(Customer, Customer.id, ticket.customer_id)[0]
        flight = self.repo.get_by_column_value(Flights, Flights.id, ticket.flight_id)[0]
        if customer is None or flight is None:
            self.logger.logger.error(f'CustomerFacade: customer or flight are not exist')
            raise Exception('CustomerOrFlightAreNotExist')
        else:
            try:
                self.logger.logger.info(f'CustomerFacade: adding ticket')
                self.repo.add(ticket)
                self.logger.logger.info(f'CustomerFacade: ticket add successfully')
                print('ticket add successfully')
            except Exception:
                self.logger.logger.error(f'CustomerFacade: unexpected error')
                print("An exception occurred when we try add ticket")
                raise Exception('UnknowError')

    def remove_ticket(self, ticket):
        self.logger.logger.info(f'CustomerFacade: removing ticket {ticket}')
        if not self.check_roll_is_correct():
                return
        my_ticket = self.repo.get_by_column_value(Ticket, Ticket.id, ticket.id)[0]
        if my_ticket is None:
            print("ticket does not exist, failed to remove")
            raise Exception('TicketNotFoundException')
        else:
            try:
                self.logger.logger.info(f'CustomerFacade: deleting ticket by id {ticket.id}')
                self.repo.delete_by_id(Ticket, Ticket.id, ticket.id)
            except:
                if Ticket.id:
                    self.logger.logger.error(f'CustomerFacade: could not remove ticket')
                    raise Exception('UnknownError')
        return True

    def get_tickets_by_customer(self, customer):
        self.logger.logger.info(f'CustomerFacade: getting tickets by customer id {customer.id}')
        if not self.check_roll_is_correct():
            return
        my_customer = self.repo.get_by_column_value(Customer, Customer.id, customer.id)[0]
        if customer.id < 0:
            self.logger.logger.error(f'CustomerFacade: customer id is negative')
            print("customer id is negative")
            raise Exception('NegativeDataError')
        elif my_customer.id != customer.id:
            self.logger.logger.error(f'CustomerFacade: get_tickets_by_customer - customer id is not yours')
        elif my_customer is None:
            print('customer does not exist')
            self.logger.logger.error(f'CustomerFacade: customer {customer.id} does not exist')
            raise Exception('CustomerDoesNotExist')
        else:
            try:
                return self.repo.get_by_column_value(Ticket, Ticket.customer_id, customer.id)[0]
            except:
                self.logger.logger.error(f'something went wrong, unable to get ticket by customer')
                print("could not get ticket, something went wrong")
                raise UnknownError

