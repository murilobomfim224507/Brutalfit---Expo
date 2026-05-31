from mysql  import connector
conexao = connector.connect(
    host = 'localhost',
    user = 'root',
    password = '130807Mm@',
    database = 'academia_expo'
)
cursor = conexao.cursor()
cursor.execute("SELECT * FROM tbl_alunos")
alunos = cursor.fetchall()

print('Conexão bem sucedida!')
print(alunos)