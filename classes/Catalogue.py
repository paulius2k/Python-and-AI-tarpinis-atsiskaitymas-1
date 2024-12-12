from InquirerPy import prompt
from InquirerPy.validator import EmptyInputValidator
from datetime import datetime
import pickle
import os
import constants as const
from classes.book import Book

class Catalogue():
    """
    A catalogue of all items the library owns.
    """
    def __init__(self):
        # First try to load data from file if such exists
        if os.path.isfile(const.CATALOGUE_FILE_NAME):
            with open(const.CATALOGUE_FILE_NAME, "rb") as file:
                obj = pickle.load(file)

            # copy all attributes from the loaded object to self
            self.__dict__.update(obj.__dict__)
            
        else:
            self.items = []
        
    def __str__(self):
        result = ""
        for item in self.items:
            result += f"{item}\n"
        return result
       
    def _dump_data_to_storage(self):
        result = 0
        msg = ""
        
        try:
            with open(const.CATALOGUE_FILE_NAME, "wb") as file:
                pickle.dump(self, file)
            result = 1
            msg = f"Data stored successfully"
            
        except Exception as err:
            msg = f"Error storing data. {err}\n"
        
        return (result, msg)
    
    def add_book(self):
        """Add new Book to the catalogue"""
        
        result = ()
        
        try:       
            # inform user that new catalogue will be created because there was none found / or it was empty
            if not self.items:
                print("Creating new catalogue.\n")

            # form a list of input fields to user (using InquirerPy library)
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
                    "default": None,
                    "invalid_message": "Input should be number.",
                    "name": "total_units"
                },
            ]
            
            # show a list of input fields to user and ask for data input
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
                
                self.items.append(new_item)
                
            # save data to file
            result = self._dump_data_to_storage()
                
        except KeyboardInterrupt as err:
            result = (0, f"Entry cancelled by user. Item was not saved.\n")        
        except Exception as err:
            result = (0, f"{err}\n")
        
        return result

    def get_items(self, search_phrase = "", item_status = 1):
        """Returns a list of items from the catalogue depending of request criteria"""

        found_items = []    
        
        if self.items:                
            for item in self.items:
                if item.status == item_status:
                    if search_phrase:
                        if search_phrase in item.__str__().lower() and item.status == item_status:
                            found_items.append(item)    
                    else:
                        found_items.append(item)     
        
        return found_items
    
    def delete_item(self, id):
        """Marks item as deleted"""
        
        result = ()
        
        try:
            for item in self.items:
                if item.id == id:
                    item.status = 2
                    dump_result = self._dump_data_to_storage()
                    result = (1, "\nItem deleted successfully")
                    break
        
        except Exception as err:
            result = (0, f"Error deleting item: {err}\n")
        
        return result
    
    