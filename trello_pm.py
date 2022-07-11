# Script to run app Trello-PM-Tool fom command line interface

import trello_calls as tc


# Terminal line interation for user


run = tc.TrelloCalls()  # initate class
choice = ''

while True:   
    choice = input('\nLoad current data (1), Refresh api data (2), Export checklists (3): ')    
    if choice == '1':
        run.get_data()
    elif choice == '2':
        run.delete_api_data()
        run.get_data()
    elif choice == '3':
        run.export_checklist()  # TODO will need to end up exporting