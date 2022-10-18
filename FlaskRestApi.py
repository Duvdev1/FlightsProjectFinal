from flask import Flask, render_template, jsonify
from flask_cors import CORS
from DbRepoPool import DbRepoPool
from db2_config import config
from AnonymousFacade import AnonymousFacade
from Country import Country
from AirlineCompany import AirlineCompany

app = Flask(__name__)
CORS(app)

repoPool = DbRepoPool.get_instance()
repo = repoPool.get_connections()
repo.reset_db()
repoPool.return_connection(repo)

@app.route("/")
def home():
    return render_template("homePage.html")

@app.route("/departures", methods=['GET'])
def getDeparuesFlightsByTime():
    repo = repoPool.get_connections()
    anonymousFacade = AnonymousFacade(repo, config)
    departures = anonymousFacade.get_departure_flights_delta(12)
    print(departures)
    if departures:
        flights_ = []
        for flight in departures:
            originCountry = repo.get_by_column_value(Country, Country.id, flight.origin_country_id)[0]
            destinationCountry = repo.get_by_column_value(Country, Country.id, flight.destination_country_id)[0]
            airlinecompany = repo.get_by_column_value(AirlineCompany, AirlineCompany.id, flight.airline_company_id)[0]
            flightData = (airlinecompany.name, flight.id, originCountry.name, destinationCountry.name, str(flight.landing_time))
            flights_.append(flightData)  
    else:
        flights_ = []
    repoPool.return_connection(repo)
    return render_template('departures.html', data=flights_)

@app.route("/landing", methods=['GET'])
def getLandingFlightsByTime():
    repo = repoPool.get_connections()
    anonymousFacade = AnonymousFacade(repo, config)
    landings = anonymousFacade.get_landing_flights_delta(12)
    if landings:
        flights_ = []
        for flight in landings:
            originCountry = repo.get_by_column_value(Country, Country.id, flight.origin_country_id)[0]
            destinationCountry = repo.get_by_column_value(Country, Country.id, flight.destination_country_id)[0]
            airlinecompany = repo.get_by_column_value(AirlineCompany, AirlineCompany.id, flight.airline_company_id)[0]
            flightData = (airlinecompany.name, flight.id, originCountry.name, destinationCountry.name, str(flight.landing_time))
            flights_.append(flightData)
    else:
        flights_ = []
    repoPool.return_connection(repo)
    return render_template('landing.html', data=flights_)

@app.route("/flights", methods=['GET'])
def getAllFlights():
    repo = repoPool.get_connections()
    anonymousFacade = AnonymousFacade(repo, config)
    allFlights = anonymousFacade.get_all_flights()
    if allFlights:
        data = (())
        flights_ = []
        for flight in allFlights:
            t = flight.dataWeb()
            originCountry = repo.get_by_column_value(Country, Country.id, flight.origin_country_id)[0]
            destinationCountry = repo.get_by_column_value(Country, Country.id, flight.destination_country_id)[0]
            airlinecompany = repo.get_by_column_value(AirlineCompany, AirlineCompany.id, flight.airline_company_id)[0]
            flightData = (airlinecompany.name, flight.id, originCountry.name, destinationCountry.name, str(flight.landing_time))
            flights_.append(flightData)
    else:
        flights_ = []
    repoPool.return_connection(repo) 
    print(data)
    #return jsonify(flights)
    heading = ("Airline Company", "Flight Number", "Origin Country", "Destination Country", "Landing Time")
    return render_template('Allflights.html', heading=heading, data=flights_)
    
#if __name__ == 'main':
    #app.run(host='127.0.0.1', port=8443, debug=True)
    
app.run(host='127.0.0.3',port=5000, debug=True)

