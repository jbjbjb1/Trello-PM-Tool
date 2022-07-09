# Logic behind getting date from Trello API

import trello_structure as ts

import requests
import json
import pandas as pd
import time


class TrelloCalls():
    """ Loads, saves and displays all data."""

    def __init__(self):
        """ Load settings"""
        
        with open("settings.json", "r") as f:
            self.settings = json.load(f)[0]
    

    def get_response(self, url_ending):
        """" Get a response from the Trello API. """

        url = "https://api.trello.com/" + url_ending

        headers = {
        "Accept": "application/json"
        }

        query = {
        'key': self.settings['key'],
        'token': self.settings['token']
        }

        response = requests.request(
        "GET",
        url,
        headers=headers,
        params=query
        )

        data = json.loads(response.text)

        with open('output.json', 'w', encoding='utf-8') as json_file:   # save to file every time
            json.dump(data, json_file,ensure_ascii=False, indent=4)

        return data    # returns in json format


    def api_list_boards(self, public):
        """ Get a list of all boards and their ID's. """
        
        id = self.settings['user']     # the id is fixed because it is the user accessing
        url_ending = "1/members/" + id + "/boards"
        data = self.get_response(url_ending)

        df = pd.DataFrame(data)     # put in Pandas dataframe
        df = df.loc[:, df.columns.intersection(['name', 'desc', 'closed', 'id', 'idOrganization'])]   # get only required columns
        df = df[['name', 'desc', 'closed', 'id', 'idOrganization']]   # re-order columns
        if public:  # if called by command line show
            print('Listing all boards:')
            print(df.head(n=99))

        return df.to_dict()     # returns as dictionary


    def board_lists(self, id, public):
        """ Get a list of all lists on a board. """

        url_ending = "1/boards/" + id + "/lists"
        data = self.get_response(url_ending)

        df = pd.DataFrame(data)     # put in Pandas dataframe
        df = df.loc[:, df.columns.intersection(['id', 'name', 'closed'])]   # get only required columns
        df = df.drop(df[df.closed == True].index) # drop any closed
        df = df[df['name'].isin(self.settings['card_list'])] # drop any not in pre-defined settings list
        df = df[['id', 'name']]   # re-order columns
        if public:
            print('Listing all cards:')
            print(df.head()) 

        return df.to_dict()     # returns as dictionary


    def api_list_cards(self, id, public):
        """ Get a list of all cards and their ID's. """

        url_ending = "1/boards/" + id + "/cards"
        data = self.get_response(url_ending)

        df = pd.DataFrame(data)     # put in Pandas dataframe
        df = df.loc[:, df.columns.intersection(['id', 'name', 'desc', 'idList', 'idMembers', 'closed', 'idChecklists'])]   # get only required columns
        df = df.drop(df[df.closed == True].index) # drop any closed cards
        df = df[['id', 'name', 'desc', 'idList', 'idMembers', 'idChecklists']]   # re-order columns
        if public:
            print('Listing all cards:')
            print(df.loc[:,['name', 'idMembers']].head()) 

        return df.to_dict()     # returns as dictionary


    def export(self):
        """ Export all checklists to Excel. """
        pass


    def get_data(self):
        """ Collects all data from Trello. """

        # For boards in workspace group
        a = ts.Workspace(self.settings['user'])
        # For all boards in list
        boards_api = self.api_list_boards(public=False)     # call api
        for board_id in self.settings['export_boards']:   # go through boards we want
            lists_api = self.board_lists(id=board_id, public=False)  # get lists on the board
            index = list(boards_api['id'].values()).index(board_id)   # find what index number the desired board is
            new_board = ts.Board(id=boards_api['id'][index], name=boards_api['name'][index], 
            desc=boards_api['desc'][index], lists=lists_api)
            a.boards.append(new_board)
        # Get list of card [ids, title, status, assigned] on board
        for board in a.boards:
            cards_api = self.api_list_cards(id=board.id, public=False)     # call api
            for i in range(len(cards_api['id'])):
                new_card = ts.Card(id=cards_api['id'][i], name=cards_api['name'][i], desc=cards_api['desc'][i],
                 idList=cards_api['idList'][i], idMembers=cards_api['idMembers'][i], idChecklists=cards_api['idChecklists'][i])
                board.cards.append(new_card)
            
            print('Hello world')
        
        # Get list of checklists [ids, title] on card
        print('Hello world')
        # Get checkitems [ids, name, assigned, due date, complete] on checklists on card

        pass

    def export_checklist(self):
        """ Export all checklists to Excel. """