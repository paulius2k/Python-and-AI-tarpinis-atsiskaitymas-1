import views.lists as lists
from classes.clients import Clients

def prepare_to_list_clients(clients: Clients, search_by = "", client_status = 1, top_msg = ""):
    """
    Prepares items from the client list according to search criteria 
    for listing in terminal window 
    """
    found_clients = []
    error = 0
    msg = ""
    selected_client = None
    
    try:
        # get clients from the client list by search phrase and client status
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