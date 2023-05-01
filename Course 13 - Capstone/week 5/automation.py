# Import libraries required for connecting to mysql
import mysql.connector

# Import libraries required for connecting to DB2
import ibm_db

import datetime


# Connect to MySQL
connection = mysql.connector.connect(user='root', password='MTczMDEtbXB0b2xl',host='127.0.0.1',database='sales')

cursor = connection.cursor()

# Connect to DB2
dsn_hostname = "815fa4db-dc03-4c70-869a-a9cc13f33084.bs2io90l08kqb1od8lcg.databases.appdomain.cloud" # e.g.: "dashdb-txn-sbox-yp-dal09-04.services.dal.bluemix.net"
dsn_uid = "kgy38833"        # e.g. "abc12345"
dsn_pwd = "1bdonIsLl6qcw8Lu"      # e.g. "7dBZ3wWt9XN6$o0J"
dsn_port = "30367"                # e.g. "50000" 
dsn_database = "bludb"            # i.e. "BLUDB"
dsn_driver = "{IBM DB2 ODBC DRIVER}" # i.e. "{IBM DB2 ODBC DRIVER}"           
dsn_protocol = "TCPIP"            # i.e. "TCPIP"
dsn_security = "SSL"              # i.e. "SSL"

#Create the dsn connection string
dsn = (
    "DRIVER={0};"
    "DATABASE={1};"
    "HOSTNAME={2};"
    "PORT={3};"
    "PROTOCOL={4};"
    "UID={5};"
    "PWD={6};"
    "SECURITY={7};").format(dsn_driver, dsn_database, dsn_hostname, dsn_port, dsn_protocol, dsn_uid, dsn_pwd, dsn_security)

# create connection
conn = ibm_db.connect(dsn, "", "")
print ("Connected to database: ", dsn_database, "as user: ", dsn_uid, "on host: ", dsn_hostname)


# Find out the last rowid from DB2 data warehouse
# The function get_last_rowid must return the last rowid of the table sales_data on the IBM DB2 database.

def get_last_rowid():
    sql_query = "SELECT max(rowid) FROM sales_data"
    exec_stmt = ibm_db.exec_immediate(conn, sql_query)
    fetchtuple = ibm_db.fetch_tuple(exec_stmt)
    return fetchtuple


last_row_id = get_last_rowid()
print("Last row id on production datawarehouse = ", last_row_id)

# List out all records in MySQL database with rowid greater than the one on the Data warehouse
# The function get_latest_records must return a list of all records that have a rowid greater than the last_row_id in the sales_data table in the sales database on the MySQL staging data warehouse.

def get_latest_records(rowid):
    SQL = f"select *, 0 as price, '{str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}' from sales_data where ROWID > {rowid[0]}"

    cursor.execute(SQL)
    fetched_records = cursor.fetchall()
    print(fetched_records)
    return fetched_records

new_records = get_latest_records(last_row_id)

print("New rows on staging datawarehouse = ", len(new_records))

# Insert the additional records from MySQL into DB2 data warehouse.
# The function insert_records must insert all the records passed to it into the sales_data table in IBM DB2 database.

def insert_records(records):
    # pass
    for new_row in records:
        print(new_row)
        new_row_SQL = "INSERT INTO sales_data VALUES " + str(new_row)
        stmt = ibm_db.prepare(conn, new_row_SQL)
        ibm_db.execute(stmt)

insert_records(new_records)
print("New rows inserted into production datawarehouse = ", len(new_records))

# disconnect from mysql warehouse
connection.close()

# disconnect from DB2 data warehouse
ibm_db.close(conn)


# End of program
