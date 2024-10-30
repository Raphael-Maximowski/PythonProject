import pandas as pd
import os
import random as rd
import datetime
import time


# Configuração para não mostrar informações de resumo
pd.set_option('display.show_dimensions', False)


def limpar_terminal():
    # Verifica o sistema operacional
    if os.name == 'nt':  # Para Windows
        os.system('cls')
    else:  # Para Mac e Linux
        os.system('clear')


def pausar():
    input("Pressione Enter para continuar...")


class Usuario:
    def __init__(self, nome, email, cpf, password, typeUser):
        self.nome = nome
        self.email = email
        self.cpf = cpf
        self.password = password
        self.typeUser = typeUser


class GerenciamentoUser:
    def __init__(self):
        self.bancoDadosUsers = self.carregarUsuario()  # Carrega os usuários na inicialização

    def carregarUsuario(self):
        try:
            # Tenta carregar os dados do arquivo Excel
            tabelaUsers_df = pd.read_excel('users.xlsx')

            # Converte as linhas do DataFrame em objetos Usuario
            usuarios = [
                Usuario(
                    row['Nome'], row['Email'], row['CPF'], row['Password'], row['typeUser']
                )
                for index, row in tabelaUsers_df.iterrows()
            ]
        except FileNotFoundError:
            # Se o arquivo não existir, retorna uma lista vazia
            usuarios = []

        return usuarios

    def cadastroUsuario(self, nome, email, cpf, password, typeUser="user"):
        # Cria uma nova instância de Usuario
        novoUser = Usuario(nome, email, cpf, password, typeUser)

        # Adiciona o novo usuário à lista carregada anteriormente
        self.bancoDadosUsers.append(novoUser)

        # Salva a lista atualizada de usuários
        self.salvarUsuario()

    def cadastroAdmin(self, nome, email, cpf, password, typeUser="adm"):
        novoUser = Usuario(nome, email, cpf, password, typeUser)
        self.bancoDadosUsers.append(novoUser)
        self.salvarUsuario()

    def salvarUsuario(self):
        # Converte as instâncias de Usuario de volta para um formato que o pandas pode salvar
        userList = self.bancoDadosUsers

        # Cria uma lista de dicionários, onde cada dicionário representa um usuário
        dados = [{
            'Nome': user.nome,
            'Email': user.email,
            'CPF': user.cpf,
            'Password': user.password,
            'typeUser': user.typeUser
        } for user in userList]

        # Cria um DataFrame com esses dados
        bancoDeDadosAuxiliar_df = pd.DataFrame(dados)

        # Salva o DataFrame no arquivo Excel
        bancoDeDadosAuxiliar_df.to_excel("users.xlsx", index=False)


class Validador:
    def __init__(self, gerenciador, admin):
        self.gerenciador = gerenciador  # Referência ao gerenciador de usuários
        self.admin = admin

    def validar_cadastro(self, nome_input, email_input, cpf_input, password_input, admin):
        # Verifica CPF
        for cpf in [user.cpf for user in self.gerenciador.bancoDadosUsers]:
            if cpf == cpf_input:
                return f"Já existe um usuário com este CPF: {cpf_input}"

        # Verifica Email
        for email in [user.email for user in self.gerenciador.bancoDadosUsers]:
            if email == email_input:
                return f"Email já existente: {email_input}"

        if admin:
            self.gerenciador.cadastroAdmin(nome_input, email_input, cpf_input, password_input)
            return "Admin Cadastrado com sucesso! Realize o Login"

        self.gerenciador.cadastroUsuario(nome_input, email_input, cpf_input, password_input)

        return "Usuário cadastrado com sucesso!"

    def validar_login(self, email_user, password_user):

        email_user = email_user.strip().lower()
        password_user = password_user.strip()

        # Converte os dados de todos os usuários em um DataFrame
        tabelaUsers_df = pd.DataFrame([{
            'Nome': user.nome,
            'Email': user.email,
            'CPF': user.cpf,
            'Password': user.password,
            'typeUser': user.typeUser
        } for user in self.gerenciador.bancoDadosUsers])

        # Verifica se o email e a senha coincidem
        VerificaUser = tabelaUsers_df[
            (tabelaUsers_df['Email'] == email_user) & (tabelaUsers_df['Password'] == password_user)
            ]

        if not VerificaUser.empty:
            return True
        else:
            return False


