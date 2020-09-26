from tkinter import *
import pymysql
from tkinter import messagebox, ttk


class AdminJanela:

    def cadastrar_produto(self):
        self.cadastrar = Tk()
        self.cadastrar.title('Cadastro de produtos')
        self.cadastrar['bg'] = '#dddddd'

        Label(self.cadastrar, text='Cadastre os produtos', bg='#dddddd', fg='black').grid(row=0, column=0, columnspan=4, padx=5, pady=5)

        Label(self.cadastrar, text='Nome', bg='#dddddd', fg='black').grid(row=1, column=0, columnspan=1, padx=5, pady=5)
        self.nome = Entry(self.cadastrar)
        self.nome.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

        Label(self.cadastrar, text='Ingredientes', bg='#dddddd', fg='black').grid(row=2, column=0, columnspan=1, padx=5, pady=5)
        self.ingredientes = Entry(self.cadastrar)
        self.ingredientes.grid(row=2, column=1, columnspan=2, padx=5, pady=5)

        Label(self.cadastrar, text='Grupo', bg='#dddddd', fg='black').grid(row=3, column=0, columnspan=1, padx=5, pady=5)
        self.grupo = Entry(self.cadastrar)
        self.grupo.grid(row=3, column=1, columnspan=2, padx=5, pady=5)

        Label(self.cadastrar, text='Preço', bg='#dddddd', fg='black').grid(row=4, column=0, columnspan=1, padx=5, pady=5)
        self.preco = Entry(self.cadastrar)
        self.preco.grid(row=4, column=1, columnspan=2, padx=5, pady=5)

        Button(self.cadastrar, text='Cadastrar', width=15, bg='green3', relief='flat', highlightbackground='#dddddd', command=self.cadastrar_produtos_backend).grid(row=5, column=0, padx=5, pady=5)
        Button(self.cadastrar, text='Excluir', width=15, bg='gray', relief='flat', highlightbackground='#dddddd', command=self.remover_cadastros_backend).grid(row=5, column=1, padx=5, pady=5)
        Button(self.cadastrar, text='Atualizar', width=15, bg='green3', relief='flat', highlightbackground='#dddddd', command=self.mostrar_produto_backend).grid(row=6, column=0, padx=5, pady=5)
        Button(self.cadastrar, text='Limpar Produtos', width=15, bg='gray', relief='flat', highlightbackground='#dddddd', command=self.limpar_cadastros_backend).grid(row=6, column=1, padx=5, pady=5)

        self.tree = ttk.Treeview(self.cadastrar, selectmode='browse', column=('coluna1', 'coluna2', 'coluna3', 'coluna4'),
                                 show='headings')

        self.tree.column('coluna1', width=200, minwidth=500, stretch=NO)
        self.tree.heading('#1', text='nome')

        self.tree.column('coluna2', width=400, minwidth=500, stretch=NO)
        self.tree.heading('#2', text='ingredientes')

        self.tree.column('coluna3', width=200, minwidth=500, stretch=NO)
        self.tree.heading('#3', text='grupo')

        self.tree.column('coluna4', width=60, minwidth=500, stretch=NO)
        self.tree.heading('#4', text='preco')

        self.tree.grid(row=0, column=4, padx=10, pady=10, columnspan=3, rowspan=6)

        self.mostrar_produto_backend()

        self.cadastrar.mainloop()

    def __init__(self):
        self.root = Tk()
        self.root.title('ADMIN')

        Button(self.root, text='Pedidos', width=20, bg='#69CB15').grid(row=0, column=0, padx=10, pady=10)
        Button(self.root, text='Cadastros', width=20, bg='#485A88', command=self.cadastrar_produto).grid(row=1, column=0, padx=10, pady=10)

        self.root.mainloop()

    def mostrar_produto_backend(self):
        try:
            conexao = pymysql.connect(

                host='localhost',
                user='Vitor',
                password='vitor1230',
                db='erp',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except:
            print('erro ao conectar ao banco de dados')

        try:
            with conexao.cursor() as cursor:
                cursor.execute('SELECT * FROM produtos')
                resultados = cursor.fetchall()

        except:
            print('erro ao fazer consulta')

        self.tree.delete(*self.tree.get_children())

        linhaV = []

        for linha in resultados:
            linhaV.append(linha['nome'])
            linhaV.append(linha['ingredientes'])
            linhaV.append(linha['grupo'])
            linhaV.append(linha['preco'])

            self.tree.insert('', END, values=linhaV, iid=linha['id'], tag='1')

            linhaV.clear()

    def cadastrar_produtos_backend(self):
        nome = self.nome.get()
        ingredientes = self.ingredientes.get()
        grupo = self.grupo.get()
        preco = self.preco.get()

        try:
            conexao = pymysql.connect(

                host='localhost',
                user='Vitor',
                password='vitor1230',
                db='erp',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except:
            print('erro ao conectar ao banco de dados')

        try:
            with conexao.cursor() as cursor:
                cursor.execute(f'INSERT INTO produtos(nome, ingredientes, grupo, preco) VALUES {nome, ingredientes, grupo, preco}')
                conexao.commit()

        except:
            print('erro ao fazer consulta')

        self.mostrar_produto_backend()

    def remover_cadastros_backend(self):
        id_deletar = int(self.tree.selection()[0])
        try:
            conexao = pymysql.connect(

                host='localhost',
                user='Vitor',
                password='vitor1230',
                db='erp',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except:
            print('erro ao conectar ao banco de dados')

        try:
            with conexao.cursor() as cursor:
                cursor.execute(f'DELETE FROM produtos WHERE id = {id_deletar}')
                conexao.commit()

        except:
            print('erro ao fazer consulta')

        self.mostrar_produto_backend()

    def limpar_cadastros_backend(self):
        if messagebox.askokcancel('Limpar dados CUIDADO!!!', 'Deseja realmente limpar todos os dados?'):
            try:
                conexao = pymysql.connect(

                    host='localhost',
                    user='Vitor',
                    password='vitor1230',
                    db='erp',
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor
                )
            except:
                print('erro ao conectar ao banco de dados')

            try:
                with conexao.cursor() as cursor:
                    cursor.execute('TRUNCATE TABLE produtos')
                    conexao.commit()

            except:
                print('erro ao fazer consulta')

            self.mostrar_produto_backend()

class JanelaLogin:

    def verifica_login(self):
        autenticado = False
        usuario_master = False

        try:
            conexao = pymysql.connect(

                host='localhost',
                user='Vitor',
                password='vitor1230',
                db='erp',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except:
            print('erro ao conectar ao banco de dados')

        usuario = self.login.get()
        senha = self.senha.get()
        resultados = ()
        try:
            with conexao.cursor() as cursor:
                cursor.execute('SELECT * FROM cadastros')
                resultados = cursor.fetchall()

        except:
            print('erro ao fazer consulta')

        for linha in resultados:
            if usuario == linha['nome'] and senha == linha['senha']:
                if linha['nivel'] == 1:
                    usuario_master = False
                elif linha['nivel'] == 2:
                    usuario_master = True
                autenticado = True
                break
            else:
                autenticado = False

        if not autenticado:
            messagebox.showinfo('login', 'Email ou Senha inválido')

        if autenticado:
            self.root.destroy()
            if usuario_master:
                AdminJanela()

    def cadastro(self):
        Label(self.root, text='Chave de segurança').grid(row=3, column=0, pady=5, padx=5)
        self.codigo_seguranca = Entry(self.root, show='*')
        self.codigo_seguranca.grid(row=3, column=1, pady=5, padx=10)
        Button(self.root, text='Confirmar cadastro', width=15, bg='blue1', command=self.cadastro_backend).grid(row=4, column=0, columnspan=3, pady=5, padx=10)

    def cadastro_backend(self):
        codigo_padrao = '123@h'

        if self.codigo_seguranca.get() == codigo_padrao:
            if len(self.login.get()) <= 20:
                if len(self.senha.get()) <= 50:
                    nome = self.login.get()
                    senha = self.senha.get()

                    try:
                        conexao = pymysql.connect(

                            host='localhost',
                            user='Vitor',
                            password='vitor1230',
                            db='erp',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor
                        )
                    except:
                        print('erro ao conectar ao banco de dados')

                    try:
                        with conexao.cursor() as cursor:
                            cursor.execute(f'INSERT INTO cadastros (nome, senha, nivel) VALUES {nome, senha, 1}')
                            conexao.commit()
                            messagebox.showinfo('Cadastro', 'Usuário cadastrado com sucesso')
                            self.root.destroy()

                    except:
                        print('Erro ao inserir dados')
                else:
                    messagebox.showinfo('ERRO', 'Por favor insira uma SENHA com 50 ou menos caracteres!')
            else:
                messagebox.showinfo('ERRO', 'Por favor insira um NOME com 20 ou menos caracteres!')
        else:
            messagebox.showinfo('ERRO', 'Erro no código de segurança')

    def visualizar_cadastros(self):
        self.vc = Toplevel()
        self.vc.resizable(False, False)
        self.vc.title('Visualizar cadastros')

        self.tree = ttk.Treeview(self.vc, selectmode='browse', column=('coluna1', 'coluna2', 'coluna3', 'coluna4'), show='headings')

        self.tree.column('coluna1', width=40, minwidth=500, stretch=NO)
        self.tree.heading('#1', text='ID')

        self.tree.column('coluna2', width=100, minwidth=500, stretch=NO)
        self.tree.heading('#2', text='Usuario')

        self.tree.column('coluna3', width=100, minwidth=500, stretch=NO)
        self.tree.heading('#3', text='Senha')

        self.tree.column('coluna4', width=40, minwidth=500, stretch=NO)
        self.tree.heading('#4', text='Nível')

        self.tree.grid(row=0, column=0, padx=10, pady=10)

        self.update_backend()

        self.vc.mainloop()

    def update_backend(self):
        try:
            conexao = pymysql.connect(

                host='localhost',
                user='Vitor',
                password='vitor1230',
                db='erp',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except:
            print('erro ao conectar ao banco de dados')

        try:
            with conexao.cursor() as cursor:
                cursor.execute('SELECT * FROM cadastros')
                resultados = cursor.fetchall()
        except:
            print('erro ao fazer consulta')

        self.tree.delete(*self.tree.get_children())

        linhaV = []

        for linha in resultados:
            linhaV.append(linha['id'])
            linhaV.append(linha['nome'])
            linhaV.append(linha['senha'])
            linhaV.append(linha['nivel'])

            self.tree.insert('', END, values=linhaV, iid=linha['id'], tag='1')

            linhaV.clear()

    def __init__(self):
        self.root = Tk()
        self.root.title('Login')
        Label(self.root, text='Faça o login').grid(row=0, column=0, columnspan=2)

        Label(self.root, text='Usuário').grid(row=1, column=0)

        self.login = Entry(self.root)
        self.login.grid(row=1, column=1, padx=5, pady=5)

        Label(self.root, text='Senha').grid(row=2, column=0)

        self.senha = Entry(self.root, show='*')
        self.senha.grid(row=2, column=1, padx=5, pady=5)

        Button(self.root, text='Login', bg='green3', command=self.verifica_login, width=10).grid(row=5, column=0, padx=5, pady=5)

        Button(self.root, text='Cadastrar', bg='orange3', width=10, command=self.cadastro).grid(row=5, column=1, padx=5, pady=5)

        Button(self.root, text='Visualizar Cadastros', bg='white', command=self.visualizar_cadastros).grid(row=6, column=0, columnspan=2, padx=5, pady=5)

        self.root.mainloop()


JanelaLogin()
