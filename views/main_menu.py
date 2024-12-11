# full docs: https://inquirerpy.readthedocs.io/en/latest/

from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
import os

import modules.item_actions as item_actions

def show_main_menu():  
    stop_menu = False
    
    while not stop_menu:
        os.system('cls')  
        print()
        print("="*80)
        
        area = inquirer.select(
            message="\nSELECT AN AREA TO WORK WITH:",
            choices=[
                Choice(value="lend", name="• LEND ITEM •"),
                Choice(value="return", name="• RETURN ITEM •"),
                Separator(),
                Choice(value="catalogue", name="• LIBRARY CATALOGUE •"),
                Choice(value="persons", name="• MANAGE CLIENTS •"),
                Separator(),
                Choice(value=None, name="Exit"),
            ],
            default=1,
        ).execute()
        
        match area:
            case None:
                stop_menu = True
                print()
                print("Thank you for using this program.\nSee you next time.")
                print()

            case "lend": 
                pass
            
            case "return": 
                pass
                     
            case "persons":        
                action = persons_menu()
                
                match action:
                    case 1:
                        pass
                    
                    case 2:
                        pass
                
                
            case "catalogue":      
                action = catalogue_menu()
                
                match action:
                    case 1: #SEARCH
                        pass
                    
                    case 2: #ADD
                        result = item_actions.add_book()
                        if result[0] == 1:
                            print("New book added")
                        elif result[0] == 0:
                            print(result[1])
                            
                    case 3: #DELETE
                        pass

                    case 4: #LIST
                        result = item_actions.list_items()
                        if result[0] == 0:
                            print("Could not list items.")
                            print(result[1])
                
                any_key = input("Press ENTER to continue...")
                
def persons_menu():
    selected_action = inquirer.select(
        message="Select action:",
        choices=[
            Choice(value=1, name="Add new person"),
            Choice(value=2, name="REGISTER new reader"),
            Separator(),
            Choice(value=99, name="Back to main menu"),
        ],
        default=1,
    ).execute()
        
    return selected_action

def catalogue_menu():
    """
    Display a menu for catalogue-related actions and return the selected action.

    This function presents a menu to the user with options related to managing
    a library catalogue, such as searching for books, adding new books, or 
    deleting books from the catalogue.

    Returns:
        int: The selected action, where:
            1 - Search
            2 - Add new book
            3 - Delete a book from catalogue
            99 - Back to main menu
    """
    selected_action = inquirer.select(
        message="Select action:",
        choices=[
            Choice(value=1, name="SEARCH"),
            Choice(value=4, name="LIST all items"),            
            Choice(value=2, name="ADD new book"),
            Choice(value=3, name="DELETE a book from catalogue"),
            Separator(),
            Choice(value=99, name="Back to main menu"),
        ],
        default=1,
    ).execute()

    return selected_action
