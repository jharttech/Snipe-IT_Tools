import subprocess
from helper_tools import misc


def main():
    backup = input("\nDo you want to back up the database? ").lower()
    if backup == "y":
        misc.backup_db()
    elif backup == "n":
        misc.connect_to_db()


if __name__ == "__main__":
    main()