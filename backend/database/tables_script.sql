USE `todo-database`;

CREATE TABLE IF NOT EXISTS `todo-database`.`Usuario`(
	id VARCHAR(36) PRIMARY KEY DEFAULT (UUID()),
    nome VARCHAR(255) NOT NULL,
    senha VARCHAR(8) NOT NULL,
    email VARCHAR(255) NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_comprimento_senha CHECK (LENGTH(senha) >= 4 AND LENGTH(senha) <= 8)
);

CREATE TABLE IF NOT EXISTS `todo-database`.`Senhas-Usuario`(
	id VARCHAR(36) PRIMARY KEY DEFAULT (uuid()),
    id_usuario VARCHAR(36) NOT NULL,
    ultima_senha VARCHAR(8) NOT NULL,
    data_alteracao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_Usuario_Senhas FOREIGN KEY (id_usuario) REFERENCES `todo-database`.`Usuario`(id)
		ON DELETE CASCADE
        ON UPDATE RESTRICT
);

CREATE TABLE IF NOT EXISTS `todo-database`.`Tarefa`(
	id VARCHAR(36) PRIMARY KEY DEFAULT (uuid()),
    id_usuario VARCHAR(36) NOT NULL,
    titulo VARCHAR(255) NOT NULL,
    descricao TEXT,
    status_tarefa ENUM("PENDENTE", "FAZENDO", "FEITA", "CANCELADA") NOT NULL,
    prazo DATE,
    data_inicio DATE,
    data_encerramento DATE,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_Usuario_Tarefa FOREIGN KEY (id_usuario) REFERENCES `todo-database`.`Usuario`(id)
		ON DELETE RESTRICT
        ON UPDATE RESTRICT,
    CONSTRAINT chk_datas_inicio_fim CHECK(data_inicio <= data_encerramento)
);

CREATE TABLE IF NOT EXISTS `todo-database`.`Status-Tarefa`(
	id VARCHAR(36) PRIMARY KEY DEFAULT (uuid()),
    id_tarefa VARCHAR(36) NOT NULL,
    ultimo_status ENUM("PENDENTE", "FAZENDO", "FEITA", "CANCELADA") NOT NULL,
    data_alteracao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_Tarefa_StatusTarefa FOREIGN KEY (id_tarefa) REFERENCES `todo-database`.`Tarefa`(id)
      ON DELETE CASCADE
      ON UPDATE RESTRICT
);
