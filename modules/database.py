#!/usr/bin/python
#
# 2019 (c) GNU, WeakNet Labs
# This product should come with the GNU License
# Douglas Berdeaux
# weaknetlabs@gmail.com
#
# OS Independent PII/SysPII Query and Alert Tool
# Databse class module.
#
##
import sqlite3
from sqlite3 import Error
import sys
class Database:
    # Get all records - this won't realistically be used
    def queryAllRecords(self):
        try:
            db_file = "config/db/idqat_default.db"
            connection = sqlite3.connect(db_file) # connect to the database
            select_all_sql = "SELECT * from files_scanned;" # files_scanned is the table with all file data
            executeSQL = connection.cursor()
            executeSQL.execute(create_table_sql)
            rows = executeSQL.fetchall()
            for rown in rows:
                print row
        except Error as error:
            print colors.DANGER+"[!] There was an error accessing the file: "+sys.argv[1]+":\n"+str(error)+"\n"+colors.RST
            sys.exit(1) # exit with no connection
        finally:
            connection.close()

    # Method to insert a file record for each file scanned.
    def insertFile(self,valueList):
        # print valueList # DEBUG
        try:
            db_file = "config/db/idqat_default.db" # TODO offload this value to a config file.
            connection = sqlite3.connect(db_file) # create a connection object
            # construct an INSERT statement, pass an arrya of values to this method. Order is important.
            insert_file_sql = "INSERT into files_scanned(file_id,file_name,date_pii_discovered,date_scanned,date_no_pii,pii_count,pii_types_found) values(NULL,?,?,?,?,?,?)"
            with connection:
                executeSQL = connection.cursor() # open the connetcion object
                executeSQL.execute(insert_file_sql,valueList) # send the SQL statement to SQLite3
            return executeSQL.lastrowid # returned it
        except Error as error:
            print error
            sys.exit(1)
        finally:
            connection.close()

    # Method to check if file record exists:
    def checkFileRecord(self,file):
        db_file = "config/db/idqat_default.db"
        connection = sqlite3.connect(db_file)
        check_file_exists_sql = "SELECT * from files_scanned where file_name = '"+file+"';"
        with connection:
            executeSQL = connection.cursor()
            executeSQL.execute(check_file_exists_sql)
            resultSet = executeSQL.fetchone()
            if resultSet == None:
                return 0
            else:
                return 1
















# EOF
