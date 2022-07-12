# Logic behind getting date from Trello API


import trello_structure as ts

import requests
import json
import pandas as pd
import time
import os
import shutil


class TrelloCalls():
    """ Loads, saves and displays all data."""

    def __init__(self):
        """ Load settings"""
        
        with open("settings.json", "r") as f:
            self.settings = json.load(f)[0]
    

    def get_response(self, api_call, fname):
        """" Get a response from the Trello API. """

        url = "https://api.trello.com/" + api_call

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

        with open(f'json\{fname}.json', 'w', encoding='utf-8') as json_file:   # save to file every time
            json.dump(data, json_file,ensure_ascii=False, indent=4)

        return data    # returns in json format

    def auto_load(self, api_call, fname):
        ''' If the api has already called then load locally. '''

        loal_file = f'json\{fname}.json'
        if os.path.isfile(loal_file):   # if the file exists
            with open(loal_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            print('Loaded api')
            data = self.get_response(api_call, fname)
        return data


    def delete_api_data(self):
        """ Delete all data in \json file. """

        cwd = os.path.abspath(os.getcwd())  # current working directory
        path = os.path.join(cwd, 'json')   
        try:
            shutil.rmtree(path)
        except:
            print('No previous data loaded.')
        os.mkdir(path)


    def members_boards(self, public):
        """ Lists the boards that the user is a member of. """
        
        id = self.settings['user']     # the id is fixed because it is the user accessing
        api_call = f'/1/members/{id}/boards'    # from Trello docs
        data = self.auto_load(api_call, 'me_boards')

        df = pd.DataFrame(data)     # put in Pandas dataframe
        df = df.loc[:, df.columns.intersection(['name', 'desc', 'closed', 'id', 'idOrganization'])]   # get only required columns
        df = df[['name', 'desc', 'closed', 'id', 'idOrganization']]   # re-order columns
        if public:  # if called by command line show
            print('Listing all boards:')
            print(df.head(n=99))

        return df.to_dict()     # returns as dictionary


    def boards_lists(self, id, public):
        """ Get the Lists on a Board. """

        api_call = f'/1/boards/{id}/lists'    # from Trello docs, id is board
        data = self.auto_load(api_call, f'{id}_boards_lists')

        df = pd.DataFrame(data)     # put in Pandas dataframe
        df = df.loc[:, df.columns.intersection(['id', 'name', 'closed'])]   # get only required columns
        df = df.drop(df[df.closed == True].index) # drop any closed
        df = df[df['name'].isin(self.settings['card_list'])] # drop any not in pre-defined settings list
        df = df[['id', 'name']]   # re-order columns
        if public:
            print('Listing all cards:')
            print(df.head()) 

        return df.to_dict()     # returns as dictionary

    def boards_cards(self, id, public):
        """ Get all of the open Cards on a Board. """

        api_call = f'/1/boards/{id}/cards'    # from Trello docs, id is board
        data = self.auto_load(api_call, f'{id}_boards_cards')

        df = pd.DataFrame(data)     # put in Pandas dataframe
        df = df.loc[:, df.columns.intersection(['id', 'name', 'desc', 'idList', 'idMembers', 'closed', 'idChecklists'])]   # get only required columns
        df = df.drop(df[df.closed == True].index) # drop any closed cards
        df = df[['id', 'name', 'desc', 'idList', 'idMembers', 'idChecklists']]   # re-order columns
        if public:
            print('Listing all cards:')
            print(df.loc[:,['name', 'idMembers']].head()) 

        return df.to_dict()     # returns as dictionary


    def boards_checklists(self, id, public):
        """ Get all of the checklists on a Board. """

        api_call = f'/1/boards/{id}/checklists'    # from Trello docs, id is board
        data = self.auto_load(api_call, f'{id}_boards_checklists')

        df = pd.DataFrame(data)     # put in Pandas dataframe
        '''
        df = df.loc[:, df.columns.intersection(['id', 'name', 'desc', 'idList', 'idMembers', 'closed', 'idChecklists'])]   # get only required columns
        df = df.drop(df[df.closed == True].index) # drop any closed cards
        df = df[['id', 'name', 'desc', 'idList', 'idMembers', 'idChecklists']]   # re-order columns
        if public:
            print('Listing all cards:')
            print(df.loc[:,['name', 'idMembers']].head()) 
        '''

        return df.to_dict()     # returns as dictionary


    def member(self, id, public):
        """ Get a particular property of a member; username. """

        api_call = f'/1/members/{id}'    # from Trello docs, id is board
        data = self.auto_load(api_call, f'{id}_member')

        filtered_data = {'id': data['id'], 'fullName': data['fullName'],
          'username': data['username']}

        return filtered_data     # returns as dictionary


    def export(self):
        """ Export all checklists to Excel. """
        pass


    def get_data(self):
        """ Collects all data from Trello. """

        # For boards in workspace group
        a = ts.Workspace(self.settings['user'])
        
        # For all users of interest get their id
        for username in self.settings['filter_usernames']:   # go through usernames we want
            member = self.member(id=username, public=False)

        # For all boards in list
        members_boards = self.members_boards(public=False)     # api for boards user has
        for board_id in self.settings['export_boards']:   # go through boards we want
            boards_lists = self.boards_lists(id=board_id, public=False)  # api for board lists
            index = list(members_boards['id'].values()).index(board_id)   # find what index number the desired board is
            new_board = ts.Board(id=members_boards['id'][index], name=members_boards['name'][index], 
            desc=members_boards['desc'][index], lists=boards_lists)
            a.boards.append(new_board)
        
        # Get list of card [ids, title, status, assigned] on board
        for board in a.boards:
            boards_cards = self.boards_cards(id=board.id, public=False)     # api for cards
            for i in range(len(boards_cards['id'])):
                new_card = ts.Card(id=boards_cards['id'][i], name=boards_cards['name'][i], desc=boards_cards['desc'][i],
                    idList=boards_cards['idList'][i], idMembers=boards_cards['idMembers'][i], 
                    idChecklists=boards_cards['idChecklists'][i])
                board.cards.append(new_card)
            boards_checklists = self.boards_checklists(id=board.id, public=False)     # api for checklists
            time.sleep(2*10/100)    # max 100 requests per 10 second

            return a