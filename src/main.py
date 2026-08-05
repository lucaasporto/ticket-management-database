import mysql.connector
from mysql.connector import errorcode

# Variáveis
# Valores para criação de tabelas do Banco de Dados
tables = {'PONTO_DE_VENDA': (
    """CREATE TABLE `PONTO_DE_VENDA` (
      `id_ponto_de_venda` integer PRIMARY KEY NOT NULL,
      `nome` varchar(50) NOT NULL,
      `bairro` varchar(50) NOT NULL,
      `cidade` varchar(50) NOT NULL,
      `estado` varchar(50) NOT NULL,
      `rua` varchar(50) NOT NULL,
      `numero` integer NOT NULL
    ) ENGINE=InnoDB"""),
    'LOTE': (
        """CREATE TABLE `LOTE` (
            `id_lote` integer PRIMARY KEY NOT NULL,
            `numero` integer NOT NULL,
            `data_fim` timestamp NOT NULL,
            `valor` float NOT NULL,
            `data_inicio` timestamp NOT NULL
        ) ENGINE=InnoDB"""),
    'CATEGORIA': (
        """CREATE TABLE `CATEGORIA` (
        `id_categoria` integer PRIMARY KEY NOT NULL,
        `nome` varchar(50) NOT NULL
        ) ENGINE=InnoDB"""),
    'LOCAL': (
        """CREATE TABLE `LOCAL` (
        `id_local` integer PRIMARY KEY NOT NULL,
        `nome` varchar(50) NOT NULL,
        `capacidade_maxima` integer NOT NULL,
        `bairro` varchar(50) NOT NULL,
        `rua` varchar(50) NOT NULL,
        `cidade` varchar(50) NOT NULL,
        `estado` varchar(50) NOT NULL,
        `numero` integer NOT NULL
        ) ENGINE=InnoDB"""),
    'TIPO': (
        """CREATE TABLE `TIPO` (
        `id_tipo` integer PRIMARY KEY NOT NULL,
        `nome` varchar(50) NOT NULL
        ) ENGINE=InnoDB"""),
    'CARTAO_DE_CREDITO': (
        """CREATE TABLE `CARTAO_DE_CREDITO` (
        `id_cartao_de_credito` integer PRIMARY KEY NOT NULL,
        `nome_do_titular` varchar(50) NOT NULL,
        `codigo_de_seguranca` integer NOT NULL,
        `numero` varchar(50) NOT NULL,
        `data_de_validade` timestamp NOT NULL,
        UNIQUE(`numero`)
        ) ENGINE=InnoDB"""),
    'USUARIO': (
        """CREATE TABLE `USUARIO` (
        `id_usuario` integer PRIMARY KEY NOT NULL,
        `email` varchar(50) NOT NULL,
        `celular` varchar(50) NOT NULL,
        `cpf` varchar(50) NOT NULL,
        `nome` varchar(50) NOT NULL,
        `estado` varchar(50) NOT NULL,
        `bairro` varchar(50) NOT NULL,
        `cidade` varchar(50) NOT NULL,
        `rua` varchar(50) NOT NULL,
        `numero` integer NOT NULL,
        UNIQUE(`cpf`)
        ) ENGINE=InnoDB"""),
    'PATROCINADOR': (
        """CREATE TABLE `PATROCINADOR` (
        `id_patrocinador` integer PRIMARY KEY NOT NULL,
        `url_logomarca` varchar(100) NOT NULL,
        `url_site` varchar(100) NOT NULL,
        `nome` varchar(50) NOT NULL
        ) ENGINE=InnoDB"""),
    'USUARIO_CARTAO_DE_CREDITO': (
        """CREATE TABLE `USUARIO_CARTAO_DE_CREDITO` (
        `id_cartao_de_credito` integer NOT NULL,
        `id_usuario` integer NOT NULL,
        PRIMARY KEY(`id_cartao_de_credito`,`id_usuario`),
        FOREIGN KEY(`id_cartao_de_credito`) REFERENCES `CARTAO_DE_CREDITO` (`id_cartao_de_credito`),
        FOREIGN KEY(`id_usuario`) REFERENCES `USUARIO` (`id_usuario`)
        ) ENGINE=InnoDB"""),
    'ATRACAO': (
        """CREATE TABLE `ATRACAO` (
        `id_atracao` integer PRIMARY KEY NOT NULL,
        `nome` varchar(50) NOT NULL,
        `id_tipo` integer NOT NULL,
        FOREIGN KEY(`id_tipo`) REFERENCES `TIPO` (`id_tipo`)
        ) ENGINE=InnoDB"""),
    'EVENTO': (
        """CREATE TABLE `EVENTO` (
        `id_evento` integer PRIMARY KEY NOT NULL,
        `data` timestamp NOT NULL,
        `nome` varchar(50) NOT NULL,
        `horario_inicio` time NOT NULL,
        `id_local` integer NOT NULL,
        `id_categoria` integer NOT NULL,
        FOREIGN KEY(`id_local`) REFERENCES `LOCAL` (`id_local`),
        FOREIGN KEY(`id_categoria`) REFERENCES `CATEGORIA` (`id_categoria`)
        ) ENGINE=InnoDB"""),
    'EVENTO_ATRACAO': (
        """CREATE TABLE `EVENTO_ATRACAO` (
        `id_evento_atracao` integer PRIMARY KEY NOT NULL,
        `horario_inicio` time NOT NULL,
        `id_evento` integer NOT NULL,
        `id_atracao` integer NOT NULL,
        FOREIGN KEY(`id_evento`) REFERENCES `EVENTO` (`id_evento`),
        FOREIGN KEY(`id_atracao`) REFERENCES `ATRACAO` (`id_atracao`)
        ) ENGINE=InnoDB"""),
    'EVENTO_PATROCINADOR': (
        """CREATE TABLE `EVENTO_PATROCINADOR` (
        `id_patrocinador` integer NOT NULL,
        `id_evento` integer NOT NULL,
        PRIMARY KEY(`id_patrocinador`,`id_evento`),
        FOREIGN KEY(`id_patrocinador`) REFERENCES `PATROCINADOR` (`id_patrocinador`),
        FOREIGN KEY(`id_evento`) REFERENCES `EVENTO` (`id_evento`)
        ) ENGINE=InnoDB"""),
    'INGRESSO': (
        """CREATE TABLE `INGRESSO` (
        `id_ingresso` integer PRIMARY KEY NOT NULL,
        `id_ponto_de_venda` integer NOT NULL,
        `id_lote` integer NOT NULL,
        `id_evento` integer NOT NULL,
        FOREIGN KEY(`id_ponto_de_venda`) REFERENCES `PONTO_DE_VENDA` (`id_ponto_de_venda`),
        FOREIGN KEY(`id_lote`) REFERENCES `LOTE` (`id_lote`),
        FOREIGN KEY(`id_evento`) REFERENCES `EVENTO` (`id_evento`)
        ) ENGINE=InnoDB"""),
    'COMPRA': (
        """CREATE TABLE `COMPRA` (
        `id_ingresso` integer NOT NULL,
        `id_cartao_de_credito` integer NOT NULL,
        `id_usuario` integer NOT NULL,
        `data` timestamp NOT NULL,
        PRIMARY KEY(`id_ingresso`, `id_cartao_de_credito`,`id_usuario`),
        FOREIGN KEY(`id_ingresso`) REFERENCES `INGRESSO` (`id_ingresso`),
        FOREIGN KEY(`id_cartao_de_credito`) REFERENCES `CARTAO_DE_CREDITO` (`id_cartao_de_credito`),
        FOREIGN KEY(`id_usuario`) REFERENCES `USUARIO` (`id_usuario`)
        ) ENGINE=InnoDB"""),
}

