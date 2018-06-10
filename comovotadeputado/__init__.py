import requests
import json
import xmltodict
import pandas as pd

#ObterProposicaoPorID
def obterProposicaoPorID(propostion_id):
    url = "http://www.camara.leg.br/SitCamaraWS/Proposicoes.asmx/ObterProposicaoPorID?IdProp=" + propostion_id
    resp = requests.get(url)
    resp_json = json.loads(json.dumps(xmltodict.parse(resp.content)))
    propostion = resp_json['proposicao']
    return propostion

#ObterVotacaoProposicao
def obterVotacaoProposicao(tipo, numero, ano):
    url = "http://www.camara.leg.br/SitCamaraWS/Proposicoes.asmx/ObterVotacaoProposicao?tipo=" + tipo + "&numero=" + numero + "&ano=" + ano

    resp = requests.get(url)
    
    if resp.status_code != 200:
        raise Exception('Nao foi possivel obter dados')
        
    resp_json = json.loads(json.dumps(xmltodict.parse(resp.content)))

    year = resp_json['proposicao']['Ano']
    number = resp_json['proposicao']['Numero']
    polls = resp_json['proposicao']['Votacoes']['Votacao']

    if '@Resumo' in resp_json['proposicao']['Votacoes']['Votacao']: #has one vote just
        polls = [polls]

    polls_df = pd.DataFrame()
    for poll in polls:
        date = poll['@Data']
        hour = poll['@Hora']
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

class ComoVotaDeputado:

    def __init__(self):
        pass

    def test(self):
        url = "http://www.camara.leg.br/SitCamaraWS/Proposicoes.asmx/ListarProposicoesVotadasEmPlenario?ano=2017&tipo="
        resp = requests.get(url)
        resp_json = json.loads(json.dumps(xmltodict.parse(resp.content)))
        propositions_df = pd.io.json.json_normalize(resp_json['proposicoes']['proposicao'])
        propositions_df = propositions_df[['codProposicao', 'nomeProposicao']]
        propositions_df.drop_duplicates(inplace=True)

        df = pd.DataFrame()
        for index, row in propositions_df.iterrows():
            cod_proposition = row['codProposicao']

            proposition = obterProposicaoPorID(cod_proposition)
            proposition_type = proposition['@tipo'].strip()
            proposition_year = proposition['@ano'].strip()
            proposition_number = proposition['@numero'].strip()
            
            try:
                polls_df = obterVotacaoProposicao(proposition_type, proposition_number, proposition_year)
            except Exception as e:
                if e.args == 'Nao foi possivel obter dados':
                    continue
                
            if df.empty:
                df = polls_df
            else:
                df = df.append(polls_df)
        
        return df.to_dict()
