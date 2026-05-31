import mysql.connector
from datetime import datetime

# =====================================
# CONEXÃO MYSQL
# =====================================

conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='130807Mm@',
    database='academia_expo'
)

cursor = conexao.cursor(buffered=True)

print('Conectado com sucesso!')

tipo_usuario = ''

# =====================================
# MENU INICIAL
# =====================================

while True:

    print('\n===== BEM-VINDO À BRUTALFIT EXPO =====')
    print('1 - Login ADM')
    print('2 - Login Aluno')
    print('3 - Cadastrar ADM')
    print('4 - Sair')

    escolha = input('Escolha uma opção: ')

    # =====================================
    # LOGIN ADM
    # =====================================

    if escolha == '1':

        usuario = input('Usuário ADM: ')
        senha = input('Senha: ')

        sql = '''
        SELECT *
        FROM tbl_usuarios
        WHERE usuario = %s
        AND senha = %s
        AND tipo = 'ADM'
        '''

        cursor.execute(sql, (usuario, senha))

        resultado = cursor.fetchone()

        if resultado:

            tipo_usuario = 'ADM'

            print('Login ADM realizado!')
            break

        else:

            print('Usuário ou senha inválidos!')

    # =====================================
    # LOGIN ALUNO
    # =====================================

    elif escolha == '2':

        email_login = input('Digite seu e-mail: ')
        senha = input('Digite sua senha: ')

        sql = '''
        SELECT
            tbl_usuarios.usuario,
            tbl_alunos.email

        FROM tbl_usuarios

        INNER JOIN tbl_alunos
            ON tbl_usuarios.usuario = tbl_alunos.nome_aluno

        WHERE tbl_alunos.email = %s
        AND tbl_usuarios.senha = %s
        AND tbl_usuarios.tipo = 'ALUNO'
        '''

        cursor.execute(sql, (email_login, senha))

        resultado = cursor.fetchone()

        if resultado:

            tipo_usuario = 'ALUNO'

            nome_aluno = resultado[0]
            email_aluno = resultado[1]

            print('Login de aluno realizado!')
            break

        else:

            print('Usuário ou senha inválidos!')

    # =====================================
    # CADASTRAR ADM
    # =====================================

    elif escolha == '3':

        usuario = input('Crie um usuário ADM: ')
        senha = input('Crie uma senha: ')

        sql = '''
        INSERT INTO tbl_usuarios
        (usuario, senha, tipo)
        VALUES (%s, %s, %s)
        '''

        cursor.execute(sql, (usuario, senha, 'ADM'))

        conexao.commit()

        print('ADM cadastrado com sucesso!')

    # =====================================
    # SAIR
    # =====================================

    elif escolha == '4':

        print('Sistema encerrado!')
        exit()

    else:

        print('Opção inválida!')

# =====================================
# MENU ALUNO
# =====================================

