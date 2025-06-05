import json
from datetime import datetime
import pandas as pd


class Utils:

    @staticmethod
    def data_para_iso():
        """Retorna a data atual no formato ISO"""
        return datetime.now().isoformat()

    @staticmethod
    def texto_json(texto):
        """Converte um texto em json"""
        return json.loads(texto)

    @staticmethod
    def dict_para_str(mapa):
        """Converte um json em string"""
        return json.dumps(mapa)

    @staticmethod
    def str_para_df(texto):
        """Converte uma string passada em json e retorna um dataframe do pandas"""
        a = json.loads(texto)
        for i in a:
            for k, v in i.items():
                i[k] = datetime.strptime(v, "%Y-%m-%dT%H:%M:%S.%f").strftime(
                    "%d/%m/%Y %H:%M:%S"
                )
        df = pd.DataFrame(a)
        df = df.melt(var_name="Evento", value_name="Data/Hora")
        df = df.dropna()
        return df

    @staticmethod
    def filtro_extrato(df, evento):
        """Filtra a coluna do dataframe pelo evento, retorna apenas os itens que atendem a condição"""
        filtro = df["Evento"].str.contains(evento)
        # Retorna apenas itens que atendem a condição
        return df[filtro]

    @staticmethod
    def compara_datas(data1):
        """Compara datas e retorna True ou False se forem iguais ou diferentes"""
        b = datetime.strptime(data1, "%d/%m/%Y %H:%M:%S").strftime("%d/%m/%Y")
        a = datetime.today().strftime("%d/%m/%Y")
        return a == b

    @staticmethod
    def tupla_para_dicionario(tupla):
        '''Converte uma tupla em dicionário com base nas chaves presentes na variavel "chaves"'''
        chaves = [
            "id",
            "agencia",
            "nome",
            "senha",
            "saldo",
            "saques_dia",
            "data_nascimento",
            "cpf",
            "endereco",
            "historico",
        ]
        dicionario = dict(zip(chaves, tupla))
        return dicionario
