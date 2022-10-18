from flask import Flask, make_response, request, render_template, Response, jsonify, current_app
import jwt
import uuid
from functools import wraps
from ThreadLocksMgmt import ThreadLocksMgmt
from RabbitProducerObject import RabbitProducerObject


rabbitProducer = RabbitProducerObject('dbRequest')
threadLock = ThreadLocksMgmt.get_instance()

app = Flask(__name__)

def airlineCompanyToken(f):
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
            if payload['role'] == 'airline company':
                return f(payload, *args, **kwargs)
            else:
                jsonify({'message' : 'Invalid Token'}), 401
        except KeyError:
            return jsonify({'message' : 'Invalid Token'}), 401
        except (jwt.ExpiredSignature, jwt.InvalidTokenError, jwt.DecodeError):
            return jsonify({'message' : 'Invalid Token'})
    return decorated

@app.route("/")
@airlineCompanyToken
def home(loginToken):
    return ''''
        <html>
            Ready!
        </html>
'''

@app.route('/flight', methods=['POST', 'DELETE', 'PATCH'])
@airlineCompanyToken
def get_or_delete_or_update_flight(loginToken):
    requestId = str(uuid.uuid4())
    if request.method == 'POST':
        newData : dict = request.get_json()
        rabbitProducer.publish({'id_': requestId, 'loginToken': loginToken, 'method':'post','resource':'flight','data': newData})
        threadLock.thread_lock(requestId)
        answerFromHandler: dict = threadLock.get_answer(requestId=requestId)
        return make_response(jsonify(answerFromHandler), 201)
    if request.method == 'DELETE':
        airlineId = request.form
        rabbitProducer.publish({'id_': requestId, 'loginToken':loginToken,'method':'delete','resource':'flight', 'data': airlineId})
        threadLock.thread_lock(requestId)
        answerFromHandler: dict = threadLock.get_answer(requestId=requestId)
        return make_response(jsonify(answerFromHandler),201)
    if request.method == 'PATCH':
        newData: dict = request.get_json()
        rabbitProducer.publish({'id_': requestId, 'loginToken':loginToken,'method':'patch', 'resource':'flight','data':newData})
        threadLock.thread_lock(requestId)
        answerFromHandler: dict = threadLock.get_answer(requestId=requestId)
        return make_response(jsonify(answerFromHandler),201)
       #Stop here 
app.route('/airline/<init:id>', methods=['GET'])
@airlineCompanyToken
def get_flight_by_airline(loginToken, countryId):
    requestId = str(uuid.uuid4())
    if request.method == 'GET':
        rabbitProducer.publish({'id_': requestId, 'loginToken':loginToken, 'method':'get','resource':'airline','data':countryId})
        threadLock.thread_lock(requestId)
        answerFromHandler: dict= threadLock.get_answer(requestId=requestId)
        pass
    
app.route('/airline', methods=['PATCH'])
@airlineCompanyToken
def update_airline(loginToken):
    requestId = str(uuid.uuid4())
    if request.method == 'PATCH':
        newData: dict = request.get_json()
        rabbitProducer.publish({'id_': requestId, 'loginToken':loginToken,'method':'patch','resource':'airline', 'data':newData})
        threadLock.thread_lock(requestId)
        answerFromHandler: dict= threadLock.get_answer(requestId=requestId)
        return make_response(jsonify(answerFromHandler),201)

