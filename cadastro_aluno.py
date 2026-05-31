import mysql.connector
from conexao import conexao

nome = input('Digite seu nome: ')
idade = int(input('Digite sua idade: '))
telefone = input('Digite seu telefone: ')
plano = input('Digite seu plano: ')
    
sql = '''
INSERT INTO tbl_alunos (nome_aluno, idade, telefone,fk_plano) VALUES
(%s, %s, %s, %s)
'''
cursor = conexao.cursor()
cursor.execute(sql, (nome, idade, telefone, plano))
conexao.commit()
print('Aluno cadastrado com sucesso!')

cursor.execute("SELECT * FROM tbl_alunos ORDER BY id_aluno DESC LIMIT 1")
print(cursor.fetchone())