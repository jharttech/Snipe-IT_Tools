import subprocess
from helper_tools import misc


# Create tool class
class Tool:
    def __init__(self,tool):
        self.tool=tool

    def __str__(self):
        return self.tool
    
    @classmethod
    def get(cls,tool_dict):
        # Get user input on what tool they want to use
        dict_num = input("\nWhat tool would you like to utilize?\n")
        tool = tool_dict.get(dict_num)
        return cls(tool)


def main():
    # Define tool dictionary
    tool_dict = {
        "1":"move_users_to_new_ou_in_DB",
        "2":"update_assets_in_DB",
        "3":"Exit"
    }

    # Clear the terminal
    subprocess.Popen(["clear"], stdout=subprocess.PIPE)
    print("\nWelcome to the MG GAM tools\n")
    #MAKE SETUP CLASS IN MISC misc.Setup()
    misc.Dict_Print(tool_dict)
    tool = Tool.get(tool_dict)
    # Change to a case in the future as case switch now exists in Python >=3.10
    if str(tool) == "move_users_to_new_ou_in_DB":
        move_users_to_new_ou_in_DB.main()
    elif str(tool) == "update_assets_in_DB":
        update_assets_in_DB.main()
    elif str(tool) == "Exit":
        misc.exit_message()
    


if __name__ == "__main__":
    main()