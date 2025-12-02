-- Cria o schema
CREATE SCHEMA IF NOT EXISTS app;

-- Função para atualizar capacidade da turma
CREATE OR REPLACE FUNCTION app.atualizar_capacidade_turma() RETURNS trigger
LANGUAGE plpgsql AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE app.turma
        SET capacidade = capacidade + 1
        WHERE turma_id = NEW.turma_id;
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE app.turma
        SET capacidade = GREATEST(capacidade - 1, 0)
        WHERE turma_id = OLD.turma_id;
        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$$;

-- Tabelas principais
CREATE TABLE app.aluno (
    aluno_id SERIAL PRIMARY KEY,
    nome VARCHAR(120),
    telefone VARCHAR(20),
    email VARCHAR(120),
    telefone_pai VARCHAR(20),
    CONSTRAINT aluno_telefone_check CHECK (telefone ~ '^[0-9]{10,11}$'),
    CONSTRAINT aluno_telefone_pai_check CHECK (telefone_pai ~ '^[0-9]{10,11}$')
);

CREATE TABLE app.escola (
    escola_id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    cnpj VARCHAR(14) NOT NULL,
    telefone VARCHAR(20),
    email VARCHAR(120),
    cep VARCHAR(20),
    CONSTRAINT escola_cep_check CHECK (cep ~ '^[0-9]{8}$'),
    CONSTRAINT escola_cnpj_check CHECK (cnpj ~ '^[0-9]{14}$'),
    CONSTRAINT escola_telefone_check CHECK (telefone ~ '^[0-9]{10,11}$')
);

CREATE TABLE app.turma (
    turma_id SERIAL PRIMARY KEY,
    nome VARCHAR(20),
    data_inicio DATE,
    data_fim DATE,
    periodo VARCHAR(20),
    escola_id INT NOT NULL REFERENCES app.escola(escola_id),
    capacidade SMALLINT DEFAULT 0,
    capacidade_max SMALLINT,
    CONSTRAINT turma_check CHECK (capacidade_max >= capacidade),
    CONSTRAINT turma_check1 CHECK (data_inicio < data_fim),
    CONSTRAINT turma_periodo_check CHECK (periodo IN ('matutino','vespertino','noturno','integral'))
);

CREATE TABLE app.matricula (
    matricula_id SERIAL PRIMARY KEY,
    turma_id INT NOT NULL REFERENCES app.turma(turma_id),
    aluno_id INT NOT NULL REFERENCES app.aluno(aluno_id)
);

CREATE TABLE app.disciplina (
    disciplina_id SERIAL PRIMARY KEY,
    nome VARCHAR(30) NOT NULL
);

CREATE TABLE app.avaliacao (
    id SERIAL PRIMARY KEY,
    matricula_id INT NOT NULL REFERENCES app.matricula(matricula_id),
    disciplina_id INT NOT NULL REFERENCES app.disciplina(disciplina_id),
    avaliacao VARCHAR(20) NOT NULL,
    nota NUMERIC(4,2) NOT NULL CHECK (nota >= 0 AND nota <= 10),
    data_avaliacao DATE,
    prova BYTEA,
    UNIQUE (matricula_id, disciplina_id, avaliacao)
);

CREATE TABLE app.presenca (
    matricula_id INT NOT NULL REFERENCES app.matricula(matricula_id),
    disciplina_id INT NOT NULL REFERENCES app.disciplina(disciplina_id),
    data_aula DATE NOT NULL,
    presente BOOLEAN DEFAULT TRUE,
    justificada BOOLEAN DEFAULT FALSE,
    justificativa TEXT,
    UNIQUE (matricula_id, disciplina_id, data_aula)
);

CREATE TABLE app.professor (
    professor_id SERIAL PRIMARY KEY,
    cpf VARCHAR(11) NOT NULL,
    nome VARCHAR(30) NOT NULL,
    telefone VARCHAR(20),
    email VARCHAR(120),
    endereco VARCHAR(120),
    CONSTRAINT professor_cpf_check CHECK (cpf ~ '^[0-9]{11}$'),
    CONSTRAINT professor_telefone_check CHECK (telefone ~ '^[0-9]{10,11}$')
);

CREATE TABLE app.turma_disciplina (
    turma_id INT NOT NULL REFERENCES app.turma(turma_id),
    disciplina_id INT NOT NULL REFERENCES app.disciplina(disciplina_id),
    UNIQUE(turma_id, disciplina_id)
);

CREATE TABLE app.turma_professor (
    turma_id INT NOT NULL REFERENCES app.turma(turma_id),
    professor_id INT NOT NULL REFERENCES app.professor(professor_id),
    UNIQUE(turma_id, professor_id)
);

CREATE TABLE app.endereco (
    endereco_id SERIAL PRIMARY KEY,
    aluno_id INT NOT NULL REFERENCES app.aluno(aluno_id),
    estado VARCHAR(20),
    cidade VARCHAR(60),
    bairro VARCHAR(70),
    rua VARCHAR(70),
    casa VARCHAR(20)
);

-- View de médias
CREATE OR REPLACE VIEW app.vw_media_notas_escolas AS
SELECT 
    e.escola_id,
    e.nome AS escola_nome,
    d.disciplina_id,
    d.nome AS disciplina_nome,
    ROUND(AVG(a.nota), 2) AS media_notas
FROM app.escola e
JOIN app.turma t ON t.escola_id = e.escola_id
JOIN app.matricula m ON m.turma_id = t.turma_id
JOIN app.avaliacao a ON a.matricula_id = m.matricula_id
JOIN app.disciplina d ON d.disciplina_id = a.disciplina_id
GROUP BY e.escola_id, e.nome, d.disciplina_id, d.nome;


--Procedure 
CREATE OR REPLACE PROCEDURE app.atualizar_aluno(
    p_aluno_id INT,
    p_nome TEXT,
    p_telefone TEXT,
    p_email TEXT,
    p_telefone_pai TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE app.aluno
    SET nome = p_nome,
        telefone = p_telefone,
        email = p_email,
        telefone_pai = p_telefone_pai
    WHERE aluno_id = p_aluno_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Aluno não encontrado';
    END IF;
END;
$$;
