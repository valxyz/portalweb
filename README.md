# CaptiveWeb

Dependencias

```bash
pip install Flask
pip install Flask-SQLAlchemy
pip install waitress
pip install Werkzeug
pip install Paste
```

Base de datos SQLite
`./database/Database.db`

```sql
CREATE TABLE IF NOT EXISTS Users ( 
id INTEGER PRIMARY KEY AUTOINCREMENT, 
username TEXT NOT NULL UNIQUE, 
password TEXT NOT NULL, 
created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP 
);
```

```sql
CREATE TABLE IF NOT EXISTS Logins(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    ip_address TEXT NOT NULL,
    user_agent TEXT NULL,
    session_started_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    session_ended_at TEXT NULL,
    is_active INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
);
```

```sql
CREATE TABLE IF NOT EXISTS Profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    first_name TEXT,
    last_name TEXT,
    card_id TEXT,
    phone_number TEXT,
    email TEXT UNIQUE,
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
);
```

Ejemplo crear nuevo usario

`sqlite3 Database.db`

```sql
INSERT INTO Users (username, password) VALUES ('admin', 'abc123');

INSERT INTO Users (username, password) VALUES ('jaime.bernal', 'jb_rasp7283wt');
INSERT INTO Users (username, password) VALUES ('thais.samudio', 'ths19_1234');
INSERT INTO Users (username, password) VALUES ('orlando.montenegro', 'orl001_mt12');
INSERT INTO Users (username, password) VALUES ('luis.caballero', 'ls99_cl1666');

INSERT INTO Profiles (user_id, first_name, last_name, card_id, phone_number, email)VALUES (2, 'Jaime', 'Bernal', '8-222-1919', '6933-7777', 'jaime.bernal1@utp.ac.pa');
INSERT INTO Profiles (user_id, first_name, last_name, card_id, phone_number, email)VALUES (3, 'Thais', 'Samudio', '4-333-1212', '6777-4444', 'thais.samudio@utp.ac.pa');
INSERT INTO Profiles (user_id, first_name, last_name, card_id, phone_number, email)VALUES (4, 'Orlando', 'Montenegro', '4-666-9191', '6191-8888', 'orlando.montenegro2@utp.ac.pa');
INSERT INTO Profiles (user_id, first_name, last_name, card_id, phone_number, email)VALUES (5, 'Luis', 'Caballero', '4-111-6565', '6393-3333', 'luis.caballero6@utp.ac.pa');
```

`.quit`


Ejemplo limpiar tabla
```sql
-- Para eliminar todas las filas
DELETE FROM Logins;

-- Para reiniciar el contador AUTOINCREMENT (opcional)
DELETE FROM sqlite_sequence WHERE name='Logins';

-- Para verificar (opcional)
SELECT COUNT(*) FROM Logins;
```

Ejecutar servidor web

```bash
python app.py
```
