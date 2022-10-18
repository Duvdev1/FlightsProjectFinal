import json
import threading
from RabbitConsumerObject import RabbitConsumerObject
from ThreadLocksMgmt import ThreadLocksMgmt

treaadLock = ThreadLocksMgmt.get_instance()

def main():
    rabbitConsumer = RabbitConsumerObject(q_name='dbAnswers', callback=callback)
    rabbitConsumer.consume()
    
    
def callback(ch, method, properties, body):
    data = json.loads(body)
    print(data)
    requestId = data['id']
    treaadLock.handler_answer_release_thread(requestId=requestId, data=data)
    
t = threading.Thread(target=main)
t.setDaemon(True)
t.start()
    