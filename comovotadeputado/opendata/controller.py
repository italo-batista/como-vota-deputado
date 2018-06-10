import requests
import json
import xmltodict
from comovotadeputado.cache import fetch_data
from comovotadeputado.opendata.constants import OpenDataConstants

# def _get_proposition(propostion_id):
    
#     cache_key = 'proposition' + propostion_id    
#     @cache.cache(cache_key, expire=3600)
#     def fetch_data(propostion_id):
#         query_url = OpenDataConstants.PROPOSITION_ENDPOINT + "?IdProp=" + propostion_id
#         resp = requests.get(query_url)
#         return resp

#     results = fetch_data(propostion_id)
#     return results

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