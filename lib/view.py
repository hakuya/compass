import model
import datetime

def get_schedules():

    WEEKDAYS = [ 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday' ]

    session = model.Session()

    today = datetime.date.today()

    dow_filter = getattr( model.Calendar, WEEKDAYS[today.weekday()] )

    schedules = session.query( model.Calendar ) \
            .filter( model.Calendar.start_date <= today ) \
            .filter( model.Calendar.end_date >= today ) \
            .filter( dow_filter != 0 )

    return map( lambda x: x.service_id, list( schedules ) )

def ping_stop( stop_ids ):

    schedules = get_schedules()

    time = datetime.datetime.time( datetime.datetime.now() )
    time = time.second + time.minute * 60 + time.hour * 3600

    time_begin = time
    time_end = time + 3600

    session = model.Session()

    busses = session.query( model.StopTimes.stop_id, model.Trips.route_id, model.Trips.trip_headsign, model.StopTimes.departure_time ) \
            .filter( model.Trips.service_id.in_( schedules ) ) \
            .filter( model.StopTimes.stop_id.in_( stop_ids ) ) \
            .filter( model.Trips.trip_id == model.StopTimes.trip_id ) \
            .filter( model.StopTimes.departure_time > time_begin ) \
            .filter( model.StopTimes.departure_time <= time_end ) \
            .order_by( model.StopTimes.departure_time )

    return map( lambda x: ( x.stop_id, x.route_id, x.trip_headsign, x.departure_time ), list( busses ) )

if( __name__ == '__main__' ):

    model.init( 'grt.db' )

    for stop, route, name, time in ping_stop( [ '1966', '2678', '2779', '3589', '3631' ] ):
        print '%s: %02d:%02d - Route %s' % (
                stop, time / 3600, (time / 60) % 60, name )
