import sqlite3
conn = sqlite3.connect('app.db')
conn.execute("ALTER TABLE processo ADD COLUMN status VARCHAR(50) NOT NULL DEFAULT 'Em Andamento'")
conn.commit()
conn.close()
