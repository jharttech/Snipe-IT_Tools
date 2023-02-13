import subprocess
import re
from helper_tools import misc
import mysql.connector
import os


class Get_Current_Location_Of_Users:
    def __init__(self,db):
        self.locale_code_to_org_unit_map = {}
        self.org_unit_to_locale_code_map = {}
        self.cursor = db.cursor()
        
        self.get_locations(self.cursor,self.locale_code_to_org_unit_map,self.org_unit_to_locale_code_map)


    def get_locations(self,cursor,locale_code_to_org_unit_map,org_unit_to_locale_code_map):
        self.cursor = cursor
        self.cursor.execute("SELECT id, name FROM locations")
        self.records = self.cursor.fetchall()
        self.locale_code_to_org_unit_map = dict(locale_code_to_org_unit_map)
        self.org_unit_to_locale_code_map = dict(org_unit_to_locale_code_map)
        
        for row in self.records:
            self.locale_code_to_org_unit_map.update({row[0] : row[1]})
            self.org_unit_to_locale_code_map.update({row[1] : row[0]})

        if(len(self.locale_code_to_org_unit_map) != 0) and (len(self.org_unit_to_locale_code_map) != 0):
            self.cursor.close()
            return [self.locale_code_to_org_unit_map,self.org_unit_to_locale_code_map]

    def get_locale_code_to_org_unit_map(self):
        return self.locale_code_to_org_unit_map

    def get_org_unit_to_locale_code_map(self):
        return self.org_unit_to_locale_code_map
        

def write_logs_and_move_user(locale_code_to_org_unit_map,org_unit_to_locale_code_map,db,filename):
    file = filename
    line_count = 0
    error_count = 0
    moved = 0
    divider = "#########################"
    error_file = 'students/error_log.csv'
    log_file = 'students/moving_ou_logs.csv'


    



def main():
    while True:
        backup = input("\nDo you want to back up the database? ").lower()
        if not re.search(r"^(y|n)$", backup):
            print("Invalid response please enter 'y' or 'n'")
        else:
            break

    if backup == "y":
        misc.backup_db()
    connect = misc.connect_to_db()
    db = connect
    
    while True:
        filename = input("\nPlease enter the path and csv file of users you want moved: ")
        if os.path.isfile(filename):
            break
        else:
            print("\nFile does not exist, please try again!!")

    needed_dicts = Get_Current_Location_Of_Users(db)
    locale_code_to_org_unit_map = needed_dicts.get_locale_code_to_org_unit_map()
    org_unit_to_locale_code_map = needed_dicts.get_org_unit_to_locale_code_map()

    write_logs_and_move_user(locale_code_to_org_unit_map,org_unit_to_locale_code_map,db,filename)
    
    


    

if __name__ == "__main__":
    main()