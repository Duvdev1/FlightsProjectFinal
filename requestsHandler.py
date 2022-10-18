import json
from RabbitConsumerObject import RabbitConsumerObject
from RabbitProducerObject import RabbitProducerObject
from ThreadLocksMgmt import ThreadLocksMgmt
from LoginToken import LoginToken
from MyLogger import Logger
from db2_config import config
from AnonymousFacade import AnonymousFacade
from AdministratorFacade import AdministratorFacade
from AirlineCompanyFacade import AirlineCompanyFacade
from CustomerFacade import CustomerFacade
from DbRepoPool import DbRepoPool
from Customer import Customer
from AirlineCompany import AirlineCompany
import time

# Params:
lockManager = ThreadLocksMgmt.get_instance()
rabbitProducer = RabbitProducerObject('dbRespons')
repoPool = DbRepoPool.get_instance()

def main():
    rabbit = RabbitConsumerObject(q_name='dbRequests', callback=callback)
    rabbit.consume()
    
def getLoginToken(loginTokenJson):
    loginToken = LoginToken(id= loginTokenJson['id_'], name=loginTokenJson['name'], role=loginTokenJson['role'])
    return loginToken
    
def callback(ch, method, properties, body):
    #dbRepo = repoPool.get_connections()
    request = json.loads(body)
    requestId = request['id']
    
    
    resource = request['resource']    
    method = request['method']
    
    if resource == 'administrator':
        loginToken = getLoginToken(request['loginToken'])
        dbRepo = repoPool.get_connections()
        administratorFacade = AdministratorFacade(loginToken, dbRepo, config)
        if method == 'delete':
            resourceId = request['data']
            try:
                administratorFacade.remove_administrator(resourceId)
                rabbitProducer.publish(json.dumps({'id_': requestId, 'error': None}))
            except Exception:
                rabbitProducer.publish(json.dumps({'id_': requestId, 'error': 'NegativeDataError'}))
                return
            except Exception:
                rabbitProducer.publish(json.dumps({'id_': requestId, 'error': 'WorngLoginToken'}))
                return
            finally:
                repoPool.return_connection(dbRepo)
        elif method == 'post':
            try:
                administratorFacade.add_administrator(administrator=request['data']['administrator'])
                rabbitProducer.publish(json.dumps({'id_': requestId, 'error': None}))
            except Exception:
                rabbitProducer.publish(json.dumps({'id_': requestId, 'error': 'NegativeDataError'}))
                return
            except Exception:
                rabbitProducer.publish(json.dumps({'id_': requestId, 'error': 'WorngLoginToken'}))
                return
            finally:
                repoPool.return_connection(dbRepo)
            
    elif resource == 'country':
        loginToken = getLoginToken(request['loginToken'])
        dbRepo = repoPool.get_connections()
        administratorFacade = AdministratorFacade(loginToken, dbRepo, config)
        anonymousFacade = AnonymousFacade(dbRepo, config)
        if method == 'post':
            try:
                administratorFacade.add_country(name= request['country']['name'])
                rabbitProducer.publish(json.dumps({'id_': requestId, 'error': None}))
            except Exception:
                rabbitProducer.publish(json.dumps({'id_': requestId, 'error': 'NegativeDataError'}))
                return
            except Exception:
                rabbitProducer.publish(json.dumps({'id_': requestId, 'error': 'WorngLoginToken'}))
                return
            finally:
                repoPool.return_connection(dbRepo)
            
    elif resource == 'customer':
        loginToken = getLoginToken(request['loginToken'])
        dbRepo = repoPool.get_connections()
        administratorFacade = AdministratorFacade(loginToken, dbRepo, config)
        customerFacade = CustomerFacade(loginToken,dbRepo, config)
        if method == 'get':
            if 'customerId' in request:
                try:
                    customer = dbRepo.get_by_column_value(Customer,Customer.id, request['customerId'])[0]
                    rabbitProducer.publish(json.dumps({'id_': requestId, 'error': None, 'data': customer}))
                    return
                except Exception:
                    rabbitProducer.publish(json.dumps({'id_': requestId, 'error':'negativeDataError'}))
                    return
                finally:
                    repoPool.return_connection(dbRepo)
            else:
                customers = administratorFacade.get_all_customers()
                customers = [customer.get_dictionary() for customer in customers]
                rabbitProducer.publish(json.dumps({'id_': requestId, 'error':None,'data':customers}))
                repoPool.return_connection(dbRepo)
        if method == 'post':
            try:
                administratorFacade.add_customer(customer=request['data']['customer'])
                rabbitProducer.publish(json.dumps({'id_': requestId, 'error': None}))
            except Exception:
                rabbitProducer.publish(json.dumps({'id_': requestId, 'error': 'NegativeDataError'}))
                return
            except Exception:
                rabbitProducer.publish(json.dumps({'id_': requestId, 'error': 'WorngLoginToken'}))
                return
            finally:
                repoPool.return_connection(dbRepo)
        if method == 'delete':
            resourceId = request['data']
            try:
                administratorFacade.remove_customer(resourceId)
                rabbitProducer.publish(json.dumps({'id_': requestId, 'error': None}))
            except Exception:
                rabbitProducer.publish(json.dumps({'id_': requestId, 'error': 'NegativeDataError'}))
                return
            except Exception:
                rabbitProducer.publish(json.dumps({'id_': requestId, 'error': 'WorngLoginToken'}))
                return
            finally:
                repoPool.return_connection(dbRepo)
        if method == 'patch':
            try:
                customerFacade.update_customer(request['data'])
                rabbitProducer.publish(json.dumps({'id_': requestId, 'error': None}))
            except Exception:
                rabbitProducer.publish(json.dumps({'id_': requestId, 'error':'negativeDataError'}))
                return
            except Exception:
                rabbitProducer.publish(json.dumps({'id_': requestId, 'error': 'worngToken'}))
                return
            finally:
                repoPool.return_connection(dbRepo)
            
    elif resource == 'airline':
        loginToken = getLoginToken(request['loginToken'])
        dbRepo = repoPool.get_connections()
        administratorFacade = AdministratorFacade(loginToken, dbRepo, config)
        airlineFacade = AirlineCompanyFacade(loginToken, dbRepo, config)
        if method == 'post':
            try:
                administratorFacade.add_airline(request['data'])
                rabbitProducer.publish(json.dumps({'id_': requestId, 'error':None}))
            except Exception:
                rabbitProducer.publish(json.dumps({'id_': requestId, 'error': 'NegativeDataError'}))
                return
            except Exception:
                rabbitProducer.publish(json.dumps({'id_': requestId, 'error': 'WorngLoginToken'}))
                return
            finally:
                repoPool.return_connection(dbRepo)
        if method == 'delete':
            resourceId = request['data']
            try:
                administratorFacade.remove_airline(resourceId)
                rabbitProducer.publish(json.dumps({'id_': requestId, 'error': None}))
            except Exception:
                rabbitProducer.publish(json.dumps({'id_': requestId, 'error': 'NegativeDataError'}))
                return
            except Exception:
                rabbitProducer.publish(json.dumps({'id_':requestId, 'error':'WorngToken'}))
                return
            finally:
                repoPool.return_connection(dbRepo)
        if method == 'get':
            if 'airlineId' in request:
                try:
                    airline = dbRepo.get_by_column_value(AirlineCompany, AirlineCompany.id, request['airlineId'])[0]
                    rabbitProducer.publish(json.dumps({'id_':requestId,'error':None,'data':airline}))
                    return
                except Exception:
                    rabbitProducer.publish(json.dumps({'id_':requestId,'error':'NegativeDataError'}))
                    return
                finally:
                    repoPool.return_connection(dbRepo)
            else:
                airlines = dbRepo.get_all('airline')
                airlines = [airline.get_dictionary() for airline in airlines]
                rabbitProducer.publish(json.dumps({'id_':requestId, 'error':None,'data':airlines}))
                repoPool.return_connection(dbRepo)
        if method == 'patch':
            try:
                airlineFacade.update_airline(request['data'])
                rabbitProducer.publish(json.dumps({'id_': requestId, 'error': None}))
            except Exception:
                rabbitProducer.publish(json.dumps({'id_':requestId,'error':'NegativeDataError'}))
                return
            except Exception:
                rabbitProducer.publish(json.dumps({'id_':requestId,'error':'worngToken'}))
            finally:
                repoPool.return_connection(dbRepo)
            
    elif resource == 'flight':
        loginToken = getLoginToken(request['loginToken'])
        dbRepo = repoPool.get_connections()
        airlineFacade = AirlineCompanyFacade(loginToken, dbRepo, config)
        if method == 'post':
            try:
                airlineFacade.add_flight(request['data'])
                rabbitProducer.publish(json.dumps({'id_': requestId, 'error':None}))
            except Exception:
                rabbitProducer.publish(json.dumps({'id_': requestId, 'error': 'NegativeDataError'}))
                return
            except Exception:
                rabbitProducer.publish(json.dumps({'id_':requestId,'error':'worngToken'}))
            finally:
                repoPool.return_connection(dbRepo)
        if method == 'delete':
            resourceId = request['data']
            try:
                airlineFacade.remove_flight(requestId)
                rabbitProducer.publish(json.dumps({'id_':requestId,'error':None}))
            except Exception:
                rabbitProducer.publish(json.dumps({'id_': requestId, 'error':'negativeDataError'}))
                return
            except Exception:
                rabbitProducer.publish(json.dumps({'id_':requestId,'error':'WorngToken'}))
                return
            finally:
                repoPool.return_connection(dbRepo)
        if method == 'patch':
            try:
                airlineFacade.update_flight(request['data'])
                rabbitProducer.publish(json.dumps({'id_': requestId,'error':None}))
            except Exception:
                rabbitProducer.publish(json.dumps({'id_':requestId,'error':'NegativeDataError'}))
                return
            except Exception:
                rabbitProducer.publish(json.dumps({'id_': requestId,'error':'WorngToken'}))
                return
            finally:
                repoPool.return_connection(dbRepo)
            
    elif resource == 'ticket':
         loginToken = getLoginToken(request['login_token'])
         dbRepo = repoPool.get_connections()
         customerFacade = CustomerFacade(loginToken, dbRepo, config)
         if method == 'post':
            try:
                 customerFacade.add_ticket(request['data'])
                 rabbitProducer.publish(json.dumps({'id_': requestId,'error':None}))
            except Exception:
                rabbitProducer.publish(json.dumps({'id_':requestId,'error':'negativeDataError'}))
                return
            except Exception:
                rabbitProducer.publish(json.dumps({'id_':requestId,'error':'worngToken'}))
                return
            finally:
                repoPool.return_connection(dbRepo)
         if method == 'delete':
             try:
                 customerFacade.remove_ticket(request['data'])
                 rabbitProducer.publish(json.dumps({'id_': requestId, 'error': None}))
             except Exception:
                 rabbitProducer.publish(json.dumps({'id_': requestId, 'error': ' NegativeDataError'}))
                 return
             except Exception:
                 rabbitProducer.publish(json.dumps({'id_': requestId, 'error': 'WorngToken'}))
                 return
             finally:
                 repoPool.return_connection(dbRepo)