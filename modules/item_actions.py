from classes.book import Book
import modules.services as services
import views.lists as lists
import constants as const
from InquirerPy import prompt
from InquirerPy.validator import EmptyInputValidator
from datetime import datetime

def list_items():
    """Prints all items in the catalogue to terminal"""
    result = 0
    msg = ""
    selected_item = None
    
    try:
        # load catalogue from the storage
        catalogue = []
        load_result = services.load_data_from_storage(const.CATALOGUE_FILE_NAME)
        catalogue = load_result[0]
        msg = load_result[1]

        if catalogue:
            found_items = []
            
            #go through all items and select only active (non-deleted) ones
            for item in catalogue:
                if item.status == 1:
                    found_items.append(item)  
            
            result = 1
            top_msg = f"LISTING ALL ITEMS"
            print_result = lists.list_catalogue_dynamic(found_items, top_msg)

            if print_result[0] == 0:
                result = 0
                msg = print_result[1]

            selected_item = print_result[2]
            
    except KeyboardInterrupt as err:
        msg = f""           
    except Exception as err:
        msg = f"Error listing items: {err}"
    
    return (result, msg, selected_item)

def search_item():
    """Search for item(s) in the catalogue"""
    result = 0
    msg = ""
    selected_item = None
    
    try:
        # load catalogue from the storage
        catalogue = []
        load_result = services.load_data_from_storage(const.CATALOGUE_FILE_NAME)
        catalogue = load_result[0]
        msg = load_result[1]

        if catalogue:
            found_items = []
            search_by = str(input("  Enter search keyword: ")).lower()
            
            if search_by:
                for item in catalogue:
                    if search_by in item.__str__().lower() and item.status == 1:
                        found_items.append(item)    
                    
            result = 1
            top_msg = f"LISTING ITEMS BY SEARCH KEYWORD '{search_by}'"
            print_result = lists.list_catalogue_dynamic(found_items, top_msg)

            if print_result[0] == 0:
                result = 0
                msg = print_result[1]
                
            selected_item = print_result[2]
    except Exception as err:
        msg = f"Error searching for items: {err}"
    
    return (result, msg, selected_item)