CREATE TABLE MyDimDate(
    dateid integer not null primary key,
    month integer NOT NULL,
    monthname varchar(10) NOT NULL,
    year integer NOT NULL,
    weekday integer NOT NULL,
    weekdayname varchar(5) NOT NULL,
    quarter integer NOT NULL,
    quartername varchar (2) NOT NULL
    );


CREATE TABLE MyDimWaste(
    wasteid integer not null primary key,
    waste_type varchar(30) not null
);

CREATE TABLE MyDimZone(
    zoneid integer not null primary key,
    collection_zone varchar(30) not null,
    city varchar(30) not null
);





CREATE TABLE MyFactTrips(
    tripid integer not null primary key,
    dateid integer not null,
    wasteid integer not null,
    zoneid integer not null,
    tons_waste decimal(10,2) not null
);
