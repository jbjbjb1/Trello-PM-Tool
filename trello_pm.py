# Script to run app Trello-PM-Tool fom command line interface


import trello_calls as tc
import trello_export as te


# Terminal line interation for user


run = tc.TrelloCalls()  # initate data collection & storage class

choice = ''

while True:   
    run.a = run.get_data()  # get data on load
    choice = input('\nExport checklists (1), refresh api data (2), : ')    
    if choice == '1':
        export = te.TrelloExport(run.a)  # initial export class
        export.export_checklist()
    elif choice == '2':
        run.delete_api_data()   # delete current data and re-load
        run.a = run.get_data()