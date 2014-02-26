import model
import gtfs
import datetime

def load_from_gtfs( arch ):

    session = model.Session()
    tables = [ model.Agency, model.Stops, model.Routes, model.Trips, model.StopTimes, model.Calendar ]

    for t in tables:
        reader = arch.read_table( t.__tablename__ )
        schema = reader.schema()

        for row in reader.iter():
            inst = t()

            for col_idx, col_name in enumerate( schema ):
                col_type = getattr( t, col_name ).property.columns[0].type

                val = row[col_idx]

                if( len( val ) == 0 ):
                    val = None

                else:
                    try:
                        if( col_name == 'arrival_time' or col_name == 'departure_time' ):
                            val = map( int, val.split( ':' ) )
                            val = val[2] + 60 * val[1] + 3600 * val[0]
                        elif( isinstance( col_type, model.Integer ) ):
                            val = int( val )
                        elif( isinstance( col_type, model.Float ) ):
                            val = float( val )
                        elif( isinstance( col_type, model.Date ) ):
                            val = map( int, [ val[0:4], val[4:6], val[6:8] ] )
                            val = datetime.date( *val )
                    except:
                        print schema
                        print row
                        raise

                setattr( inst, col_name, val )

            session.add( inst ) 

    session.commit()

if( __name__ == '__main__' ):

    import sys
    import os

    if( len( sys.argv ) < 3 ):
        print 'Usage: %s zip db' % ( sys.argv[0] )
        sys.exit( 0 )

    gtfs_zip = sys.argv[1]
    db_file = sys.argv[2]

    if( os.path.isfile( db_file ) ):
        os.remove( db_file )

    model.init( db_file )
    gtfs_db = gtfs.GtfsArchive( gtfs_zip )
    load_from_gtfs( gtfs_db )
