from controller.banco_controler import Controle

class Cliente:
  def __init__(self, nome=None, nascimento=None, endereco=None, /, *, cpf, senha):
    """Recebe os dados do cliente."""
    self.nome = nome
    self.senha = senha
    self.nascimento = nascimento
    self.cpf = cpf
    self.endereco = endereco

  def validacao_cliente(self):
    """ Chama a classe Controle para validar os dados do cliente."""
    dict_conta = {
        "nome": self.nome,
        "senha": self.senha,
        "data_nascimento": self.nascimento,
        "cpf": self.cpf,
        "endereco": self.endereco,
    }
    controle = Controle()
    validacao = controle.valida_cliente(dict_conta)
    return validacao
  