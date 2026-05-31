import mysql.connector
from datetime import datetime

conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='130807Mm@',
    database='academia_expo'
)

cursor = conexao.cursor(buffered=True)

print('Conectado com sucesso!')

tipo_usuario = ''

while True:

    print('\n===== BEM-VINDO À NOSSA ACADEMIA, BRUTALFIT EXPO! =====')
    print('1 - Login ADM')
    print('2 - Login Aluno')
    print('3 - Cadastrar ADM')
    print('4 - Sair')

    escolha = input('Escolha uma opção: ')

    if escolha == '1':

        usuario = input('Usuário ADM: ')
        senha = input('Senha: ')

        cursor.execute('''
        SELECT * FROM tbl_usuarios
        WHERE usuario = %s AND senha = %s AND tipo = 'ADM'
        ''', (usuario, senha))

        resultado = cursor.fetchone()

        if resultado:
            tipo_usuario = 'ADM'
            print('Login ADM realizado com sucesso!')
            break
        else:
            print('Usuário ou senha inválidos!')

    elif escolha == '2':

        usuario = input('Digite seu nome completo: ')
        senha = input('Digite sua senha: ')

        cursor.execute('''
        SELECT * FROM tbl_usuarios
        WHERE usuario = %s AND senha = %s AND tipo = 'ALUNO'
        ''', (usuario, senha))

        resultado = cursor.fetchone()

        if resultado:
            tipo_usuario = 'ALUNO'
            print('Login de aluno realizado!')
            break
        else:
            print('Usuário ou senha inválidos!')

    elif escolha == '3':

        usuario = input('Crie um usuário ADM: ')
        senha = input('Crie uma senha: ')

        cursor.execute(
            'INSERT INTO tbl_usuarios (usuario, senha, tipo) VALUES (%s, %s, %s)',
            (usuario, senha, 'ADM')
        )
        conexao.commit()
        print('ADM cadastrado com sucesso!')

    elif escolha == '4':
        print('Sistema encerrado!')
        exit()

    else:
        print('Opção inválida!')

#MENU DO ALUNO

