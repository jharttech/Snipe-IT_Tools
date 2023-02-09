import subprocess
import re
from helper_tools import misc


class Get_Current_Location_Of_Users:
    def __init__(self):
        locale_code_to_org_unit_map = {}
        org_unit_to_locale_code_map = {}
        #cursor = db.cursor()


def main():
    while True:
        backup = input("\nDo you want to back up the database? ").lower()
        if not re.search(r"^(y|n)$", backup):
            print("Invalid response please enter 'y' or 'n'")
        else:
            break

    if backup == "y":
        misc.backup_db()
    elif backup == "n":
        connect = misc.connect_to_db()
        db = connect

    #Get_Current_Location_Of_Users()

    

if __name__ == "__main__":
    main()