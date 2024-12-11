from classes.catalogue import Catalogue
import pickle
import os

def load_data_from_storage(file_name):
    data = []
    msg = ""
    
    if os.path.isfile(file_name):
        try:
            with open(file_name, "rb") as failas:
                data = pickle.load(failas)
                if not data:
                    data = []
                    msg = f"Data file is empty.\n"
        except Exception as err:
            msg = f"Error reading data file. {err}\n"
    else:
        msg = f"Data file does not exist.\n"
    
    return (data, msg)
    
def dump_data_to_storage(file_name, data):
    status = 0
    msg = ""
    
    try:
        with open(file_name, "wb") as file:
            pickle.dump(data, file)
        status = 1
        msg = f"Data stored successfully"
        
    except Exception as err:
        msg = f"Error storing data. {err}\n"
        
    return (status, msg)


def print_catalogue(data: Catalogue):
    status = 0
    msg = ""
    
    try:
        big_separator = f"{"=" * 150}"
        small_separator = f"{"-" * 150}"
        
        col_width = 15
        header = f"{"Eil.nr":<{col_width}}{"Title":<{col_width}}{"Author":<{col_width}}{"Genre":<{col_width}}{"Year of pub.":>{col_width}}{"Total pcs.":>{col_width}}{"Available pcs.":>{col_width}}"
        
        print()
        print(big_separator)
        print(header)
        print(small_separator)
        
        for idx, item in enumerate(data, start=1):
            data_line = f"{idx:<{col_width}}{item.title:<{col_width}}{item.author:<{col_width}}{item.genre:<{col_width}}{item.publication_year:>{col_width}}{item.total_units:>{col_width}}{item.available_units:>{col_width}}"
            print(data_line)
            
            if idx % 10 == 0:
                input("<<< Press ENTER to continue listing items >>>") 
                
        print(big_separator)
        print()
        
        status = 1
        
    except Exception as err:
        msg = f"Error printing catalogue. {err}\n"
        
    return (status, msg)