#one_day = 3600 * 24
one_day = 240


class CacheConstants:
    EXPIRATION_TIME = one_day


class CachePrefixesKeys:
    ALL_VOTES_PREFIXE_KEY = 'all_votes_dataframe_'
    PROPOSITION_PREFIXE_KEY = 'proposition_'
    HTTP_VOTED_PROPOSITIONS_PREFIXE_KEY = 'http_voted_propositions_'
    HTTP_POOLS_JSON_PREFIXE_KEY = 'http_polls_json_'
