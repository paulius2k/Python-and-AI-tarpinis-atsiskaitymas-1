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
                search_str = str(input("\n  Enter search keyword to find the item: ")).lower()
                top_msg = f"LISTING ITEMS BY SEARCH KEYWORD '{search_str}'"
                list_result = item_actions.list_items(catalogue, search_str, 1, top_msg)
                
                if list_result[0] == 1:
                    print("Search failed.")
                    print(list_result[1])
            
                if list_result[2]:
                    print(f"\nSelected item id: {list_result[2]}\n")
                    show_item_menu(catalogue, list_result[2])
            
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
                    case "search":
                        search_str = str(input("\n  Enter search keyword: ")).lower()
                        top_msg = f"LISTING ITEMS BY SEARCH KEYWORD '{search_str}'"
                        list_result = item_actions.list_items(catalogue, search_str, 1, top_msg)
                        
                        if list_result[0] == 1:
                            print("Search failed.")
                            print(list_result[1])
                    
                        if list_result[2]:
                            print(f"\nSelected item id: {list_result[2]}\n")
                            show_item_menu(catalogue, list_result[2])
                            
                    case "add":
                        result = catalogue.add_book()
                        if result[0] == 1:
                            print("New book added")
                        elif result[0] == 0:
                            print(result[1])
                        
                        wait_for_keypress = input("Press ENTER to continue...")
                        
                    case "delete":
                        pass

                    case "list_all":
                        search_str = ""
                        top_msg = f"LISTING ALL ITEMS"
                        list_result = item_actions.list_items(catalogue, search_str, 1, top_msg)

                        if list_result[0] == 1:
                            print("No items in the catalogue.")
                            print(list_result[1])
                            wait_for_keypress = input("Press ENTER to continue...")
                            
                        if list_result[2]:
                            print(f"\nSelected item id: {list_result[2]}\n")
                            show_item_menu(catalogue, list_result[2])
                                    
                    case "list_del":
                        search_str = ""
                        top_msg = f"LISTING ALL DELETED ITEMS"
                        list_result = item_actions.list_items(catalogue, search_str, 2, top_msg)

                        if list_result[0] == 1:
                            print("No items in the catalogue.")
                            print(list_result[1])  
                            wait_for_keypress = input("Press ENTER to continue...")
                         
                    # case _:
                    #     print("Function not ready yet.")
                    #     any_key = input("Press ENTER to continue...")
                                 
def show_item_menu(catalogue: Catalogue, item_id):
    item_action = item_menu_selection()

    match item_action:
        case "lend":
            pass
        
        case "delete_item":
            answer = user_confirmation("Do you really want to delete the item?")
            
            if answer == "yes":
                delete_result = catalogue.delete_item(item_id)
                if delete_result == 1:
                    print("\nItem deleted successfully.")
                else:
                    print(delete_result[1])                                            
            else:
                print("\nAction cancelled by user.")
                
            any_key = input("Press ENTER to continue...")

def main_menu_selection():
    selected_action = inquirer.select(
        message="\nLIBRARIAN MENU. SELECT AN AREA TO WORK WITH:\n",
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
            Choice(value="search", name="1. SEARCH for item"),
            Choice(value="list_all", name="2. LIST all active items"),            
            Choice(value="add", name="3. ADD new book to catalogue"),
            Choice(value="delete", name="4. DELETE a book from catalogue"),
            Separator(),
            Choice(value="list_del", name="5. List deleted items"),
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

def item_menu_selection():
    selected_action = inquirer.select(
        message="Select action with the item:",
        choices=[
            Choice(value="lend", name="1. LEND the item"),
            Choice(value="delete_item", name="2. DELETE the item"),
            Separator(),
            Choice(value=99, name="Back to main menu"),
        ],
        default=1,
    ).execute()
        
    return selected_action

def user_confirmation(prompt_text = "Yes or no"):
    selected_action = inquirer.select(
        message=prompt_text,
        choices=[
            Choice(value="yes", name="YES"),
            Choice(value="no", name="NO"),
        ],
        default=1,
    ).execute()
        
    return selected_action