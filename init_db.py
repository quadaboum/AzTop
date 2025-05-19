import os
import psycopg2
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv

load_dotenv()

PGHOST = os.getenv("PGHOST", "localhost")
PGDATABASE = os.getenv("PGDATABASE", "aztop")
PGUSER = os.getenv("PGUSER", "postgres")
PGPASSWORD = os.getenv("PGPASSWORD", "postgres")
PGPORT = os.getenv("PGPORT", 5432)

def main():
    print("Connexion à la base PostgreSQL...")
    conn = psycopg2.connect(
        host=PGHOST,
        database=PGDATABASE,
        user=PGUSER,
        password=PGPASSWORD,
        port=PGPORT
    )
    cur = conn.cursor()
    with open('schema.sql', 'r', encoding='utf-8') as f:
        cur.execute(f.read())
        conn.commit()
    pseudo = "AzTop"
    password = "azertyuiop"
    hash_pw = generate_password_hash(password)
    cur.execute("SELECT id FROM "user" WHERE pseudo = %s", (pseudo,))
    if not cur.fetchone():
        cur.execute("""
            INSERT INTO "user" (pseudo, password, is_admin, level, prestige, last_ip, user_agent, money, donations, invite_code)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (pseudo, hash_pw, True, 666, 666, '127.0.0.1', 'init-script', 666, 0, 'INITCODE666'))
        conn.commit()
        print("Utilisateur AzTop (admin) créé !")
    else:
        print("Utilisateur AzTop déjà présent.")
    conn.close()

if __name__ == "__main__":
    main()
