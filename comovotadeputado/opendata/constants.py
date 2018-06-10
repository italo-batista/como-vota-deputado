
class OpenDataConstants:

    # endpoints
    PROPOSITION_ENDPOINT = "http://www.camara.leg.br/SitCamaraWS/Proposicoes.asmx/ObterProposicaoPorID"
    POLLS_PROPOSITIONS_ENDPOINT = "http://www.camara.leg.br/SitCamaraWS/Proposicoes.asmx/ObterVotacaoProposicao"
    VOTED_PROPOSITIONS_ENDPOINT = "http://www.camara.leg.br/SitCamaraWS/Proposicoes.asmx/ListarProposicoesVotadasEmPlenario"

    # data colnames
    PROPOSITION_DATE_COLNAME = '@Data'
    PROPOSITION_HOUR_COLNAME = '@Houre'
    PROPOSITION_SUMMARY_COLNAME = '@Resumo'
    PROPOSITION_TYPE_COLNAME = "@tipo"
    PROPOSITION_YEAR_COLNAME = "@ano"
    PROPOSITION_NUMBER_COLNAME = "@numero"
    CONGRESSMAN_ID_COLNAME = '@ideCadastro'

    # json keys
    PROPOSITION_JSON_KEY = 'proposicao'
    PROPOSITIONS_JSON_KEY = 'proposicoes'
    POLL_JSON_KEY = 'Votacao'
    POLLS_JSON_KEY = 'Votacoes'
    VOTE_JSON_KEY = 'votos'
    CONGRESSMAN_JSON_KEY = 'Deputado'
