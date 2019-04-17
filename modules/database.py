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
    def insertFile(self,file,datePiiDiscovered,dateScanned,dateNoPii,piiCount,piiTypes):
        try:
            db_file = "config/db/idqat_default.db"
            connection = sqlite3.connect(db_file)
            insert_file_sql = "INSERT INTO files_scanned values(NULL,'"+file+"','"+str(datePiiDiscovered)+"','"+dateScanned+"','"+str(dateNoPii)+"','"+str(piiCount)+"','"+piiTypes+"')" # insert file record
            print insert_file_sql
            executeSQL = connection.cursor()
            executeSQL.execute(insert_file_sql)
            return executeSQL.lastrowid
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
        executeSQL = connection.cursor()
        executeSQL.execute(check_file_exists_sql).rowcount
