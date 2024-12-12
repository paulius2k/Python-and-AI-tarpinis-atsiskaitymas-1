import views.lists as lists
from classes.clients import Clients

def prepare_to_list_clients(clients: Clients, search_by = "", client_status = 1, top_msg = ""):
    """Prints clients to terminal by specified criteria"""
    
    found_clients = []
    error = 0
    msg = ""
    selected_client = None
    
    try:
        # get ALL active (non-deleted) items from the catalogue
        found_clients = clients.get_clients(search_by, client_status)        
        list_result = lists.list_clients_dynamic(found_clients, top_msg)

        if list_result["error"] == 1:
            error = 1
            msg = list_result["msg"]

        selected_client = list_result["selected_client_id"]
            
    except KeyboardInterrupt as err:
        msg = f"Keyboard interrupt."           
    except Exception as err:
        msg = f"Error listing items: {err}"
    
    return (error, msg, selected_client)