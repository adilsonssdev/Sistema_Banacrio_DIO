from datetime import datetime
class Controle:
  def __init__(self):
    """Recebe um dicionario com os dados do cliente para validação antes de criar a conta."""


  
  def valida_cliente(self, dicionario:dict={}):

    if not dicionario:
      return ValueError("\033[91m*** Nenhum dado foi passado. ***\033[0m")
    
    if not 'nome' in dicionario.keys():
      return ValueError("\033[91m*** Nome cliente não informado. ***\033[0m")
    
    if not 'senha' in dicionario.keys():
      return ValueError("\033[91m*** Senha cliente não informada. ***\033[0m")
    elif len(dicionario['senha']) < 6:
      return ValueError("\033[91m*** Senha muito curta, mínimo 6 caracteres. ***\033[0m")
    
    if not 'saldo' in dicionario.keys():
      dicionario['saldo'] = 0
    
    if not 'data_nascimento' in dicionario.keys():
      return ValueError("\033[91m*** Data nascimento cliente não informada. ***\033[0m")
    elif dicionario['data_nascimento'] != None:
      date_string = dicionario['data_nascimento']
      try:
          date_obj = datetime.strptime(date_string, "%d/%m/%Y").strftime("%d/%m/%Y")
      except:
          return ValueError("\033[91m*** A data fornecida é inválida. ***\033[0m")
    
    if not 'cpf' in dicionario.keys():
      return ValueError("\033[91m*** CPF cliente não informado. ***\033[0m")
    elif len(dicionario['cpf']) < 11:
      return ValueError("\033[91m*** CPF inválido. ***\033[0m")
    
    if not 'endereco' in dicionario.keys():
      return ValueError("\033[91m*** Endereço cliente não informado. ***\033[0m")
    
    return True
  
  def valida_deposito(self, valor_deposito):
    '''Valida o valor do depósito'''
    if valor_deposito <= 0:
        raise ValueError('\033[91m*** Valor de depósito inválido. ***\033[0m')
        
  def valida_saque(self, valor_saque, auth):
    '''Valida o valor do saque'''
    if auth is None:
      raise ValueError("\033[91m*** Conta não autenticada. Faça login primeiro. ***\033[0m")
    elif valor_saque <= 0:
      raise ValueError('\033[91m*** Valor de saque inválido. Digite um valor válido ***\033[0m')
    elif auth['saldo'] < valor_saque:
      raise ValueError("\033[91m*** Saldo insuficiente para este saque. ***\033[0m")
  

    
  
  