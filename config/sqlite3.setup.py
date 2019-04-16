#!/usr/bin/python
import sqlite3
from sqlite3 import Error
import sys # pass to me the db file

def create_connection(db_file):
    try:
        connection = sqlite3.connect(db_file)
        print "[*] Connection to database file successful. Version: "+sqlite3.version
        print "[*] Creating table structure for new database file."

        create_table_sql = """
            create table if not exists files_scanned(
                file_id int not null primary key, -- id of file
                file_name text not null, -- file name including path from idqat
                date_pii_discovered text not null, -- date pii discovered in file
                date_scanned text not null, -- date scanned
                date_no_pii text not null, -- date scanned and no PII found
                pii_count int not null,
                pii_types_found text -- FK to pii_types.type_id
            );
        """
        executeSQL = connection.cursor()
        executeSQL.execute(create_table_sql)
        print "[*] Process completed."
        sys.exit(0)
    except Error as error:
        print "[!] There was an error accessing the file: "+sys.argv[1]+":\n"+str(error)+"\n"
        sys.exit(1) # exit with no connection
    finally:
        connection.close()

# Create tables:


# connect to the DB file:
create_connection(sys.argv[1])
