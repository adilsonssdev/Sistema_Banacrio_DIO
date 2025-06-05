from models.agencia_conta import Conta
from models.cliente import Cliente
from data.conexao_bd import DadosBanco
from models.agencia_conta import Conta

def verificar_cpf_existe(cpf):
    """Verifica se o CPF existe na base de dados."""
    banco = DadosBanco()
    con = banco.conectar_bd() 
    query = con.cursor()

    query.execute(
        '''
        SELECT cpf FROM contas WHERE cpf = ? LIMIT 1
        ''',
        (cpf,)
    )
    resultado = query.fetchone()
    query.close()
    con.close()
    return resultado

def cria_nova_conta(cpf, senha):
  """
  Cria uma nova conta para o cliente.
  """
  nome = input('Digite seu nome: ')
  nascimento = input('Digite sua data de nascimento (DD/MM/AAAA): ')
  cidade = input('Digite sua cidade: ')
  estado = input('Digite seu estado (UF): ')
  bairro = input('Digite seu bairro: ', )
  rua_nome = input('Digite o nome da rua: ')
  rua_numero = input('Digite o número de sua casa: ')
  endereco = f"{rua_nome}, {rua_numero}, {bairro} - {cidade}/{estado}"
  cliente = Cliente(nome, nascimento, endereco, cpf=cpf, senha=senha)
  obj_conta = Conta(cliente=cliente)
  auth = obj_conta.criar_conta()
  
  return auth

def conta_cliente(cpf=None, senha=None):
  """Retorna o objeto Conta com ou sem autenticação."""
  try:
    cliente = Cliente(cpf=cpf, senha=senha)
    obj_conta = Conta(cliente)
  except:
    obj_conta = Conta()
  return obj_conta

def login():
  """Faz login de usuário existentes no banco de dados."""
  cpf = input('Digite seu CPF (apenas números): ')
  if verificar_cpf_existe(cpf) is not None:
    senha = input('Digite sua senha: ')
    obj_conta = conta_cliente(cpf, senha)
    auth = obj_conta.login(cliente=Cliente(cpf=cpf, senha=senha))
    print('=='*20)
  else:
    print('CPF não cadastrado')
    print('=='*20)
    resposta = input('Deseja criar nova conta? (s/n): ')
    if resposta == 'n':
      return None
    else:
        senha = input('Digite a senha de acesso: ')
        auth = cria_nova_conta(cpf, senha)
  return auth

def deposito(auth=None):
  """Deposita dinheiro na conta do usuário locado ou de terceiros."""
  tipo_deposito = None
  agencia = None
  cont_numero = None

  if auth is not None:
    tipo_deposito = input('Deposito para sua conta ou de terceiros? \n 1 - Minha conta \n 2 - Conta de terceiros \n R => ')
    if tipo_deposito == '2':
      agencia = input('Digite o número da agência: ')
      cont_numero = int(input('Digite o número da conta: '))
      deposito_valor = float(input('Digite o valor a depositar: '))
      obj_conta = conta_cliente()
      obj_conta.depositar(agencia, cont_numero, deposito_valor)
      return auth
    elif tipo_deposito == '1':
      deposito_valor = float(input('Digite o valor a depositar: '))
      obj_conta = conta_cliente(auth['cpf'], auth['senha'])
      auth = obj_conta.depositar(auth['agencia'], auth['id'], deposito_valor, conta_auth=auth)
      return auth
  else:
    agencia = input('Digite o número da agência: ')
    cont_numero = int(input('Digite o número da conta: '))
    deposito_valor = float(input('Digite o valor a depositar: '))
    obj_conta = conta_cliente()
    obj_conta.depositar(agencia, cont_numero, deposito_valor)
    return auth

def saque(auth=None):
  """Saca dinheiro da conta do usuário locado respeitando o limite diário"""
  if auth is not None:
    saque_valor = float(input('Digite o valor a sacar: '))
    obj_conta = conta_cliente()
    auth = obj_conta.sacar(valor_saque=saque_valor,conta_auth=auth)
    return auth

def extrato(auth=None):
  """Retorna uma tabela com o extrato da conta do usuário locado"""
  if auth is not None:
    obj_conta = conta_cliente()
    auth = obj_conta.extrato(conta_auth=auth)
    return auth

def opcoes_usuario(auth=None):
    '''Retorna opções ao usuario dependendo se ele esta logado ou nao'''
    if auth is None:
        opcoes = '''
        0 - Login
        1 - Depositar (sem login)
        4 - Sair
        '''
    else:
        opcoes = '''
        1 - Depositar
        2 - Sacar
        3 - Extrato
        4 - Sair
        '''
    return opcoes

def user_interface():
  """
  Loop principal do programa.
  Realiza ação de acordo com a opção escolhida pelo usuário.
  """
  auth = None
  inicio = input('Bem vindo ao Banco APVCASH! \nDeseja fazer login ou criar uma nova conta? (s/n): ')

  if inicio == 's':
    print('=='*20)
    auth = login()
    print('=='*20)
  
  loop = True

  while loop:
    
    
    print(opcoes_usuario(auth))

    opcao = input('Escolha uma opção: ')
    if opcao == '0':
      auth = login()
    elif opcao == '1':
      auth = deposito(auth)
    elif opcao == '2':
      auth = saque(auth)
    elif opcao == '3':
      auth = extrato(auth)
    elif opcao == '4':
      print('=='*20)
      print("Obrigado pela visita! Volte sempre!")
      print('=='*20)
      loop = False
      

