import sqlite3 as bd

class DadosBanco:
  def __init__(self):
    self.bd_local = './contas.db'
    self.con = bd.connect(self.bd_local)
    self.querys = self.con.cursor()
    self.cria_tabela()

  def cria_tabela(self):
    ''' Cria uma tabela caso ela nao exista com as informações necessarias '''
    self.querys.execute('''
                CREATE TABLE IF NOT EXISTS contas (
                  id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  agencia TEXT DEFAULT "0001",
                  nome TEXT NOT NULL, 
                  senha TEXT NOT NULL,
                  saldo REAL NOT NULL,
                  saques_dia INTEGER DEFAULT 0,
                  data_nascimento TEXT DEFAULT NULL,
                  cpf TEXT UNIQUE,
                  endereco TEXT DEFAULT NULL,
                  historico TEXT DEFAULT NULL
                )
                ''')
    self.con.commit()

  def conectar_bd(self):
    '''Faz a conexao com o banco de dados, tabela contas'''
    con = self.con
    return con
