import views.lists as lists
from classes.registry import Registry
from classes.catalogue import Catalogue
from datetime import datetime

def prepare_to_list_transactions(registry: Registry, catalogue: Catalogue, client_id, txn_status_set:set = {1,3}, top_msg = ""):
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
        found_items = registry.get_transactions(client_id=client_id, txn_status_set=txn_status_set)        
        list_result = lists.list_transactions_dynamic(registry_items=found_items, catalogue_data=catalogue, scope_msg=top_msg)

        if list_result["error"] == 1:
            error = 1
            msg = list_result["msg"]

        selected_item = list_result["selected_txn_id"]
            
    except KeyboardInterrupt as err:
        error = 0
        msg = f"Keyboard interrupt."           
    except Exception as err:
        error = 1
        msg = f"Error listing items: {err}"
    
    return (error, msg, selected_item)

def mark_overdue_transactions(registry: Registry):
    
    try:
        today_dt = datetime.today()
        today_dt = today_dt.replace(hour=0, minute=0, second=0, microsecond=0)
        
        counter = 0
        if registry:
            for item in registry.items:
                if item.txn_status == 1 and item.txn_type == 1:
                    if item.finish_dt < today_dt:
                        item.txn_status = 3
                        counter += 1
        
        if counter > 0:
            result = registry._dump_data_to_storage()
        else:
            result = (0, "No overdue records found")
    
    except Exception as err:
        result = (0, "Error processing records")
        
    return result