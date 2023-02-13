import subprocess
import re
from helper_tools import misc


class Get_Current_Location_Of_Users:
    def __init__(self,db):
        self.locale_code_to_org_unit_map = {}
        self.org_unit_to_locale_code_map = {}
        self.cursor = db.cursor()
        
        self.get_locations(self.cursor,self.locale_code_to_org_unit_map,self.org_unit_to_locale_code_map)

    def get_locations(self,cursor,locale_code_to_org_unit_map,org_unit_to_locale_code_map):
        self.cursor = cursor
        self.records = self.cursor.fetchall()
        self.locale_code_to_org_unit_map = dict(locale_code_to_org_unit_map)
        self.org_unit_to_locale_code_map = dict(org_unit_to_locale_code_map)
        
        for row in self.records:
            self.locale_code_to_org_unit_map.update({row[0] : row[1]})
            self.org_unit_to_locale_code_map.update({row[1] : row[0]})

        if(len(self.locale_code_to_org_unit_map) != 0) and (len(self.org_unit_to_locale_code_map) != 0):
            self.cursor.close()
            return [self.locale_code_to_org_unit_map,self.org_unit_to_locale_code_map]
        
    



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

    needed_dicts = Get_Current_Location_Of_Users(db)
    print(needed_dicts[0] + "\n" + needed_dicts[1])

    

if __name__ == "__main__":
    main()