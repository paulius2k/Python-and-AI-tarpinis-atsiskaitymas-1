import pickle
import os

# def load_data_from_storage(file_name):
#     os.system('cls')  
    
#     data = []
#     msg = ""
    
#     if os.path.isfile(file_name):
#         try:
#             with open(file_name, "rb") as failas:
#                 data = pickle.load(failas)
#                 if not data:
#                     data = []
#                     msg = f"Data file is empty.\n"
#         except Exception as err:
#             msg = f"Error reading data file. {err}\n"
#     else:
#         msg = f"Data file does not exist.\n"
    
#     return (data, msg)
    
# def dump_data_to_storage(file_name, data):
#     status = 0
#     msg = ""
    
#     try:
#         with open(file_name, "wb") as file:
#             pickle.dump(data, file)
#         status = 1
#         msg = f"Data stored successfully"
        
#     except Exception as err:
#         msg = f"Error storing data. {err}\n"
        
#     return (status, msg)

