import subprocess
from helper_tools import misc


class Get_Db_Info:
    def __init__(self,hostname,dbase,username,passw):
        self.hostname = hostname
        self.dbase = dbase
        self.username = username
        self.passw = passw

    def return_db_info(self):
        return self.hostname,self.dbase,self.username,self.passw

    @classmethod
    def get(cls):
        hostname = input("\nPlease enter the host of the Database: ")
        dbase = input("\nPlease enter the database you wish to use: ")
        username = input("\nPlease enter the user for the Database: ")
        # Implenent way to obfuscate
        passw = input("Please enter the Database password: ")
        return cls(hostname,dbase,username,passw)



def main():
    db_info = Get_Db_Info.get()
    misc.connect_to_db(db_info[0],db_info[1],db_info[2],db_info[3])


if __name__ == "__main__":
    main()