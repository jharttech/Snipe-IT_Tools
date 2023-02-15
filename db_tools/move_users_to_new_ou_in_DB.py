import subprocess
import re
from helper_tools import misc
import mysql.connector
import os
import csv
import datetime


class Get_Locations:
    def __init__(self, db):
        self.locale_code_to_org_unit_map = {}
        self.org_unit_to_locale_code_map = {}
        self.cursor = db.cursor()

        self.get_locations(
            self.cursor,
            self.locale_code_to_org_unit_map,
            self.org_unit_to_locale_code_map,
        )

    def get_locations(
        self, cursor, locale_code_to_org_unit_map, org_unit_to_locale_code_map
    ):
        self.cursor = cursor
        print("Now going to gather all possible locations...")
        self.cursor.execute("SELECT id, name FROM locations")
        self.records = self.cursor.fetchall()
        self.locale_code_to_org_unit_map = dict(locale_code_to_org_unit_map)
        self.org_unit_to_locale_code_map = dict(org_unit_to_locale_code_map)

        for row in self.records:
            self.locale_code_to_org_unit_map.update({row[0]: row[1]})
            self.org_unit_to_locale_code_map.update({row[1]: row[0]})

        if (len(self.locale_code_to_org_unit_map) != 0) and (
            len(self.org_unit_to_locale_code_map) != 0
        ):
            self.cursor.close()
            return [self.locale_code_to_org_unit_map, self.org_unit_to_locale_code_map]

    def get_locale_code_to_org_unit_map(self):
        return self.locale_code_to_org_unit_map

    def get_org_unit_to_locale_code_map(self):
        return self.org_unit_to_locale_code_map


class Get_User_Location:
    def __init__(self, db):
        self.user_locale = {}
        self.cursor = db.cursor()

        self.get_user_location(self.user_locale, self.cursor)

    def get_user_location(self, user_locale, cursor):
        self.cursor = cursor
        self.user_locale = dict(user_locale)
        print("Now gathering user locations...")
        self.cursor.execute("SELECT location_id, username FROM users")
        self.table_records = self.cursor.fetchall()

        for row in self.table_records:
            self.user_locale.update({row[1]: row[0]})
        if len(self.user_locale) != 0:
            self.cursor.close()
            return self.user_locale
        else:
            self.cursor.close()
            print("No User Data Found!!")

    def get_user_locale_dict(self):
        return self.user_locale


class Write_Logs_And_Move_User:
    def __init__(
        self,
        locale_code_to_org_unit_map,
        org_unit_to_locale_code_map,
        db,
        filename,
        user_locale,
    ):
        self.file = filename
        self.line_count = 0
        self.error_count = 0
        self.moved = 0
        self.locale_code_to_org_unit_map = locale_code_to_org_unit_map
        self.org_unit_to_locale_code_map = org_unit_to_locale_code_map
        self.user_locale = user_locale
        self.db = db
        self.divider = ["#########################"]
        self.error_file = "logs/error_log.csv"
        self.log_file = "logs/moving_ou_logs.csv"
        self.timestamp = datetime.datetime.now()

        self.move_user_and_write_log()

    def move_user_and_write_log(self):
        with open(self.file, mode="r") as self.csv_file:
            self.csv_reader = csv.reader(self.csv_file, delimiter=",")
            self.n_col = len(next(self.csv_reader))
            self.csv_file.seek(0)
            for row in self.csv_reader:
                if self.line_count == 0:
                    for x in range(0, self.n_col):
                        self.col_name = str(row[x])
                        if self.col_name == "Location":
                            # print("Location Header Found!")
                            self.org_unit_col = x
                        if self.col_name == "Username":
                            # print("Username Header found!")
                            self.username_col = x
                    self.line_count += 1
                else:
                    self.real_username = row[self.username_col]
                    self.real_OU = row[self.org_unit_col]
                    self.OU_locale_number = self.org_unit_to_locale_code_map.get(
                        self.real_OU
                    )
                    self.original_locale_num = self.user_locale.get(self.real_username)
                    self.original_OU = self.locale_code_to_org_unit_map.get(
                        self.original_locale_num
                    )

                    if str(self.original_locale_num) == str(self.OU_locale_number):
                        # print("Nothing to move here...")
                        continue
                    elif self.OU_locale_number == None:
                        self.error_count += 1
                        self.temp_line = (self.timestamp, "ORG user Error", row)
                        with open(self.error_file, mode="a") as self.needed_file:
                            self.errors = csv.writer(self.needed_file, delimiter=",")
                            self.errors.writerow(self.temp_line)
                    elif self.original_locale_num == None:
                        self.error_count += 1
                        self.temp_line = (
                            self.timestamp,
                            "User was never in Snipe DB",
                            row,
                        )
                        with open(self.error_file, mode="a") as self.needed_file:
                            self.errors = csv.writer(self.needed_file, delimiter=",")
                            self.errors.writerow(self.temp_line)
                    elif str(self.original_locale_num) != str(self.OU_locale_number):
                        self.moved += 1
                        update_db(self.db, self.real_username, self.OU_locale_number)
                        self.temp_move_line = (
                            self.timestamp,
                            "user "
                            + self.real_username
                            + " was moved from "
                            + self.original_OU
                            + " to "
                            + self.real_OU,
                        )
                        with open(self.log_file, mode="a") as self.needed_file:
                            self.logs = csv.writer(self.needed_file, delimiter=",")
                            self.logs.writerow(self.temp_move_line)
                    else:
                        print(
                            "Unknown error, check csv data in "
                            + self.file
                            + "! Quitting now!"
                        )
                        misc.exit_message()

        if self.error_count > 0:
            print(
                """There were some errors in the moving of users to their new OU in the database,
            Old user OU will remain in use.  Please check the error log for more details
            (logs/error_log.csv)"""
            )

            with open(self.error_file, mode="a") as self.needed_file:
                self.errors = csv.writer(self.needed_file, delimiter=",")
                self.errors.writerow(self.divider)
        if self.moved > 0:
            with open(self.log_file, mode="a") as self.needed_file:
                self.logs = csv.writer(self.needed_file, delimiter=",")
                self.logs.writerow(self.divider)
        print(
            str(self.moved)
            + """ users were moved.
        All done moving students to new OUs in snipe database.  Thank you!"""
        )
        misc.exit_message()


def update_db(db, user, location):
    cursor = db.cursor()
    db = db
    user = user
    location = location
    print("Fixing to move user...")
    # try:
    cursor.execute(
        "UPDATE users SET location_id=%s WHERE username=%s",
        (location, user),
    )
    db.commit()
    cursor.close()


# except mysql.connector.errors.Error as e:
# self.cursor.close()
# print(e)


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
        filename = input(
            "\nPlease enter the path and csv file of users you want moved: "
        )
        if os.path.isfile(filename):
            break
        else:
            print("\nFile does not exist, please try again!!")

    needed_dicts = Get_Locations(db)
    needed_user_locale_dict = Get_User_Location(db)
    user_locale = needed_user_locale_dict.get_user_locale_dict()
    print("User locales are " + str(user_locale))
    locale_code_to_org_unit_map = needed_dicts.get_locale_code_to_org_unit_map()
    print("Locale to Org Unit " + str(locale_code_to_org_unit_map))
    org_unit_to_locale_code_map = needed_dicts.get_org_unit_to_locale_code_map()
    print("Org unit to Locale " + str(org_unit_to_locale_code_map))

    Write_Logs_And_Move_User(
        locale_code_to_org_unit_map,
        org_unit_to_locale_code_map,
        db,
        filename,
        user_locale,
    )


if __name__ == "__main__":
    main()
