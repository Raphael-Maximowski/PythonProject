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

    def validar_login(self, email_user, password_user, admin):

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

        VerificaUser = ''

        if admin:
            # Caso seja um administrador
            VerificaUser = tabelaUsers_df[
                (tabelaUsers_df['Email'] == email_user) &
                (tabelaUsers_df['Password'] == password_user) &
                (tabelaUsers_df['typeUser'] == 'adm')
                ]
        else:
            # Caso seja um usuário comum
            VerificaUser = tabelaUsers_df[
                (tabelaUsers_df['Email'] == email_user) &
                (tabelaUsers_df['Password'] == password_user)
                ]

        if not VerificaUser.empty:
            return True
        else:
            return False

def WrongInput():
    limpar_terminal()
    print("Insira uma opção válida!")
    pausar()
    limpar_terminal()

class Transportadora:
    def __init__(self, name, loc_central, cnpj):
        self.name = name
        self.loc_central = loc_central
        self.cnpj = cnpj

    def CreateTransportadora(self):
        data = ([{
            "Nome": self.name,
            "Loc_Central": self.loc_central,
            "CNPJ": self.cnpj
        }])

        transportadora = pd.DataFrame(data)
        transportadoras = pd.read_excel('transportadora.xlsx')
        transportadoras = pd.concat([transportadoras, transportadora], ignore_index=True)
        transportadoras.to_excel("transportadora.xlsx")

    @staticmethod
    def LerTransportadora():
        return pd.read_excel("transportadora.xlsx")


def DeleteTransportadora(deleteName):
    df = pd.read_excel("transportadora.xlsx")
    existe = (df["Nome"] == deleteName).any()

    if existe:
        name = deleteName
        df = df[df["Nome"] != name]
        df.to_excel("transportadora.xlsx", index=False)
        print("Fornecedor Removido")
        return "Fornecedor Removido"

    else:
        print("Fornecedor Não Encontrado")
        return


class Fornecedores:
    def __init__(self, fornecedor_name=None, fornecedor_loc=None, fornecedor_cnpj=None, fornecedor_nicho=None,
                 deleteName=None):
        self.fornecedor_name = fornecedor_name
        self.fornecedor_loc = fornecedor_loc
        self.fornecedor_cnpj = fornecedor_cnpj
        self.fornecedor_nicho = fornecedor_nicho

    @staticmethod
    def LerFornecedores():
        return pd.read_excel("fornecedor.xlsx")

    def CadastroFornecedor(self):
        data = {
            "Nome": [self.fornecedor_name],
            "Loc": [self.fornecedor_loc],
            "CNPJ": [self.fornecedor_cnpj],
            "Nicho": [self.fornecedor_nicho]
        }

        fornecedor = pd.DataFrame(data)
        fornecedores = pd.read_excel("fornecedor.xlsx")
        fornecedores = pd.concat([fornecedores, fornecedor], ignore_index=True)
        fornecedores.to_excel("fornecedor.xlsx", index=False)

        return "Fornecedor Adicionado"


def DeleteFornecedor(deleteName):
    df = pd.read_excel("fornecedor.xlsx")

    existe = (df["Nome"] == deleteName).any()

    if existe:
        name = deleteName
        df = df[df["Nome"] != name]
        df.to_excel("fornecedor.xlsx", index=False)
        print("Fornecedor Removido")
        return

    else:
        print("Fornecedor Não Encontrado")
        return


def ReceberFeedbacks():
    return pd.read_excel("feedbacks.xlsx")


def VerVendas():
    return pd.read_excel("historico_vendas.xlsx")


def VerFaturamento():
    df = pd.read_excel("historico_vendas.xlsx")
    col = df["Total da Venda"]
    faturamento_lista = col.tolist()
    return faturamento_lista


