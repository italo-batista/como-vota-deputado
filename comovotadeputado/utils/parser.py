import json
import xmltodict


def xml_to_json(xml):
    to_dict = xmltodict.parse(xml)
    str_json = json.dumps(to_dict)
    return json.loads(str_json)