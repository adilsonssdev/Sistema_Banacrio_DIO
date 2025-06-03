from abc import ABC, abstractmethod
from controller.banco_controler import Controle
from data.conexao_bd import DadosBanco
from models.cliente import Cliente
from utils.utilidades import Utils


UTILS = Utils()
CONTROLE = Controle()


class Agencia(ABC):
    def __init__(self, agNumero="0001"):
        """Inicia a classe setando a agencia padrão como 0001"""
        self.agNumero = agNumero

    @abstractmethod
    def conectar_bd(self):
        """Metodo abstrato que obriga os "filhos" criaram uma conexão com baco de dados"""
        pass


class Conta(Agencia):

    def __init__(self, cliente: Cliente = None):
        """Recebe um objeto do tipo Cliente e os atributos da classe pai"""
        super().__init__()
        self.cliente = cliente

    @property
    def conectar_bd(self):
        banco = DadosBanco()
        return banco.conectar_bd()

    def criar_conta(self, saldo_inicial=0):
        """Função principal para criar uma nova conta com as infoações do cliente"""
        dict_conta = self.cliente.__dict__  # Converte o objeto cliente em um dicionário
        con = self.conectar_bd
        query = con.cursor()

        # Faz a validação dos dados passados antes de criar a conta
        validacao_cliente = self.cliente.validacao_cliente()
        if isinstance(validacao_cliente, Exception):
            print("Erro na validação:", validacao_cliente)

        # Se a validação for bem sucedida, tenta adicionar um novo registro na tabela com historico de criação de conta
        if validacao_cliente == True:
            try:
                historico = f"[{UTILS.dict_para_str({'Criação de conta': UTILS.data_para_iso()})}]"
                query.execute(
                    """
                    INSERT INTO contas 
                    (nome, senha, saldo, saques_dia, data_nascimento, cpf, endereco, historico)
                    VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        dict_conta["nome"],
                        dict_conta["senha"],
                        saldo_inicial,
                        0,
                        dict_conta["nascimento"],
                        dict_conta["cpf"],
                        dict_conta["endereco"],
                        historico,
                    ),
                )
            # Caso falhe a criação, retorna erro, e verifica se o erro é de duplicidade no CPF
            except Exception as e:
                if "UNIQUE constraint failed" in str(e):
                    print("CPF já cadastrado.")
                    return
                else:
                    print("Erro ao criar conta:", e)
                    return

            # Obtem o ultimo id registrado na tabela
            ultimo_id = query.lastrowid

            query.execute(
                f"""
               SELECT * FROM contas
               WHERE id = {ultimo_id}
               AND agencia = "{self.agNumero}"
               """
            )

            conta = UTILS.tupla_para_dicionario(query.fetchone())
            print(
                f'Conta criada com sucesso!, agencia: {conta["agencia"]}, conta: {conta['id']}'
            )

            con.commit()
            query.close()
            con.close()
            # Apos criar nova conta, é realizado um login automatico do novo usuário
            return self.login(Cliente(cpf=conta["cpf"], senha=conta["senha"]))

    def login(self, cliente: Cliente = None, e_reload=False):
        """Função principal para realizar login com dados do cliente"""
        cpf = cliente.cpf
        senha = cliente.senha
        con = self.conectar_bd
        query = con.cursor()

        try:
            query.execute(
                """
                        SELECT * FROM contas
                        WHERE cpf = ? AND senha = ?
                        """,
                (cpf, senha),
            )

            conta = UTILS.tupla_para_dicionario(query.fetchone())
            # Se o login for bem sucedido, retorna os dados da conta
            if not conta is None:
                if not e_reload:
                    print(f'Bem-vindo(a) {conta["nome"]}!')
                return conta
            else:
                print("Conta inexistente ou senha incorreta.")
                return None
        # Caso falhe o login, retorna erro
        except Exception as e:
            print(f"Autenticação atual falhou, refaça o login.\n {e}")
            return None
        finally:
            query.close()
            con.close()

    def depositar(self, agencia, conta_numero, valor_deposito, /, *, conta_auth=None):
        """Função principal para realizar depositos com ou sem autenticação"""
        con = self.conectar_bd
        query = con.cursor()
        cliente: Cliente = None

        # Cria um cliente com os dados do auth passado
        # Esta variavel é usada para atualizar os dados do cliente chamando a função de login
        if cliente == None and conta_auth is not None:
            try:
                cliente = Cliente(cpf=conta_auth["cpf"], senha=conta_auth["senha"])
            except:
                print("Autenticação atual falhou, refaça o login.")

        try:
            # Obtem o historico da conta passada usando agencia e conta
            if not (agencia is None or conta_numero is None):
                query.execute(
                    """
                        SELECT historico FROM contas WHERE id = ? AND agencia = ?
                        """,
                    (conta_numero, agencia),
                )
            else:
                # Obtem o historico da conta usando o auth
                query.execute(
                    """
                        SELECT historico FROM contas WHERE id = ? AND agencia = ?
                        """,
                    (conta_auth["id"], conta_auth["agencia"]),
                )

            historico = UTILS.texto_json(query.fetchone()[0])
            # Realiza o deposito sem autenticação de usuário e atualiza o historico da conta que recebeu o deposito
            if conta_auth is None:
                print("Depósito sem autenticação...")
                # Valida o valor a ser depositado
                try:
                    CONTROLE.valida_deposito(valor_deposito)
                except ValueError as e:
                    print(e)
                    return conta_auth

                # Atualiza o historico da conta do usuario que recebe o deposito
                historico.append(
                    {f"Depósito - {valor_deposito:.2f}": UTILS.data_para_iso()}
                )
                novo_historico = UTILS.dict_para_str(historico)
                query.execute(
                    """
                    UPDATE contas SET 
                    saldo = saldo + ?,
                    historico = ?
                    WHERE id = ? AND agencia = ?
                    """,
                    (
                        valor_deposito,
                        novo_historico,
                        conta_numero,
                        agencia,
                    ),
                )
                con.commit()
                print(f"Depósito de R$ {valor_deposito:.2f} realizado com sucesso!")

            # Realiza o deposito com autenticação de usuário e atualiza o historico da conta
            elif conta_auth:
                # Valida o valor a ser depositado
                try:
                    CONTROLE.valida_deposito(valor_deposito)
                except ValueError as e:
                    print(e)
                    return conta_auth

                # Atualiza o historico da conta
                historico.append(
                    {f"Depósito - {valor_deposito:.2f}": UTILS.data_para_iso()}
                )
                novo_historico = UTILS.dict_para_str(historico)

                query.execute(
                    """
                    UPDATE contas SET 
                    saldo = saldo + ?,
                    historico = ?
                    WHERE id = ? AND agencia = ?
                    """,
                    (
                        valor_deposito,
                        novo_historico,
                        conta_numero,
                        agencia,
                    ),
                )
                con.commit()
                print(f"Depósito de R$ {valor_deposito:.2f} realizado com sucesso!")
                print("==" * 20)
                # Atualiza o auth para retornar um historico e saldo atualizados
                recarrega_conta = self.login(cliente, True)
                conta_auth = recarrega_conta
                print(f"Saldo atual: R$ {recarrega_conta['saldo']:.2f}")
                return conta_auth

        except Exception as e:
            print("Não foi possivel realizar depósito")
            print("Verifique se os dados foram digitados corretamente.\n", e)
        finally:
            query.close()
            con.close()

    def sacar(self, conta_auth=None, valor_saque=0):
        """Função principal para realizar saques da conta, usuario precisa esta autenticado"""
        con = self.conectar_bd
        query = con.cursor()
        cliente: Cliente = None

        print("==" * 20)
        print("Validando infomações de saque...")

        # Cria um cliente com os dados do auth passado
        # Esta variavel é usada para atualizar os dados do cliente chamando a função de login
        if cliente == None:
            try:
                cliente = Cliente(cpf=conta_auth["cpf"], senha=conta_auth["senha"])
            except:
                print("Autenticação atual falhou, refaça o login.")

        # Valida saque a ser realizado
        try:
            CONTROLE.valida_saque(valor_saque, conta_auth)
            pass
        except ValueError as e:
            print(e)
            return conta_auth

        print("==" * 20)
        print("Autenticação realizada com sucesso!")
        print("Efetuando saque solicitado...")
        print("==" * 20)

        # Obtem historico para determinar limite de saques diarios
        historico = UTILS.str_para_df(conta_auth["historico"])
        historico_saques = UTILS.filtro_extrato(historico, "Saque")

        # Verifica se a conta atingiu o limite de saques diários
        if conta_auth["saques_dia"] >= 5:
            # Se limite tiver atingido, verifica se a ultima data de saque é hoje
            if UTILS.compara_datas(historico_saques["Data/Hora"].to_list()[-1]):
                print("Limite de saques diários atingido.")
                return conta_auth

            # Se o limite for atingido e a data for diferente de hoje, recomeça a contagem
            else:
                query.execute(
                    """
                    UPDATE contas SET saques_dia = 0 WHERE id = ? AND agencia = ?
                    """,
                    (conta_auth["id"], conta_auth["agencia"]),
                )
                con.commit()

        print("==" * 20)

        # Realiza o saque subtraindo o valor solicitado do saldo no bd
        query.execute(
            """
                UPDATE contas SET saldo = saldo - ?, saques_dia = saques_dia + 1 WHERE id = ? AND agencia = ?
                """,
            (valor_saque, conta_auth["id"], conta_auth["agencia"]),
        )
        con.commit()
        print(f"Saque de R$ {valor_saque:.2f} realizado com sucesso!")

        # Obtem historico de saques e adicona o saque realizado ao extrato
        historico_dict = UTILS.texto_json(conta_auth["historico"])
        historico_dict.append({f"Saque - {valor_saque:.2f}": UTILS.data_para_iso()})
        att_historico = UTILS.dict_para_str(historico_dict)

        query.execute(
            """
            UPDATE contas SET historico = ? WHERE id = ? AND agencia = ?
            """,
            (att_historico, conta_auth["id"], conta_auth["agencia"]),
        )

        con.commit()
        recarrega_conta = self.login(cliente, True)
        conta_auth = recarrega_conta
        print(f'Saldo atual: R$ {conta_auth["saldo"]:.2f}')

        query.close()
        con.close()
        return conta_auth

    def extrato(self, conta_auth=None):
        """Função principal para visualizar o extrato da conta, usuario precisa estar autenticado"""
        print("==" * 20)
        print("Validando infomações do usúario...")

        if conta_auth is None:
            print("Conta não autenticada. Faça login primeiro.")
        else:
            print("==" * 20)
            print("Autenticação realizada com sucesso!")
            print("==" * 20)

        print(f'Saldo atual: R$ {conta_auth["saldo"]:.2f}')

        # Exibe a tabela com movimentações da conta
        print("==" * 20)
        print(UTILS.str_para_df(conta_auth["historico"]))
        print("==" * 20)

        return conta_auth
