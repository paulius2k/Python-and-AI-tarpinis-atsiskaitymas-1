import views.lists as lists
from classes.catalogue import Catalogue

def prepare_to_list_items(catalogue: Catalogue, search_by = "", item_status = 1, top_msg = ""):
    """
    Prepares items from the catalogue according to search criteria 
    for listing in terminal window 
    """
    found_items = []
    error = 0
    msg = ""
    selected_item = None
    
    try:
        # get items from the catalogue by search phrase and item status
        found_items = catalogue.get_items(search_by, item_status)        
        list_result = lists.list_catalogue_dynamic(found_items, top_msg)

        if list_result["error"] == 1:
            error = 1
            msg = list_result["msg"]

        selected_item = list_result["selected_item_id"]
            
    except KeyboardInterrupt as err:
        msg = f"Keyboard interrupt."           
    except Exception as err:
        msg = f"Error listing items: {err}"
    
    return (error, msg, selected_item)

    