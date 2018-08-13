

class OpenDataConstants:

    # endpoints
    PROPOSITION_ENDPOINT = "http://www.camara.leg.br/SitCamaraWS/Proposicoes.asmx/ObterProposicaoPorID"
    POLLS_PROPOSITIONS_ENDPOINT = "http://www.camara.leg.br/SitCamaraWS/Proposicoes.asmx/ObterVotacaoProposicao"
    VOTED_PROPOSITIONS_ENDPOINT = "http://www.camara.leg.br/SitCamaraWS/Proposicoes.asmx/ListarProposicoesVotadasEmPlenario"
    ATTENDANCE_ENDPOINT = "http://www.camara.leg.br/SitCamaraWSV2/sessoesreunioes.asmx/ListarPresencasDia"

    # data colnames
    PROPOSITION_DATE_COLNAME = '@Data'
    PROPOSITION_HOUR_COLNAME = '@Hora'
    PROPOSITION_SUMMARY_COLNAME = '@Resumo'
    PROPOSITION_TYPE_COLNAME = "@tipo"
    PROPOSITION_YEAR_COLNAME = "@ano"
    PROPOSITION_NUMBER_COLNAME = "@numero"
    CONGRESSMAN_ID_COLNAME = '@ideCadastro'
    ATTENDANCE_DATE_STR_COLNAME = 'Date'
    ATTENDANCE_CONGRESSPERSON_MAT_COLNAME = "CongresspersonId"
    ATTENDANCE_CONGRESSPERSON_NAME_COLNAME = 'CongresspersonName'
    ATTENDANCE_POLITICAL_PARTY_COLNAME = "PoliticalParty"
    ATTENDANCE_FEDERATION_UNITY_COLNAME = 'FedUnity'
    ATTENDANCE_DESC_COLNAME = 'Attendance'

    # json keys
    PROPOSITION_JSON_KEY = 'proposicao'
    PROPOSITIONS_JSON_KEY = 'proposicoes'
    POLL_JSON_KEY = 'Votacao'
    POLLS_JSON_KEY = 'Votacoes'
    VOTE_JSON_KEY = 'votos'
    CONGRESSMAN_JSON_KEY = 'Deputado'
    ATTENDANCE_DAY_JSON_KEY = "dia"
    ATTENDANCE_DATE_JSON_KEY = "data"
    ATTENDANCE_CONGRESSPEOPLE_JSON_KEY = "parlamentares"
    ATTENDANCE_CONGRESSPERSON_JSON_KEY = "parlamentar"
    ATTENDANCE_CONGRESSPERSON_MAT_JSON_KEY = "carteiraParlamentar"
    ATTENDANCE_CONGRESSPERSON_NAME_JSON_KEY = "nomeParlamentar"
    ATTENDANCE_POLITICAL_PARTY_JSON_KEY = "siglaPartido"
    ATTENDANCE_FED_UNITY_JSON_KEY = "siglaUF"
    ATTENDANCE_DAY_FREQ_JSON_KEY = "descricaoFrequenciaDia"





