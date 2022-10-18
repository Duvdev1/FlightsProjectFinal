import uuid
from flask import Flask, make_response, request, render_template, Response, jsonify, current_app
import jwt
import uuid
from functools import wraps
from ThreadLocksMgmt import ThreadLocksMgmt
from RabbitProducerObject import RabbitProducerObject
from User import User


rabbitProducer = RabbitProducerObject('dbRequest')
threadLock = ThreadLocksMgmt.get_instance()

app = Flask(__name__)



@app.route("/")
def home():
    return ''''
        <html>
            Ready!
        </html>
'''

# to check
@app.route('/login', methods=['POST'])
def login():
    data = request.form
    username_ = data.get("username")
    password_ = data.get("password")
    if not data or not username_ or not password_:
        return make_response('username or password are required', 401)
    checkUser = DbRepo.get_by_condition(User, lambda query: query.filter(User.user_name == username_,
                                                                           User.password == password_).first())
    if checkUser is None:
        return make_response('username does not exist or worng password', 401)
    answer = anonymusFacade.login(username_, password_)
    token = jwt.encode({
        'publicID' : checkUser.id, 
        'exp' : datetime.utcnow() + timedelta(minutes=30)
        }, app.config['SECRET_KEY'])
    return make_response(jsonify({'token':token.decode('UTP-8')}), 201)

@app.route('/customer', methods=['POST'])
def add_customer(loginToken):
    newData: dict = request.get_json()
    requestId = str(uuid.uuid4())
    rabbitProducer.publish({'id_': requestId, 'loginToken': loginToken, 'method':'post','resource':'customer','data': newData})
    threadLock.thread_lock(requestId)
    answerFromHandler: dict = threadLock.get_answer(requestId=requestId)
    return make_response(jsonify(answerFromHandler),201)
    