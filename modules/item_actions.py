from classes.book import Book
import modules.services as services
import views.lists as lists
import constants as const
from InquirerPy import prompt
from InquirerPy.validator import EmptyInputValidator
from datetime import datetime

# def add_book():
#     """Add new item=Book to the catalogue"""
#     try:
#         # load catalogue from the storage
#         catalogue = []
#         load_result = services.load_data_from_storage(const.CATALOGUE_FILE_NAME)
#         catalogue = load_result[0]
        
#         if not catalogue:
#             print(load_result[1])
#             print("Creating new catalogue.\n")

#         questions = [
#             {
#                 "type": "input", 
#                 "message": "Enter the book title:",
#                 "name": "title",
#             },
#             {
#                 "type": "input", 
#                 "message": "Enter the author:", 
#                 "name": "author",
#             },
#             {
#                 "type": "number", 
#                 "message": "Enter year of publication:", 
#                 "min_allowed": 1,
#                 "max_allowed": datetime.today().year + 1,
#                 "default": None,
#                 "validate": EmptyInputValidator(),
#                 "invalid_message": "Input should be number.",
#                 "name": "publication_year"
#             },
#             {
#                 "type": "rawlist", 
#                 "message": "Select genre:", 
#                 "choices": ["Fiction", "Non-Fiction", "Science Fiction (Sci-Fi)","Mystery/Thriller","Romance", "Horror", "Historical Fiction", "Young Adult (YA)","Poetry"],
#                 "name": "genre", 
#             },
#             {
#                 "type": "number", 
#                 "message": "How many units received:", 
#                 "min_allowed": 1,
#                 "max_allowed": 100,
#                 "validate": EmptyInputValidator(),
#                 "default": None,
#                 "invalid_message": "Input should be number.",
#                 "name": "total_units"
#             },
#         ]

#         answers = prompt(
#             questions,
#             keybindings={"interrupt": [{"key": "escape"}]},
#             # raise_keyboard_interrupt=False
#             )

#         if answers:
#             new_item = Book(
#                 title = answers["title"],
#                 author = answers["author"],
#                 publication_year = int(answers["publication_year"]),
#                 genre = answers["genre"],
#                 total_units = answers["total_units"],
#                 available_units = answers["total_units"]
#             )
            
#             catalogue.append(new_item)
        
#         result = services.dump_data_to_storage(const.CATALOGUE_FILE_NAME, catalogue)
            
#     except KeyboardInterrupt as err:
#         result = (0, f"Entry cancelled by user. Item was not saved.\n")        
#     except Exception as err:
#         result = (0, f"{err}\n")
    
#     return result

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