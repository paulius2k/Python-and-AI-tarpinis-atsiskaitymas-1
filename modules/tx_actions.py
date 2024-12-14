import views.lists as lists
from classes.registry import Registry
from classes.catalogue import Catalogue

def prepare_to_list_transactions(registry: Registry, catalogue: Catalogue, search_by = "", txn_status = 1, top_msg = ""):
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
        found_items = registry.get_transactions(search_by, txn_status)        
        list_result = lists.list_transactions_dynamic(registry_items=found_items, catalogue_data=catalogue, scope_msg=top_msg)

        if list_result["error"] == 1:
            error = 1
            msg = list_result["msg"]

        selected_item = list_result["selected_item_id"]
            
    except KeyboardInterrupt as err:
        msg = f"Keyboard interrupt."           
    except Exception as err:
        msg = f"Error listing items: {err}"
    
    return (error, msg, selected_item)
