import os, sys, inspect

src_dir = os.path.dirname( inspect.getfile( inspect.currentframe() ) )
script_dir = "../LeapSDK/lib/"
arch_dir = 'x64' if sys.maxsize > 2**32 else 'x86'
sys.path.insert( 0, os.path.abspath( os.path.join( src_dir, script_dir ) ) )
sys.path.insert( 0, os.path.abspath( os.path.join( src_dir, script_dir, arch_dir ) ) )

import Leap

GRAB_SENSITIVITY = 0.7

class LeapEventListener( Leap.Listener ):
    def get_grabbing( self, controller, OBJECT ):
		frame = controller.frame()
		hands = frame.hands
		hand = frame.hands[ 0 ]
		data = {
			'Device': 'Leap',
			'Name': 'Hand',
			'Position': str( hand.palm_position.to_tuple() ),
			'Rotation': str( hand.direction.to_tuple() ),
			'Scale': '(0.0, 0.0, 0.0)'
		}
		
		if hand.grab_strength > GRAB_SENSITIVITY:
			data[ 'Description' ] = 'Grabbing'
			data[ 'Object' ] = OBJECT
		else:
			data[ 'Description' ] = None
			data[ 'Object' ] = None
			
		return data