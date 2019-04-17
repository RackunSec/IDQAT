#!/usr/bin/python
#
# 2019 (c) GNU, WeakNet Labs
# This product should come with the GNU License
# Douglas Berdeaux
# weaknetlabs@gmail.com
#
# IDQAT Setup Script - requires SQLite3
#
#
##
import sqlite3
from sqlite3 import Error
import sys # pass to me the db file
from modules.colors import Colors

colors = Colors()

if len(sys.argv) != 2:
    # Help
    print colors.DANGER+"\n[*] Usage:\n\tpython sqlite3.setup.py (path to db file)\n"+colors.RST
    exit (1) # die

def create_connection(db_file):
    try:
        connection = sqlite3.connect(db_file)
        print "[*] Connection to database file successful. Version: "+sqlite3.version
        print "[*] Creating table structure for new database file."

        create_table_sql = """
            create table if not exists files_scanned(
                file_id integer primary key, -- id of file
                file_name text not null, -- file name including path from idqat
                date_pii_discovered text, -- date pii discovered in file
                date_scanned text not null, -- date scanned
                date_no_pii text not null, -- date scanned and no PII found
                pii_count int not null,
                pii_types_found text -- FK to pii_types.type_id
            );
        """
        executeSQL = connection.cursor()
        executeSQL.execute(create_table_sql)
        print colors.OK+"[*] Process completed."+colors.RST
        sys.exit(0)
    except Error as error:
        print colors.DANGER+"[!] There was an error accessing the file: "+sys.argv[1]+":\n"+str(error)+"\n"+colors.RST
        sys.exit(1) # exit with no connection
    finally:
        connection.close()

# Create tables:


# connect to the DB file:
create_connection(sys.argv[1])
