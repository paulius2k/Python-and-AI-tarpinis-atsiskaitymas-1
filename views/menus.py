# full docs: https://inquirerpy.readthedocs.io/en/latest/

from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
import os
from datetime import datetime

import modules.item_actions as item_actions
import modules.client_actions as client_actions
import modules.tx_actions as tx_actions
from classes.catalogue import Catalogue
from classes.clients import Clients
from classes.registry import Registry

def main_menu_logic(catalogue: Catalogue, clients: Clients, registry: Registry):  
# def main_menu_logic(): 
    """
    Main menu logic and master loop. 
    Calls functions to display menu and sub-menu items.
    Also calls feature functions based on user's selections.
    """
    try:
        stop_menu = False
        
        while not stop_menu:
            
            # Option 2: re-load lists on every main menu draw
            # this is done 
            # catalogue = Catalogue()
            # clients = Clients()
            # registry = Registry()
            
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
                                                  
                case "catalogue":      
                    action = catalogue_menu_selection()
                    
                    match action:
                        case "search":
                            search_str = str(input("\n  Enter search keyword: ")).lower()
                            top_msg = f"LISTING ITEMS BY SEARCH KEYWORD '{search_str}'"
                            list_result = item_actions.prepare_to_list_items(catalogue, search_str, 1, top_msg)
                            item_id = list_result[2]
                            
                            if list_result[0] == 1:
                                print("Search failed.")
                                print(list_result[1])
                        
                            if item_id:
                                print(f"\nSelected item id: {item_id}\n")
                                item_menu_logic(catalogue, clients, registry, item_id)
                                
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
                            item_id = list_result[2]
                            
                            if list_result[0] == 1:
                                print("No items in the catalogue.")
                                print(list_result[1])
                                wait_for_keypress = input("Press ENTER to continue...")
                                
                            if item_id:
                                print(f"\nSelected item id: {item_id}\n")
                                item_menu_logic(catalogue, clients, registry, item_id)
                                        
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
                                
                        case "list_overdue":
                            wait_for_keypress = input("\nThis function is not available yet. Press ENTER to continue...")
                                                   
                case "clients":        
                    action = clients_menu_selection()
                    
                    match action:                       
                        case "search_reader": 
                            search_str = str(input("\n  Enter search keyword: ")).lower()
                            top_msg = f"LISTING CLIENTS BY SEARCH KEYWORD '{search_str}'"
                            list_result = client_actions.prepare_to_list_clients(clients, search_str, 1, top_msg)
                            
                            if list_result[0] == 1:
                                print("Search failed.")
                                print(list_result[1])
                        
                            if list_result[2]:
                                print(f"\nSelected client id: {list_result[2]}\n")
                                
                                reader_menu_logic(registry, clients, catalogue, list_result[2])

                        case "new_reader":
                            result = clients.add_client()
                            if result[0] == 1:
                                print("\nNew client added")
                            elif result[0] == 0:
                                print(result[1])
                            
                            wait_for_keypress = input("Press ENTER to continue...")
                                                    
                        case "deactivate_reader": 
                            pass

                        case "new_librarian":
                            pass

    except KeyboardInterrupt:
        print()
        print("Thank you for using this program.\nSee you next time.")
        print()
        wait_for_keypress = input("Press ENTER to close...")
    
def item_menu_logic(catalogue: Catalogue, clients: Clients, registry: Registry, item_id):
    """
    Catalogue item menu, gives options for item management, 
    gets user input and calls specific feature methods.
    """
    item_action = selected_item_menu()

    match item_action:
        case "lend":
            
            # check if there item balance is not 0, else stop lending process
            item = catalogue.get_item_by_id(item_id)
            if item.available_units == 0:
                print("Item is out of stock.")
                print()
                wait_for_keypress = input("Press ENTER to continue...")
                return
            
            # search_for_reader
            search_str = str(input("\n  Enter keyword to search for reader: ")).lower()
            top_msg = f"LISTING CLIENTS BY SEARCH KEYWORD '{search_str}'"
            list_result = client_actions.prepare_to_list_clients(clients, search_str, 1, top_msg)
            client_id = list_result[2]
            
            if list_result[0] == 1:
                print("Search failed.")
                print(list_result[1])
        
            if client_id:
                print(f"\nSelected client id: {client_id}\n")
                client = clients.get_client_by_id(client_id)
                
                print()
                print(f"NEW LENDING TRANSACTION: *{item.title} ({item.publication_year})* to *{client.name} {client.last_name} (b.{client.dob.strftime("%Y-%m-%d")})*")
                print()
                creation_result = registry.new_transaction(catalogue, client_id, item_id, item.available_units, 1, datetime.today())

                print()
                
                if creation_result[0] == 1:
                    print("Lending transaction created successfully.")
                
                elif creation_result[0] == 0:
                    print(f"Lending failed: {creation_result[1]}")
                    
                print()
                wait_for_keypress = input("Press ENTER to continue...") 
        
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
                
            wait_for_keypress = input("Press ENTER to continue...")       

def tx_menu_logic(catalogue: Catalogue, item_id):
    """
    Catalogue item menu, gives options for item management, 
    gets user input and calls specific feature methods.
    """
    item_action = selected_transaction_menu()

    match item_action:
        case "return":
            # pseudo:
            # registry.new_transaction(type="return")    
                
            wait_for_keypress = input("Press ENTER to continue...") 
                                        
def reader_menu_logic(registry: Registry, clients: Clients, catalogue: Catalogue, client_id):
    """
    Client-reader item menu, gives options for reader management, 
    gets user input and calls specific feature methods.
    """
    item_action = selected_client_menu()

    match item_action:
        case "active_tx":
            reader = clients.get_client_by_id(client_id)
            top_msg = f"LISTING ACTIVE TRANSACTIONS OF *{reader.name} {reader.last_name}*"
            list_result = tx_actions.prepare_to_list_transactions(registry=registry, catalogue=catalogue, txn_status=1, top_msg=top_msg)
            
            if list_result[0] == 0:
                print("Search failed.")
                print(list_result[1])
        
            if list_result[2]:
                pass
                # print(f"\nSelected transaction id: {list_result[2]}\n")
                # tx_menu_logic(catalogue, list_result[2])
                
            wait_for_keypress = input("Press ENTER to continue...") 
        case "closed_tx":
            pass
        
        case "deactivate":
            pass


#DRAW MENUS 
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
            Choice(value="clients", name="• CLIENTS (incl. RETURN ITEM) •"),
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
            Choice(value="list_overdue", name="3. List OVERDUE items"),           
            Separator(),
            Choice(value="add", name="4. ADD new book"),
            Choice(value="delete", name="5. DELETE a book"),
            Separator(),
            Choice(value="list_del", name="6. List deleted items"),
            Choice(value="stats", name="7. Catalogue statistics"),
            Separator(),
            Choice(value=99, name="Back to main menu"),
        ],
        default=1,
        keybindings={"interrupt": [{"key": "escape"}]},
        raise_keyboard_interrupt=False,

    ).execute()

    return selected_action

def clients_menu_selection():
    """
    Menu item display and user selection capture and return to main menu logic.
    """
    selected_action = inquirer.select(
        message="Select action:",
        choices=[
            Choice(value="search_reader", name="1. SEARCH for a reader"),
            Choice(value="new_reader", name="2. Register NEW reader"),
            Separator(),
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
            Choice(value="return", name="1. RETURN the item"),
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