# Valores para serem inseridos no Banco de Dados
inserts = {'PONTO_DE_VENDA': (
    """insert into PONTO_DE_VENDA (id_ponto_de_venda, nome, bairro, cidade, estado, rua, numero) values
    (1, 'EletroStar Eletrônicos', 'Centro', 'São Paulo', 'SP', 'Rua das Flores', 120),
    (2, 'Arte e Cia Decorações', 'Santana', 'São Paulo', 'SP', 'Avenida do Estado', 4567), 
    (3, 'Papelaria Criativa', 'Moema', 'São Paulo', 'SP', 'Avenida Ibirapuera', 340)"""),
    'LOTE': (
        """insert into LOTE (id_lote, numero, data_fim, valor, data_inicio) values
        (1, 1, '2024-07-01', 100.00, '2024-06-01'),
        (2, 2, '2024-07-10', 120.00, '2024-07-02'),
        (3, 3, '2024-07-14', 150.00, '2024-07-11'),
        (4, 1, '2024-08-01', 200.00, '2024-07-01'),
        (5, 2, '2024-08-15', 250.00, '2024-08-02'),
        (6, 1, '2024-08-15', 80.00, '2024-08-01'),
        (7, 2, '2024-08-30', 90.00, '2024-08-16'),
        (8, 3, '2024-09-04', 100.00, '2024-08-31'),
        (9, 1, '2024-09-01', 150.00, '2024-08-01'),
        (10, 2, '2024-09-30', 180.00, '2024-09-02'),
        (11, 3, '2024-10-09', 200.00, '2024-10-01'),
        (12, 1, '2024-11-01', 120.00, '2024-10-01'),
        (13, 2, '2024-11-20', 140.00, '2024-11-02'),
        (14, 1, '2024-11-15', 100.00, '2024-11-01'),
        (15, 2, '2024-11-30', 120.00, '2024-11-16'),
        (16, 3, '2024-12-11', 150.00, '2024-12-01'),
        (17, 1, '2024-12-20', 70.00, '2024-12-01'),
        (18, 2, '2025-01-10', 90.00, '2024-12-21'),
        (19, 3, '2025-01-19', 110.00, '2025-01-11'),
        (20, 1, '2025-01-01', 100.00, '2024-12-01'),
        (21, 2, '2025-02-10', 120.00, '2025-01-02'),
        (22, 1, '2025-03-01', 150.00, '2025-02-01'),
        (23, 2, '2025-04-10', 180.00, '2025-03-02'),
        (24, 3, '2025-04-17', 200.00, '2025-04-11'),
        (25, 1, '2024-04-01', 130.00, '2024-03-01'),
        (26, 2, '2024-04-30', 150.00, '2024-04-02'),
        (27, 3, '2024-05-09', 170.00, '2024-05-01')"""),
    'CATEGORIA': (
        """insert into CATEGORIA (id_categoria, nome) values
        (1, 'Show'),
        (2, 'Teatro'), 
        (3, 'Stand-up Comedy'), 
        (4, 'Palestra'), 
        (5, 'Concerto')"""),
    'LOCAL': (
        """insert into LOCAL (id_local, nome, capacidade_maxima, bairro, rua, cidade, estado, numero) values
        (1, 'Arena Musical', 15000, 'Bela Vista', 'Rua das Flores', 'São Paulo', 'SP', 123),
        (2, 'Teatro Municipal', 1200, 'Centro', 'Avenida Ipiranga', 'Porto Alegre', 'RS', 456),
        (3, 'Cine Art', 300, 'Centro', 'Rua 7 de Setembro', 'Rio de Janeiro', 'RJ', 789),
        (4, 'Expo Center', 5000, 'Jardim Paulista', 'Alameda Santos', 'São Paulo', 'SP', 1011),
        (5, 'Feira Permanente', 800, 'Luz', 'Rua Mauá', 'São Paulo', 'SP', 234)"""),
    'TIPO': (
        """insert into TIPO (id_tipo, nome) values
        (1, 'Cantor'),
        (2, 'Banda'),
        (3, 'Palestrante'),
        (4, 'Comediante'),
        (5, 'DJ'),
        (6, 'Ator'),
        (7, 'Orquestra'),
        (8, 'Músico')"""),
    'CARTAO_DE_CREDITO': (
        """insert into CARTAO_DE_CREDITO (id_cartao_de_credito, nome_do_titular, codigo_de_seguranca, numero, data_de_validade) values
        (1, 'Maria Oliveira', 456, '3121 7442 4894 2345', '2026-08-01'),
        (2, 'João Silva', 789, '4257 9644 9909 3453', '2025-07-12'), 
        (3, 'Ana Pereira', 123, '8953 5367 6783 1314', '2024-06-03'), 
        (4, 'Carlos Sousa', 321, '4212 4156 7865 4321', '2026-12-05'), 
        (5, 'Lucia Fernandes', 654, '3178 7899 12300 3123', '2023-05-15')"""),
    'USUARIO': (
        """insert into USUARIO (id_usuario, email, celular, cpf, nome, estado, bairro, cidade, rua, numero) values
        (1, 'maria.oliveira@example.com', '(11) 91234-5678', '123.456.789-00', 'Maria Oliveira', 'SP', 'Centro', 'São Paulo', 'Rua das Flores', 120),
        (2, 'joao.silva@example.com', '(21) 98765-4321', '234.567.890-11', 'João Silva', 'RJ', 'Copacabana', 'Rio de Janeiro', 'Avenida Atlântica', 2500),
        (3, 'ana.pereira@example.com', '(31) 99887-6655', '345.678.901-22', 'Ana Pereira', 'MG', 'Savassi', 'Belo Horizonte', 'Rua da Bahia', 150),
        (4, 'carlos.sousa@example.com', '(41) 91234-1234', '456.789.012-33', 'Carlos Sousa', 'PR', 'Batel', 'Curitiba', 'Avenida Batel', 330),
        (5, 'lucia.fernandes@example.com', '(51) 97654-3210', '567.890.123-44', 'Lucia Fernandes', 'RS', 'Moinhos de Vento', 'Porto Alegre', 'Rua Padre Chagas', 400)"""),
    'PATROCINADOR': (
        """insert into PATROCINADOR (id_patrocinador, url_logomarca, url_site, nome) values
        (1, 'https://upload.wikimedia.org/wikipedia/commons/1/11/Logo_of_Coca-Cola.svg', 'https://www.coca-cola.com', 'Coca-Cola'),
        (2, 'https://upload.wikimedia.org/wikipedia/commons/7/73/Pepsi_logo_2014.svg', 'https://www.pepsi.com', 'Pepsi'),
        (3, 'https://upload.wikimedia.org/wikipedia/commons/6/6b/Netflix_2015_logo.svg', 'https://www.netflix.com', 'Netflix'),
        (4, 'https://upload.wikimedia.org/wikipedia/commons/1/1b/Spotify_logo_with_text.svg', 'https://www.spotify.com', 'Spotify'),
        (5, 'https://upload.wikimedia.org/wikipedia/commons/0/0c/Adidas_Logo.svg', 'https://www.adidas.com', 'Adidas')"""),
    'USUARIO_CARTAO_DE_CREDITO': (
        """insert into USUARIO_CARTAO_DE_CREDITO (id_cartao_de_credito, id_usuario) values
        (1, 1),
        (2, 2),
        (3, 3), 
        (4, 4), 
        (5, 5)"""),
    'ATRACAO': (
        """insert into ATRACAO (id_atracao, nome, id_tipo) values
        (1, 'Calbin Harris', 1),
        (2, 'The Rolling Stones', 2),
        (3, 'Tony Robbins', 3),
        (4, 'Jerry Seinfeld', 4),
        (5, 'David Guetta', 5),
        (6, 'Leonardo DiCaprio', 6),
        (7, 'Orquestra Filarmônica de Viena', 7),
        (8, 'John Mayer', 8),
        (9, 'Michael Bublé', 1),
        (10, 'Coldplay', 2),
        (11, 'Bruno Mars', 1),
        (12, 'U2', 2),
        (13, 'Brené Brown', 3),
        (14, 'Kevin Hart', 4),
        (15, 'Tiesto', 5),
        (16, 'Scarlett Johansson', 6),
        (17, 'Orquestra Sinfônica de Chicago', 7),
        (18, 'Ed Sheeran', 8),
        (19, 'Sam Smith', 1),
        (20, 'Foo Fighters', 2),
        (21, 'Justin Timberlake', 1),
        (22, 'Metallica', 2),
        (23, 'Simon Sinek', 3),
        (24, 'Amy Schumer', 4),
        (25, 'Martin Garrix', 5),
        (26, 'Brad Pitt', 6),
        (27, 'Orquestra Filarmônica de Berlim', 7),
        (28, 'Carlos Santana', 8),
        (29, 'Bruno Mars', 1),
        (30, 'Red Hot Chili Peppers', 2)"""),
    'EVENTO': (
        """insert into EVENTO (id_evento, data, nome, horario_inicio, id_local, id_categoria) values 
        (1, '2024-07-15', 'Noite de Rock', '20:00:00', 1, 1),
        (2, '2024-08-20', 'O Fantasma da Ópera', '19:00:00', 2, 2),
        (3, '2024-09-05', 'Risos Garantidos', '21:30:00', 3, 3),
        (4, '2024-10-10', 'Inovação e Tecnologia', '08:30:00', 4, 4),
        (5, '2024-11-25', 'Concerto Sinfônico', '18:30:00', 1, 5),
        (6, '2024-12-12', 'Magia do Teatro', '20:00:00', 2, 2),
        (7, '2025-01-20', 'Noite de Comédia', '22:00:00', 3, 3),
        (8, '2025-02-15', 'Palestra de Liderança', '09:00:00', 4, 4),
        (9, '2025-04-18', 'Noite de Música de Câmara', '19:00:00', 5, 5),
        (10, '2024-05-10', 'Festival de Rock Nacional', '19:00:00', 1, 1)"""),
    'EVENTO_ATRACAO': (
        """insert into EVENTO_ATRACAO (id_evento_atracao, horario_inicio, id_evento, id_atracao) values 
        (1, '20:00:00', 1, 1),
        (2, '20:30:00', 1, 2),
        (3, '21:00:00', 1, 10),
        (4, '21:30:00', 1, 22),
        (5, '19:00:00', 2, 6),
        (6, '19:30:00', 2, 16),
        (7, '20:00:00', 2, 26),
        (8, '21:30:00', 3, 4),
        (9, '22:00:00', 3, 14),
        (10, '22:30:00', 3, 24),
        (11, '08:30:00', 4, 3),
        (12, '09:00:00', 4, 13),
        (13, '09:30:00', 4, 23),
        (14, '18:30:00', 5, 7),
        (15, '19:00:00', 5, 17),
        (16, '19:30:00', 5, 27),
        (17, '20:00:00', 6, 6),
        (18, '20:30:00', 6, 16),
        (19, '21:00:00', 6, 26),
        (20, '22:00:00', 7, 4),
        (21, '22:30:00', 7, 14),
        (22, '23:00:00', 7, 24),
        (23, '09:00:00', 8, 3),
        (24, '09:30:00', 8, 13),
        (25, '10:00:00', 8, 23),
        (26, '19:00:00', 9, 7),
        (27, '19:30:00', 9, 17),
        (28, '20:00:00', 9, 27),
        (29, '19:00:00', 10, 1),
        (30, '19:30:00', 10, 2),
        (31, '20:00:00', 10, 10),
        (32, '20:30:00', 10, 22)"""),
    'EVENTO_PATROCINADOR': (
        """insert into EVENTO_PATROCINADOR (id_patrocinador, id_evento) values 
        (1, 1),
        (2, 1),
        (3, 2),
        (4, 2),
        (1, 3),
        (5, 3),
        (2, 4),
        (3, 4),
        (4, 5),
        (5, 5),
        (1, 6),
        (3, 6),
        (2, 6),
        (5, 7),
        (1, 8),
        (4, 8),
        (3, 8),
        (2, 9),
        (3, 9),
        (4, 10),
        (5, 10)"""),
    'INGRESSO': (
        """insert into INGRESSO (id_ingresso, id_ponto_de_venda, id_lote, id_evento) values 
        (1, 1, 1, 1), 
        (2, 1, 2, 1), 
        (3, 1, 3, 1),
        (4, 1, 4, 2), 
        (5, 1, 5, 2),
        (6, 1, 6, 3), 
        (7, 2, 7, 3), 
        (8, 2, 8, 3),
        (9, 2, 9, 4), 
        (10, 2, 10, 4), 
        (11, 2, 11, 4),
        (24, 2, 13, 5),
        (12, 2, 14, 6), 
        (13, 2, 15, 6), 
        (14, 2, 16, 6),
        (15, 1, 17, 7), 
        (16, 1, 18, 7), 
        (17, 1, 19, 7),
        (25, 1, 20, 8),
        (18, 3, 22, 9), 
        (19, 3, 23, 9), 
        (20, 3, 24, 9),
        (21, 3, 25, 10), 
        (22, 3, 26, 10), 
        (23, 3, 27, 10)"""),
    'COMPRA': (
        """insert into COMPRA (id_ingresso, id_cartao_de_credito, id_usuario, data) values 
        (1, 1, 1, '2024-06-01'),
        (2, 2, 2, '2024-07-02'),
        (3, 3, 3, '2024-07-11'),
        (4, 4, 4, '2024-07-01'),
        (5, 5, 5, '2024-08-01'),
        (6, 1, 1, '2024-08-01'),
        (7, 2, 2, '2024-08-16'),
        (8, 3, 3, '2024-08-31'),
        (9, 4, 4, '2024-08-01'),
        (10, 5, 5, '2024-09-02'),
        (11, 2, 2, '2024-10-01'),
        (12, 2, 2, '2024-07-02'),
        (13, 5, 5, '2024-08-03'),
        (14, 1, 1, '2024-08-02'),
        (15, 2, 2, '2024-08-13'),
        (16, 4, 4, '2024-08-31'),
        (17, 4, 4, '2024-08-01'),
        (18, 5, 5, '2024-09-02'),
        (19, 2, 2, '2024-10-02'),
        (24, 1, 1, '2024-11-04'),
        (25, 2, 2, '2025-01-03'),
        (21, 2, 2, '2024-04-01')
        """)
}

