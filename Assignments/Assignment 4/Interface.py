#!/usr/bin/python2.7
#
# Assignment2 Interface
#

import psycopg2
import os
import sys
# Donot close the connection inside this file i.e. do not perform openconnection.close()
def RangeQuery(ratingsTableName, ratingMinValue, ratingMaxValue, openconnection):
	cur = openconnection.cursor()
	cur.execute("Select table_name from INFORMATION_SCHEMA.tables where table_schema = 'public' ;")
	tab = cur.fetchall() 

	f1, f2 = [], []
	for i in tab:
		if 'meta' not in i[0]:
			if 'round' not in i[0]:
				f1.append(i[0])
			if 'round' in i[0]:
				f2.append(i[0])
	
	l1,l2 = [], []
	for i in f1:	
		stm = 'Select * from ' + i + ' where rating >= ' +str(ratingMinValue)+ ' and rating <= ' +str(ratingMaxValue)+ ';'
		cur.execute(stm)
		iterate = cur.fetchall()
		i = i.replace("rangeratingspart","RangeRatingsPart")
		for k in iterate:
			l1.append([i,k[0],k[1],k[2]])
	
	for i in f2:	
		stm = 'Select * from ' + i + ' where rating >= ' +str(ratingMinValue)+ ' and rating <= ' +str(ratingMaxValue)+ ';'
		cur.execute(stm)
		iterate = cur.fetchall()
		i = i.replace("roundrobinratingspart","RoundRobinRatingsPart")
		for k in iterate:
			l2.append([i,k[0],k[1],k[2]])
	l2 = l2 + l1
	writeToFile('RangeQueryOut.txt',l2)
	#print(l2)
	cur.close()
	

def PointQuery(ratingsTableName, ratingValue, openconnection):
    	cur = openconnection.cursor()
	cur.execute("Select table_name from INFORMATION_SCHEMA.tables where table_schema = 'public' ;")
	tab = cur.fetchall() 

	f1, f2 = [], []
	for i in tab:
		if 'meta' not in i[0]:
			if 'round' not in i[0]:
				f1.append(i[0])
			if 'round' in i[0]:
				f2.append(i[0])
	
	l1,l2 = [], []
	for i in f1:	
		stm = 'Select * from ' + i + ' where rating = ' +str(ratingValue)+ ';'
		cur.execute(stm)
		iterate = cur.fetchall()
		i = i.replace("rangeratingspart","RangeRatingsPart")
		for k in iterate:
			l1.append([i,k[0],k[1],k[2]])
	
	for i in f2:	
		stm = 'Select * from ' + i + ' where rating = ' +str(ratingValue)+ ';'
		cur.execute(stm)
		iterate = cur.fetchall()
		i = i.replace("roundrobinratingspart","RoundRobinRatingsPart")
		for k in iterate:
			l2.append([i,k[0],k[1],k[2]])
	l2 = l2 + l1
	writeToFile('PointQueryOut.txt',l2)
	#print(l2)
	cur.close()


def writeToFile(filename, rows):
    f = open(filename, 'w')
    for line in rows:
        f.write(','.join(str(s) for s in line))
        f.write('\n')
    f.close()
