import mysql.connector

conexao = mysql.connector.connect(
    host = 'localhost',
    user ='root',
    password = '130807Mm@',
    database = 'academia_expo'
)
cursor = conexao.cursor()

id_aluno = int(input('Digite o ID do aluno que deseja alterar: '))
novo_nome = input('Digite o novo nome do aluno: ')
nova_idade = int(input('Digite a nova idade do aluno: '))
novo_telefone = input('Digite o novo telefone do aluno: ')
novo_plano = input('Digite o novo plano do aluno: ')

sql = '''
UPDATE tbl_alunos
SET nome_aluno = %s, idade = %s, telefone = %s, fk_plano = %s
WHERE id_aluno = %s
'''

cursor.execute(sql, (novo_nome, nova_idade, novo_telefone, novo_plano, id_aluno))

conexao.commit()

print('Aluno alterado com sucesso!')