if tipo_usuario == 'ALUNO':

    while True:

        print('\n===== ÁREA DO ALUNO =====')
        print('1 - Ver meus dados')
        print('2 - Ver mensalidade')
        print('3 - Ver plano')
        print('4 - Alterar senha')
        print('5 - Ver histórico')
        print('6 - Ver total já pago')
        print('7 - Ver débitos pendentes')
        print('8 - Simular troca de plano')
        print('9 - Trocar plano')
        print('10 - Sair')

        opcao_aluno = input('Escolha: ')

        if opcao_aluno == '1':

            cursor.execute('''
            SELECT nome_aluno, idade, telefone
            FROM tbl_alunos WHERE nome_aluno = %s
            ''', (usuario,))

            dados = cursor.fetchone()

            if dados:
                print(f'Nome: {dados[0]}')
                print(f'Idade: {dados[1]}')
                print(f'Telefone: {dados[2]}')
            else:
                print('Aluno não encontrado!')

        elif opcao_aluno == '2':

            cursor.execute('''
            SELECT status_pagamento, valor_pago
            FROM tbl_mensalidade
            INNER JOIN tbl_alunos ON tbl_mensalidade.fk_aluno = tbl_alunos.id_aluno
            WHERE tbl_alunos.nome_aluno = %s
            ''', (usuario,))

            mensalidade = cursor.fetchone()

            if mensalidade:
                print(f'Status: {mensalidade[0]}')
                print(f'Valor Pago: R$ {mensalidade[1]:.2f}')
            else:
                print('Mensalidade não encontrada!')

        elif opcao_aluno == '3':

            cursor.execute('''
            SELECT tbl_planos.nome_plano, tbl_planos.valor
            FROM tbl_alunos
            INNER JOIN tbl_planos ON tbl_alunos.fk_plano = tbl_planos.id_plano
            WHERE tbl_alunos.nome_aluno = %s
            ''', (usuario,))

            plano = cursor.fetchone()

            if plano:
                print(f'Plano: {plano[0]}')
                print(f'Valor: R$ {plano[1]:.2f}')
            else:
                print('Plano não encontrado!')

        elif opcao_aluno == '4':

            nova_senha = input('Digite a nova senha: ')

            cursor.execute(
                'UPDATE tbl_usuarios SET senha = %s WHERE usuario = %s',
                (nova_senha, usuario)
            )
            conexao.commit()
            print('Senha alterada com sucesso!')

        elif opcao_aluno == '5':

            cursor.execute('''
            SELECT status_pagamento, valor_pago
            FROM tbl_mensalidade
            INNER JOIN tbl_alunos ON tbl_mensalidade.fk_aluno = tbl_alunos.id_aluno
            WHERE tbl_alunos.nome_aluno = %s
            ''', (usuario,))

            historico = cursor.fetchall()

            if historico:
                for h in historico:
                    print(f'Status: {h[0]}')
                    print(f'Valor: R$ {h[1]:.2f}')
                    print('----------------')
            else:
                print('Nenhum histórico encontrado!')

        elif opcao_aluno == '6':

            cursor.execute('''
            SELECT SUM(valor_pago)
            FROM tbl_mensalidade
            INNER JOIN tbl_alunos ON tbl_mensalidade.fk_aluno = tbl_alunos.id_aluno
            WHERE tbl_alunos.nome_aluno = %s
            AND tbl_mensalidade.status_pagamento = 'PAGO'
            ''', (usuario,))

            total = cursor.fetchone()

            if total[0]:
                print(f'Total já pago: R$ {total[0]:.2f}')
            else:
                print('Nenhum pagamento encontrado!')

        elif opcao_aluno == '7':

            cursor.execute('''
            SELECT valor_pago
            FROM tbl_mensalidade
            INNER JOIN tbl_alunos ON tbl_mensalidade.fk_aluno = tbl_alunos.id_aluno
            WHERE tbl_alunos.nome_aluno = %s
            AND tbl_mensalidade.status_pagamento = 'PENDENTE'
            ''', (usuario,))

            pendentes = cursor.fetchall()

            if pendentes:

                total_pendente = 0

                for p in pendentes:
                    print(f'Valor: R$ {p[0]:.2f}')
                    print('----------------')
                    total_pendente += p[0]

                print(f'Total pendente: R$ {total_pendente:.2f}')

            else:
                print('Nenhum débito pendente!')

        elif opcao_aluno == '8':

            cursor.execute('''
            SELECT tbl_planos.nome_plano, tbl_planos.valor
            FROM tbl_alunos
            INNER JOIN tbl_planos ON tbl_alunos.fk_plano = tbl_planos.id_plano
            WHERE tbl_alunos.nome_aluno = %s
            ''', (usuario,))

            plano_atual = cursor.fetchone()

            if not plano_atual:
                print('Plano não encontrado!')
            else:

                print(f'Seu plano atual: {plano_atual[0]} | R$ {plano_atual[1]:.2f}')

                cursor.execute('SELECT id_plano, nome_plano, valor FROM tbl_planos')
                planos = cursor.fetchall()

                print('\n===== SIMULAÇÃO DE TROCA =====')

                for p in planos:
                    diferenca = p[2] - plano_atual[1]
                    sinal = '+' if diferenca > 0 else ''
                    print(f'ID: {p[0]} | {p[1]} | R$ {p[2]:.2f} | Diferença: {sinal}R$ {diferenca:.2f}')

                print('\nIsso é apenas uma simulação, nenhuma alteração foi feita!')

        elif opcao_aluno == '9':

            cursor.execute('SELECT id_plano, nome_plano, valor FROM tbl_planos')
            planos = cursor.fetchall()

            print('\n===== PLANOS DISPONÍVEIS =====')

            for p in planos:
                print(f'ID: {p[0]} | {p[1]} | R$ {p[2]:.2f}')

            novo_plano = input('Digite o ID do novo plano: ')

            cursor.execute(
                'SELECT id_plano FROM tbl_planos WHERE id_plano = %s',
                (novo_plano,)
            )

            if not cursor.fetchone():
                print('Plano inválido! Digite um ID da lista.')
            else:
                cursor.execute(
                    'UPDATE tbl_alunos SET fk_plano = %s WHERE nome_aluno = %s',
                    (novo_plano, usuario)
                )
                conexao.commit()
                print('Plano trocado com sucesso!')

        elif opcao_aluno == '10':
            print('Saindo...')
            break

        else:
            print('Opção inválida!')