# Valores para deletar as tabelas
drop = {'COMPRA': (
    "drop table COMPRA"),
    'INGRESSO': (
    "drop table INGRESSO"),
    'PONTO_DE_VENDA': (
    "drop table PONTO_DE_VENDA"),
    'LOTE': (
        "drop table LOTE"),
    'EVENTO_ATRACAO': (
        "drop table EVENTO_ATRACAO"),
    'EVENTO_PATROCINADOR': (
        "drop table EVENTO_PATROCINADOR"),
    'EVENTO': (
        "drop table EVENTO"),
    'CATEGORIA': (
        "drop table CATEGORIA"),
    'ATRACAO': (
        "drop table ATRACAO"),
    'LOCAL': (
        "drop table LOCAL"),
    'TIPO': (
        "drop table TIPO"),
    'USUARIO_CARTAO_DE_CREDITO': (
        "drop table USUARIO_CARTAO_DE_CREDITO"),
    'CARTAO_DE_CREDITO': (
        "drop table CARTAO_DE_CREDITO"),
    'USUARIO': (
        "drop table USUARIO"),
    'PATROCINADOR': (
        "drop table PATROCINADOR"),
    'CARTAO_DE_CREDITO': (
        "drop table CARTAO_DE_CREDITO"),
}

# Valores para teste de update
update = {'PONTO_DE_VENDA': (
    """update PONTO_DE_VENDA
        SET bairro = 'Coloninha',
        numero = '4',
        cidade = 'Araranguá',
        estado = 'SC',
        rua = 'Getúlio vargas'
        where id_ponto_de_venda = 1"""),
    'LOTE': (
        """update LOTE
        SET data_fim = '2024-06-02'
        where id_lote = 1"""),
    'USUARIO': (
        """update USUARIO
        SET celular = '(11) 91234-5678'
        where id_usuario = 1"""),
    'ATRACAO': (
        """update ATRACAO
        SET nome = 'Freddie Mercury'
        where id_atracao = 1"""),
}

