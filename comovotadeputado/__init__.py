from comovotadeputado.controllers.votes import VotesCtrl


class ComoVotaDeputado:

    def __init__(self):
        self.votes_ctrl = VotesCtrl()

    def get_all_votes_dataframe(self, year):        
        return self.votes_ctrl.get_all_votes_dataframe(year)

    def get_congressman_votes(self, congressman_id, year):        
        return self.votes_ctrl.get_congressman_votes(congressman_id, year)
