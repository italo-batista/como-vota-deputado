import pandas as pd

import comovotadeputado.cache as cache
from comovotadeputado.opendata.constants import OpenDataConstants
from comovotadeputado.errors.messages import ErrorMessages
from comovotadeputado.constants.http import HttpStatusCode
from comovotadeputado.utils.parser import xml_to_json
from comovotadeputado.models.proposition import Proposition
from comovotadeputado.cache.constants import CachePrefixesKeys


def _get_voted_propositions(year):
    cache_key =  CachePrefixesKeys.HTTP_VOTED_PROPOSITIONS_PREFIXE_KEY + year
    query_url = OpenDataConstants.VOTED_PROPOSITIONS_ENDPOINT + "?ano=" + year + "&tipo="
    resp = cache.http_fetch_data(cache_key, query_url)
    return resp

def get_voted_propositions_dataframe(year):
    resp = _get_voted_propositions(year)
    resp_json = xml_to_json(resp.content)
    propositions_df = pd.io.json.json_normalize(resp_json['proposicoes']['proposicao'])
    return propositions_df

def _get_proposition(propostion_id):
    cache_key = CachePrefixesKeys.PROPOSITION_PREFIXE_KEY + propostion_id
    query_url = OpenDataConstants.PROPOSITION_ENDPOINT + "?IdProp=" + propostion_id
    resp = cache.http_fetch_data(cache_key, query_url)
    return resp

def get_proposition(propostion_id):
    resp = _get_proposition(propostion_id)
    resp_json = xml_to_json(resp.content)
    proposition_json = resp_json['proposicao']
    p_type = proposition_json['@tipo'].strip()
    p_year = proposition_json['@ano'].strip()
    p_number = proposition_json['@numero'].strip()      
    proposition = Proposition(p_number, p_type, p_year)
    return proposition

def _get_polls(p_type, p_number, p_year):
    cache_key = CachePrefixesKeys.HTTP_POOLS_JSON_PREFIXE_KEY + p_type + p_number + p_year
    query_url = OpenDataConstants.POLLS_PROPOSITIONS_ENDPOINT + "?tipo=" + p_type + "&numero=" + p_number + "&ano=" + p_year
    resp = cache.http_fetch_data(cache_key, query_url)
    return resp

def get_polls_dataframe(p_type, p_number, p_year, voted_date):

    resp = _get_polls(p_type, p_number, p_year)    
    if resp.status_code != HttpStatusCode.OK:
        raise Exception(ErrorMessages.UNOBTAINABLE_DATA)
        
    resp_json = xml_to_json(resp.content)
    polls = resp_json['proposicao']['Votacoes']['Votacao']
    if '@Resumo' in polls: # has only one vote
        polls = [polls]

    polls_df = pd.DataFrame()
    for poll in polls:

        date = poll['@Data']
        hour = poll['@Hora']
                
        #if date != voted_date: 
            #continue
            # date = 10/3/2018, voted_date = 10/03/2018

        if polls_df.empty:
            polls_df = pd.io.json.json_normalize(poll['votos']['Deputado'])
            polls_df['@Data'] = date
            polls_df['@Hora'] = hour
        else:
            new_votes = pd.io.json.json_normalize(poll['votos']['Deputado'])
            new_votes['@Data'] = date
            new_votes['@Hora'] = hour
            polls_df = polls_df.append(new_votes)
    
    return polls_df    
