from views.menus import show_main_menu
from classes.catalogue import Catalogue
from classes.clients import Clients

if __name__ == '__main__':
    new_catalogue = Catalogue()
    new_clients_db = Clients()
    
    show_main_menu(new_catalogue, new_clients_db)
    
 