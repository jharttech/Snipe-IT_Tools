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
    


if __name__ == "__main__":
    main()