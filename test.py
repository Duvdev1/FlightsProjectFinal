from flask import Flask, render_template, jsonify, request, make_response
from flask_cors import CORS
import json
from db2_config import config
from DbRepoPool import DbRepoPool
from RabbitProducerObject import RabbitProducerObject
from ThreadLocksMgmt import ThreadLocksMgmt
from AnonymousFacade import AnonymousFacade

app = Flask(__name__)
CORS(app)

repoPool = DbRepoPool.get_instance()
lockMgmt = ThreadLocksMgmt.get_instance
rabbitProducer = RabbitProducerObject('db_request')

@app.route("/")
def home():
    return render_template("homePage.html")


@app.route("/flights", methods=['GET'])
def getAllFlights():
    repo = repoPool.get_connections()
    anonymousFacade = AnonymousFacade(repo, config)
    allFlights = anonymousFacade.get_all_flights()
    if allFlights:
        flight = []
        for flight in allFlights:
            print(flight)
            t = flight.dataWeb()
            flight.append(t)
        #flights = [flight.dataWeb() for flight in allFlights]
    else:
        flights = []
    repoPool.return_connection(repo)
    return jsonify(flights)