class Estoque:
    def __init__(self, caminho_arquivo):
        self.tabelaProdutos_df = pd.read_excel(caminho_arquivo)
        self.caminho = caminho_arquivo

    def carregarEstoque(self):
        return self.tabelaProdutos_df

    def atualizarEstoque(self):
        # Salva o DataFrame atualizado no arquivo Excel
        self.tabelaProdutos_df.to_excel(self.caminho, index=False)


class HistoricoVendas:
    def __init__(self):
        self.vendas = []  # Aqui vai ficar armazenado os dic que contém os dados da venda

    def registrarVenda(self, itens, total):
        data_venda = datetime.datetime.now()

        # Assegura que o total seja numérico
        if total is None:
            total = 0.0

        venda = {
            "data_hora": data_venda,
            "itens": itens,
            "total": total  # Usa 'valor' como chave para manter consistência
        }

        self.vendas.append(venda)
        self.salvarNoArquivoExcel()

    def exibir_historico(self):

        if not self.vendas:
            print("Nenhuma venda registrada no histórico.")
            return

        for venda in self.vendas:
            print(f"\nData da Venda: {venda['data_hora']}")
            print("Itens:")
            for item in venda['itens']:
                print(
                    f"- {item['produto']['Produto']} (Código: {item['produto']['Code']}) - Quantidade: {item['quantidade']} - Valor Unitário: R${item['produto']['Valor']:.2f}")

            # Garantia de que valor seja sempre numérico para evitar erro de formatação
            valor_total = venda['total'] if venda['total'] is not None else 0.0
            print(f"Total da venda: R${valor_total:.2f}")

    def salvarNoArquivoExcel(self):
        dados = []

        for venda in self.vendas:
            for item in venda['itens']:
                produto = item["produto"]

                # Constrói a estrutura de dados para o arquivo Excel
                dados.append({
                    "Data": venda["data_hora"],
                    "Produto": produto["Produto"],
                    "Código": produto["Code"],
                    "Quantidade": item["quantidade"],
                    "Valor Unitário": produto["Valor"],
                    "Total da Venda": venda["total"]
                })

        # Cria um DataFrame e salva em um arquivo Excel
        historico_df = pd.DataFrame(dados)
        historico_df.to_excel("historico_vendas.xlsx", index=False)


class Carrinho:
    def __init__(self):
        self.itens = []

    def adicionar_produto(self, produto, quantidade, estoque):
        # Carrega o estoque atual diretamente do DataFrame em memória
        estoqueAtual = estoque.tabelaProdutos_df
        for index, row in estoqueAtual.iterrows():
            if row['Code'] == produto['Code']:
                if row['Estoque'] <= 0:
                    print(f"Estoque insuficiente! Disponível: {row['Estoque']}")
                    pausar()
                    return
                else:
                    # Converte para dicionário antes de adicionar ao carrinho
                    produto_dict = produto.to_dict() if isinstance(produto, pd.Series) else produto
                    self.itens.append({"produto": produto_dict, "quantidade": quantidade})
                    estoqueAtual.at[index, 'Estoque'] -= quantidade
                    estoque.atualizarEstoque()
                    print(f"{produto_dict['Produto']} adicionado ao carrinho com sucesso!")
                    pausar()
                    return

    def remover_produto(self, codigo_produto, estoque):
        codigo_produto = int(codigo_produto)

        for item in self.itens:

            if item['produto']['Code'] == codigo_produto:

                produto_encontrado = True  # Produto encontrado
                # Aumenta a quantidade no estoque
                estoqueAtual = estoque.carregarEstoque()
                index = estoqueAtual.index[estoqueAtual['Code'] == codigo_produto].tolist()

                if index:
                    # Restaura a quantidade do produto no estoque
                    estoqueAtual.at[index[0], 'Estoque'] += item["quantidade"]
                    estoque.atualizarEstoque()  # Atualiza o arquivo com o novo estoque

                self.itens.remove(item)
                print(f"Produto removido: {item['produto']['Produto']}")
                pausar()
                limpar_terminal()
                return

        if not produto_encontrado:
            print("Produto não encontrado no carrinho.")  # Agora apenas fora do loop

    def comprar(self, historico):
        total = self.exibir_carrinho()
        limpar_terminal()
        if input("Deseja finalizar a compra? (s/n): ").strip().lower() == 's':
            # Registrar a venda no histórico e esvaziar o carrinho
            historico.registrarVenda(self.itens, total)

            self.itens.clear()
            print("Compra realizada com sucesso e registrada no histórico!")
        else:
            print("Compra cancelada.")

    def exibir_carrinho(self):
        # Exibe os itens no carrinho e o total
        if not self.itens:
            print("O carrinho está vazio.")
            pausar()
            return "Vazio"

        print("Itens no carrinho:")
        total = 0
        for item in self.itens:
            code = item["produto"]["Code"]
            produto = item["produto"]
            quantidade = item["quantidade"]
            valor = produto["Valor"] * quantidade
            total += valor
            print(
                f'{code} - {produto["Produto"]} - Quantidade: {quantidade} - Valor unitário: R${produto["Valor"]:.2f}')

        print(f"Total: R${total:.2f}")

        return total


