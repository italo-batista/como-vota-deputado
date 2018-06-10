import mock
import requests
from unittest import TestCase

import comovotadeputado.opendata.controller as opendata_ctrl
from comovotadeputado.opendata.constants import OpenDataConstants
from comovotadeputado.models.proposition import Proposition

PROPOSITION_ID = "354258"

def _get_mocked_proposition_response():
    query_url = OpenDataConstants.PROPOSITION_ENDPOINT + "?IdProp=" + PROPOSITION_ID
    resp = requests.get(query_url)
    return resp

def _get_mocked_proposition_obj():
    p_number, p_type, p_year = "81", "PEC", "2007"
    proposition = Proposition(p_number, p_type, p_year)
    return proposition

class PropositionTest(TestCase):

    def test_get_proposition_obj(self):

        opendata_ctrl._get_proposition = mock.Mock(return_value= _get_mocked_proposition_response())

        expected_proposition = _get_mocked_proposition_obj()
        proposition = opendata_ctrl.get_proposition(PROPOSITION_ID)

        self.assertIsNotNone(proposition)
        self.assertIsInstance(proposition, Proposition)
        self.assertEquals(proposition.number, expected_proposition.number)