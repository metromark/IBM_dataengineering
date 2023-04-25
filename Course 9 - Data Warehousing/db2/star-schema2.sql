
-- drop table
-- drop table FactBilling;
-- dropped table
CREATE TABLE FactBilling(billid integer not null primary key,customerid integer NOT NULL,monthid integer NOT NULL,billedamount integer NOT NULL);

-- drop table
-- drop table DimMonth;
-- dropped table

CREATE TABLE DimMonth(monthid integer NOT NULL PRIMARY KEY,year integer NOT NULL,month integer NOT NULL,monthname varchar(10) NOT NULL,quarter integer NOT NULL,quartername varchar(2) NOT NULL);

-- drop table
-- drop table DimCustomer;
-- dropped table


CREATE TABLE DimCustomer(customerid integer NOT NULL PRIMARY KEY,category varchar(10) NOT NULL,country varchar(40) NOT NULL,industry varchar(40) NOT NULL);

ALTER TABLE FactBilling ADD FOREIGN KEY (customerid) REFERENCES DimCustomer (customerid);
ALTER TABLE FactBilling ADD FOREIGN KEY (monthid) REFERENCES DimMonth (monthid);
