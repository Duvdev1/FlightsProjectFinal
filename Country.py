from sqlalchemy import MetaData, String, Column, BigInteger
#from db_config import Base, create_all_entities
from db2_config import Base1, create_all_entities

meta = MetaData()


class Country(Base1):
    __tablename__ = 'countries'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)

    def __repr__(self):
        return f'Country(id={self.id}, name={self.name})'

    def __str__(self):
        return f'Country[id={self.id}, name={self.name}]'
    
    def getDictionary(self):
        return{'id': self.id, 'name': self.name}


create_all_entities()