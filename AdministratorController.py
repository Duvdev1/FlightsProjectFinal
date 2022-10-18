import uuid
from flask import Flask, make_response, request, render_template, Response, jsonify, current_app
import jwt
import uuid
from functools import wraps
from ThreadLocksMgmt import ThreadLocksMgmt
from RabbitProducerObject import RabbitProducerObject
from MyLogger import Logger


rabbitProducer = RabbitProducerObject('dbRequest')
threadLock = ThreadLocksMgmt.get_instance()
logger = Logger.get_instance()

app = Flask(__name__)

def adminToken(f):
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
            if payload['role'] == 'administrator':
                return f(payload, *args, **kwargs)
            else:
                jsonify({'message' : 'Invalid Token'}), 401
        except KeyError:
            return jsonify({'message' : 'Invalid Token'}), 401
        except (jwt.ExpiredSignature, jwt.InvalidTokenError, jwt.DecodeError):
            return jsonify({'message' : 'Invalid Token'})
    return decorated

@app.route("/")
@adminToken
def home(loginToken):
    return ''''
        <html>
            Ready!
        </html>
'''

@app.route('/customers', methods=['GET', 'POST', 'DELETE'])
@adminToken
def get_or_post_customer(loginToken):
    requestId = str(uuid.uuid4())
    if request.method == 'GET':
        rabbitProducer.publish({'id_': requestId, 'loginToken': loginToken, 'method': 'get', 'resource' : 'customer'})
        threadLock(requestId)
        answerFromHandler: dict = threadLock.get_answer(requestId=requestId)
        pass
    if request.method == 'POST':
        newData: dict = request.get_json()
        rabbitProducer.publish({'id_': requestId, 'loginToken' : loginToken, 'method':'post', 'resource':'customer', 'data' : newData})
        threadLock.thread_lock(requestId)
        answerFromHandler: dict = threadLock.get_answer(requestId=requestId)
        return make_response(jsonify(answerFromHandler), 201)
    if request.method == 'DELETE':
        customerId = request.form
        rabbitProducer.publish({'id_': requestId, 'loginToken':loginToken,'method':'delete','resource':'customer','data':customerId})
        threadLock.thread_lock(requestId)
        answerFromHandler: dict = threadLock.get_answer(requestId=requestId)
        return make_response(jsonify(answerFromHandler), 201)
        
@app.route('/airline', methods=['POST', 'DELETE'])
@adminToken
def add_or_delete_airline(loginToken):
    requestId = str(uuid.uuid4())
    if request.method == 'POST':
        newData: dict = request.get_json()
        rabbitProducer.publish({'id_': requestId, 'loginToken': loginToken, 'method':'post','resource':'airline','data':newData})
        threadLock.thread_lock(requestId)
        answerFromHandler: dict = threadLock.get_answer(requestId=requestId)
        return make_response(jsonify(answerFromHandler), 201)
    if request.method == 'DELETE':
        airlineId = request.form
        rabbitProducer.publish({'id_': requestId, 'loginToken':loginToken,'method':'delete','resource':'airline','data':airlineId})
        threadLock.thread_lock(requestId)
        answerFromHandler: dict=threadLock.get_answer(requestId=requestId)
        return make_response(jsonify(answerFromHandler), 201)
        
@app.route('/administrator', methods=['POST', 'DELETE'])
@adminToken
def add_or_delete_administrator(loginToken):
    requestId = str(uuid.uuid4())
    if request.method == 'POST':
        newData: dict = request.get_json()
        rabbitProducer.publish({'id_': requestId, 'loginToken':loginToken,'method':'post','resource':'administrator','data':newData})
        threadLock.thread_lock(requestId)
        answerFromHandler: dict=threadLock.get_answer(requestId=requestId)
        return make_response(jsonify(answerFromHandler), 201)
    if request.method == 'DELETE':
        administratorId = request.form
        rabbitProducer.publish({'id_': requestId,'loginToken':loginToken, 'method':'delete', 'resource':'administrator','data':administratorId})
        threadLock.thread_lock(requestId)
        answerFromHandler: dict=threadLock.get_answer(requestId=requestId)
        return make_response(jsonify(answerFromHandler), 201)
    
    
@app.route('/country', methods=['POST'])
@adminToken
def add_country(loginToken):
    requestId = str(uuid.uuid4())
    if request.method == 'POST':
        newData: dict = request.get_json()
        rabbitProducer.publish({'id_': requestId, 'loginToken':loginToken,'method':'post','resource':'country', 'data': newData})
        threadLock.thread_lock(requestId)
        answerFromHandler: dict=threadLock.get_answer(requestId=requestId)
        return make_response(jsonify(answerFromHandler), 201)
        

app.run(host='127.0.0.1', port=8443, debug=True)