# Valores para teste de delete
delete = {'EVENTO_ATRACAO': (
    """delete from EVENTO_ATRACAO
        where id_atracao = 1 or id_atracao = 2"""),
    'ATRACAO': (
        """delete from ATRACAO
        where id_atracao = 1 or id_atracao = 2"""),
    'USUARIO_CARTAO_DE_CREDITO': (
        """delete from USUARIO_CARTAO_DE_CREDITO
        where (id_cartao_de_credito = 1 and id_usuario = 1) or (id_cartao_de_credito = 1 and id_usuario = 2)""")
}


# Funções
def connect_resgatocao():
    cnx = mysql.connector.connect(host='localhost', database='modelo', user='root', password='123')
    if cnx.is_connected():
        db_info = cnx.get_server_info()
        print("Conectado ao servidor MySQL versão ", db_info)
        cursor = cnx.cursor()
        cursor.execute("select database();")
        linha = cursor.fetchone()
        print("Conectado ao banco de dados ", linha)
        cursor.close()
    return cnx


def drop_all_tables(connect):
    print("\n---DROP DB---")
    # Esvazia o Banco de Dados
    cursor = connect.cursor()
    for drop_name in drop:
        drop_description = drop[drop_name]
        try:
            print("Deletando {}: ".format(drop_name), end='')
            cursor.execute(drop_description)
        except mysql.connector.Error as err:
            print(err.msg)
        else:
            print("OK")
    connect.commit()
    cursor.close()


