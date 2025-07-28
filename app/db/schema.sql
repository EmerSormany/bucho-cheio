
DROP TABLE IF EXISTS usuarios;
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    nome TEXT NOT NULL,               
    email TEXT UNIQUE NOT NULL,   
    senha_hash TEXT NOT NULL,         
    administrador INTEGER NOT NULL,  -- 0 Falso, 1 Verdadeiro
    matricula TEXT UNIQUE NOT NULL,  
    curso TEXT 
);

DROP TABLE IF EXISTS quadro_vagas;
CREATE TABLE quadro_vagas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_vagas TEXT NOT NULL UNIQUE,  -- formato 'YYYY-MM-DD'
    quantidade INTEGER NOT NULL 
);

DROP TABLE IF EXISTS reserva;
CREATE TABLE reserva (
    usuario_id INTEGER,   
    vaga_id INTEGER, 
    situacao TEXT NOT NULL CHECK (situacao IN ('ativa', 'cancelada', 'usada')), 
    qr_code TEXT NOT NULL UNIQUE,  
    chekin TEXT DEFAULT NULL, -- formato 'YYYY-MM-DD HH:MM:SS'
  
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (vaga_id) REFERENCES quadro_vagas(id),

    CONSTRAINT pk_reserva PRIMARY KEY (usuario_id, vaga_id)
);
