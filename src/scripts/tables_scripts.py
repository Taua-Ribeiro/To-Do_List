# Por padrão o sqlite converte o tipo TIMESTAMP em TEXT, por esse motivo que
# os campos "criado_em" e "atualizado_em" estão como TEXT.
# O mesmo vale para os campos relacionados à datas, no formato (YYYY-MM-DD HH:MM:SS.SSS)

TABLES_SCRIPTS = ["""
CREATE TABLE IF NOT EXISTS Usuario(
    id TEXT PRIMARY KEY,
    nome TEXT NOT NULL,
    senha TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""",
"""
CREATE TABLE IF NOT EXISTS Senhas_Usuario(
    id TEXT PRIMARY KEY,
    id_usuario TEXT NOT NULL,
    ultima_senha TEXT NOT NULL,
    data_alteracao TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id) ON DELETE CASCADE
);
""",
"""
CREATE TABLE IF NOT EXISTS Tarefa(
    id TEXT PRIMARY KEY,
    id_usuario TEXT NOT NULL,
    titulo TEXT NOT NULL,
    descricao TEXT,
    status_tarefa TEXT NOT NULL,
    prazo TEXT,
    data_inicio TEXT,
    data_encerramento TEXT,
    atualizado_em TEXT DEFAULT CURRENT_TIMESTAMP,
    criado_em TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id)
);
""",
"""
CREATE TABLE IF NOT EXISTS Status_Tarefa(
    id TEXT PRIMARY KEY,
    id_tarefa TEXT NOT NULL,
    ultimo_status TEXT NOT NULL,
    data_alteracao TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_tarefa) REFERENCES Tarefa(id)
);
"""]
