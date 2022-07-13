# Logic to export data from Trello in readable format.


class TrelloExport():
    """ Synthesises data from Trello and exports in useable format. """

    def __init__(self, a):
        self.a = a


    def member_filter(self, member):
        """ Filter all checkitems for member chosen. """
        pass

    
    def save_csv(self, data):
        """ Save to csv. """
        data.to_csv(index=False)

    
    def export_checklist(self):
        """ Export all checklists to Excel. """

        # For each member
        for member in self.a.members:
            data = self.member_filter(member.id)    # call member filter
            self.save_csv(data)     # export