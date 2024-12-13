from classes.catalogue import Catalogue
from classes.clients import Clients
from classes.registry import Registry
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from datetime import datetime

def list_catalogue_dynamic(data: Catalogue, scope_msg = ""):
    """
    Generates a dynamic list of catalogue items on the screen for viewing and actions.
    """
    
    error = 0
    msg = ""
    items_list = []
    selected_item_id = None
    
    try:
        if len(data) == 0:
            display_text = f"\n  No items found.\n"
            print(display_text)
            wait_for_keypress = input("Press ENTER to continue...")
            
        else:
            big_separator = f"{"=" * 145}"
            small_separator = f"{"-" * 145}"
            col_width = 30
            col_width_narrow = 9
            
            header = f"{"Eil.nr":<{col_width_narrow}}{"Title":<{col_width}}{"Author":<{col_width}}{"Genre":<{col_width}}{"Year":<{col_width_narrow}}{"Pcs.total":>{col_width_narrow}}{"/availbl:":>{col_width_narrow}}"

            inquirer_msg_text = f"Keys: ↑, ↓ - to move, ENTER - to choose action with item, ESC - to exit\n"        
            inquirer_msg_text += f"\n  {scope_msg} (found: {len(data)})\n"
            inquirer_msg_text += f"  {big_separator}\n  {header}\n  {small_separator}\n"
            
            for idx, item in enumerate(data, start=1):
                if len(item.title) >= col_width:
                    title_checked = f"{item.title[:col_width-5].strip()}..."
                else:
                    title_checked = item.title
                
                if len(item.author) >= col_width:
                    author_checked = f"{item.author[:col_width-5].strip()}..."
                else:
                    author_checked = item.author
                
                item_line = f"{idx:<{col_width_narrow}}{title_checked:<{col_width}}{author_checked:<{col_width}}{item.genre:<{col_width}}{item.publication_year:<{col_width_narrow}}{item.total_units:>{col_width_narrow}}{item.available_units:>{col_width_narrow}}"
                items_list.append(Choice(value=item.id, name=item_line))   
        
            selected_item_id = inquirer.select(
                message=inquirer_msg_text,
                choices=items_list,
                default=1,
                keybindings={"interrupt": [{"key": "escape"}]},
                raise_keyboard_interrupt=False,
            ).execute()
                
    except Exception as err:
        error = 1
        msg = f"Error printing catalogue. {err}\n"
        
    return {"error": error, "msg": msg, "selected_item_id": selected_item_id}

def list_clients_dynamic(data: Clients, scope_msg = ""):
    """
    Generates a dynamic list of clients-readers on the screen for viewing and actions.
    """
    
    error = 0
    msg = ""
    clients_list = []
    selected_client_id = None
    
    try:

        if len(data) == 0:
            display_text = f"\n  No clients found.\n"
            print(display_text)
            wait_for_keypress = input("Press ENTER to continue...")
            
        else:
            big_separator = f"{"=" * 110}"
            small_separator = f"{"-" * 110}"
            col_width = 20
            col_width_narrow = 9
            
            header = f"{"Eil.nr":<{col_width_narrow}}{"Name":<{col_width}}{"Last name":<{col_width}}{"Date of birth":<{col_width}}{"Card #":<{col_width_narrow}}{"Status":>{col_width_narrow}}"

            inquirer_msg_text = f"Keys: ↑, ↓ - to move, ENTER - to choose action with item, ESC - to exit\n"        
            inquirer_msg_text += f"\n  {scope_msg} (found: {len(data)})\n"
            inquirer_msg_text += f"  {big_separator}\n  {header}\n  {small_separator}\n"
            
            for idx, item in enumerate(data, start=1):
                if len(item.name) >= col_width:
                    name_checked = f"{item.name[:col_width-5].strip()}..."
                else:
                    name_checked = item.name
                
                if len(item.last_name) >= col_width:
                    lastname_checked = f"{item.last_name[:col_width-5].strip()}..."
                else:
                    lastname_checked = item.last_name
                
                dob_string = datetime.strftime(item.dob, "%Y-%m-%d")
                
                if item.status == 1:
                    status_string = "Active"
                elif item.status == 2:
                    status_string = "Not Active"


                item_line = f"{idx:<{col_width_narrow}}{name_checked:<{col_width}}{lastname_checked:<{col_width}}{dob_string:<{col_width}}{item.client_card_no:<{col_width_narrow}}{status_string:>{col_width_narrow}}"
                clients_list.append(Choice(value=item.id, name=item_line))   
        
            selected_client_id = inquirer.select(
                message=inquirer_msg_text,
                choices=clients_list,
                default=1,
                keybindings={"interrupt": [{"key": "escape"}]},
            ).execute()
                
    except Exception as err:
        error = 1
        msg = f"Error printing clients. {err}\n"
        
    return {"error": error, "msg": msg, "selected_client_id": selected_client_id}

