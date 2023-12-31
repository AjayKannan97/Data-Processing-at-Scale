
import psycopg2
import os
import sys
import threading
'''

FIRST_TABLE_NAME = 'table1'
SECOND_TABLE_NAME = 'table2'
SORT_COLUMN_NAME_FIRST_TABLE = 'column1'
SORT_COLUMN_NAME_SECOND_TABLE = 'column2'
JOIN_COLUMN_NAME_FIRST_TABLE = 'column1'
JOIN_COLUMN_NAME_SECOND_TABLE = 'column2'
'''

FIRST_TABLE_NAME = 'MovieRating'
SECOND_TABLE_NAME = 'MovieBoxOfficeCollection'
SORT_COLUMN_NAME_FIRST_TABLE = 'Rating'
SORT_COLUMN_NAME_SECOND_TABLE = 'Collection'
JOIN_COLUMN_NAME_FIRST_TABLE = 'MovieID'
JOIN_COLUMN_NAME_SECOND_TABLE = 'MovieID'

#-------------------------------- parallel sort -----------------------------

def ParallelSort (InputTable, SortingColumnName, OutputTable, openconnection):
        cur = openconnection.cursor()
	interval_sort, rangeMin = Range(InputTable,SortingColumnName,openconnection)
        
	cur.execute("SELECT COLUMN_NAME,DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='" + InputTable + "'")
	schema = cur.fetchall()
	for i in range(5):
		tableName = "range_part" + str(i)
		cur.execute("DROP TABLE IF EXISTS " + tableName + "")
		cur.execute("CREATE TABLE " + tableName + " ("+schema[0][0]+" "+schema[0][1]+")")
		for d in range(1, len(schema)):
			cur.execute("ALTER TABLE " + tableName + " ADD COLUMN " + schema[d][0] + " " + schema[d][1] + ";")
	thread = [0,0,0,0,0]
	for i in range(5):
		if i == 0:
			lowerValue = rangeMin
			upperValue = rangeMin + interval_sort
		else:
			lowerValue = upperValue
			upperValue = upperValue + interval_sort
    		thread[i] = threading.Thread(target=range_insert, args=(InputTable, SortingColumnName, i, lowerValue, upperValue, openconnection))
		thread[i].start()

	for i in range(0,5):
		thread[i].join()
	cur.execute("DROP TABLE IF EXISTS " + OutputTable + "")
	cur.execute("CREATE TABLE " + OutputTable + " ( "+schema[0][0]+" "+schema[0][1]+")")

	for i in range(1, len(schema)):
		cur.execute("ALTER TABLE " + OutputTable + " ADD COLUMN " + schema[i][0] + " " + schema[i][1] + ";")
	for i in range(5):
		query = "INSERT INTO " + OutputTable + " SELECT * FROM " + "range_part" + str(i) + ""
		cur.execute(query)
	
	#cur.execute("Select * from " + InputTable)	
	#print(cur.fetchall()[:10])
	#cur.execute("Select * from " + OutputTable)
	#print(cur.fetchall())
	
	for i in range(5):
		tableName = "range_part" + str(i)
		cur.execute("DROP TABLE IF EXISTS " + tableName + "")

	cur.close()


def Range(InputTable, SortingColumnName,openconnection):
	cur = openconnection.cursor()
	cur.execute("SELECT MIN(" + SortingColumnName + ") FROM " + InputTable + "")
	MinVal=cur.fetchone()
	range_min_value = (float)(MinVal[0])

	cur.execute("SELECT MAX(" + SortingColumnName + ") FROM " + InputTable + "")
	MaxVal=cur.fetchone()
	range_max_value = (float)(MaxVal[0])

	interval = (range_max_value - range_min_value)/5
	return interval , range_min_value

 
def range_insert(InputTable, SortingColumnName, index, min_val, max_val, openconnection):

	cur=openconnection.cursor()
	table_name = "range_part" + str(index)

	if index == 0:
		query = "INSERT INTO " + table_name + " SELECT * FROM " + InputTable + "  WHERE " + SortingColumnName + ">=" + str(min_val) + " AND " + SortingColumnName + " <= " + str(max_val) + " ORDER BY " + SortingColumnName + " ASC"
	else:
		query = "INSERT INTO " + table_name + " SELECT * FROM " + InputTable + "  WHERE " + SortingColumnName + ">" + str(min_val) + " AND " + SortingColumnName + " <= " + str(max_val) + " ORDER BY " + SortingColumnName + " ASC"

	cur.execute(query)
	cur.close()
	return

# ---------------- parallel join --------------