if tipo_usuario == 'ALUNO':

    while True:

        print('\n===== ÁREA DO ALUNO =====')
        print('1 - Ver meus dados')
        print('2 - Ver mensalidade')
        print('3 - Ver vencimento')
        print('4 - Ver plano')
        print('5 - Ver e-mail')
        print('6 - Atualizar e-mail')
        print('7 - Alterar senha')
        print('8 - Trocar plano')
        print('9 - Cancelar plano')
        print('10 - Ver histórico')
        print('11 - Sair')

        opcao_aluno = input('Escolha: ')

        # =====================================
        # VER DADOS
        # =====================================

        if opcao_aluno == '1':

            sql = '''
            SELECT
                nome_aluno,
                idade,
                telefone

            FROM tbl_alunos

            WHERE nome_aluno = %s
            '''

            cursor.execute(sql, (nome_aluno,))

            dados = cursor.fetchone()

            if dados:

                print(f'Nome: {dados[0]}')
                print(f'Idade: {dados[1]}')
                print(f'Telefone: {dados[2]}')

            else:

                print('Aluno não encontrado!')

        # =====================================
        # VER MENSALIDADE
        # =====================================

        elif opcao_aluno == '2':

            sql = '''
            SELECT
                status_pagamento,
                valor_pago

            FROM tbl_mensalidade

            INNER JOIN tbl_alunos
                ON tbl_mensalidade.fk_aluno = tbl_alunos.id_aluno

            WHERE tbl_alunos.nome_aluno = %s
            '''

            cursor.execute(sql, (nome_aluno,))

            mensalidade = cursor.fetchone()

            if mensalidade:

                print(f'Status: {mensalidade[0]}')
                print(f'Valor: R$ {mensalidade[1]:.2f}')

            else:

                print('Mensalidade não encontrada!')

        # =====================================
        # VER VENCIMENTO
        # =====================================

        elif opcao_aluno == '3':

            sql = '''
            SELECT
                data_pagamento

            FROM tbl_mensalidade

            INNER JOIN tbl_alunos
                ON tbl_mensalidade.fk_aluno = tbl_alunos.id_aluno

            WHERE tbl_alunos.nome_aluno = %s
            '''

            cursor.execute(sql, (nome_aluno,))

            data = cursor.fetchone()

            if data:

                print(f'Data de vencimento: {data[0]}')

            else:

                print('Data não encontrada!')

        # =====================================
        # VER PLANO
        # =====================================

        elif opcao_aluno == '4':

            sql = '''
            SELECT
                tbl_planos.nome_plano,
                tbl_planos.valor

            FROM tbl_alunos

            INNER JOIN tbl_planos
                ON tbl_alunos.fk_plano = tbl_planos.id_plano

            WHERE tbl_alunos.nome_aluno = %s
            '''

            cursor.execute(sql, (nome_aluno,))

            plano = cursor.fetchone()

            if plano:

                print(f'Plano: {plano[0]}')
                print(f'Valor: R$ {plano[1]:.2f}')

            else:

                print('Plano não encontrado!')

        # =====================================
        # VER EMAIL
        # =====================================

        elif opcao_aluno == '5':

            sql = '''
            SELECT email
            FROM tbl_alunos
            WHERE nome_aluno = %s
            '''

            cursor.execute(sql, (nome_aluno,))

            email = cursor.fetchone()

            if email:

                print(f'E-mail: {email[0]}')

            else:

                print('E-mail não encontrado!')

        # =====================================
        # ATUALIZAR EMAIL
        # =====================================

        elif opcao_aluno == '6':

            novo_email = input('Digite o novo e-mail: ')

            sql = '''
            UPDATE tbl_alunos
            SET email = %s
            WHERE nome_aluno = %s
            '''

            cursor.execute(sql, (novo_email, nome_aluno))

            conexao.commit()

            print('E-mail atualizado!')

        # =====================================
        # ALTERAR SENHA
        # =====================================

        elif opcao_aluno == '7':

            nova_senha = input('Digite a nova senha: ')

            sql = '''
            UPDATE tbl_usuarios
            SET senha = %s
            WHERE usuario = %s
            '''

            cursor.execute(sql, (nova_senha, nome_aluno))

            conexao.commit()

            print('Senha alterada!')

        # =====================================
        # TROCAR PLANO
        # =====================================

        elif opcao_aluno == '8':

            cursor.execute(
                'SELECT id_plano, nome_plano, valor FROM tbl_planos'
            )

            planos = cursor.fetchall()

            print('\n===== PLANOS DISPONÍVEIS =====')

            for plano in planos:

                print(f'ID: {plano[0]}')
                print(f'Plano: {plano[1]}')
                print(f'Valor: R$ {plano[2]:.2f}')
                print('----------------')

            novo_plano = input('Digite o ID do novo plano: ')

            sql = '''
            UPDATE tbl_alunos
            SET fk_plano = %s
            WHERE nome_aluno = %s
            '''

            cursor.execute(sql, (novo_plano, nome_aluno))

            conexao.commit()

            print('Plano alterado com sucesso!')

        # =====================================
        # CANCELAR PLANO
        # =====================================

        elif opcao_aluno == '9':

            confirmar = input(
                'Deseja cancelar o plano? (S/N): '
            ).upper()

            if confirmar == 'S':

                sql = '''
                UPDATE tbl_alunos
                SET fk_plano = NULL
                WHERE nome_aluno = %s
                '''

                cursor.execute(sql, (nome_aluno,))

                conexao.commit()

                print('Plano cancelado!')

            else:

                print('Cancelamento cancelado!')

        # =====================================
        # HISTÓRICO
        # =====================================

        elif opcao_aluno == '10':

            sql = '''
            SELECT
                data_pagamento,
                status_pagamento,
                valor_pago

            FROM tbl_mensalidade

            INNER JOIN tbl_alunos
                ON tbl_mensalidade.fk_aluno = tbl_alunos.id_aluno

            WHERE tbl_alunos.nome_aluno = %s
            '''

            cursor.execute(sql, (nome_aluno,))

            historico = cursor.fetchall()

            if historico:

                for h in historico:

                    print(f'Data: {h[0]}')
                    print(f'Status: {h[1]}')
                    print(f'Valor: R$ {h[2]:.2f}')
                    print('----------------')

            else:

                print('Nenhum histórico encontrado!')

        # =====================================
        # SAIR
        # =====================================

        elif opcao_aluno == '11':

            print('Saindo...')
            break

        else:

            print('Opção inválida!')