class ManipularProdutos:
    def __init__(self, Code, Produto, Categoria, Descricao, Custo, Valor, Estoque):
        self.Code = Code
        self.Produto = Produto
        self.Categoria = Categoria
        self.Descricao = Descricao
        self.Custo = Custo
        self.Valor = Valor
        self.Estoque = Estoque

    @staticmethod
    def editProduto(code):
        df = pd.read_excel("produtos.xlsx")
        product = df[df["Code"] == code].values.tolist()
        product_index = df[df["Code"] == code].index
        keys = [ "Code", "Produto", "Categoria", "Descricao", "Custo", "Valor", "Lucro", "Estoque" ]
        editInput = 1000
        limpar_terminal()

        while editInput != 9:
            print("===========================================")
            for x in range(len(keys)):
                print(f'[{x + 1}] {keys[x]}: {product[0][x]}')
            print('[9] Salvar: ')
            print("===========================================")
            editInput = int(input('Insira sua qual campo deseja editar: '))
            limpar_terminal()
            if editInput != 9:
                newValue = input(f"Insira o novo valor do produto {product[0][1]} no campo {keys[editInput - 1]}: ")
                product[0][editInput - 1] = newValue

        df.loc[product_index[0], keys] = product[0]
        df.to_excel("produtos.xlsx", index=False)
        pausar()

    def createProduto(self):
        lucro = int(self.Valor) - int(self.Custo)

        produto = [{
            "Code": self.Code,
            "Produto": self.Produto,
            "Categoria": self.Categoria,
            "Descricao": self.Descricao,
            "Custo": self.Custo,
            "Valor": self.Valor,
            "Lucro": lucro,
            "Estoque": self.Estoque
        }]

        df = pd.DataFrame(produto)
        produtos = pd.read_excel("produtos.xlsx")
        new_produtos = pd.concat([produtos, df], ignore_index=True)
        new_produtos.to_excel("produtos.xlsx", index=False)

    @staticmethod
    def loadProdutos():
        return pd.read_excel("produtos.xlsx")

    @staticmethod
    def deleteProduto(name):
        df = pd.read_excel("produtos.xlsx")

        existe = (df["Produto"] == name).any()

        if existe:
            productname = name
            df = df[df["Produto"] != productname]
            df.to_excel("produtos.xlsx", index=False)
            print("Produto Excluido")
            return

        else:
            print("Produto Não Encontrado")




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
        
        itens_carrinho = []
        
        for item in itens:
            
            itens_carrinho.append(item)
            
        # Assegura que o total seja numérico
        if total is None:
            total = 0.0

        venda = {
            "data_hora": data_venda,
            "itens": itens_carrinho,
            "total": total  # Usa 'valor' como chave para manter consistência
        }

        self.vendas.append(venda)
        self.salvarNoArquivoExcel()

    def exibir_historico(self):

        if not self.vendas:
            print("Nenhuma venda registrada no histórico.")
            return

        historico_vendas_df = pd.read_excel('historico_vendas.xlsx')
        
        print(historico_vendas_df)

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
        
# Function para feedback da compra
def feedbackCompra(itens_carrinho, nome_usuario):
    feedbackValue = input("Feedback: ")

    # Supondo que `usuarioLogado` contém o nome do usuário
    usuario = nome_usuario

    # Extrai o nome do produto do primeiro item do carrinho como exemplo
    nome_produto = itens_carrinho[0]['produto']["Produto"]

    # Cria o dicionário com o feedback
    feedback = {
        "Comprador": usuario,
        "Produto": nome_produto,
        "Feedback": feedbackValue,
    }

    # Passa o dicionário como uma lista de um único elemento
    feedback_df = pd.DataFrame([feedback])

    # Adiciona ou salva no arquivo Excel
    try:
        feedbacks_existentes = pd.read_excel('feedbacks.xlsx')
        feedback_df = pd.concat([feedbacks_existentes, feedback_df], ignore_index=True)
    except FileNotFoundError:
        pass

    feedback_df.to_excel('feedbacks.xlsx', index=False)
    print("Feedback registrado com sucesso!")

