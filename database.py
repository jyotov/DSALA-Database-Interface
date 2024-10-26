from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# Create a base class for models
Base = declarative_base()

class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    date_created = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    suffix = Column(String, nullable=True)
    preferred_name = Column(String, nullable=True)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    dob = Column(String, nullable=False)
    ethnicity = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    language = Column(String, nullable=False)
    address1 = Column(String, nullable=False)
    address2 = Column(String, nullable=True)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    zip = Column(String, nullable=False)
    birth_hospital = Column(String, nullable=True)
    birth_city = Column(String, nullable=True)
    birth_state = Column(String, nullable=False)
    notes = Column(String, nullable=False)

class Contact(Base):
    __tablename__ = 'contacts'

    client_id = Column(Integer, primary_key=True)
    index = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    relationship = Column(String, nullable=False)
    address1 = Column(String, nullable=False)
    address2 = Column(String, nullable=True)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    zip = Column(String, nullable=False)
    receive_emails = Column(String, nullable=False)
    notes = Column(String, nullable=False)

class Database:
    def __init__(self):
        engine = create_engine('sqlite:///dsala.db')
        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        self.session = Session()
