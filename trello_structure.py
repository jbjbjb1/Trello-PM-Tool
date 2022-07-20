# Trello structure classes for storing data

class Workspace():
    """ Storage structure for a workspace group. """

    def __init__(self, id):
        self.id = id
        self.members = []
        self.boards = []


class Members():
    """ Storage structure for members. """

    def __init__(self, id, username, fullName):
        self.id = id
        self.username = username
        self.fullName = fullName


class Board():
    """ Storage structure for a board. """

    def __init__(self, id, name, desc):
        self.id = id
        self.name = name
        self.desc = desc
        self.lists = []
        self.cards = []


class Lists():
    """ Storage structure for lists. """

    def __init__(self, id, name):
        self.id = id
        self.name = name


class Card():
    """ Storage structure for a card. """

    def __init__(self, id, name, desc, idList, idMembers, shortUrl):
        self.id = id
        self.name = name
        self.desc = desc[:40]   # first 30 characters only
        self.idList = idList    # id of list it is a part of
        self.nameList = ''    # name of the list
        self.idMembers = idMembers  # id of members assigned
        self.shortUrl = shortUrl    # short url  
        self.checklists = []


class Checklist():
    """ Storage structure for a checklist. """

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.checkitem = []


class Checkitem():
    """ Storage structure for a checkitems. """

    def __init__(self, id, state, name, due, idmember):
        self.id = id
        self.state = state
        self.name = name
        self.due = due
        self.idmember = idmember
        self.nameMember = ''    # member as their name
        self.hours = 0
        self.get_time()   # get the hours
    
    def get_time(self):
        """ Gets the hours for the task and saves it back to the checkitem, cleans name. """
        
        if '|' in self.name:
            part_a = self.name.split('|')
            part_b = part_a[-1]
            part_c = part_b.strip()
            if part_c.isdigit():
                self.hours = part_c     # add hours
                self.name =  part_a[0].strip()   # clean description to remove hours

