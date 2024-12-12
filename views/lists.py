from classes.catalogue import Catalogue
from InquirerPy import inquirer
from InquirerPy.base.control import Choice

def list_catalogue_dynamic(data: Catalogue, scope_msg = ""):
    status = 0
    msg = ""
    items_list = []
    selected_item = None
    
    try:
        big_separator = f"{"=" * 145}"
        small_separator = f"{"-" * 145}"
        
        col_width = 30
        col_width_narrow = 8
        
        header = f"{"Eil.nr":<{col_width_narrow}}{"Title":<{col_width}}{"Author":<{col_width}}{"Genre":<{col_width}}{"Year":<{col_width_narrow}}{"Pcs.total:":>{col_width_narrow}}{"availbl:":>{col_width_narrow}}"

        inquirer_msg_text = f"Press ENTER to select an item, Esc to exit\n"        
        inquirer_msg_text += f"\n  {scope_msg}\n"
        
        if len(data) == 0:
            inquirer_msg_text += f"\n  No items found.\n"
        
        else:
            # print(big_separator)
            # print(header)
            # print(small_separator)
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
                
                name_line = f"{idx:<{col_width_narrow}}{title_checked:<{col_width}}{author_checked:<{col_width}}{item.genre:<{col_width}}{item.publication_year:<{col_width_narrow}}{item.total_units:>{col_width_narrow}}{item.available_units:>{col_width_narrow}}"
                items_list.append(Choice(value=item.id, name=name_line))   
        
            selected_item = inquirer.select(
                message=inquirer_msg_text,
                choices=items_list,
                default=1,
                # page_size=2,
                keybindings={"interrupt": [{"key": "escape"}]},
            ).execute()
        
        status = 1
        
    except Exception as err:
        msg = f"Error printing catalogue. {err}\n"
        
    return (status, msg, selected_item)

"""
def print_catalogue(data: Catalogue, scope_msg = ""):
    status = 0
    msg = ""
    
    try:
        big_separator = f"{"=" * 145}"
        small_separator = f"{"-" * 145}"
        
        col_width = 30
        col_width_narrow = 10
        
        header = f"{"Eil.nr":<{col_width_narrow}}{"Title":<{col_width}}{"Author":<{col_width}}{"Genre":<{col_width}}{"Year":<{col_width_narrow}}{"Total pcs.":>{col_width_narrow}}{"Available pcs.":>{col_width_narrow}}"
        
        print()
        print(scope_msg)
        
        if len(data) == 0:
            print()
            print("No items found.")
            print()

        
        else:
            print(big_separator)
            print(header)
            print(small_separator)

            for idx, item in enumerate(data, start=1):
                if len(item.title) >= col_width:
                    title_checked = f"{item.title[:col_width-5].strip()}..."
                else:
                    title_checked = item.title
                
                if len(item.author) >= col_width:
                    author_checked = f"{item.author[:col_width-5].strip()}..."
                else:
                    author_checked = item.author
                
                data_line = f"{idx:<{col_width_narrow}}{title_checked:<{col_width}}{author_checked:<{col_width}}{item.genre:<{col_width}}{item.publication_year:<{col_width_narrow}}{item.total_units:>{col_width_narrow}}{item.available_units:>{col_width_narrow}}"
                print(data_line)
                
                if idx % 10 == 0:
                    input("<<< Press ENTER to continue listing items >>>") 
                    
            print(big_separator)
            print()
        
        status = 1
        
    except Exception as err:
        msg = f"Error printing catalogue. {err}\n"
        
    return (status, msg)
"""
