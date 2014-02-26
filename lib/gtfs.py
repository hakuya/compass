import zipfile
import csv

class GtfsTableIterator:

    def __init__( self, stream ):

        self.__stream = csv.reader( stream )
        self.__schema = None

        self.__read_schema()

    def __read_schema( self ):

        self.__schema = self.__stream.next()

    def schema( self ):

        return self.__schema

    def iter( self ):

        return self.__stream

    def close( self ):

        self.__stream.close()

class GtfsArchive:

    def __init__( self, path ):

        self.__zf = zipfile.ZipFile( path, 'r' )
        self.__tables = {}

        self.__load_tables()

    def __load_tables( self ):

        ils = self.__zf.infolist()

        for i in ils:
            try:
                table, ext = i.filename.split( '.' )
                if( ext != 'txt' ):
                    pass
                self.__tables[table] = i
            except:
                print 'WARNING: %s not loaded from zip' % ( i.filename, )
                pass

    def tables( self ):

        return self.__tables.keys()

    def read_table( self, table ):

        return GtfsTableIterator( self.__zf.open( self.__tables[table], 'r' ) )

if( __name__ == '__main__' ):

    grt = GtfsArchive( 'GRT_GTFS.zip' )
    print grt.tables()
    stops = grt.read_table( 'stops' )
    print stops.schema()
