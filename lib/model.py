from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base                        
from sqlalchemy.orm import relation, backref, sessionmaker, scoped_session     
from sqlalchemy.ext.associationproxy import association_proxy 

from gtfs import GtfsArchive

Base = declarative_base()

class Agency( Base ):

    __tablename__ = 'agency'

    agency_id = Column( Text )
    agency_name = Column( Text, primary_key = True )
    agency_url = Column( Text, nullable = False )
    agency_timezone = Column( Text, nullable = False )
    agency_lang = Column( String( 2 ) )
    agency_phone = Column( Text )
    agency_fare_url = Column( Text )

class Stops( Base ):

    __tablename__ = 'stops'

    stop_id = Column( Text, primary_key = True )
    stop_code = Column( Text )
    stop_name = Column( Text, nullable = False )
    stop_desc = Column( Text )
    stop_lat = Column( Float )
    stop_lon = Column( Float )
    zone_id = Column( Text )
    stop_url = Column( Text )
    location_type = Column( Integer )
    parent_station = Column( Text )
    stop_timezone = Column( Text )
    wheelchair_boarding = Column( Integer )

class Routes( Base ):

    __tablename__ = 'routes'

    route_id = Column( Text, primary_key = True )
    agency_id = Column( Text )
    route_short_name = Column( Text, nullable = False )
    route_long_name = Column( Text ) # Technically should be not-null
    route_desc = Column( Text )
    route_type = Column( Integer, nullable = False )
    route_url = Column( Text )
    route_color = Column( String( 6 ) )
    route_text_color = Column( String( 6 ) )

class Trips( Base ):

    __tablename__ = 'trips'

    route_id = Column( Text, nullable = False )
    service_id = Column( Text, nullable = False )
    trip_id = Column( Text, primary_key = True )
    trip_headsign = Column( Text )
    trip_short_name = Column( Text )
    direction_id = Column( Integer )
    block_id = Column( Text )
    shape_id = Column( Text )
    wheelchair_accessible = Column( Integer )
    bikes_allowed = Column( Integer )

class StopTimes( Base ):

    __tablename__ = 'stop_times'

    stop_time_id = Column( Integer, primary_key = True )
    trip_id = Column( Text, nullable = False )
    arrival_time = Column( Integer, nullable = False )
    departure_time = Column( Integer, nullable = False )
    stop_id = Column( Text, nullable = False )
    stop_sequence = Column( Integer, nullable = False )
    stop_headsign = Column( Text )
    pickup_type = Column( Integer )
    drop_off_type = Column( Integer )
    shape_dist_traveled = Column( Float )

class Calendar( Base ):

    __tablename__ = 'calendar'

    service_id = Column( Text, primary_key = True )
    monday = Column( Integer, nullable = False )
    tuesday = Column( Integer, nullable = False )
    wednesday = Column( Integer, nullable = False )
    thursday = Column( Integer, nullable = False )
    friday = Column( Integer, nullable = False )
    saturday = Column( Integer, nullable = False )
    sunday = Column( Integer, nullable = False )
    start_date = Column( Date, nullable = False )
    end_date = Column( Date, nullable = False )

def init( database_file ):                                                     
    global Session
    global engine                                                              
        
    engine = create_engine( 'sqlite:///' + database_file )
    Base.metadata.create_all( engine )                                         
        
    session_factory = sessionmaker( bind = engine )                            
    Session = scoped_session( session_factory )                                
            
def dispose():
            
    Session = None
    engine.dispose()                                                           
