import viz, vizshape, vizact
import random
import oculus

EYEHEIGHT = 1.65
USERID = 0
SIZE = 50
RAY = SIZE * 2

viz.setMultiSample( 4 )
viz.fov( 60 )
viz.go()
viz.clip( 0.01, RAY )
viz.mouse.setVisible( False )
viz.setOption( 'viz.glFinish', 1 )

headLight = viz.MainView.getHeadLight()
headLight.disable()

#Lights
pointlight = viz.addLight( parent = viz.WORLD, scene = viz.MainScene )
pointlight.setEuler( 45, 90, 0 )
pointlight.color( viz.WHITE )
pointlight.linearattenuation( 0.2 )

# Setup Oculus Rift HMD
hmd = oculus.Rift()
if not hmd.getSensor():
	headset = False
	#sys.exit( 'Oculus Rift not detected' )
	print 'Oculus Rift not detected'
else:
	headset = True
	if hmd.getSensor().getDisplayMode() == oculus.DISPLAY_DESKTOP:
		viz.window.setFullscreen( True )

#Set Up View
tracker = hmd.getSensor()
view = viz.MainView
view.eyeheight = EYEHEIGHT
link1 = viz.link( tracker, view )
#link1.setMask( viz.LINK_ORI )
link1.setOffset( [ 0, EYEHEIGHT, 0 ] )

#Set Up Target
target = vizshape.addCube( size = 1 )
target.color( viz.WHITE )
target.disable( mode = viz.INTERSECT_INFO_OBJECT )

#Geometries
plane = vizshape.addPlane( [ SIZE, SIZE, 0 ], axis = vizshape.AXIS_Y, cullFace = True )
plane.disable( mode = viz.INTERSECT_INFO_OBJECT )
plane.color( viz.SLATE )

colors = {}
colors[ 0 ] = viz.PURPLE
colors[ 1 ] = viz.GREEN
colors[ 2 ] = viz.BLUE
colors[ 3 ] = viz.RED
colors[ 4 ] = viz.ORANGE
colors[ 5 ] = viz.GRAY
colors[ 6 ] = viz.YELLOW

spheres = {}
for i in range( 0, 10 ):
	radius = random.randrange( 1, 5 )
	color = random.randrange( 0, len( colors ) )
	spheres[ i ] = vizshape.addSphere( radius = radius, slices = 20, stacks = 20, axis = vizshape.AXIS_Y )
	spheres[ i ].color( colors[ color ] )
	spheres[ i ].specular( [ 1.0 ] * 3 )
	spheres[ i ].enable( mode = viz.INTERSECTION )
	spheres[ i ].name = "sphere_" + str( i )
	spheres[ i ].description = "description_" + str( i )
	x = random.randrange( -SIZE, SIZE )
	y = random.randrange( 0, 10 )
	z = random.randrange( -SIZE, SIZE )
	spheres[ i ].setPosition( [ x, y, z ] )

def line( source, target ):
	viz.startLayer( viz.LINES )
	viz.lineWidth( 1 )
	viz.vertex( source )
	viz.vertex( target )
	thisline = viz.endLayer()

def remove( object ):
	object.remove()

def fadeOut( object ):
	fade = vizact.fadeTo( 0, time = 2 )
	sequence = vizact.sequence( fade, vizact.call( remove, object ) )
	object.runAction( sequence )

def action( object ):
	fadeOut( object )

	#fade = vizact.fadeTo( 0, time = 2 )
	#sequence = vizact.sequence( fade, vizact.call( remove, object ) )
	#object.runAction( sequence )


def update():
	matrix = tracker.getMatrix()
	targetmatrix = matrix
	targetmatrix.preTrans( [ 0, EYEHEIGHT, RAY ] )
	target.setMatrix( targetmatrix )
	ray = viz.intersect( view.getPosition(), target.getPosition(), all = False, ignoreBackFace = True, computePath = False )

	if ray.valid:
		print "Intersect:", ray.object.id, ray.object.name, ray.object.description
		action( ray.object )
		#line( view.getPosition(), target.getPosition() )
vizact.onupdate( 0, update )
