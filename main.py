import time, datetime, cx_insert, cx_leap
PERIOD = 0.5
KEYID = 0
OBJECT = 'Target'

listener = cx_leap.LeapEventListener()
controller = cx_leap.Leap.Controller()
controller.add_listener( listener )

def logData():
	global OBJECT
	ts = datetime.datetime.now()
	d = listener.get_grabbing( controller, OBJECT )
	d[ 'KeyID' ] = KEYID
	d[ 'Timestamp' ] = str( ts.isoformat() )
	cx_insert.insert( d )
	
def main():
	global i
	logData()
	time.sleep( PERIOD )
	main()

main()
