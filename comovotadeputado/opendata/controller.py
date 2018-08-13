import pandas as pd
import datetime as dt

import comovotadeputado.cache as cache
from comovotadeputado.opendata.constants import OpenDataConstants
from comovotadeputado.opendata.attendance_values import CongressPersonAttendance
from comovotadeputado.errors.messages import ErrorMessages
from comovotadeputado.constants.http import HttpStatusCode
from comovotadeputado.utils.parser import xml_to_json
from comovotadeputado.models.proposition import Proposition
from comovotadeputado.cache.constants import CachePrefixesKeys
from comovotadeputado.utils import is_empty_or_none


def _get_voted_propositions(year):
    cache_key =  CachePrefixesKeys.HTTP_VOTED_PROPOSITIONS_PREFIXE_KEY + year
    query_url = OpenDataConstants.VOTED_PROPOSITIONS_ENDPOINT + "?ano=" + year + "&tipo="
    resp = cache.http_fetch_data(cache_key, query_url)
    return resp

def get_voted_propositions_dataframe(year):
    resp = _get_voted_propositions(year)
    resp_json = xml_to_json(resp.content)
    propositions_df = pd.io.json.json_normalize(
        resp_json[OpenDataConstants.PROPOSITIONS_JSON_KEY][OpenDataConstants.PROPOSITION_JSON_KEY])
    return propositions_df

def _get_proposition(propostion_id):
    cache_key = CachePrefixesKeys.PROPOSITION_PREFIXE_KEY + propostion_id
    query_url = OpenDataConstants.PROPOSITION_ENDPOINT + "?IdProp=" + propostion_id
    resp = cache.http_fetch_data(cache_key, query_url)
    return resp

def get_proposition(propostion_id):
    resp = _get_proposition(propostion_id)
    resp_json = xml_to_json(resp.content)
    proposition_json = resp_json[OpenDataConstants.PROPOSITION_JSON_KEY]
    p_type = proposition_json[OpenDataConstants.PROPOSITION_TYPE_COLNAME].strip()
    p_year = proposition_json[OpenDataConstants.PROPOSITION_YEAR_COLNAME].strip()
    p_number = proposition_json[OpenDataConstants.PROPOSITION_NUMBER_COLNAME].strip()
    proposition = Proposition(p_number, p_type, p_year)
    return proposition

def _get_polls_response(p_type, p_number, p_year):
    cache_key = CachePrefixesKeys.HTTP_POOLS_JSON_PREFIXE_KEY + p_type + p_number + p_year
    query_url = OpenDataConstants.POLLS_PROPOSITIONS_ENDPOINT + "?tipo=" + p_type + "&numero=" + p_number + "&ano=" + p_year
    resp = cache.http_fetch_data(cache_key, query_url)
    return resp

def get_polls_dataframe(p_type, p_number, p_year, voted_date):

    resp = _get_polls_response(p_type, p_number, p_year)
    if resp.status_code != HttpStatusCode.OK:
        raise Exception(ErrorMessages.UNOBTAINABLE_DATA)
        
    resp_json = xml_to_json(resp.content)
    proposition_json = resp_json[OpenDataConstants.PROPOSITION_JSON_KEY]
    polls = proposition_json[OpenDataConstants.POLLS_JSON_KEY][OpenDataConstants.POLL_JSON_KEY]
    if OpenDataConstants.PROPOSITION_SUMMARY_COLNAME in polls: # has only one vote
        polls = [polls]

    polls_df = pd.DataFrame()
    for poll in polls:

        date = poll[OpenDataConstants.PROPOSITION_DATE_COLNAME]
        hour = poll[OpenDataConstants.PROPOSITION_HOUR_COLNAME]
                
        #if date != voted_date: 
            #continue
            # date = 10/3/2018, voted_date = 10/03/2018

        new_votes = pd.io.json.json_normalize(
            poll[OpenDataConstants.VOTE_JSON_KEY][OpenDataConstants.CONGRESSMAN_JSON_KEY])
        new_votes[OpenDataConstants.PROPOSITION_DATE_COLNAME] = date
        new_votes[OpenDataConstants.PROPOSITION_HOUR_COLNAME] = hour
        if polls_df.empty:
            polls_df = new_votes
        else:
            polls_df = polls_df.append(new_votes)
    
    return polls_df    

