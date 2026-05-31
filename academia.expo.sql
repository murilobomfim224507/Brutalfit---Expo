CREATE DATABASE academia_expo;
USE academia_expo;
CREATE TABLE tbl_usuarios (
id_usuario INT AUTO_INCREMENT PRIMARY KEY,
usuario VARCHAR (100),
senha VARCHAR (100),
);
CREATE TABLE tbl_planos (
id_plano INT AUTO_INCREMENT PRIMARY KEY,
nome_plano VARCHAR (100),
valor DECIMAL (10,2)
);
CREATE TABLE tbl_alunos (
id_aluno INT AUTO_INCREMENT PRIMARY KEY,
nome_aluno VARCHAR (100),
idade INT,
telefone VARCHAR (100),
fk_plano INT
);

ALTER TABLE tbl_alunos ADD CONSTRAINT FOREIGN KEY (fk_plano)
REFERENCES tbl_planos (id_plano);

CREATE TABLE tbl_mensalidade (
id_mensalidade INT AUTO_INCREMENT PRIMARY KEY,
data_pagamento DATE,
status_pagamento VARCHAR (100),
valor_pago DECIMAL (10,2),
fk_aluno INT
);

ALTER TABLE tbl_mensalidade ADD CONSTRAINT FOREIGN KEY (fk_aluno)
REFERENCES tbl_alunos (id_aluno);

INSERT INTO tbl_usuarios (usuario, senha, tipo) VALUES
('admin', '12345', 'adm'),
('matheus', '54321', 'aluno'),
('expo', '789', 'adm');

INSERT INTO tbl_planos (nome_plano, valor) VALUES 
('Basico', 99.90),
('Premium', 149.90),
('Musculacao', 119.90),
('VIP', 199.90);

INSERT INTO tbl_alunos (nome_aluno, idade, telefone, fk_plano) VALUES
('Matheus', 20, '11983769784', 1),
('Murilo', 18, '11951528083', 2),
('Lucas', 18, '11991328258', 3),
('Kaic', 19, '11977610937', 3);

INSERT INTO tbl_mensalidade (data_pagamento, status_pagamento, valor_pago, fk_aluno) VALUES
('2026-03-09', 'PAGO', 99.90, 1),
('2026-05-12', 'PENDENTE', 99.90, 1),
('2026-06-15', 'PAGO', 149.90, 2),
('2026-02-25', 'PENDENTE', 119.90, 3);

INSERT INTO tbl_alunos (nome_aluno, idade, telefone, fk_plano) VALUES
('Kaic', 19, '11977610937', 3);

SELECT tbl_alunos.nome_aluno,
tbl_planos.nome_plano,
tbl_planos.valor
FROM tbl_alunos
INNER JOIN tbl_planos
ON tbl_alunos.fk_plano = tbl_planos.id_plano;

SELECT *
FROM tbl_mensalidade
WHERE status_pagamento = 'PENDENTE';

UPDATE tbl_alunos
SET nome_aluno = 'Murilo Santos'
WHERE id_aluno = 2;

UPDATE tbl_alunos
SET telefone = NULL
WHERE id_aluno = 2;

DELETE FROM tbl_alunos
WHERE id_aluno = 4;

SELECT *
FROM tbl_alunos
ORDER BY nome_aluno ASC;

SELECT status_pagamento, COUNT(*) AS quantidade
FROM tbl_mensalidade
GROUP BY status_pagamento;

UPDATE tbl_planos SET descricao = 'Acesso a musculação e cardio' WHERE id_plano = 1;
UPDATE tbl_planos SET descricao = 'Acesso completo + aulas em grupo' WHERE id_plano = 2;
UPDATE tbl_planos SET descricao = 'Acesso exclusivo a musculação' WHERE id_plano = 3;
UPDATE tbl_planos SET descricao = 'Acesso completo + personal trainer' WHERE id_plano = 4;

ALTER TABLE tbl_usuarios
ADD tipo VARCHAR (100), tipo_usuario VARCHAR (100);

SELECT 
    tbl_alunos.id_aluno,
    tbl_alunos.nome_aluno,
    tbl_alunos.idade,
    tbl_alunos.telefone,
    tbl_alunos.fk_plano,
    tbl_mensalidade.fk_aluno,
    tbl_mensalidade.status_pagamento AS pagamento,
    tbl_mensalidade.valor_pago 
FROM tbl_alunos
LEFT JOIN tbl_mensalidade
    ON tbl_alunos.id_aluno = tbl_mensalidade.fk_aluno
ORDER BY tbl_alunos.nome_aluno ASC;
