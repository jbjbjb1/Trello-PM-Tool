# Script to run app Trello-PM-Tool fom command line interface

import trello_calls as tc


# Terminal line interation for user


run = tc.TrelloCalls()  # initate class
choice = ''

while True:   
    choice = input('\nList boards (1), Export checklists (2): ')    
    if choice == '1':
        run.api_list_boards(public=True)
    elif choice == '2':
        run.get_data()  # TODO will need to end up exporting