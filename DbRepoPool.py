#from db2_config import local_session2, config
from db_config import local_session, config
import time
import threading
from DbRepo import DbRepo

class DbRepoPool(object):
    _instance = None
    _lock_pool = threading.Lock()
    _lock = threading.Lock()
    _max_con = int(config["limit"]["max_con"])
    
    def __init__(self):
        raise RuntimeError('call get_instance!')
    
    @classmethod
    def get_instance(cls):
        if cls._instance:
            return cls._instance
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls.__new__(cls)
                cls._instance.connections = [DbRepo(local_session=local_session) for i in range(cls._max_con)]
            return cls._instance
    
    def return_connection(self, con):
        with self._lock_pool:
            self.connections.append(con)
    
    def get_max_possible_connections(cls):
        return cls._max_con
    
    def get_free_connections(self):
        return len(self.connections)
    
    def get_connections(self):
        while True:
            if len(self.connections) == 0:
                time.sleep(1)
                continue
            with self._lock_pool:
                if len(self.connections) > 0:
                    return self.connections.pop(0)