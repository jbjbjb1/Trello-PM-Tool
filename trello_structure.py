# Trello structure classes for storing data

class Workspace():
    """ Storage structure for a workspace group. """

    def __init__(self, id):
        self.id = id
        self.boards = []


class Board():
    """ Storage structure for a board. """

    def __init__(self, id, name, desc, lists):
        self.id = id
        self.name = name
        self.desc = desc
        self.lists = lists     # dictionary of list name and id
        self.cards = []


class Card():
    """ Storage structure for a card. """

    def __init__(self, id, name, desc, idList, idMembers, idChecklists):
        self.id = id
        self.name = name
        self.desc = desc[:30]   # first 30 characters only
        self.idList = idList    # id of list it is a part of
        self.idMembers = idMembers  # id of members assigned  
        self.idChecklists = idChecklists
        self.checklists = []


class Checklist():
    """ Storage structure for a checkitems. """

    def __init__(self, id, name, assigned, status):
        self.id = id
        self.name = name
        self.assigned = assigned
        self.status = status
        self.checkitem = []