def _get_attendances_response(date, congressperson_id, political_party_initials, uf_initials):
    cache_key = CachePrefixesKeys.HTTP_ATTENDANCES_JSON_PREFIXE_KEY + congressperson_id + date.ctime() \
                + political_party_initials + uf_initials
    query_url = OpenDataConstants.ATTENDANCE_ENDPOINT + "?data="

    if isinstance(date, dt.datetime):
        query_url += str(date.day) + "/" + str(date.month) + "/" + str(date.year)

    query_url += "&numMatriculaParlamentar="
    if not is_empty_or_none(congressperson_id):
        query_url += congressperson_id

    # TO DO: for the future
    query_url += "&siglaPartido="
    if not is_empty_or_none(political_party_initials):
        query_url += political_party_initials

    # TO DO: for the future
    query_url += "&siglaUF="
    if not is_empty_or_none(uf_initials):
        query_url += uf_initials

    resp = cache.http_fetch_data(cache_key, query_url)
    return resp

def get_attendances_dataframe(date, congressperson_id, political_party_initials, uf_initials):
    resp = _get_attendances_response(date, congressperson_id, political_party_initials, uf_initials)

    if resp.status_code != HttpStatusCode.OK:
        raise Exception(ErrorMessages.UNOBTAINABLE_DATA)

    resp_json = xml_to_json(resp.content)

    if resp_json[OpenDataConstants.ATTENDANCE_DAY_JSON_KEY] == None:
        raise Exception(ErrorMessages.EMPTY_DATA)

    attendance_day_json = resp_json[OpenDataConstants.ATTENDANCE_DAY_JSON_KEY]
    date_str = attendance_day_json[OpenDataConstants.ATTENDANCE_DATE_JSON_KEY].split(" ")[0]
    congresspeople_json = attendance_day_json[OpenDataConstants.ATTENDANCE_CONGRESSPEOPLE_JSON_KEY][OpenDataConstants.ATTENDANCE_CONGRESSPERSON_JSON_KEY]

    if congressperson_id != "":
        congresspeople_json = [congresspeople_json]

    columns = [OpenDataConstants.ATTENDANCE_DATE_STR_COLNAME, OpenDataConstants.ATTENDANCE_CONGRESSPERSON_MAT_COLNAME,
               OpenDataConstants.ATTENDANCE_CONGRESSPERSON_NAME_COLNAME, OpenDataConstants.ATTENDANCE_POLITICAL_PARTY_COLNAME,
               OpenDataConstants.ATTENDANCE_FEDERATION_UNITY_COLNAME, OpenDataConstants.ATTENDANCE_DESC_COLNAME]
    attendances_df = pd.DataFrame(columns=columns)

    for congressperson in congresspeople_json:
        congressperson_mat = congressperson[OpenDataConstants.ATTENDANCE_CONGRESSPERSON_MAT_JSON_KEY]
        congressperson_name = congressperson[OpenDataConstants.ATTENDANCE_CONGRESSPERSON_NAME_JSON_KEY].split("-")[0]
        congressperson_ppi = congressperson[OpenDataConstants.ATTENDANCE_POLITICAL_PARTY_JSON_KEY]
        congressperson_uf = congressperson[OpenDataConstants.ATTENDANCE_FED_UNITY_JSON_KEY]
        attendances_description = congressperson[OpenDataConstants.ATTENDANCE_DAY_FREQ_JSON_KEY]

        if attendances_description == "Ausência":
            congressperson_att = CongressPersonAttendance.ABSENT
        elif attendances_description == "Ausência justificada":
            congressperson_att = CongressPersonAttendance.JUSTIFIED_ABSCENCE
        else:
            congressperson_att = CongressPersonAttendance.PRESENT

        attendances_df = attendances_df.append({
            OpenDataConstants.ATTENDANCE_DATE_STR_COLNAME: date_str,
            OpenDataConstants.ATTENDANCE_CONGRESSPERSON_MAT_COLNAME: congressperson_mat,
            OpenDataConstants.ATTENDANCE_CONGRESSPERSON_NAME_COLNAME: congressperson_name,
            OpenDataConstants.ATTENDANCE_POLITICAL_PARTY_COLNAME: congressperson_ppi,
            OpenDataConstants.ATTENDANCE_FEDERATION_UNITY_COLNAME: congressperson_uf,
            OpenDataConstants.ATTENDANCE_DESC_COLNAME: congressperson_att
        }, ignore_index=True)

    return attendances_df
