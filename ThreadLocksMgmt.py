from threading import Lock, Event

class ThreadLocksMgmt:
    _instance = None
    _lock = Lock()
    _lockDictLock = Lock()
    _answersFromCoreLock = Lock()
    
    def __init__(self):
        self.locksDict = {}
        self.answersFromCoreDict = {}
        raise RuntimeError('call def instance')
        
    @classmethod
    def get_instance(cls):
        if cls._instance:
            return cls._instance
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls.__new__(cls)
                cls._instance.locks_dict = {}
                return cls._instance
            else:
                return cls._instance
            
    def thread_lock(self, requestId: str):
        event = Event()
        with self._lockDictLock:
            self.locksDict[requestId] = event
        event.wait()
        
    def handler_answer_release_thread(self, requestId: str, data: dict):
        with self._answersFromCoreLock:
            self.answersFromCoreDict[requestId] = data
        with self._lockDictLock:
            event = self.locksDict.pop(requestId)
        event.set()
        
    def get_answer(self, requestId: str):
        with self._answersFromCoreLock:
            return self.answersFromCoreDict.pop(requestId)
        
    
            