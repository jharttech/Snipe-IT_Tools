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
    try:
        db = mysql.connector.connect(
            host = db_info[0],
            database = db_info[1],
            user = db_info[2],
            password = db_info[3]
        )
        if db.is_connected():
            return [True,db]
    except mysql.connector.Error as e:
        return [e,None]
        