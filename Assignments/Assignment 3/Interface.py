#!/usr/bin/python2.7
#
# Interface for the assignement
#

import psycopg2

def getOpenConnection(user='postgres', password='1234', dbname='postgres'):
    return psycopg2.connect("dbname='" + dbname + "' user='" + user + "' host='localhost' password='" + password + "'")

def loadRatings(ratingstablename, ratingsfilepath, openconnection):	
	cur = openconnection.cursor()
	f = open(ratingsfilepath,'r')
	create = "create table " + ratingstablename + " (userid integer not null, movieid integer not null,rating numeric not null)"
	cur.execute(create)
	#print("Creation completed")
	sqlstm = "INSERT INTO " + ratingstablename + " VALUES (%s,%s,%s);"
	#count = 0 
	for fil in f:		
		x = fil.split("::")			
		cur.execute(sqlstm , (x[0],x[1],x[2]))
		#count += 1
		#if count == 1000:
			#break
	#print("Insertion completed")
	f.close()
	cur.close()

def rangePartition(ratingstablename, numberofpartitions, openconnection):
    	cur = openconnection.cursor()
	k = 5/numberofpartitions
	i = 0
	while i < numberofpartitions:
		if i == 0:
			create = "create table range_part" + str(i) + " As Select * from " + ratingstablename + " where rating >= " + str(i*k ) + " and rating <= " + str(i*k + k) + ";"
			cur.execute(create)
		else:
			create = "create table range_part" + str(i) + " As Select * from " + ratingstablename + " where rating > " + str(i*k ) + " and rating <= " + str(i*k + k) + ";"
			cur.execute(create)
		i += 1 
	cur.close()


def roundRobinPartition(ratingstablename, numberofpartitions, openconnection):
	cur = openconnection.cursor()
	k = 5/numberofpartitions
	for i in range(numberofpartitions):
		create = "create table rrobin_part" + str(i) + " (userid integer not null, movieid integer not null,rating numeric not null);"
		cur.execute(create) 
	stm = "Select * from " + ratingstablename
	cur.execute(stm)
	r = cur.fetchall()
	j = 0
	#print("Rrobin created")
	for i in r:
		if j == numberofpartitions:
			j = 0
		ins = "INSERT INTO rrobin_part" + str(j) + " VALUES (%s,%s,%s); "
		cur.execute(ins,(i[0],i[1],i[2]))
		j = j + 1
	cur.close()

def roundrobininsert(ratingstablename, userid, itemid, rating, openconnection):
	cur = openconnection.cursor()
	cur.execute("Select table_name from INFORMATION_SCHEMA.tables where table_schema = 'public' ;")
	tab = cur.fetchall()
	numberofpartitions = 0
	for i in tab:
		if 'rrobin_part' in i[0]:
			numberofpartitions += 1
	stm = "Select count(*) from " + ratingstablename + ";"
	cur.execute(stm)
	j = cur.fetchall()[0][0]

	table_num = j%numberofpartitions
	ins = "INSERT INTO rrobin_part" + str(table_num) + " VALUES (%s,%s,%s); "
	cur.execute(ins,(userid,itemid,rating))
	ins = "INSERT INTO " + ratingstablename + " VALUES (%s,%s,%s); "
	cur.execute(ins,(userid,itemid,rating))
	cur.close()	
	

def rangeinsert(ratingstablename, userid, itemid, rating, openconnection):
	cur = openconnection.cursor()
	cur.execute("Select table_name from INFORMATION_SCHEMA.tables where table_schema = 'public' ;")
	tab = cur.fetchall()
	numberofpartitions = 0
	for i in tab:
		if 'range_part' in i[0]:
			numberofpartitions += 1
	step = 5/numberofpartitions
	table_num = 0
	for i in range(numberofpartitions):
		if rating <= step:
			table_num = i
			break		
		if rating > i*step and rating <= i*step + step :
			table_num = i
			break
	ins = "INSERT INTO range_part" + str(table_num) + " VALUES (%s,%s,%s); "
	cur.execute(ins,(userid,itemid,rating))
	ins = "INSERT INTO " + ratingstablename + " VALUES (%s,%s,%s); "
	cur.execute(ins,(userid,itemid,rating))
	cur.close()

def createDB(dbname='dds_assignment'):
    """
    We create a DB by connecting to the default user and database of Postgres
    The function first checks if an existing database exists for a given name, else creates it.
    :return:None
    """
    # Connect to the default database
    con = getOpenConnection(dbname='postgres')
    con.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()

    # Check if an existing database with the same name exists
    cur.execute('SELECT COUNT(*) FROM pg_catalog.pg_database WHERE datname=\'%s\'' % (dbname,))
    count = cur.fetchone()[0]
    if count == 0:
        cur.execute('CREATE DATABASE %s' % (dbname,))  # Create the database
    else:
        print 'A database named {0} already exists'.format(dbname)

    # Clean up
    cur.close()
    con.close()

def deletepartitionsandexit(openconnection):
    cur = openconnection.cursor()
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    l = []
    for row in cur:
        l.append(row[0])
    for tablename in l:
        cur.execute("drop table if exists {0} CASCADE".format(tablename))

    cur.close()

def deleteTables(ratingstablename, openconnection):
    try:
        cursor = openconnection.cursor()
        if ratingstablename.upper() == 'ALL':
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
            tables = cursor.fetchall()
            for table_name in tables:
                cursor.execute('DROP TABLE %s CASCADE' % (table_name[0]))
        else:
            cursor.execute('DROP TABLE %s CASCADE' % (ratingstablename))
        openconnection.commit()
    except psycopg2.DatabaseError, e:
        if openconnection:
            openconnection.rollback()
        print 'Error %s' % e
    except IOError, e:
        if openconnection:
            openconnection.rollback()
        print 'Error %s' % e
    finally:
        if cursor:
            cursor.close()
