import mysql.connector

conexao = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '130807Mm@',
    database = 'academia_expo'
)

def cadastrar_aluno(nome, idade, telefone, plano):

    sql = '''
    INSERT INTO tbl_alunos
    (nome_aluno, idade, telefone, fk_plano)
    VALUES (%s, %s, %s, %s)
    '''

    cursor.execute(sql, (nome, idade, telefone, plano))

    conexao.commit()

    id_aluno = cursor.lastrowid

    sql_mensalidade = '''
    INSERT INTO tbl_mensalidade
    (data_pagamento, status_pagamento, valor_pago, fk_aluno)
    VALUES (%s, %s, %s, %s)
    '''

    cursor.execute(
        sql_mensalidade,
        ('2026-01-01', 'PENDENTE', 99.90, id_aluno)
    )

    conexao.commit()