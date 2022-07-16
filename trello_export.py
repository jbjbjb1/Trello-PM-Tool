# Logic to export data from Trello in readable format.

import pandas as pd
import json


class TrelloExport():
    """ Synthesises data from Trello and exports in useable format. """

    def __init__(self, a):
        self.a = a

        with open("settings.json", "r") as f:
            self.settings = json.load(f)[0]


    def load_data_table(self):
        """ Load all checklists into dataframe. """
        
        # Loop over every line
        data = []   # store each row
        for board in self.a.boards:
            for card in board.cards:
                # Match up the actual name of the list
                for list in board.lists:
                    if list.id == card.idList:
                        card.nameList = list.name
                # Don't add cards not in filtered lists
                if card.nameList not in self.settings['card_list']:
                    print('Card list does not meet filter')
                    continue
                # Don't add if does not meet filtered string criteria
                start_string = card.name[:4]
                if start_string not in self.settings['filter_startstring']:
                    print('Card title does not meet filter')
                    continue

                # Create new entry for each checklist item
                for checklist in card.checklists:
                    for checkitem in checklist.checkitem:
                        # Match up the member name with the member id on the checkitem
                        for member in self.a.members:
                            if checkitem.idmember == member.id:
                                checkitem.nameMember = member.fullName
                        # Add new line
                        new_line = {'Card title':card.name, 'Card Link':card.shortUrl, 'List':card.nameList, 'Checklist':checklist.name, 
                            'Name':checkitem.name, 'Due':checkitem.due, 'Member':checkitem.nameMember}
                        data.append(new_line)

        df = pd.DataFrame(data)

        return df


    def export_checklist(self):
        """ Export all checklists to Excel. """

        df = self.load_data_table()   # load all checklists into dataframe
        self.df = df                  # save to class
        df.to_csv('export.csv', index=False)        # export to csv

        