def list_transactions_dynamic(data: Registry, scope_msg = ""):
    """
    Generates a dynamic list of client transactions on the screen for viewing and actions.
    """
    
    error = 0
    msg = ""
    tx_list = []
    selected_client_id = None
    
    try:

        if len(data) == 0:
            display_text = f"\n  No transactions found.\n"
            print(display_text)
            wait_for_keypress = input("Press ENTER to continue...")
            
        else:
            big_separator = f"{"=" * 110}"
            small_separator = f"{"-" * 110}"
            col_width = 20
            col_width_narrow = 9
            
        # self.client_id:str = client_id
        # self.item_id:str = item_id
        # self.amount:int = amount                    # amount of items
        # self.txn_type:int = txn_type                # 1-lend, 2-return
        # self.txn_status:int = txn_status            # 1-open, 2-closed
        # self.start_dt:datetime = start_dt           # e.g. lending period start date
        # self.finish_dt:datetime = finish_dt         # e.g. lending period deadline date
        # self.comment: str = comment                 # free text comment
            
            header = f"{"Eil.nr":<{col_width_narrow}}{"Name":<{col_width}}{"Last name":<{col_width}}{"Date of birth":<{col_width}}{"Card #":<{col_width_narrow}}{"Status":>{col_width_narrow}}"

            inquirer_msg_text = f"Keys: ↑, ↓ - to move, ENTER - to choose action with item, ESC - to exit\n"        
            inquirer_msg_text += f"\n  {scope_msg} (found: {len(data)})\n"
            inquirer_msg_text += f"  {big_separator}\n  {header}\n  {small_separator}\n"
            
            for idx, item in enumerate(data, start=1):
                if len(item.name) >= col_width:
                    name_checked = f"{item.name[:col_width-5].strip()}..."
                else:
                    name_checked = item.name
                
                if len(item.last_name) >= col_width:
                    lastname_checked = f"{item.last_name[:col_width-5].strip()}..."
                else:
                    lastname_checked = item.last_name
                
                dob_string = datetime.strftime(item.dob, "%Y-%m-%d")
                
                if item.status == 1:
                    status_string = "Active"
                elif item.status == 2:
                    status_string = "Not Active"


                item_line = f"{idx:<{col_width_narrow}}{name_checked:<{col_width}}{lastname_checked:<{col_width}}{dob_string:<{col_width}}{item.client_card_no:<{col_width_narrow}}{status_string:>{col_width_narrow}}"
                tx_list.append(Choice(value=item.id, name=item_line))   
        
            selected_client_id = inquirer.select(
                message=inquirer_msg_text,
                choices=tx_list,
                default=1,
                keybindings={"interrupt": [{"key": "escape"}]},
                raise_keyboard_interrupt=False,
            ).execute()
                
    except Exception as err:
        error = 1
        msg = f"Error printing transactions. {err}\n"
        
    return {"error": error, "msg": msg, "selected_client_id": selected_client_id}