def create_all_tables(connect):
    print("\n---CREATE ALL TABLES---")
    # Criação das tabelas
    cursor = connect.cursor()
    for table_name in tables:
        table_description = tables[table_name]
        try:
            print("Criando tabela {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("Tabela já existe.")
            else:
                print(err.msg)
        else:
            print("OK")
    connect.commit()
    cursor.close()


def show_table(connect):
    print("\n---SELECIONAR TABELA---")
    # Criação das tabelas
    cursor = connect.cursor()
    for table_name in tables:
        print("Nome: {}".format(table_name))
    try:
        name = input(str("\nDigite o nome da tabela que deseja consultar. ")).upper()
        select = "select * from " + name
        cursor.execute(select)
    except mysql.connector.Error as err:
        print(err.msg)
    else:
        print("TABELA {}".format(name))
        myresult = cursor.fetchall()
        for x in myresult:
            print(x)
    cursor.close()


def update_value(connect):
    print("\n---SELECIONAR TABELA PARA ATUALIZAÇÃO---")
    # Criação das tabelas
    cursor = connect.cursor()
    for table_name in tables:
        print("Nome: {}".format(table_name))
    try:
        name = input(str("\nDigite o nome da tabela que deseja consultar. ")).upper()
        for table_name in tables:
            table_description = tables[table_name]
            if table_name == name:
                print("Para criar a tabela: {}, foi utilizado o seguinte código {}".format(table_name,
                                                                                           table_description))
        atributo = input("Digite o atributo a ser alterado: ")
        valor = input("Digite o valor a ser atribuido: ")
        codigo_f = input("Digite a variavel primaria: ")
        codigo = input("Digite o codigo numerico: ")
        query = ['UPDATE ', name, ' SET ', atributo, ' = ', valor, ' WHERE ', codigo_f, '= ', codigo]
        sql = ''.join(query)
        cursor.execute(sql)
    except mysql.connector.Error as err:
        print(err.msg)
    else:
        print("Atributo atualizado")
    connect.commit()
    cursor.close()


def insert_test(connect):
    print("\n---INSERT TEST---")
    # Inesrsão dos valores nas tabelas
    cursor = connect.cursor()
    for insert_name in inserts:
        insert_description = inserts[insert_name]
        try:
            print("Inserindo valores para {}: ".format(insert_name), end='')
            cursor.execute(insert_description)
        except mysql.connector.Error as err:
            print(err.msg)
        else:
            print("OK")
    connect.commit()
    cursor.close()


def update_test(connect):
    print("\n---UPDATE TEST---")
    # Inesrsão dos valores nas tabelas
    cursor = connect.cursor()
    for update_name in update:
        update_description = update[update_name]
        try:
            print("Teste de atualização de valores para {}: ".format(update_name), end='')
            cursor.execute(update_description)
        except mysql.connector.Error as err:
            print(err.msg)
        else:
            print("OK")
    connect.commit()
    cursor.close()


def delete_test(connect):
    print("\n---DELETE TEST---")
    # Inesrsão dos valores nas tabelas
    cursor = connect.cursor()
    for delete_name in delete:
        delete_description = delete[delete_name]
        try:
            print("Teste de atualização de valores para {}: ".format(delete_name), end='')
            cursor.execute(delete_description)
        except mysql.connector.Error as err:
            print(err.msg)
        else:
            print("OK")
    connect.commit()
    cursor.close()


def consulta1(connect):
    select_query = """
    SELECT
            EVENTO.id_evento,
            EVENTO.nome,
            sum(valor)
    FROM 
            EVENTO,
            INGRESSO,
            LOTE,
            COMPRA
    WHERE 
            EVENTO.id_evento = INGRESSO.id_evento AND 
            INGRESSO.id_ingresso = COMPRA.id_ingresso AND
            INGRESSO.id_lote = LOTE.id_lote
    GROUP BY 
            EVENTO.id_evento
    ORDER BY 
            EVENTO.id_evento;
    """
    print("Primeira Consulta: Exibir o valor total arrecadado com a venda de ingressos para cada evento."
        "")
    cursor = connect.cursor()
    cursor.execute(select_query)
    myresult = cursor.fetchall()
    for x in myresult:
        print(x)


def consulta2(connect):
    select_query = """
    SELECT 
        EVENTO.id_evento,
        EVENTO.nome,
        count(*) 
    FROM 
        EVENTO,
        EVENTO_ATRACAO,
        ATRACAO
    WHERE 
        EVENTO.id_evento = EVENTO_ATRACAO.id_evento AND
        ATRACAO.id_atracao = EVENTO_ATRACAO.id_atracao
    GROUP BY 
        EVENTO.id_evento
    ORDER BY 
        EVENTO.id_evento;
    """
    print("\nSegunda Consulta: Mostrar o número de atrações em cada evento.")

    cursor = connect.cursor()
    cursor.execute(select_query)
    myresult = cursor.fetchall()
    for x in myresult:
        print(x)


def consulta3(connect):
    select_query = """
    SELECT 
        EVENTO.id_evento,
        EVENTO.nome,
        LOCAL.capacidade_maxima - count(*)
    FROM 
        EVENTO,
        INGRESSO,
        COMPRA,
        LOCAL
    WHERE 
        EVENTO.id_evento = INGRESSO.id_evento AND 
        INGRESSO.id_ingresso = COMPRA.id_ingresso AND
        EVENTO.id_local = LOCAL.id_local
    GROUP BY 
        EVENTO.id_evento, EVENTO.nome
    ORDER BY 
        EVENTO.id_evento;
    """
    print("\nTerceira Consulta: Exibir a quantidade de ingressos que restam ser vendidos para atingir a capacidade máxima de lotação em cada evento.")
    cursor = connect.cursor()
    cursor.execute(select_query)
    myresult = cursor.fetchall()
    for x in myresult:
        print(x)


def consulta_extra(connect):
    select_query = """
    SELECT 
        USUARIO.id_usuario,
        USUARIO.nome,
        count(*)
    FROM 
        USUARIO,
        COMPRA
    WHERE 
        USUARIO.id_usuario = COMPRA.id_usuario
    GROUP BY 
        USUARIO.id_usuario, USUARIO.nome
    ORDER BY 
        count(*) DESC;
    """
    print("\nConsulta Extra: Ranking de quantidade de compras por usuários.")
    cursor = connect.cursor()
    cursor.execute(select_query)
    myresult = cursor.fetchall()
    for x in myresult:
        print(x)


def exit_db(connect):
    print("\n---EXIT DB---")
    connect.close()
    print("Conexão ao MySQL foi encerrada")


def crud_resgatocao(connect):
    drop_all_tables(connect)
    create_all_tables(connect)
    insert_test(connect)

    print("\n---CONSULTAS BEFORE---")
    consulta1(connect)
    consulta2(connect)
    consulta3(connect)
    consulta_extra(connect)

    update_test(connect)
    delete_test(connect)

    print("\n---CONSULTAS AFTER---")
    consulta1(connect)
    consulta2(connect)
    consulta3(connect)
    consulta_extra(connect)


# Main
try:
    # Estabelece Conexão com o DB
    con = connect_resgatocao()

    power_up = 1
    while power_up == 1:
        interface = """\n       ---MENU---
        1.  CRUD RESGATOCAO
        2.  TEST - Create all tables
        3.  TEST - Insert all values
        4.  TEST - Update
        5.  TEST - Delete
        6.  CONSULTA 01
        7.  CONSULTA 02
        8.  CONSULTA 03
        9.  CONSULTA EXTRA
        10. Show Table
        11. Update Value
        12. CLEAR ALL RESGATOCAO
        0.  Disconnect DB\n """
        print(interface)

        choice = int(input("Opção: "))
        if choice < 0 or choice > 12:
            print("Erro tente novamente")
            choice = int(input())

        if choice == 0:
            if con.is_connected():
                exit_db(con)
                print("Muito obrigado.")
                break
            else:
                break

        if choice == 1:
            crud_resgatocao(con)

        if choice == 2:
            create_all_tables(con)

        if choice == 3:
            insert_test(con)

        if choice == 4:
            update_test(con)

        if choice == 5:
            delete_test(con)

        if choice == 6:
            consulta1(con)

        if choice == 7:
            consulta2(con)

        if choice == 8:
            consulta3(con)

        if choice == 9:
            consulta_extra(con)

        if choice == 10:
            show_table(con)

        if choice == 11:
            update_value(con)

        if choice == 12:
            drop_all_tables(con)

except mysql.connector.Error as err:
    print("Erro na conexão com o sqlite", err.msg)
