# full docs: https://inquirerpy.readthedocs.io/en/latest/

from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
import os

import modules.item_actions as item_actions
from classes.catalogue import Catalogue

def show_main_menu(catalogue: Catalogue):  
    stop_menu = False
    
    while not stop_menu:
        os.system('cls')  
        print()
        print("="*80)
        
        area = main_menu_selection()
        
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
                     
            case "people":        
                action = people_menu_selection()
                
                match action:
                    case 1:
                        pass
                    
                    case 2:
                        pass
                             
            case "catalogue":      
                action = catalogue_menu_selection()
                
                match action:
                    case 1: #SEARCH
                        result = item_actions.search_item()
                        if result[0] == 0:
                            print("Search failed.")
                            print(result[1])
                    
                    case 2: #ADD
                        result = catalogue.add_book()
                        if result[0] == 1:
                            print("New book added")
                        elif result[0] == 0:
                            print(result[1])
                        
                        wait_for_keypress = input("Press ENTER to continue...")
                    case 3: #DELETE
                        pass

                    case 4: #LIST
                        result = item_actions.list_items()
                        if result[0] == 0:
                            print("Could not list items.")
                            print(result[1])

                        if result[2]:
                            print(f"You selected item: {result[2]}")
                            any_key = input("Press ENTER to continue...")
                

def main_menu_selection():
    selected_action = inquirer.select(
        message="\nSELECT AN AREA TO WORK WITH:",
        choices=[
            Choice(value="lend", name="• LEND ITEM •"),
            Choice(value="return", name="• RETURN ITEM •"),
            Separator(),
            Choice(value="catalogue", name="• LIBRARY CATALOGUE •"),
            Choice(value="people", name="• MANAGE CLIENTS •"),
            Separator(),
            Choice(value=None, name="Exit"),
        ],
        default=1,
    ).execute()

    return selected_action    
                    
def catalogue_menu_selection():
    """
    Display a menu for catalogue-related actions and return the selected action.

    This function presents a menu to the user with options related to managing
    a library catalogue, such as searching for books, adding new books, or 
    deleting books from the catalogue.
    """
    selected_action = inquirer.select(
        message="Select action:",
        choices=[
            Choice(value=1, name="1. SEARCH for item"),
            Choice(value=4, name="2. LIST all active items"),            
            Choice(value=2, name="3. ADD new book to catalogue"),
            Choice(value=3, name="4. DELETE a book from catalogue"),
            Separator(),
            Choice(value=5, name="5. List deleted items"),
            Separator(),
            Choice(value=99, name="Back to main menu"),
        ],
        default=1,
    ).execute()

    return selected_action

def people_menu_selection():
    selected_action = inquirer.select(
        message="Select action:",
        choices=[
            Choice(value=1, name="1. Register new READER"),
            Choice(value=2, name="2. Register new LIBRARIAN"),
            Separator(),
            Choice(value=99, name="Back to main menu"),
        ],
        default=1,
    ).execute()
        
    return selected_action
