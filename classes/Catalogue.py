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
    def __init__(self, items = []) -> None:
        self.items = items
        
    def __str__(self):
        for item in self.items:
            print(item)
    
    def _load_data_from_storage(self):
        
        result = 0
        msg = ""
        
        try:
            if os.path.isfile(const.CATALOGUE_FILE_NAME):
                with open(const.CATALOGUE_FILE_NAME, "rb") as file:
                    self.items = pickle.load(file)
                    if not self.items:
                        msg = f"Data file is empty.\n"
                    result = 1
            else:
                msg = f"Data file does not exist.\n"

        except Exception as err:
            msg = f"Error reading data file. {err}\n"        
        return (result, msg)
    
    def _dump_data_to_storage(self):
        
        result = ()
        msg = ""
        
        try:
            with open(const.CATALOGUE_FILE_NAME, "wb") as file:
                pickle.dump(self.items, file)
            result[0] = 1
            msg = f"Data stored successfully"
            
        except Exception as err:
            msg = f"Error storing data. {err}\n"
        
        result[1] = msg
        return result
    
    
    
    def add_book(self):
        """Add new Book to the catalogue"""
        
        result = ()
        msg = ""
        
        try:
            # load catalogue from the storage
            load_result = self._load_data_from_storage()
            
            if not self.items:
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
                    "default": None,
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
                
                self.items.append(new_item)
            
            # save data to file
            result = self._dump_data_to_storage(const.CATALOGUE_FILE_NAME, self.items)
                
        except KeyboardInterrupt as err:
            result = (0, f"Entry cancelled by user. Item was not saved.\n")        
        except Exception as err:
            result = (0, f"{err}\n")
        
        return result


    