def logicaAdicionarAoCarrinho(df_filtrado, df, carrinho, estoque):
    limpar_terminal()
    print(df_filtrado)

    codeProduto = input("Code: ")  # Busca o produto pelo código

    produto_encontrado = df[df["Code"].astype(str) == codeProduto]

    if produto_encontrado.empty:
        print("Produto não encontrado! Verifique o código e tente novamente.")
        pausar()
        return False

    produto = produto_encontrado.iloc[0]

    try:
        quantidade = int(input("Quantidade: "))
        if quantidade <= 0:
            print("Quantidade inválida! Tente novamente.")
            pausar()
    except ValueError:
        print("Insira uma quantidade válida!")
        pausar()

    limpar_terminal()
    if quantidade > 0:
        carrinho.adicionar_produto(produto, quantidade, estoque)


def pesquisarPorItem(dados, produto):
    df_filtrado = dados[["Code", "Produto", "Categoria", "Estoque", "Valor"]]

    produto_encontrado = df_filtrado[
        (dados["Code"].astype(str) == produto) |
        (dados["Produto"] == produto) |
        (dados["Categoria"] == produto)
        ]

    return produto_encontrado


def sign_in(gerenciador):
    # Entrar
    limpar_terminal()

    print("ENTRAR")
    email_user = input("Email: ").strip().lower()
    password_user = input('Senha: ').strip()

    validador = Validador(gerenciador)
    entrou = validador.validar_login(email_user, password_user)

    if entrou:
        return True
    else:
        return False


def sign_up(gerenciador, admin=False):
    # Cadastro do usuário
    limpar_terminal()

    print("CADASTRO")
    nome_input = input('Nome: ')
    email_input = input('Email: ')
    cpf_input = (input('CPF: '))
    password_input = input('Password: ')

    # Instancia o Validador com o gerenciador de usuários
    validador = Validador(gerenciador, admin)

    # Valida o cadastro
    resultadoValidacao = validador.validar_cadastro(nome_input, email_input, cpf_input, password_input, admin)
    return resultadoValidacao


