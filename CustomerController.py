from flask import Flask, make_response, request, render_template, Response, jsonify, current_app
import jwt
import uuid
from functools import wraps
from ThreadLocksMgmt import ThreadLocksMgmt
from RabbitProducerObject import RabbitProducerObject


rabbitProducer = RabbitProducerObject('dbRequest')
threadLock = ThreadLocksMgmt.get_instance()

app = Flask(__name__)

def customerToken(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            token = token.removeprefix('Bearer')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'])
            if payload['role'] == 'customer':
                return f(payload, *args, **kwargs)
            else:
                jsonify({'message' : 'Invalid Token'}), 401
        except KeyError:
            return jsonify({'message' : 'Invalid Token'}), 401
        except (jwt.ExpiredSignature, jwt.InvalidTokenError, jwt.DecodeError):
            return jsonify({'message' : 'Invalid Token'})
    return decorated

@app.route("/")
@customerToken
def home(loginToken):
    return ''''
        <html>
            Ready!
        </html>
'''

@app.route('/ticket', methods=['POST', 'DELETE'])
@customerToken
def add_or_remove_ticket(loginToken):
    requestId = str(uuid.uuid4())
    if request.method == 'DELETE':
        ticketId = request.get_json()
        rabbitProducer.publish({'id_': requestId, 'loginToken': loginToken, 'method':'delete','resource':'ticket','data':ticketId})
        threadLock.thread_lock(requestId)
        answerFromHandler: dict = threadLock.get_answer(requestId=requestId)
        return make_response(jsonify(answerFromHandler),201)
    if request.method == 'POST':
        newData: dict = request.get_json()
        rabbitProducer.publish({'id_': requestId, 'loginToken':loginToken,'method':'post','resource':'ticket','data':newData})
        threadLock.thread_lock(requestId)
        answerFromHandler: dict = threadLock.get_answer(requestId=requestId)
        return make_response(jsonify(answerFromHandler),201)
        
@app.route('/customer', methods=['PATCH'])
@customerToken
def update_customer(loginToken):
    requestId = str(uuid.uuid4())
    if request.method == 'PATCH':
        newData: dict = request.get_json()
        rabbitProducer.publish({'id_': requestId, 'loginToken': loginToken,'method':'patch','resource':'customer','data': newData})
        threadLock.thread_lock(requestId)
        answerFromHandler: dict = threadLock.get_answer(requestId=requestId)
        return make_response(jsonify(answerFromHandler),201)
        
@app.route('/customer/<int:id>', methods=['GET'])
@customerToken
def get_ticket_by_customer(loginToken, customerId):
    requestId = str(uuid.uuid4())
    if request.method == 'GET':
        rabbitProducer.publish({'id_': requestId, 'loginToken':loginToken,'method':'get', 'resource':'customer', 'customerId': id})
        threadLock.thread_lock(requestId)
        answerFromHandler: dict = threadLock.get_answer(requestId=requestId)

app.run(host='127.0.0.1', port=8443, debug=True)