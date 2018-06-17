import pandas as pd

import comovotadeputado.opendata.controller as open_dt_ctrl
from comovotadeputado.errors.messages import ErrorMessages
from comovotadeputado.cache import cache
from comovotadeputado.cache.constants import CacheConstants, CachePrefixesKeys
from comovotadeputado.opendata.constants import OpenDataConstants


class VotesCtrl:

    def get_all_votes_dataframe(self, year):
        
        cache_key = CachePrefixesKeys.ALL_VOTES_PREFIXE_KEY + year
        
        @cache.cache(cache_key, expire=CacheConstants.EXPIRATION_TIME)
        def _get_all_votes_dataframe(year):

            propositions_df = open_dt_ctrl.get_voted_propositions_dataframe(year)        
            all_votes_df = pd.DataFrame()
            
            for index, row in propositions_df.iterrows():
        
                cod_proposition = row['codProposicao']
                voted_date = row['dataVotacao']
                proposition = open_dt_ctrl.get_proposition(cod_proposition)
               
                try:
                    polls_df = open_dt_ctrl.get_polls_dataframe(proposition.type, proposition.number, 
                        proposition.year, voted_date)
                except Exception as e:
                    error_msg = str(e)
                    if error_msg == ErrorMessages.UNOBTAINABLE_DATA:
                        continue
                    else:
                        raise Exception(e)               
        
                if all_votes_df.empty:
                    all_votes_df = polls_df
                else:
                    all_votes_df = all_votes_df.append(polls_df)
        
            return all_votes_df

        return _get_all_votes_dataframe(year)        

    def get_congressman_votes_dataframe(self, congressman_id, year):
        all_votes_df = self.get_all_votes_dataframe(year)
        congressman_votes_df = all_votes_df.loc[
            (all_votes_df[OpenDataConstants.CONGRESSMAN_ID_COLNAME] == congressman_id)]
        return congressman_votes_df