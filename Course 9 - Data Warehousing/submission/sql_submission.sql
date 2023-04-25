select facttrips.stationid, trucktype, sum(wastecollected) as total_waste
from facttrips
left join dimstation
on facttrips.stationid = dimstation.stationid
left join dimtruck
on facttrips.truckid=dimtruck.truckid
group by grouping sets(facttrips.stationid, trucktype)



select year, city, facttrips.station_id, avg(wastecollected) as average_waste
from facttrips
left join dimstation
on facttrips.stationid = dimstation.stationid
left join dimdate
on facttrips.dateid=dimdate.dateid
group by cube(year,city, facttrips.stationid)






select year, city, facttrips.stationid, avg(wastecollected) as average_waste
from facttrips
left join dimstation
on facttrips.stationid = dimstation.stationid
left join dimdate
on facttrips.dateid=dimdate.dateid
group by cube(year,city,facttrips.stationid)
order by year, city, facttrips.stationid



CREATE TABLE maxwastestats(city, stationid, trucktype, max_waste) AS
  (select city, facttrips.stationid, trucktype, max(wastecollected) as max_waste
from facttrips
left join dimtruck
on facttrips.truckid = dimtruck.truckid
left join dimdate
on facttrips.dateid=dimdate.dateid
left join dimstation
on facttrips.stationid=dimstation.stationid
group by city, facttrips.stationid, trucktype)
     DATA INITIALLY DEFERRED
     REFRESH DEFERRED
     MAINTAINED BY SYSTEM;