# Script to run app Trello-PM-Tool fom command line interface


import trello_calls as tc
import trello_export as te


# Terminal line interation for user


run = tc.TrelloCalls()  # initate class
export = te.TrelloExport()  # exports data
choice = ''

while True:   
    choice = input('\nLoad current data (1), Refresh api data (2), Export checklists (3): ')    
    if choice == '1':
        run.a = run.get_data()  # save data to instance of class so it can be used later
    elif choice == '2':
        run.delete_api_data()
        run.a = run.get_data()  # save data to instance of class so it can be used later
    elif choice == '3':
        export.export_checklist(run.a)