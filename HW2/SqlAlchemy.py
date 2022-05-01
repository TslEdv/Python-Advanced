from sqlalchemy import create_engine, MetaData, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# open the connection to the database
engine = create_engine('sqlite:///C:\\Users\\User\\HW2database2.db')
meta = MetaData()
Base = declarative_base()


# creating a class for the providers table
class Provider(Base):
    __tablename__ = 'providers'

    ID = Column(Integer, primary_key=True)
    ProviderName = Column(String, unique=True)


# creating a class for the canteens table
class Canteen(Base):
    __tablename__ = 'canteens'
    ID = Column(Integer, primary_key=True)
    ProviderID = Column(Integer, ForeignKey('providers.ID'))
    Name = Column(String, unique=True)
    Location = Column(String)
    time_open = Column(Integer)
    time_closed = Column(Integer)
    provider = relationship("Provider", back_populates="canteens")


# adding a new property canteens to provider and declaring relation
Provider.canteens = relationship("Canteen", order_by=Canteen.ID, back_populates="provider")

# started session
Session = sessionmaker(bind=engine)
session = Session()


def create_tables():
    """
    Creates tables Provider and Canteen from base
    """
    Base.metadata.create_all(engine)


def add_only_it_college():
    """
    Adds IT college canteen to table canteens
    """

    # Tries to add bitStop Kohvik, if it already exists, throws and error
    try:
        session.add(Provider(ProviderName="bitStop Kohvik OÜ",
                             canteens=[Canteen(Name="bitStop KOHVIK", Location="IT college, Raja 4c", time_open=930,
                                               time_closed=1600)]))
        session.commit()
    except:
        session.rollback()


def add_other_canteens():
    """
    Adds the list of canteens to table canteens
    """

    # Tries to add all the providers + their canteens to the table at the same time,
    # if fails, throws an error
    try:
        session.add_all(
            [Provider(ProviderName="Rahva Toit",
                      canteens=[
                          Canteen(Name="Economics- and social science building canteen",
                                  Location="Akadeemia tee 3, SOC- building", time_open=830, time_closed=1830),
                          Canteen(Name="Library canteen",
                                  Location="Akadeemia tee 1/Ehitajate tee 7", time_open=830, time_closed=1900),
                          Canteen(Name="U06 building canteen",
                                  Location="U06 building canteen", time_open=900, time_closed=1600)]),
             Provider(ProviderName="Baltic Restaurants Estonia AS",
                      canteens=[
                          Canteen(Name="Main building Deli cafe",
                                  Location="Ehitajate tee 5, U01 building", time_open=900, time_closed=1630),
                          Canteen(Name="Main building Daily lunch restaurant",
                                  Location="Ehitajate tee 5, U01 building", time_open=900, time_closed=1630),
                          Canteen(Name="Natural Science building canteen",
                                  Location="Akadeemia tee 15, SCI building", time_open=900, time_closed=1600),
                          Canteen(Name="ICT building canteen",
                                  Location="Raja 15/Mäepealse 1", time_open=900, time_closed=1600),
                      ]),
             Provider(ProviderName="TTÜ Sport OÜ",
                      canteens=[
                          Canteen(Name="Sports building canteen",
                                  Location="Männiliiva 7, S01 building", time_open=1100, time_closed=2000),
                      ])
             ])
        session.commit()
    except:
        session.rollback()


def query_all_providers():
    """
    Queries all providers
    """

    # queries all providers and prints them out
    result = session.query(Provider)
    for r in result:
        print(r.ID, r.ProviderName)


def query_1615_1800():
    """
    Queries for the canteens that are open in the time frame 16:15-18:00
    """

    # query for the canteens where the closing time is at 6 or later
    # and if the opening time is at 16:15 or earlier
    # then print out the results
    result = session.query(Canteen).filter(Canteen.time_open <= 1615, Canteen.time_closed >= 1800)
    print("Libraries open at 16:15-18:00")
    for r in result:
        print(r.ID, r.Name)


def query_rahva_toit():
    """
    Query all the canteens that belong to Provider called Rahva Toit
    """

    # if the canteen's provider's name matches to Rahva Toit print it out
    result = session.query(Canteen) \
        .join(Provider, Canteen.ProviderID == Provider.ID) \
        .filter(Provider.ProviderName == 'Rahva Toit')
    print("Canteens serviced by Rahva Toit:")
    for r in result:
        print(r.ID, r.Name)


# Executing all the functions
create_tables()
add_only_it_college()
add_other_canteens()
query_all_providers()
query_1615_1800()
query_rahva_toit()

# closing the connection
engine.dispose()
