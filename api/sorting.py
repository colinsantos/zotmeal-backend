ORDERINGS = [
    'Home',# anteatery main line
    'The Oven',# anteatery pizza
    'Fire & Ice',# anteatery mongolian
    'Grubb',# brandywine main line
    'Compass',# brandywine allergen station
    'Hearth',# brandywine pizza
    "The Farmer's Market (Deli)",# anteatery sandwiches
    'The Farm Stand/ Deli',# brandywine sandwiches
    'The Crossroads',# brandywine 2nd entree
    'Noodle Bar',# anteatery saute
    'Saute',# brandywine saute
    'Sizzle Grill',# anteatery burgers
    'Ember',# brandywine burgers
    'The Twisted Root',# both vegan
    'The Bakery',# anteatery dessert
    'Honeycakes',# brandywine dessert
    "Farmer's Market (Soups)",# anteatery soup
    'The Farm Stand (Soups)',# brandywine soup
    "Farmer's Market",# anteatery salad
    'The Farm Stand (Salad)'# brandywine salad
]

def station_ordering_key(station_name: str) -> int:
    '''
    Returns an integer used to sort station names by relevance (basically Eric's personal preferences 😋)
    '''
    try:
        return ORDERINGS.index(station_name)
    except ValueError:# if 
        print(f"ValueError (NON-BREAKING) on station orderings. Key {station_name} is not in list")
        return -1