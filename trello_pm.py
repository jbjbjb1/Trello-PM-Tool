# Script to run app Trello-PM-Tool fom command line interface


import trello_calls as tc
import trello_export as te


# Terminal line interation for user


run = tc.TrelloCalls()  # initate data collection & storage class

choice = ''

while True:   
    run.a = run.get_data()  # get data on load
    choice = input('\nExport my lists (1), Export team workload (2), refresh api data (3), exit (4) : ')    
    if choice == '1':
        export = te.TrelloExport(run.a)  # initial export class
        export.export_checklist(me=True)    # me to get it filtered for my user
    elif choice == '2':
        export = te.TrelloExport(run.a)  # initial export class
        export.export_checklist()
        export.export_workload()
        export.export_graphics()
    elif choice == '3':
        run.delete_api_data()   # delete current data and re-load
        run.a = run.get_data()
    elif choice == '4':         # exit
        break