from InquirerPy import prompt
from InquirerPy.validator import EmptyInputValidator
from datetime import datetime

# def __init__(self, title:str, author:str, publication_year:int, genre:str, total_units:int, available_units:int, added_user_id:str = "u-999")

# my custom publication year validation function

# questions = [
#     {
#         "type": "input", 
#         "message": "Enter the book title:",
#         "name": "title",
#     },
#     {
#         "type": "input", 
#         "message": "Enter the author:", 
#         "name": "author",
#     },
#     {
#         "type": "number", 
#         "message": "Enter year of publication:", 
#         "min_allowed": 1,
#         "max_allowed": datetime.today().year + 1,
#         "default": None,
#         "validate": EmptyInputValidator(),
#         "invalid_message": "Input should be number.",
#         "name": "publication_year"
#     },
#     {
#         "type": "rawlist", 
#         "message": "Select genre:", 
#         "choices": ["Fiction", "Non-Fiction", "Science Fiction (Sci-Fi)","Mystery/Thriller","Romance", "Horror", "Historical Fiction", "Young Adult (YA)","Poetry"],
#         "name": "genre", 
#     },
# ]

# answers = prompt(questions)
# print(answers)

