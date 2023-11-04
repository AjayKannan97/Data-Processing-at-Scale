/*0*/
CREATE TABLE query0 AS

SELECT username AS userfullname

FROM users

WHERE users.userid = :v1;


/*1*/
Select genreid,count(genreid) into temp from hasgenre group by genreid;
Select genres.name as name, temp.count as moviecount into query1 
	from genres inner join temp on temp.genreid = genres.genreid;
drop table if exists temp;

/*2*/
Select genres.name as name, genAve.avg as rating into query2 from
	(Select gA.genreid, avg(gA.average) from
		(Select aves.movieid, hasgenre.genreid, aves.average from 
			(select movieid,avg(rating) as average from ratings group by movieid) as aves
		inner join hasgenre on aves.movieid = hasgenre.movieid) as gA 
	group by gA.genreid) as genAve 
inner join genres on genres.genreid = genAve.genreid; 

/*
Select genres.name, (genAve.S/genAve.Ct) as rating into query2 from
(Select gA.genreid, sum(gA.s) as S,count(gA.ct) as Ct from
	(Select aves.movieid, hasgenre.genreid, aves.s, aves.ct from 
		(select movieid,sum(rating) as s,count(movieid) as ct 
		 	from ratings group by movieid) as aves
		inner join hasgenre on aves.movieid = hasgenre.movieid) as gA 
	group by gA.genreid) as genAve 
inner join genres on genres.genreid = genAve.genreid; 
*/

/*3*/
Select movies.title, (counts.ct) as countofratings into query3 from
	(Select mov.movieid,mov.ct from 
	 	(select movieid, count(rating) as ct 
			from ratings group by movieid) as mov
		where mov.ct > 9) as counts	
	inner join movies on movies.movieid = counts.movieid
order by counts.ct;

/*4*/
Select comd.movieid, movies.title into query4 from
	(Select has.movieid from 
		(Select * from hasgenre) as has
	inner join genres on has.genreid = genres.genreid 
	where genres.name like 'Comedy') as comd 
inner join movies on comd.movieid = movies.movieid;

/*5*/

Select movies.title, mavg.average as average into query5 from
	(Select movieid, avg(rating) as average
	from ratings 
	group by movieid) as mavg
inner join movies on movies.movieid = mavg.movieid;

/*6*/

Select avg(comedy.average) as average into query6 from
	(Select genres.name, (gavg.average) from
		(Select hasgenre.genreid, com.average from
			(Select movies.title, mavg.movieid, mavg.average from
				(Select movieid, (rating) as average
				from ratings) as mavg
			inner join movies on movies.movieid = mavg.movieid) as com
		inner join hasgenre on com.movieid = hasgenre.movieid) as gavg 
	inner join genres on genres.genreid = gavg.genreid 
and genres.name like 'Comedy') as comedy ;

/*7*/
Select avg(comedy.average) as average into query7 from
	(Select genres.name, (gavg.average) from
		(Select hasgenre.genreid, com.average from
			(Select movies.title, mavg.movieid, mavg.average from
				(Select movieid, (rating) as average
				from ratings) as mavg
			inner join movies on movies.movieid = mavg.movieid) as com
		inner join hasgenre on com.movieid = hasgenre.movieid) as gavg 
	inner join genres on genres.genreid = gavg.genreid 
and genres.name like 'Comedy' or genres.name like 'Romance') as comedy ;

/*8*/
Select avg(comedy.average) as average into query8 from
	(Select genres.name, (gavg.average) from
		(Select hasgenre.genreid, com.average from
			(Select movies.title, mavg.movieid, mavg.average from
				(Select movieid, (rating) as average
				from ratings ) as mavg
			inner join movies on movies.movieid = mavg.movieid) as com
		inner join hasgenre on com.movieid = hasgenre.movieid) as gavg 
	inner join genres on genres.genreid = gavg.genreid 
and genres.name like 'Romance' and  genres.name not like 'Comedy') as comedy ;


/*9*/
Select movieid, rating into query9 from ratings where userid = :v1 ;

/*10*/
Select nosim.movieid1, nosim.movieid2, nosim.totavg as sim into simil from
	(Select mid2.movieid1 as movieid1, movies.movieid as movieid2, mid2.totavg  from
		(Select movies.movieid as movieid1, mid1.movie2, mid1.totavg from
			(Select ComAvg.Movie1,ComAvg.Movie2,(1-(abs(sum(ComAvg.a1-ComAvg.b1))/5)) as totavg from
				(Select A.title as Movie1,B.title as Movie2,A.average as a1,B.Average as b1 
					from query5 A, query5 B
					where A.title <> B.title) as ComAvg
				group by ComAvg.Movie1,ComAvg.Movie2) as mid1 
			inner join movies on mid1.movie1 = movies.title) as mid2
		inner join movies on mid2.movie2 = movies.title) as nosim 
	where nosim.movieid1 != nosim.movieid2 order by nosim.movieid1;


Select movies.title into recommendation from
	(Select p.movieid2 as movieid from
		(select movieid2, Sum( s.rating*s.sim)/sum(s.sim) as simtot from 
			(select seen.movieid1,seen.rating, seen.movieid2, seen.sim from
			 	(select excset.movieid as movieid1, excset.rating,simil.movieid2, simil.sim from
					(select movieid ,rating from
						(select movieid, rating from ratings
							 where userid=:v1) as minus 
						order by minus, movieid) as excset
				 	inner join simil on excset.movieid=simil.movieid1
			 		order by excset.movieid, simil.movieid2) as seen
			 	where seen.movieid2 in
				(
					select movieid from ratings where userid = :v1
				)
			) as s
	 	group by s.movieid2) as p
	where p.simtot >3.9) tit
inner join movies on tit.movieid = movies.movieid;