# Logic to export data from Trello in readable format.

import pandas as pd
import numpy as np
import json
from datetime import date, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


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
                    continue
                # Don't add if does not meet filtered string criteria
                start_string = card.name[:4]
                if len(self.settings['filter_startstring']) != 0:   # only fiter if there is more than one item in list
                    # TODO issue is it does not capture tasks assigned in other regions to our team
                    if start_string not in self.settings['filter_startstring']:
                        continue

                # Create new entry for each checklist item
                for checklist in card.checklists:
                    for checkitem in checklist.checkitem:
                        # Match up the member name with the member id on the checkitem
                        for member in self.a.members:
                            if checkitem.idmember == member.id:
                                checkitem.nameMember = member.fullName
                        # Pass over if checkitem is complete
                        if checkitem.state == 'complete':
                            continue
                        # Add new line
                        new_line = {'Board':board.name, 'Card title':card.name, 'Card Link':card.shortUrl, 'List':card.nameList, 'Checklist':checklist.name, 
                            'Name':checkitem.name, 'Due':checkitem.due, 'Member':checkitem.nameMember, 'Hours':checkitem.hours}
                        data.append(new_line)

        df = pd.DataFrame(data)

        return df


    def export_checklist(self, me=False):
        """ Export all checklists to Excel. """

        df = self.load_data_table()   # load all checklists into dataframe
        self.df = df                  # save to class

        # Filter if required
        if me:
            df = df.loc[df['Member'] == self.a.members[0].fullName] # filter that user only
            # TODO sort by date
        else:
            pass
        df.to_csv('export.csv', index=False)        # export to csv
        print('Export of all checklists saved as csv.')


    def export_workload(self):
        """ Export workload per week per user. """

        # Transform df to get sum of hours by user per week
        dfw = self.df.copy()
        dfw['Member'].replace('', np.nan, inplace=True)
        dfw.dropna(subset=['Member'], inplace=True)     # drop rows with no member assigned
        dfw['Hours'] = dfw['Hours'].astype(str).astype(int)     # convert Hours to int
        dfw['Due'] = pd.to_datetime(dfw['Due']) - pd.to_timedelta(7, unit='d')  # transform datetime, subtrat week
        dfw = dfw.groupby(['Member', 
            pd.Grouper(key='Due', freq='W-MON')])['Hours'].sum().reset_index().sort_values('Due')   # group and sum

        # Create dataframe to eventually merge of hours avail
        # TODO Use data from settings.json, below code tempoary
        # dfw['weekHoursAvail'] = 38*60/100

        # Plot
        dfw_p = pd.pivot_table(dfw, values="Hours", index="Due", columns="Member")
        dfw_p = dfw_p.fillna(0)
        #greater than the start date and smaller than the end date
        #start_date = np.datetime64('today', 'D') - np.timedelta64(1, 'D')
        #end_date = np.datetime64('today', 'D') + np.timedelta64(32, 'D')   
        #mask = (dfw_p.index > start_date) & (dfw_p.index <= end_date)
        #dfw_p = dfw_p.loc[mask]

        fig, ax = plt.subplots()
        dfw_p.plot.bar(ax=ax)
        #ax.set_xticks(dfw_p.index)

        # use formatters to specify major and minor ticks
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        ax.xaxis.set_minor_formatter(mdates.DateFormatter("%Y-%m-%d"))
        _ = plt.xticks(rotation=90)  
        
        plt.xlabel('Week ending')
        plt.ylabel('% Capacity')
        plt.title("Engineering workload for next month")
        plt.tight_layout()
        plt.show()

        # Export to csv
        self.dfw = dfw                              # save to class
        dfw.to_csv('workload.csv', index=False)        # export to csv
        print('Export of workload saved as csv.')


    def export_graphics(self):
        """ Export an image of the count of checklist items. """

        # Make a data of count of checklis items assigned
        self.df['Member'].replace('', np.nan, inplace=True)
        self.df.dropna(subset=['Member'], inplace=True)     # drop rows with no member assigned
        series = pd.Series(self.df.Member)                # get values for plotting
        series_count = series.value_counts()
        series_count.plot(kind='bar')
        plt.xlabel('User')
        plt.ylabel('Number tasks assigned')
        plt.title("Distribution of engineering tasks")
        plt.tight_layout()
        plt.savefig('export_count.png')
        #plt.show()
        print('Plot of counts saved.')

        