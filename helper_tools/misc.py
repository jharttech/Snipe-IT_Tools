import subprocess
import mysql.connector
from datetime import date

d = date.isoformat(date.today())

# Define the Dict_Print class to print dictionary keys and values in numerical order.  This is not natively done in python3.4
class Dict_Print:
    def __init__(self, data):
        self.data = data
        self.data_list = list(map(int, self.data))
        self.data_list = sorted(self.data_list)
        print("\n")
        for i in range(0, len(self.data)):
            print(
                str(self.data_list[i]) + " : " + self.data.get(str(self.data_list[i]))
            )


class Setup:
    def __init__(self):
        files = ["logs/error_log.csv","logs/moving_ou_logs.csv"]
        
        for i in files:
            create = subprocess.Popen(["touch",str(i)], stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)

def connect_to_db():
    hostname = input("\nPlease enter the host of the Database: ")
    dbase = input("\nPlease enter the database you wish to use: ")
    username = input("\nPlease enter the user for the Database: ")
    # Implenent way to obfuscate
    passw = input("Please enter the Database password: ")
    try:
        db = mysql.connector.connect(
            host = hostname,
            database = dbase,
            user = username,
            password = passw
        )
        print("Connection to the database successful!!")
    except mysql.connector.errors.Error as e:
        print(e)


def backup_db():
    user = input("\nWhat is the database user name? ")
    dbase_name = input("\nWhat is the database name? ")
    backup = subprocess.Popen(["mysqldump","-u",user,"-p","--routines","--triggers","--result-file="+d+"_"+dbase_name+".sql",dbase_name],stderr=subprocess.PIPE)
    backup.communicate()
    backup.wait()
        