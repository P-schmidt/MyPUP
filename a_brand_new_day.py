import database2 as db
import pickle
import Mypup_vrp as mpv 
import sys


def main():
    """Controlefunctie over database en route optimalisatie via command line."""

    bool_add = input('Zijn er bedrijven die toegevoegd moeten worden aan de database? Typ y of n: ')
    while bool_add not in ('y', 'n'):
        bool_add = input('Typ y of n: ')

    while bool_add == 'y':
        add_comp = input('Geef info van nieuwe bedrijf als volgt: bedrijfsnaam,adres,laadtijd. ')
        db.add_to_database(add_comp.split(','), 'data/Mypup_ams_cleaned')
        bool_add= input('Moet er nog een bedrijf toegevoegd worden? Typ y of n: ')
        while bool_add not in ('y', 'n'):
            bool_add = input('Typ y of n: ')

    bool_remove = input('Zijn er bedrijven die verwijderd moeten worden uit de database? Typ y of n: ')
    while bool_remove not in ('y', 'n'):
        bool_remove = input('Typ y of n: ')

    while bool_remove == 'y':
        company = input('Geef naam van te verwijderen bedrijf: ')
        db.remove_from_database(company, 'data/Mypup_ams_cleaned')
        bool_remove = input('Moet er nog een bedrijf verwijderd worden? Typ y of n: ')
        while bool_remove not in ('y', 'n'):
            bool_remove = input('Typ y of n: ')

    make_route = input('Moeten er pakketten bezorgd worden? Typ y of n: ')
    while make_route not in ('y', 'n'):
        make_route = input('Typ y of n: ')

    if make_route == 'y':
        with open('data/Mypup_ams_cleaned.pkl', 'rb') as f:
            database = pickle.load(f)
        visit_all = input('Moeten alle bedrijven bezorgd worden? Typ y of n: ')
        while visit_all not in ('y', 'n'):
            visit_all = input('Typ y of n: ')

        if visit_all == 'y':
            mpv.main(list(database.keys()))
        else:
            do_not_visit = input('Geef lijst met bedrijven die niet bezocht moeten worden als volgt: bedrijf1,bedrijf2,etc. ').split(',')
            do_visit = [comp for comp in list(database.keys()) if comp not in do_not_visit]
            mpv.main(do_visit)
   
if __name__ == '__main__':
    main()