def encontrarUsuario(usuarioLogado):
    
    df = pd.read_excel("users.xlsx")
    
    nome_usuario = df[df["Email"] == usuarioLogado]
    
    nome_user = 'aaaaa'
    
    for item, value in nome_usuario.iterrows():
        nome_user = value["Nome"]
        
    return nome_user
        
class Carrinho:
    def __init__(self):
        self.itens = []

    def adicionar_produto(self, produto, quantidade, estoque):
        # Carrega o estoque atual diretamente do DataFrame em memória
        estoqueAtual = estoque.tabelaProdutos_df
        
        for index, row in estoqueAtual.iterrows():
            if row['Code'] == produto['Code']:
                if row['Estoque'] < quantidade:
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

    def comprar(self, historico, usuarioLogado):
        total = self.exibir_carrinho()
        limpar_terminal()
        if input("Deseja finalizar a compra? (s/n): ").strip().lower() == 's':
            # Registrar a venda no histórico e esvaziar o carrinho
            historico.registrarVenda(self.itens, total)
            
            nome_usuario = encontrarUsuario(usuarioLogado)
            
            feedbackCompra(self.itens, nome_usuario)

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


def sign_in(gerenciador, admin=False):
    # Entrar
    limpar_terminal()

    print("ENTRAR")
    email_user = input("Email: ").strip().lower()
    password_user = input('Senha: ').strip()

    validador = Validador(gerenciador, admin)
    entrou = validador.validar_login(email_user, password_user, admin)

    if entrou:
        return email_user
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
        num_tentativas_restantes = 4

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

            while num_tentativas_restantes > 0:

                usuario = sign_in(gerenciador)  # Retorna o usuário se ele
                
                if usuario != False: # Caso seja diferente de false
                    

                    while True:
                        limpar_terminal()
                        print("ESTOQUE COMPLETO:")
                        estoque = Estoque("produtos.xlsx")
                        df = estoque.carregarEstoque()
                        df_filtrado = df[["Code", "Produto", "Descricao", "Estoque", "Valor"]]

                        print(df_filtrado)

                        print(
                            "\n[ 1 ] Adiconar ao carrinho [ 2 ]Filtrar por categoria [ 3 ] Comprar [ 4 ] Histórico de compras [ 5 ] Sair")

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
                                print("[ 1 ] Remover Produto [ 2 ] Finalizar compra [ 3 ] Voltar")

                                escolha = int(input(": "))

                                if escolha == 1:
                                    code_produto = str(input("Code: "))
                                    carrinho.remover_produto(code_produto, estoque)

                                elif escolha == 2:
                                    carrinho.comprar(historico, usuario)
                                    pausar()

                        elif escolha_userProduto == 4:
                            limpar_terminal()
                            historico.exibir_historico()
                            pausar()

                        elif escolha_userProduto == 5:
                            limpar_terminal()
                            break

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
            
                    continue
                
                break
            
            if num_tentativas_restantes == 0:
                        limpar_terminal()
                        print("Saindo...")
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
                print("[1] LOGIN")
                print("[2] CADASTRO")
                print("[3] RETORNAR\n")

                try:

                    gestor_input = int(input("Insira sua escolha: "))


                    if gestor_input == 1:
                        usuarioEntrou = sign_in(gerenciador, True)

                        if usuarioEntrou == True:

                            gestor_function = 0

                            while gestor_function != 6:

                                limpar_terminal()
                                print("Funções disponíveis: ")
                                print("===================================")
                                print("[1] Gerenciar Estoque")
                                print("[2] Gerenciar Vendas")
                                print("[3] Fornecedores")
                                print("[4] Transportadoras")
                                print("[5] Avaliações")
                                print("[6] Retornar")
                                print("===================================")

                                try:

                                    gestor_function = int(input("Insira sua escolha: "))
                                    limpar_terminal()

                                    if gestor_function == 1:

                                        estoque_function = 1000

                                        while estoque_function != 4:
                                            print(
                                                "=====================================================================================================================================================================")
                                            df = ManipularProdutos.loadProdutos()
                                            print(df)
                                            print(
                                                "=====================================================================================================================================================================")
                                            print(
                                                "[1] Adicionar Produto \n[2] Remover Produto \n[3] Editar Produto \n[4] Retornar")

                                            try:
                                                estoque_function = int(input("Insira sua escolha: "))
                                                limpar_terminal()

                                                if estoque_function == 1:
                                                    print("Cadastrando Novo Produto: ")
                                                    print("=====================================================")
                                                    code = input("Insira o código do Produto: ")
                                                    produto = input("Insira o nome do produto: ")
                                                    categoria = input("Insira o categoria do produto: ")
                                                    descricao = input("Insira a descrição do produto: ")
                                                    custo = input("Insira o custo: ")
                                                    valor = input("Insira o valor: ")
                                                    estoque = input("Insira a quantidade em estoque: ")
                                                    print("=====================================================")
                                                    newProduct = ManipularProdutos(code, produto, categoria, descricao, custo, valor, estoque)
                                                    newProduct.createProduto()

                                                    limpar_terminal()
                                                    print("Produto Cadastrado ...")
                                                    time.sleep(5)
                                                    limpar_terminal()

                                                elif estoque_function == 2:
                                                    print(
                                                        "=====================================================================================================================================================================")
                                                    name = input("Insira o nome do produto a ser Deletado: ")
                                                    limpar_terminal()
                                                    ManipularProdutos.deleteProduto(name)
                                                    time.sleep(5)
                                                    limpar_terminal()

                                                elif estoque_function == 3:
                                                    code = int(input("Insira o código do Produto: "))
                                                    ManipularProdutos.editProduto(code)

                                                elif estoque_function > 4 or estoque_function < 1:
                                                    WrongInput()

                                            except ValueError:
                                                WrongInput()

                                    elif gestor_function == 2:

                                        vendas_action = 999

                                        while vendas_action != 3:
                                            limpar_terminal()
                                            print("===================================")
                                            print("[1] Histórico de Vendas")
                                            print("[2] Faturamento Total")
                                            print("[3] Retornar")
                                            print("===================================")

                                            try:
                                                vendas_action = int(input("Insira sua escolha: "))
                                                limpar_terminal()

                                                if vendas_action == 1:
                                                    print(
                                                        "============================================================================")
                                                    df = VerVendas()
                                                    df_filtrado = df[
                                                        ["Data", "Produto", "Código", "Valor Unitário", "Total da Venda"]]
                                                    print(df_filtrado)
                                                    print(
                                                        "============================================================================")
                                                    pausar()

                                                elif vendas_action == 2:
                                                    faturamento = VerFaturamento()
                                                    total = 0
                                                    for x in range(len(faturamento)):
                                                        total += faturamento[x]

                                                    print(
                                                        "============================================================================")
                                                    df = VerVendas()
                                                    df_filtrado = df[["Produto", "Valor Unitário", "Total da Venda"]]
                                                    print(df_filtrado)
                                                    print(
                                                        "============================================================================")
                                                    print("FATURAMENTO TOTAL: R$", total)
                                                    print(
                                                        "============================================================================")
                                                    pausar()

                                                elif vendas_action > 3 or vendas_action < 1:
                                                    WrongInput()

                                            except ValueError:
                                                WrongInput()


                                    elif gestor_function == 3:

                                        fornecedor_action = 999

                                        while fornecedor_action != 3:
                                            print(
                                                "============================================================================")
                                            df = Fornecedores.LerFornecedores()
                                            df_filtrado = df[["Nome", "Loc", "CNPJ", "Nicho"]]
                                            print(df_filtrado)
                                            print(
                                                "============================================================================")
                                            print("[1] Adicionar Fornecedor        [2] Remover Fornecedor        [3] Retornar")

                                            try:
                                                fornecedor_action = int(input("Insira sua escolha: "))

                                                if fornecedor_action == 1:
                                                    name = (input("Insira o nome do Fornecedor: "))
                                                    loc = (input("Insira a localização do Fornecedor: "))
                                                    cnpj = (input("Insira o CNPJ do Fornecedor: "))
                                                    nicho = (input("Insira o nicho do Fornecedor: "))

                                                    fornecedor = Fornecedores(name, loc, cnpj, nicho)
                                                    fornecedor.CadastroFornecedor()

                                                    limpar_terminal()
                                                    print("Fornecedor Cadastrado com Sucesso!")
                                                    time.sleep(5)
                                                    limpar_terminal()

                                                elif fornecedor_action == 2:
                                                    name = (input("Insira o nome do Fornecedor a ser Excluido: "))

                                                    limpar_terminal()
                                                    DeleteFornecedor(name)
                                                    time.sleep(5)
                                                    limpar_terminal()

                                                elif fornecedor_action > 3 or fornecedor_action < 1:
                                                    WrongInput()

                                            except ValueError:
                                                WrongInput()

                                    elif gestor_function == 4:
                                        transportadora_action = 999

                                        while transportadora_action != 3:
                                            print(
                                                "============================================================================")
                                            df = Transportadora.LerTransportadora()
                                            df_filtrado = df[["Nome", "Loc_Central", "CNPJ"]]
                                            print(df_filtrado)
                                            print(
                                                "============================================================================")
                                            print(
                                                "[1] Adicionar Transportadora        [2] Remover Transportadora        [3] Retornar")

                                            try:
                                                transportadora_action = int(input("Insira sua escolha: "))

                                                if transportadora_action == 1:
                                                    name = (input("Insira o nome do Fornecedor: "))
                                                    loc = (input("Insira a localização do Fornecedor: "))
                                                    cnpj = (input("Insira o CNPJ do Fornecedor: "))

                                                    transportadora = Transportadora(name, loc, cnpj)
                                                    transportadora.CreateTransportadora()

                                                    limpar_terminal()
                                                    print("Transportadora Cadastrado com Sucesso!")
                                                    time.sleep(5)
                                                    limpar_terminal()

                                                elif transportadora_action == 2:
                                                    name = (input("Insira o nome da Transportadora a ser Excluido: "))

                                                    limpar_terminal()
                                                    DeleteTransportadora(name)
                                                    time.sleep(5)
                                                    limpar_terminal()

                                                elif transportadora_action > 3 or transportadora_action < 1:
                                                    WrongInput()

                                            except ValueError:
                                                WrongInput()  # Chama a função se a entrada não for um número válido

                                    elif gestor_function == 5:
                                        feedbacks = ReceberFeedbacks()
                                        print(
                                            "=====================================================================================================================")
                                        print(feedbacks)
                                        print(
                                            "=====================================================================================================================")
                                        pausar()

                                    elif gestor_function < 1 or gestor_function > 6:
                                        WrongInput()

                                except ValueError:
                                    WrongInput()

                        else:
                            limpar_terminal()
                            print("Login Incorreto \nSe achar que é uma falha do sistema contate o suporte")
                            pausar()
                            limpar_terminal()

                    elif gestor_input == 2:
                        validacaoCadastro = sign_up(gerenciador, True)
                        limpar_terminal()
                        print(validacaoCadastro, "\n")
                        time.sleep(5)
                        limpar_terminal()

                    elif gestor_input == 3:
                        break

                    elif gestor_input < 1 or gestor_input > 3:
                        WrongInput()

                except ValueError:
                    WrongInput()


        else:
            print("Opção indisponível no momento!")
            pausar()
            continue


main()
