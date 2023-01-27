import subprocess
import mysql.connector
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

def connect_to_db(db_info):
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
        if db.is_connected():
            print("Connection to Database successful!")
            return [True,db]
    except mysql.connector.Error as e:
        return [e,None]
        