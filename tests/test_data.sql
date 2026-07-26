INSERT INTO Usuarios(id, nome, hash_senha) VALUES (1, "teste", "teste");

INSERT INTO Tarefas(id, id_usuario, titulo, descricao, concluido_em) VALUES (
    (1, 1, "Tarefa 1", "teste", NULL)
    (2, 1, "Tarefa 2", "", "2026-07-11")
);

COMMIT;
