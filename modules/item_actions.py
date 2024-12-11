from classes.book import Book
import modules.services as services
import constants as const
from InquirerPy import prompt
from InquirerPy.validator import EmptyInputValidator
from datetime import datetime

def add_book():
    """Add new item=Book to the catalogue"""
    try:
        # load catalogue from the storage
        catalogue = []
        load_result = services.load_data_from_storage(const.CATALOGUE_FILE_NAME)
        catalogue = load_result[0]
        
        if not catalogue:
            print(load_result[1])
            print("Creating new catalogue.\n")

        questions = [
            {
                "type": "input", 
                "message": "Enter the book title:",
                "name": "title",
            },
            {
                "type": "input", 
                "message": "Enter the author:", 
                "name": "author",
            },
            {
                "type": "number", 
                "message": "Enter year of publication:", 
                "min_allowed": 1,
                "max_allowed": datetime.today().year + 1,
                "default": None,
                "validate": EmptyInputValidator(),
                "invalid_message": "Input should be number.",
                "name": "publication_year"
            },
            {
                "type": "rawlist", 
                "message": "Select genre:", 
                "choices": ["Fiction", "Non-Fiction", "Science Fiction (Sci-Fi)","Mystery/Thriller","Romance", "Horror", "Historical Fiction", "Young Adult (YA)","Poetry"],
                "name": "genre", 
            },
            {
                "type": "number", 
                "message": "How many units received:", 
                "min_allowed": 1,
                "max_allowed": 100,
                "validate": EmptyInputValidator(),
                "default": 1,
                "invalid_message": "Input should be number.",
                "name": "total_units"
            },
        ]

        answers = prompt(
            questions,
            keybindings={"interrupt": [{"key": "escape"}]},
            # raise_keyboard_interrupt=False
            )

        if answers:
            new_item = Book(
                title = answers["title"],
                author = answers["author"],
                publication_year = int(answers["publication_year"]),
                genre = answers["genre"],
                total_units = answers["total_units"],
                available_units = answers["total_units"]
            )
            
            catalogue.append(new_item)
        
        result = services.dump_data_to_storage(const.CATALOGUE_FILE_NAME, catalogue)
            
    except KeyboardInterrupt as err:
        result = (0, f"Entry cancelled by user.\n")        
    except Exception as err:
        result = (0, f"{err}\n")
    
    return result

def list_items():
    """Prints all items in the catalogue to terminal"""
    result = 0
    msg = ""
    
    try:
        # load catalogue from the storage
        catalogue = []
        load_result = services.load_data_from_storage(const.CATALOGUE_FILE_NAME)
        catalogue = load_result[0]
        msg = load_result[1]

        if catalogue:
            result = 1
            print_result = services.print_catalogue(catalogue)

            if print_result[0] == 0:
                result = 0
                msg = print_result[1]
        
    except Exception as err:
        msg = f"Error listing items: {err}"
    
    return (result, msg)

