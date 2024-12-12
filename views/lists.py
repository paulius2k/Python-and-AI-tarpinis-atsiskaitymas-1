from classes.catalogue import Catalogue
from InquirerPy import inquirer
from InquirerPy.base.control import Choice

def list_catalogue_dynamic(data: Catalogue, scope_msg = ""):
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

            inquirer_msg_text = f"Keys: ↑, ↓ - to move, ENTER - to choose action with item, Esc - to exit\n"        
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
            ).execute()
                
    except Exception as err:
        error = 1
        msg = f"Error printing catalogue. {err}\n"
        
    return {"error": error, "msg": msg, "selected_item_id": selected_item_id}
