# full docs: https://inquirerpy.readthedocs.io/en/latest/

from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
import os

import modules.item_actions as item_actions
import modules.client_actions as client_actions
from classes.catalogue import Catalogue
from classes.clients import Clients

def main_menu_logic(catalogue: Catalogue, clients: Clients):  
    """
    Main menu logic and master loop. 
    Calls functions to display menu and sub-menu items.
    Also calls feature functions based on user's selections.
    """
    try:
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
                    wait_for_keypress = input("Press ENTER to close...")

                # case "lend": 
                #     search_str = str(input("\n  Enter search keyword to find the item: ")).lower()
                #     top_msg = f"LISTING ITEMS BY SEARCH KEYWORD '{search_str}'"
                #     list_result = item_actions.prepare_to_list_items(catalogue, search_str, 1, top_msg)
                    
                #     if list_result[0] == 1:
                #         print("Search failed.")
                #         print(list_result[1])
                
                #     if list_result[2]:
                #         print(f"\nSelected item id: {list_result[2]}\n")
                #         item_menu_logic(catalogue, list_result[2])
                
                # case "return": 
                #     pass
                        
                case "people":        
                    action = people_menu_selection()
                    
                    match action:
                        case "new_reader":
                            result = clients.add_client()
                            if result[0] == 1:
                                print("\nNew client added")
                            elif result[0] == 0:
                                print(result[1])
                            
                            wait_for_keypress = input("Press ENTER to continue...")
                        
                        case "search_reader": 
                            search_str = str(input("\n  Enter search keyword: ")).lower()
                            top_msg = f"LISTING CLIENTS BY SEARCH KEYWORD '{search_str}'"
                            list_result = client_actions.prepare_to_list_clients(clients, search_str, 1, top_msg)
                            
                            if list_result[0] == 1:
                                print("Search failed.")
                                print(list_result[1])
                        
                            if list_result[2]:
                                print(f"\nSelected client id: {list_result[2]}\n")
                                item_menu_logic(catalogue, list_result[2])
                        
                        case "deactivate_reader": 
                            pass

                        case "new_librarian":
                            pass
                                
                case "catalogue":      
                    action = catalogue_menu_selection()
                    
                    match action:
                        case "search":
                            search_str = str(input("\n  Enter search keyword: ")).lower()
                            top_msg = f"LISTING ITEMS BY SEARCH KEYWORD '{search_str}'"
                            list_result = item_actions.prepare_to_list_items(catalogue, search_str, 1, top_msg)
                            
                            if list_result[0] == 1:
                                print("Search failed.")
                                print(list_result[1])
                        
                            if list_result[2]:
                                print(f"\nSelected item id: {list_result[2]}\n")
                                item_menu_logic(catalogue, list_result[2])
                                
                        case "add":
                            result = catalogue.add_book()
                            if result[0] == 1:
                                print("\nNew book added")
                            elif result[0] == 0:
                                print(result[1])
                            
                            wait_for_keypress = input("Press ENTER to continue...")
                            
                        case "delete":
                            pass

                        case "list_all":
                            search_str = ""
                            top_msg = f"LISTING ALL ITEMS"
                            list_result = item_actions.prepare_to_list_items(catalogue, search_str, 1, top_msg)

                            if list_result[0] == 1:
                                print("No items in the catalogue.")
                                print(list_result[1])
                                wait_for_keypress = input("Press ENTER to continue...")
                                
                            if list_result[2]:
                                print(f"\nSelected item id: {list_result[2]}\n")
                                item_menu_logic(catalogue, list_result[2])
                                        
                        case "list_del":
                            search_str = ""
                            top_msg = f"LISTING ALL DELETED ITEMS"
                            list_result = item_actions.prepare_to_list_items(catalogue, search_str, 2, top_msg)

                            if list_result[0] == 1:
                                print("No items in the catalogue.")
                                print(list_result[1])  
                                wait_for_keypress = input("Press ENTER to continue...")
                                
                            if list_result[2]:
                                print(f"\nThere are no actions available with deleted items\n")
                                wait_for_keypress = input("Press ENTER to continue...")
                                                        
                        # case _:
                        #     print("Function not ready yet.")
                        #     wait_for_keypress = input("Press ENTER to continue...")
    except KeyboardInterrupt:
        print()
        print("Thank you for using this program.\nSee you next time.")
        print()
        wait_for_keypress = input("Press ENTER to close...")
    
def item_menu_logic(catalogue: Catalogue, item_id):
    """
    Catalogue item menu, gives options for item management, 
    gets user input and calls specific feature methods.
    """
    item_action = selected_item_menu()

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
                                
