import sqlite3 as lite
import os, sys, inspect

dir = os.path.dirname( inspect.getfile( inspect.currentframe() ) )
sys.path.insert( 0, os.path.abspath( dir ) )

DATABASE = dir + '\data.db'
TABLE = 'Datas'

def insert( d ):
	COLUMNS = d.keys()
	VALUES = d.values()
	try:
		con = lite.connect( DATABASE, isolation_level = None )
		cur = con.cursor()    
		sql = "INSERT INTO {} {} VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ? );".format( TABLE, tuple( COLUMNS ) )
		cur.execute( sql, tuple( VALUES ) )
	except lite.Error, e:
		print "Error %s:" % e.args[0]
		sys.exit(1)	
	finally:	
		if con:
			con.close()
		return cur.lastrowid		