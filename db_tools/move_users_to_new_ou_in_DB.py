import subprocess
from helper_tools import misc


class Get_Db_Info:
    def __init__(self,db_info):
        self.return_info_list(db_info)

    def return_info_list(self,db_info):
        self.db_info = db_info
        return self.db_info

    @classmethod
    def get(cls):
        hostname = input("\nPlease enter the host of the Database: ")
        dbase = input("\nPlease enter the database you wish to use: ")
        username = input("\nPlease enter the user for the Database: ")
        # Implenent way to obfuscate
        passw = input("Please enter the Database password: ")
        db_info = [hostname,dbase,username,passw]
        return cls(db_info)



def main():
    db_info = Get_Db_Info.get()
    misc.connect_to_db(db_info)


if __name__ == "__main__":
    main()