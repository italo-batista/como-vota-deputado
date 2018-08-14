from .controllers.votes import VotesCtrl
from .controllers.attendances import AttendancesCtrl


class ComoVotaDeputado(object):

    def __init__(self):
        self.votes_ctrl = VotesCtrl()
        self.attendances_ctrl = AttendancesCtrl()

    def get_all_votes_dataframe(self, year):        
        return self.votes_ctrl.get_all_votes_dataframe(year)

    def get_congressman_votes_dataframe(self, congressman_id, year):
        return self.votes_ctrl.get_congressman_votes_dataframe(congressman_id, year)

    def get_attendances(self, day, month, year, congressperson_id="", political_party_initials="", uf_initials=""):
        return self.attendances_ctrl \
            .get_all_attendances_date_dataframe(
                day=day, month=month, year=year, congressperson_id=str(congressperson_id),
                political_party_initials=str(political_party_initials), uf_initials=str(uf_initials))