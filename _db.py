import sqlite3 as lite
import os, sys, inspect

dir = os.path.dirname( inspect.getfile( inspect.currentframe() ) )
sys.path.insert( 0, os.path.abspath( dir ) )

DATABASE = dir + '\data.db'
TABLE = 'Datas'
COLUMNS = "'KeyID', 'Device', 'Name', 'Description', 'Position', 'Rotation', 'Scale'"

def databases():
	cur.execute( "PRAGMA database_list" )
	rows = cur.fetchall()
	for row in rows:
		print row[0], row[1], row[2]	
		
def schema():
	con = lite.connect( DATABASE )

	with con:
		cur = con.cursor()   
		#Version
		cur.execute( 'SELECT SQLITE_VERSION()' )
		data = cur.fetchone()
		print "SQLite version: %s" % data  
		#Tables		
		if TABLE:
			cur.execute( 'PRAGMA table_info( {} )'.format( TABLE ) )
			data = cur.fetchall()
			for d in data:
				print d[0], d[1], d[2]