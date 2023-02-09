import subprocess
from helper_tools import misc


def main():
    while True:
        backup = input("\nDo you want to back up the database? ").lower()
        if not re.search(r"^(y|n)$", restart):
            print("Invalid response please enter 'y' or 'n'")
        else:
            break

    if backup == "y":
        misc.backup_db()
    elif backup == "n":
        misc.connect_to_db()

    

if __name__ == "__main__":
    main()