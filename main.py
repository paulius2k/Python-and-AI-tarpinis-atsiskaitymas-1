from views.menus import show_main_menu
from classes.catalogue import Catalogue

if __name__ == '__main__':
    new_catalogue = Catalogue()
    new_catalogue._load_data_from_storage
    
    show_main_menu(new_catalogue)
    
 