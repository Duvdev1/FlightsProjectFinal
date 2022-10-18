from AirlineCompany import AirlineCompany
from Country import Country
#from db_config import Base, create_all_entities
from sqlalchemy import MetaData, BigInteger, Column, ForeignKey, DateTime, Integer
from sqlalchemy.orm import relationship, backref
from db2_config import Base1, create_all_entities

meta = MetaData()


class Flights(Base1):
    __tablename__ = 'flights'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    airline_company_id = Column(BigInteger, ForeignKey(AirlineCompany.id), nullable=False)
    origin_country_id = Column(BigInteger, ForeignKey(Country.id), nullable=False)
    destination_country_id = Column(BigInteger, ForeignKey(Country.id), nullable=False)
    departure_time = Column(DateTime, nullable=False)
    landing_time = Column(DateTime, nullable=False)
    remaining_tickets = Column(Integer, nullable=False)

    company = relationship("AirlineCompany", backref=backref("flights", uselist=True, passive_deletes=True))
    origin_country = relationship("Country", foreign_keys=[origin_country_id], backref=backref("originCountry",uselist=True))
    destination_country = relationship("Country", foreign_keys=[destination_country_id], backref=backref("destCountry",uselist=True))

    def __repr__(self):
        return f'Flight: (id={self.id}, airline_company_id={self.airline_company_id},' \
               f' origin_country_id={self.origin_country_id}, ' \
               f'destination_country_id={self.destination_country_id}, departure_time={self.departure_time}, ' \
               f'landing_time={self.landing_time},' \
               f' remaining_tickets={self.remaining_tickets})'

    def __str__(self):
        return f'Flight: [id={self.id}, airline_company_id={self.airline_company_id},' \
               f' origin_country_id={self.origin_country_id}, ' \
               f'destination_country_id={self.destination_country_id}, departure_time={self.departure_time}, ' \
               f'landing_time={self.landing_time},' \
               f' remaining_tickets={self.remaining_tickets}]'
               
    def dataWeb(self):
        return {'id': self.id, 'company': self.airline_company_id,  'origin_country': self.origin_country_id, 'destination_country': self.destination_country_id,
                'departure_time': str(self.departure_time), 'landing_time': str(self.landing_time), 'remaining_tickets': self.remaining_tickets}
        #return {'id': self.id, 'company': self.company.name,  'origin_country': self.origin_country.name, 'destination_country': self.destination_country.name,
               # 'departure_time': str(self.departure_time), 'landing_time': str(self.landing_time), 'remaining_tickets': self.remaining_tickets}
    
    def getDictionary(self):
        return self.dataWeb()


create_all_entities()