#MENU DO ADM


elif tipo_usuario == 'ADM':

    while True:

        print('\n===== MENU BRUTALFIT EXPO! =====')
        print('1 - Cadastrar aluno')
        print('2 - Listar alunos')
        print('3 - Atualizar aluno')
        print('4 - Excluir aluno')
        print('5 - Ver mensalidades')
        print('6 - Ver planos')
        print('7 - Listar por status de pagamento')
        print('8 - Quantidade de alunos por plano')
        print('9 - Sair')

        opcao = input('Escolha uma opção: ')

        if opcao == '1':

            nome = input('Digite o nome completo: ')

            if ' ' not in nome.strip():
                print('Digite nome completo!')
                continue

            if not all(c.isalpha() or c.isspace() for c in nome):
                print('O nome deve conter apenas letras!')
                continue

            cursor.execute(
                'SELECT id_aluno FROM tbl_alunos WHERE nome_aluno = %s',
                (nome,)
            )

            if cursor.fetchone():
                print('Já existe um aluno cadastrado com esse nome!')
                continue

            data_aniversario = input('Digite a data de aniversário (AAAA-MM-DD): ')

            try:
                data_nasc = datetime.strptime(data_aniversario, '%Y-%m-%d')
                hoje = datetime.today()

                if data_nasc >= hoje:
                    print('Data inválida! A data de aniversário não pode ser futura.')
                    continue

                idade_calculada = hoje.year - data_nasc.year - ((hoje.month, hoje.day) < (data_nasc.month, data_nasc.day))

                if idade_calculada < 10 or idade_calculada > 80:
                    print('Idade inválida! O aluno deve ter entre 10 e 80 anos.')
                    continue

            except ValueError:
                print('Data inválida! Digite uma data real no formato AAAA-MM-DD.')
                continue

            telefone = input('Digite o telefone: ')

            if not telefone.isdigit():
                print('Telefone inválido!')
                continue

            if len(telefone) != 11:
                print('Telefone deve conter 11 dígitos!')
                continue

            senha_aluno = input('Crie uma senha para o aluno: ')

            cursor.execute('SELECT id_plano, nome_plano, valor FROM tbl_planos')
            planos = cursor.fetchall()

            print('\n===== PLANOS DISPONÍVEIS =====')
            for p in planos:
                print(f'ID: {p[0]} | {p[1]} | R$ {p[2]:.2f}')

            plano = input('Digite o ID do plano: ')

            cursor.execute(
                'SELECT valor FROM tbl_planos WHERE id_plano = %s',
                (plano,)
            )
            valor_plano = cursor.fetchone()

            if not valor_plano:
                print('Plano inválido!')
                continue

            valor_plano = valor_plano[0]

            status = input('Digite PAGO ou PENDENTE: ').upper()

            if status != 'PAGO' and status != 'PENDENTE':
                print('Digite apenas PAGO ou PENDENTE!')
                continue

            cursor.execute(
                'INSERT INTO tbl_alunos (nome_aluno, idade, telefone, fk_plano) VALUES (%s, %s, %s, %s)',
                (nome, idade_calculada, telefone, plano)
            )
            conexao.commit()
            id_aluno = cursor.lastrowid

            cursor.execute(
                'INSERT INTO tbl_usuarios (usuario, senha, tipo) VALUES (%s, %s, %s)',
                (nome, senha_aluno, 'ALUNO')
            )
            conexao.commit()

            cursor.execute(
                'INSERT INTO tbl_mensalidade (status_pagamento, valor_pago, fk_aluno) VALUES (%s, %s, %s)',
                (status, valor_plano, id_aluno)
            )
            conexao.commit()
            print('Aluno cadastrado com sucesso!')

        elif opcao == '2':

            cursor.execute('''
            SELECT tbl_alunos.id_aluno, tbl_alunos.nome_aluno, tbl_alunos.idade,
                   tbl_alunos.telefone, tbl_planos.nome_plano, tbl_planos.valor
            FROM tbl_alunos
            INNER JOIN tbl_planos ON tbl_alunos.fk_plano = tbl_planos.id_plano
            ORDER BY tbl_alunos.id_aluno ASC
            ''')

            resultado = cursor.fetchall()

            print('\n===== LISTA DE ALUNOS =====')

            for aluno in resultado:
                print(f'ID: {aluno[0]}')
                print(f'Nome: {aluno[1]}')
                print(f'Idade: {aluno[2]}')
                print(f'Telefone: {aluno[3]}')
                print(f'Plano: {aluno[4]}')
                print(f'Valor: R$ {aluno[5]:.2f}')
                print('----------------------')

        elif opcao == '3':

            id_aluno = input('Digite o ID do aluno: ')

            cursor.execute(
                'SELECT id_aluno FROM tbl_alunos WHERE id_aluno = %s',
                (id_aluno,)
            )

            if not cursor.fetchone():
                print('Aluno não encontrado!')
                continue

            print('\n1 - Atualizar nome')
            print('2 - Atualizar idade')
            print('3 - Atualizar telefone')

            escolha = input('Escolha: ')

            if escolha == '1':

                while True:
                    novo_nome = input('Novo nome: ')

                    if ' ' not in novo_nome.strip():
                        print('Digite o nome completo!')
                        continue

                    if not all(c.isalpha() or c.isspace() for c in novo_nome):
                        print('O nome deve conter apenas letras!')
                        continue

                    cursor.execute(
                        'UPDATE tbl_usuarios SET usuario = %s WHERE usuario = (SELECT nome_aluno FROM tbl_alunos WHERE id_aluno = %s)',
                        (novo_nome, id_aluno)
                    )
                    cursor.execute(
                        'UPDATE tbl_alunos SET nome_aluno = %s WHERE id_aluno = %s',
                        (novo_nome, id_aluno)
                    )
                    conexao.commit()
                    print('Nome atualizado!')
                    break

            elif escolha == '2':

                while True:
                    nova_idade = input('Nova idade: ')

                    if not nova_idade.isdigit() or int(nova_idade) < 10 or int(nova_idade) > 80:
                        print('Idade inválida! Digite entre 10 e 80.')
                        continue

                    cursor.execute(
                        'UPDATE tbl_alunos SET idade = %s WHERE id_aluno = %s',
                        (nova_idade, id_aluno)
                    )
                    conexao.commit()
                    print('Idade atualizada!')
                    break

            elif escolha == '3':

                while True:
                    novo_telefone = input('Novo telefone: ')

                    if not novo_telefone.isdigit():
                        print('Telefone inválido! Digite apenas números.')
                        continue

                    if len(novo_telefone) != 11:
                        print('Telefone deve conter 11 dígitos!')
                        continue

                    cursor.execute(
                        'UPDATE tbl_alunos SET telefone = %s WHERE id_aluno = %s',
                        (novo_telefone, id_aluno)
                    )
                    conexao.commit()
                    print('Telefone atualizado!')
                    break

            else:
                print('Opção inválida!')

        elif opcao == '4':

            id_aluno = input('Digite o ID do aluno: ')

            cursor.execute(
                'SELECT id_aluno, nome_aluno FROM tbl_alunos WHERE id_aluno = %s',
                (id_aluno,)
            )

            aluno = cursor.fetchone()

            if not aluno:
                print('Aluno não encontrado!')
                continue

            nome_aluno = aluno[1]

            cursor.execute('DELETE FROM tbl_mensalidade WHERE fk_aluno = %s', (id_aluno,))
            cursor.execute('DELETE FROM tbl_alunos WHERE id_aluno = %s', (id_aluno,))
            cursor.execute('DELETE FROM tbl_usuarios WHERE usuario = %s AND tipo = "ALUNO"', (nome_aluno,))
            conexao.commit()
            print('Aluno excluído!')

        elif opcao == '5':

            cursor.execute('''
            SELECT tbl_alunos.nome_aluno, tbl_mensalidade.status_pagamento,
                   tbl_mensalidade.valor_pago
            FROM tbl_mensalidade
            INNER JOIN tbl_alunos ON tbl_mensalidade.fk_aluno = tbl_alunos.id_aluno
            ''')

            resultado = cursor.fetchall()

            print('\n===== MENSALIDADES =====')

            for mensalidade in resultado:
                print(f'Aluno: {mensalidade[0]}')
                print(f'Status: {mensalidade[1]}')
                print(f'Valor: R$ {mensalidade[2]:.2f}')
                print('----------------')

        elif opcao == '6':

            cursor.execute('SELECT id_plano, nome_plano, valor FROM tbl_planos')
            planos = cursor.fetchall()

            print('\n===== PLANOS =====')

            for plano in planos:
                print(f'ID: {plano[0]}')
                print(f'Plano: {plano[1]}')
                print(f'Valor: R$ {plano[2]:.2f}')
                print('----------------')

        elif opcao == '7':

            print('\n1 - PAGO')
            print('2 - PENDENTE')

            escolha_status = input('Escolha: ')

            if escolha_status == '1':
                status_filtro = 'PAGO'
            elif escolha_status == '2':
                status_filtro = 'PENDENTE'
            else:
                print('Opção inválida!')
                continue

            cursor.execute('''
            SELECT tbl_alunos.nome_aluno, tbl_mensalidade.status_pagamento,
                   tbl_mensalidade.valor_pago
            FROM tbl_mensalidade
            INNER JOIN tbl_alunos ON tbl_mensalidade.fk_aluno = tbl_alunos.id_aluno
            WHERE tbl_mensalidade.status_pagamento = %s
            ''', (status_filtro,))

            resultado = cursor.fetchall()

            print(f'\n===== ALUNOS COM MENSALIDADE {status_filtro} =====')

            if resultado:
                for mensalidade in resultado:
                    print(f'Aluno: {mensalidade[0]}')
                    print(f'Status: {mensalidade[1]}')
                    print(f'Valor: R$ {mensalidade[2]:.2f}')
                    print('----------------')
            else:
                print(f'Nenhum aluno com mensalidade {status_filtro}!')

        elif opcao == '8':

            cursor.execute('''
            SELECT tbl_planos.nome_plano, COUNT(tbl_alunos.id_aluno) AS quantidade
            FROM tbl_planos
            LEFT JOIN tbl_alunos ON tbl_planos.id_plano = tbl_alunos.fk_plano
            GROUP BY tbl_planos.nome_plano
            ORDER BY quantidade DESC
            ''')

            resultado = cursor.fetchall()

            print('\n===== ALUNOS POR PLANO =====')

            for plano in resultado:
                print(f'Plano: {plano[0]}')
                print(f'Quantidade: {plano[1]} aluno(s)')
                print('----------------')

        elif opcao == '9':
            print('Sistema encerrado!')
            break

        else:
            print('Opção inválida!')
crt