# Sistema Bancário

Este é um projeto de um sistema bancário simples desenvolvido em Python, utilizando SQLite como banco de dados. O sistema permite criar contas, realizar depósitos, saques e consultar extratos, com validações  e uma interface interativa.

## Funcionalidades

- **Criar Conta**: Criação de contas com nome, CPF, senha, data de nascimento, endereço e saldo inicial.
- **Depositar**: Realizar depósitos em contas próprias ou de terceiros.
- **Sacar**: Realizar saques de contas autenticadas, respeitando o limite diário de saques.
- **Consultar Extrato**: Exibir o saldo e o histórico de transações de uma conta autenticada.

## Estrutura do Projeto

- `main.py`: Arquivo principal que executa o loop interativo do sistema.
- `view/visualizacao.py`: Contém a interface de interação com o usuário.
- `models/cliente.py`: Define a classe Cliente e valida os dados do cliente.
- `models/agencia_conta.py`: Define as classes para gerenciar contas e agências, incluindo operações como criar conta, login, depósito, saque e extrato.
- `controller/banco_controler.py`: Contém validações de dados e regras de negócio.
- `data/conexao_bd.py`: Gerencia a conexão com o banco de dados SQLite e cria a tabela de contas, caso não exista.
- `utils/utilidades.py`: Contém funções utilitárias para manipulação de dados, como conversões de datas, JSON e validações.

## Requisitos

- Python 3.8 ou superior
- Bibliotecas adicionais (instaláveis via `requirements.txt`):
- Execute `pip install -r requirements.txt` para instalar as dependências.

## Como Executar

1. Clone este repositório:
   ```bash
   git clone https://github.com/adilsonssdev/Sistema_Banacrio_DIO
   cd sistema-bancario
   ```

2. Execute o arquivo `main.py`:
   ```bash
   python main.py
   ```

3. Siga as instruções no menu para interagir com o sistema.


### Tabela `contas`:
- `id` (INTEGER): Identificador único da conta.
- `agencia` (TEXT): Número da agência, padrão "0001".
- `nome` (TEXT): Nome do titular da conta.
- `senha` (TEXT): Senha da conta.
- `saldo` (REAL): Saldo atual da conta.
- `saques_dia` (INTEGER): Contador de saques diários.
- `data_nascimento` (TEXT): Data de nascimento do titular da conta.
- `cpf` (TEXT): CPF do titular da conta (único).
- `endereco` (TEXT): Endereço do titular da conta.
- `historico` (TEXT): Histórico de transações da conta (armazenado em formato JSON).

## Observações

- O sistema possui validações para garantir a integridade dos dados, como validação de CPF, senha e limites de saque.
- O histórico de transações é armazenado em formato JSON e exibido como tabela para facilitar a visualização.
- Limite diário de saques: 5 saques por dia.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Desafio
> Este projeto foi um desafio de BootCamp Suzano/Dio
