import Interface as ms
#ms.createDB("db_test")
with ms.getOpenConnection(dbname="postgres") as conn:
        ratingstablename = "ratingsd"
        ms.loadRatings(ratingstablename,"ratings.dat",conn)
        ms.rangePartition(ratingstablename,4,conn)
        ms.roundRobinPartition(ratingstablename,3,conn)
        ms.roundrobininsert(ratingstablename,7,101,3.5,conn)

sh = "1::122::5::838985046"

c = sh.split("::")
print(c)

print("hello")