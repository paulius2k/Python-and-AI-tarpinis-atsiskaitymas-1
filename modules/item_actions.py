
import views.lists as lists

def list_items(catalogue, search_by = "", item_status = 1, top_msg = ""):
    """Prints all items in the catalogue to terminal"""
    found_items = []
    error = 0
    msg = ""
    selected_item = None
    
    try:
        # get ALL active (non-deleted) items from the catalogue
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

# def get_user_confirmation(input_text, options):
#     try:
#         while True:
#             user_response = input(input_text).lower()
            
#             if user_response in options:
#                 return (1, user_response)
            
#     except KeyboardInterrupt as err:
#         return (0, "Quit by user")
    
#     except Exception as err:
#         return (0, err)