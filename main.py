from views.menus import main_menu_logic
from classes.catalogue import Catalogue
from classes.clients import Clients
from classes.registry import Registry

if __name__ == '__main__':
    new_catalogue = Catalogue()
    new_clients_db = Clients()
    new_registry = Registry()
        
    main_menu_logic(new_catalogue, new_clients_db, new_registry)
    
    # main_menu_logic()
    
 