import mysql.connector 

conexao = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '130807Mm@',
    database = 'academia_expo'
)

cursor = conexao.cursor()

id_aluno = int(input('Digite o ID do aluno que deseja excluir: '))

sql = '''
DELETE FROM tbl_alunos
WHERE id_aluno = %s
'''
cursor.execute(sql, (id_aluno,))

conexao.commit()

print('Aluno excluído com sucesso')

    