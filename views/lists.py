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
            
            
            header = (
                    f"{"Eil.nr":<{col_width_narrow}}"
                    f"{"Name":<{col_width}}"
                    f"{"Last name":<{col_width}}"
                    f"{"Date of birth":<{col_width}}"
                    f"{"Card #":<{col_width_narrow}}"
                    f"{"Status":>{col_width_narrow}}"
            )
            
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


                item_line = (
                    f"{idx:<{col_width_narrow}}"
                    f"{name_checked:<{col_width}}"
                    f"{lastname_checked:<{col_width}}"
                    f"{dob_string:<{col_width}}"
                    f"{item.client_card_no:<{col_width_narrow}}"
                    f"{status_string:>{col_width_narrow}}"
                )
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

def list_transactions_dynamic(registry_items:list, catalogue_data: Catalogue, scope_msg = ""):
    """
    Generates a dynamic list of client transactions on the screen for viewing and actions.
    """
    
    error = 0
    msg = ""
    txn_list = []
    selected_txn_id = None
    
    try:

        if len(registry_items) == 0:
            display_text = f"\n  No items found.\n"
            print(display_text)
            wait_for_keypress = input("Press ENTER to continue...") 
            
        else:
            big_separator = f"{"=" * 150}"
            small_separator = f"{"-" * 150}"
            col_width = 20
            col_width_narrow = 8
            col_width_mid = 12
            col_width_wide = 25
            
                        
            header = (
                f"{"Eil.nr":<{col_width_narrow}}"
                f"{"Title":<{col_width}}"
                f"{"Author":<{col_width}}"
                f"{"Year":<{col_width_narrow}}"
                f"{"Start":<{col_width_mid}}"
                f"{"Deadline":<{col_width_mid}}"
                f"{"Action":<{col_width_narrow}}"
                f"{"Pcs.":<{col_width_narrow}}"
                f"{"Status":<{col_width_narrow}}"
                f"{"Returned":<{col_width_mid}}"
                f"{"Comment":<{col_width_wide}}"
            )
            
            inquirer_msg_text = f"Keys: ↑, ↓ - to move, ENTER - to choose action with item, ESC - to exit\n"        
            inquirer_msg_text += f"\n  {scope_msg} (found: {len(registry_items)})\n"
            inquirer_msg_text += f"  {big_separator}\n  {header}\n  {small_separator}\n"
            
            for idx, item in enumerate(registry_items, start=1):
                
                # self.client_id:str = client_id
                # self.item_id:str = item_id
                # self.amount:int = amount                    # amount of items
                # self.txn_type:int = txn_type                # 1-lend, 2-return
                # self.txn_status:int = txn_status            # 1-open, 2-closed
                # self.start_dt:datetime = start_dt           # e.g. lending period start date
                # self.finish_dt:datetime = finish_dt         # e.g. lending period deadline date
                # self.comment: str = comment                 # free text comment
                
                catalogue_item = catalogue_data.get_item_by_id(item.item_id)
                
                # name formatting by length
                if len(catalogue_item.title) >= col_width:
                    title_checked = f"{catalogue_item.title[:col_width-5].strip()}..."
                else:
                    title_checked = catalogue_item.title
                
                if len(catalogue_item.author) >= col_width:
                    author_checked = f"{catalogue_item.author[:col_width-5].strip()}..."
                else:
                    author_checked = catalogue_item.author

                if len(item.comment) >= col_width_wide:
                    comment_checked = f"{item.comment[:col_width_wide-5].strip()}..."
                else:
                    comment_checked = item.comment
                
                # date formatting
                if item.start_dt:
                    start_dt_string = datetime.strftime(item.start_dt, "%Y-%m-%d")
                else:
                    start_dt_string = ""
                
                if item.finish_dt:
                    finish_dt_string = datetime.strftime(item.finish_dt, "%Y-%m-%d")
                else:
                    finish_dt_string = ""
                    
                if item.return_dt:
                    return_dt_string = datetime.strftime(item.return_dt, "%Y-%m-%d")
                else:
                    return_dt_string = ""
                
                # status parsing to words
                txn_type_dict = {1: "LEND", 2: "RETURN"}
                txn_status_dict = {1: "Open", 2: "Closed"}

                # f"{"Eil.nr":<{col_width_narrow}}"
                # f"{"Title":<{col_width}}"
                # f"{"Author":<{col_width}}"
                # f"{"Year":<{col_width_narrow}}"
                # f"{"Start":<{col_width_narrow}}"
                # f"{"Deadline":>{col_width_narrow}}"
                # f"{"Action":>{col_width_narrow}}"
                # f"{"Pcs.":<{col_width}}"
                # f"{"Status":>{col_width_narrow}}"
                # f"{"Comment":>{col_width}}"

                item_line = (
                    f"{idx:<{col_width_narrow}}"
                    f"{title_checked:<{col_width}}"
                    f"{author_checked:<{col_width}}"
                    f"{catalogue_item.publication_year:<{col_width_narrow}}"
                    f"{start_dt_string:<{col_width_mid}}"
                    f"{finish_dt_string:<{col_width_mid}}"
                    f"{txn_type_dict[item.txn_type]:<{col_width_narrow}}"
                    f"{item.amount:<{col_width_narrow}}"
                    f"{txn_status_dict[item.txn_status]:<{col_width_narrow}}"
                    f"{return_dt_string:<{col_width_mid}}"
                    f"{comment_checked:<{col_width_wide}}"
                                        
                    )      
                   
                txn_list.append(Choice(value=item._id, name=item_line))   
        
            selected_txn_id = inquirer.select(
                message=inquirer_msg_text,
                choices=txn_list,
                default=1,
                keybindings={"interrupt": [{"key": "escape"}]},
                raise_keyboard_interrupt=False,
            ).execute()
                
    except Exception as err:
        error = 1
        msg = f"Error printing transactions. {err}\n"
        
    return {"error": error, "msg": msg, "selected_txn_id": selected_txn_id}

