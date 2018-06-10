import pandas as pd
import comovotadeputado.cache as cache
from comovotadeputado.opendata.constants import OpenDataConstants
from comovotadeputado.errors.messages import ErrorMessages
from comovotadeputado.constants.http import HttpStatusCode
from comovotadeputado.utils.parser import xml_to_json
from comovotadeputado.models.proposition import Proposition

def _get_voted_propositions(year):
    cache_key = 'voted_propositions_' + year    
    query_url = OpenDataConstants.VOTED_PROPOSITIONS_ENDPOINT + "?ano=" + year + "&tipo="
    resp = cache.http_fetch_data(cache_key, query_url)
    return resp

def get_voted_propositions_dataframe(year):
    resp = _get_voted_propositions(year)
    resp_json = xml_to_json(resp.content)
    propositions_df = pd.io.json.json_normalize(resp_json['proposicoes']['proposicao'])
    return propositions_df

def _get_proposition(propostion_id):
    cache_key = 'proposition' + propostion_id    
    query_url = OpenDataConstants.PROPOSITION_ENDPOINT + "?IdProp=" + propostion_id
    resp = fetch_data(cache_key, query_url)
    return resp

def get_proposition(propostion_id):
    resp = _get_proposition(propostion_id)
    resp_json = json.loads(json.dumps(xmltodict.parse(resp.content)))
    propostion = resp_json['proposicao']
    return None