def main():
    estoque = Estoque("produtos.xlsx")
    gerenciador = GerenciamentoUser()
    carrinho = Carrinho()
    historico = HistoricoVendas()

    while True:

        # Login/Cadastro
        limpar_terminal()

        print("E-COMMERCE")
        print("[ 1 ] Entrar")
        print("[ 2 ] Cadastrar-se")
        print("[ 3 ] Gestor")

        try:
            input_usuario = int(input(': '))
        except ValueError:
            print("Insira um número válido!")
            pausar()
            continue

        if input_usuario == 1:  # Caso entrada de usuário seja um

            num_tentativas_restantes = 3

            while num_tentativas_restantes > 0:

                usuarioEntrou = sign_in(gerenciador)  # Retorna True para usuário existente e False para não existente

                if usuarioEntrou:  # Caso seja True

                    while True:
                        limpar_terminal()
                        print("ESTOQUE COMPLETO:")
                        estoque = Estoque("produtos.xlsx")
                        df = estoque.carregarEstoque()
                        df_filtrado = df[["Code", "Produto", "Descricao", "Estoque", "Valor"]]

                        print(df_filtrado)

                        print(
                            "\n[ 1 ] Adiconar ao carrinho [ 2 ] Filtrar por item [ 3 ] Exibir carrinho [ 4 ] Histórico de compras [ 5 ] Sair")

                        try:
                            escolha_userProduto = int(input(": "))
                        except ValueError:
                            print("Insira um número válido!")
                            pausar()
                            continue

                        if escolha_userProduto == 1:  # Carrinho
                            logicaAdicionarAoCarrinho(df_filtrado, df, carrinho, estoque)
                            # opção de comprar o carrinho de compras
                        elif escolha_userProduto == 2:

                            while True:

                                limpar_terminal()
                                contagemItensCategoria = df[["Categoria"]].value_counts()

                                for categoria, quantidade in contagemItensCategoria.items():
                                    print(f"[ {quantidade} ] {categoria[0]}")

                                codeProduto = input("categoria: ").capitalize()  # Busca o produto pelo código

                                item = pesquisarPorItem(df, codeProduto)

                                if not item.empty:

                                    limpar_terminal()
                                    print(item)
                                    print("[ 1 ] Adicionar ao carrinho  [ 2 ] Voltar")

                                else:
                                    limpar_terminal()
                                    print("Categoria não encontrado!")
                                    pausar()
                                    continue

                                try:
                                    input_user = int(input(": "))
                                except ValueError:
                                    print("Insira um número válido!")
                                    pausar()
                                    continue

                                if input_user == 1:
                                    while True:

                                        logicaAdicionarAoCarrinho(item, df, carrinho, estoque)

                                        # Pergunta se deseja continuar
                                        continuar = input(
                                            "Deseja adicionar outro item ao carrinho? (s/n): ").strip().lower()
                                        if continuar != 's':
                                            voltar_estoque = True  # Marca para voltar ao estoque completo
                                            break  # Sai do loop de adicionar ao carrinho

                                elif input_user == 2:
                                    break
                                else:
                                    limpar_terminal()
                                    print("Digite uma opção válida!")
                                    pausar()
                                    continue

                                if voltar_estoque == True:
                                    break

                        elif escolha_userProduto == 3:
                            limpar_terminal()
                            carrinhoExibir = carrinho.exibir_carrinho()

                            if carrinhoExibir != "Vazio":
                                print("[ 1 ] Remover Produto [ 2 ] Comprar Carrinho [ 3 ] Voltar")

                                escolha = int(input(": "))

                                if escolha == 1:
                                    code_produto = str(input("Code: "))
                                    carrinho.remover_produto(code_produto, estoque)

                                elif escolha == 2:
                                    carrinho.comprar(historico)
                                    pausar()

                        elif escolha_userProduto == 4:
                            limpar_terminal()
                            historico.exibir_historico()
                            pausar()

                        elif escolha_userProduto == 5:
                            limpar_terminal()
                            print("Saindo...")
                            pausar()
                            breakadmin

                        else:
                            limpar_terminal()
                            print("Essa escolha não existe!")
                            pausar()
                            continue  # Volta para menu estoque

                else:  # Caso entrada seja Falsa
                    num_tentativas_restantes -= 1  # Decrementa um a cada tentativas
                    limpar_terminal()
                    print("Email ou senha incorretos. Tente novamente!")
                    print(f"{num_tentativas_restantes} tentativas restantes")
                    pausar()

        elif input_usuario == 2:  # Caso usuário escolha a opção cadastrar-se
            validacaoCadastro = sign_up(gerenciador)
            print(validacaoCadastro)
            pausar()
            continue

        elif input_usuario == 3:

            while True:

                limpar_terminal()

                print("Seja bem vindo Gestor!!\n")
                print("===================================")
                print("[1] Login")
                print("[2] Cadastro")
                print("[3] Retornar")
                print("===================================")
                gestor_input = int(input("Insira sua escolha: "))

                if gestor_input == 1:
                    

                if gestor_input == 2:
                    validacaoCadastro = sign_up(gerenciador, True)
                    limpar_terminal()
                    print(validacaoCadastro, "\n")
                    time.sleep(5)
                    limpar_terminal()

                if gestor_input == 3:
                    break

        else:
            print("Opção indisponível no momento!")
            pausar()
            continue


main()