def reader_menu_logic(catalogue: Catalogue, item_id):
    """
    Catalogue item menu, gives options for item management, 
    gets user input and calls specific feature methods.
    """
    item_action = selected_client_menu()

    match item_action:
        case "active_tx":
            pass

        case "closed_tx":
            pass
        
        case "deactivate":
            pass
            # answer = user_confirmation("Do you really want to delete the item?")
            
            # if answer == "yes":
            #     delete_result = catalogue.delete_item(item_id)
            #     if delete_result == 1:
            #         print("\nItem deleted successfully.")
            #     else:
            #         print(delete_result[1])                                            
            # else:
            #     print("\nAction cancelled by user.")
                
            # any_key = input("Press ENTER to continue...")

def main_menu_selection():
    """
    Menu item display and user selection capture and return to main menu logic.
    """
    selected_action = inquirer.select(
        message="\nLIBRARIAN MENU. SELECT AN AREA TO WORK WITH:\n",
        choices=[
            # Choice(value="lend", name="• LEND ITEM •"),
            # Choice(value="return", name="• RETURN ITEM •"),
            # Separator(),
            Choice(value="catalogue", name="• LIBRARY CATALOGUE (incl. LEND ITEM) •"),
            Choice(value="people", name="• CLIENTS (incl. RETURN ITEM) •"),
            Separator(),
            Choice(value=None, name="Exit"),
        ],
        default=1,
        keybindings={"interrupt": [{"key": "escape"}]},
        raise_keyboard_interrupt=False,

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
            Choice(value="list_all", name="2. LIST all items"),            
            Separator(),
            Choice(value="add", name="3. ADD new book"),
            Choice(value="delete", name="4. DELETE a book"),
            Separator(),
            Choice(value="list_del", name="5. List deleted items"),
            Choice(value="stats", name="6. Catalogue statistics"),
            Separator(),
            Choice(value=99, name="Back to main menu"),
        ],
        default=1,
        keybindings={"interrupt": [{"key": "escape"}]},
        raise_keyboard_interrupt=False,

    ).execute()

    return selected_action

def people_menu_selection():
    """
    Menu item display and user selection capture and return to main menu logic.
    """
    selected_action = inquirer.select(
        message="Select action:",
        choices=[
            Choice(value="search_reader", name="1. SEARCH for a reader"),
            Choice(value="new_reader", name="2. Register NEW reader"),
            Separator(),
            # Choice(value="new_librarian", name="3. Register NEW librarian"),
            # Separator(),
            Choice(value=99, name="Back to main menu"),
        ],
        default=1,
        keybindings={"interrupt": [{"key": "escape"}]},
        raise_keyboard_interrupt=False,

    ).execute()
        
    return selected_action

def selected_item_menu():
    """
    Menu item display and user selection capture and return to main menu logic.
    """
    selected_action = inquirer.select(
        message="Select action with the item:",
        choices=[
            Choice(value="lend", name="1. LEND the item"),
            Choice(value="delete_item", name="2. DELETE the item"),
            Separator(),
            Choice(value=99, name="Back to main menu"),
        ],
        default=1,
        keybindings={"interrupt": [{"key": "escape"}]},
        raise_keyboard_interrupt=False,

    ).execute()
        
    return selected_action

def selected_client_menu():
    """
    Menu item display and user selection capture and return to main menu logic.
    """
    selected_action = inquirer.select(
        message="Select action with the reader:",
        choices=[
            Choice(value="active_tx", name="1. List active transactions"),
            Choice(value="closed_tx", name="2. List closed transactions"),
            Separator(),
            Choice(value="deactivate", name="3. Deactivate reader"),
            Separator(),
            Choice(value=99, name="Back to main menu"),
        ],
        default=1,
        keybindings={"interrupt": [{"key": "escape"}]},
        raise_keyboard_interrupt=False,
    ).execute()
        
    return selected_action

def selected_transaction_menu():
    """
    Menu item display and user selection capture and return to main menu logic.
    """
    selected_action = inquirer.select(
        message="Select action with the item:",
        choices=[
            Choice(value="lend", name="1. LEND the item"),
            Choice(value="delete_item", name="2. DELETE the item"),
            Separator(),
            Choice(value=99, name="Back to main menu"),
        ],
        default=1,
        keybindings={"interrupt": [{"key": "escape"}]},
        raise_keyboard_interrupt=False,

    ).execute()
        
    return selected_action

def user_confirmation(prompt_text = "Yes or no"):
    """
    Menu item display and user selection capture and return to main menu logic.
    """
    selected_action = inquirer.select(
        message=prompt_text,
        choices=[
            Choice(value="yes", name="YES"),
            Choice(value="no", name="NO"),
        ],
        default=1,
        keybindings={"interrupt": [{"key": "escape"}]},
        raise_keyboard_interrupt=False,

    ).execute()
        
    return selected_action