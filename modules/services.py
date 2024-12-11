from classes.catalogue import Catalogue
import pickle
import os
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator

def load_data_from_storage(file_name):
    os.system('cls')  
    
    data = []
    msg = ""
    
    if os.path.isfile(file_name):
        try:
            with open(file_name, "rb") as failas:
                data = pickle.load(failas)
                if not data:
                    data = []
                    msg = f"Data file is empty.\n"
        except Exception as err:
            msg = f"Error reading data file. {err}\n"
    else:
        msg = f"Data file does not exist.\n"
    
    return (data, msg)
    
def dump_data_to_storage(file_name, data):
    status = 0
    msg = ""
    
    try:
        with open(file_name, "wb") as file:
            pickle.dump(data, file)
        status = 1
        msg = f"Data stored successfully"
        
    except Exception as err:
        msg = f"Error storing data. {err}\n"
        
    return (status, msg)


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

def print_catalogue_dynamic(data: Catalogue, scope_msg = ""):
    status = 0
    msg = ""
    items_list = []
    
    try:
        big_separator = f"{"=" * 145}"
        small_separator = f"{"-" * 145}"
        
        col_width = 30
        col_width_narrow = 10
        
        header = f"{"Eil.nr":<{col_width_narrow}}{"Title":<{col_width}}{"Author":<{col_width}}{"Genre":<{col_width}}{"Year":<{col_width_narrow}}{"Total pcs.":>{col_width_narrow}}{"Avlbl pcs.":>{col_width_narrow}}"
        
        print()
        print(scope_msg)
        
        if len(data) == 0:
            print()
            print("No items found.")
            print()

        
        else:
            # print(big_separator)
            # print(header)
            # print(small_separator)
            inquirer_msg_text = f"{big_separator}\n{header}\n{small_separator}"
            
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
                
                # if idx % 10 == 0:
                #     input("<<< Press ENTER to continue listing items >>>")         
        
            selected_item = inquirer.select(
                message=inquirer_msg_text,
                choices=items_list,
                default=1,
                keybindings={"interrupt": [{"key": "escape"}]},
            ).execute()
        
            print(big_separator)
            print()
            
            # TEMPORARY
            print(selected_item)
        
        status = 1
        
    except Exception as err:
        msg = f"Error printing catalogue. {err}\n"
        
    return (status, msg)