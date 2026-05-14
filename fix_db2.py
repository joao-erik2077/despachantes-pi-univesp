import sqlite3
try:
    conn = sqlite3.connect('app.db')
    conn.execute("DROP TABLE IF EXISTS documento_digitalizado")
    conn.execute("""
    CREATE TABLE documento_digitalizado (
        id INTEGER NOT NULL PRIMARY KEY,
        nome VARCHAR(255) NOT NULL,
        dados BLOB NOT NULL,
        mimetype VARCHAR(100) NOT NULL,
        veiculo_id INTEGER,
        FOREIGN KEY(veiculo_id) REFERENCES veiculo (id)
    )
    """)
    conn.commit()
    print("Table recreated successfully.")
except Exception as e:
    print(f"Error: {e}")
finally:
    if conn:
        conn.close()