def ParallelJoin (InputTable1, InputTable2, Table1JoinColumn, Table2JoinColumn, OutputTable, openconnection):

	cur = openconnection.cursor()
	interval , range_min_value = para_thread(InputTable1, InputTable2 , Table1JoinColumn , Table2JoinColumn, openconnection)

	cur.execute("SELECT COLUMN_NAME,DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='" + InputTable1 + "'")
	schema1 = cur.fetchall()
	cur.execute("SELECT COLUMN_NAME,DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='" + InputTable2 + "'")
	schema2 = cur.fetchall()
	cur.execute("DROP TABLE IF EXISTS " + OutputTable + "")
	cur.execute("CREATE TABLE " + OutputTable + " ("+schema1[0][0]+" "+schema2[0][1]+")")

	for i in range(1, len(schema1)):
		cur.execute("ALTER TABLE " + OutputTable + " ADD COLUMN " + schema1[i][0] + " " + schema1[i][1] + ";")
	for i in range(len(schema2)):
		cur.execute("ALTER TABLE " + OutputTable + " ADD COLUMN " + schema2[i][0] + "1" +" " + schema2[i][1] + ";")

	OutputRangeTable(InputTable1, InputTable2, Table1JoinColumn, Table2JoinColumn, schema1, schema2 , interval , range_min_value, openconnection)

	thread = [0,0,0,0,0]
	for i in range(5):
		thread[i] = threading.Thread(target=range_insert_join, args=(Table1JoinColumn, Table2JoinColumn, openconnection, i))
		thread[i].start()
		for a in range(0,5):
			thread[i].join()
	for i in range(5):
		cur.execute("INSERT INTO " + OutputTable + " SELECT * FROM output_table" + str(i))
	
	#cur.execute("Select * from " + InputTable1)	
	#print(cur.fetchall()[:10])
	#cur.execute("Select * from " + InputTable2)	
	#print(cur.fetchall()[:10])
	#cur.execute("Select * from " + OutputTable)
	#print(cur.fetchall())
	cur.close()
 
def para_thread(InputTable1, InputTable2 , Table1JoinColumn , Table2JoinColumn, openconnection):
    cur = openconnection.cursor()
    cur.execute("SELECT MIN(" + Table1JoinColumn + ") FROM " + InputTable1 + "")
    minimum1=cur.fetchone()
    Min1 = (float)(minimum1[0])

    cur.execute("SELECT MIN(" + Table2JoinColumn + ") FROM " + InputTable2 + "")
    minimum2=cur.fetchone()
    Min2 = (float)(minimum2[0])

    cur.execute("SELECT MAX(" + Table1JoinColumn + ") FROM " + InputTable1 + "")
    maximum1=cur.fetchone()
    Max1 = (float)(maximum1[0])

    cur.execute("SELECT MAX(" + Table2JoinColumn + ") FROM " + InputTable2 + "")
    maximum2=cur.fetchone()
    Max2 = (float)(maximum2[0])

    if Max1 > Max2:
        rangeMax = Max1
    else:
        rangeMax = Max2

    if Min1 > Min2:
        rangeMin = Min2
    else:
        rangeMin = Min1

    interval = (rangeMax - rangeMin)/5

    return interval,rangeMin


def OutputRangeTable(InputTable1, InputTable2, Table1JoinColumn, Table2JoinColumn, schema1 , schema2 , interval , range_min_value, openconnection):
    cur = openconnection.cursor();
    for i in range(5):
        
        range_table1_name = "table1_range" + str(i)
        range_table2_name = "table2_range" + str(i)
        if i==0:
            lowerValue = range_min_value
            upperValue = range_min_value + interval
        else:
            lowerValue = upperValue
            upperValue = upperValue + interval

        cur.execute("DROP TABLE IF EXISTS " + range_table1_name + ";")
        cur.execute("DROP TABLE IF EXISTS " + range_table2_name + ";")

        if i == 0:
            cur.execute("CREATE TABLE " + range_table1_name + " AS SELECT * FROM " + InputTable1 + " WHERE (" + Table1JoinColumn + " >= " + str(lowerValue) + ") AND (" + Table1JoinColumn + " <= " + str(upperValue) + ");")
            cur.execute("CREATE TABLE " + range_table2_name + " AS SELECT * FROM " + InputTable2 + " WHERE (" + Table2JoinColumn + " >= " + str(lowerValue) + ") AND (" + Table2JoinColumn + " <= " + str(upperValue) + ");")
        else:
            cur.execute("CREATE TABLE " + range_table1_name + " AS SELECT * FROM " + InputTable1 + " WHERE (" + Table1JoinColumn + " > " + str(lowerValue) + ") AND (" + Table1JoinColumn + " <= " + str(upperValue) + ");")
            cur.execute("CREATE TABLE " + range_table2_name + " AS SELECT * FROM " + InputTable2 + " WHERE (" + Table2JoinColumn + " > " + str(lowerValue) + ") AND (" + Table2JoinColumn + " <= " + str(upperValue) + ");")
        
        output_range_table = "output_table" + str(i)
        cur.execute("DROP TABLE IF EXISTS " + output_range_table + "")
        cur.execute("CREATE TABLE " + output_range_table + " ("+schema1[0][0]+" "+schema2[0][1]+")")

        for j in range(1, len(schema1)):
            cur.execute("ALTER TABLE " + output_range_table + " ADD COLUMN " + schema1[j][0] + " " + schema1[j][1] + ";")
        for j in range(len(schema2)):
            cur.execute("ALTER TABLE " + output_range_table + " ADD COLUMN " + schema2[j][0] + "1" +" "+ schema2[j][1] + ";")
    cur.close()
    


def range_insert_join(Table1JoinColumn, Table2JoinColumn, openconnection, TempTableId):
    cur=openconnection.cursor()
    query = "INSERT INTO output_table" + str(TempTableId) + " SELECT * FROM table1_range" + str(TempTableId) + " INNER JOIN table2_range" + str(TempTableId) + " ON table1_range" + str(TempTableId) + "." + Table1JoinColumn + "=" + "table2_range" + str(TempTableId) + "." + Table2JoinColumn + ";"
    cur.execute(query)
    cur.close()
    return











