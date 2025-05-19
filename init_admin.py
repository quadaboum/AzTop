import os
import psycopg2
from werkzeug.security import generate_password_hash

PGHOST = os.getenv("PGHOST", "localhost")
PGDATABASE = os.getenv("PGDATABASE", "aztop")
PGUSER = os.getenv("PGUSER", "postgres")
PGPASSWORD = os.getenv("PGPASSWORD", "postgres")
PGPORT = os.getenv("PGPORT", 5432)

ADMIN_PSEUDO = "Topaz"
ADMIN_PASSWORD = "azertyuiop"

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
    cur.execute("SELECT id FROM "user" WHERE pseudo = %s", (ADMIN_PSEUDO,))
    if cur.fetchone():
        print(f"Un utilisateur '{ADMIN_PSEUDO}' existe déjà. Aucune action.")
    else:
        hash_pw = generate_password_hash(ADMIN_PASSWORD)
        cur.execute("""
            INSERT INTO "user" (pseudo, password, is_admin, level, prestige, last_ip, user_agent, money, donations, invite_code)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (ADMIN_PSEUDO, hash_pw, True, 666, 666, '127.0.0.1', 'init-script', 666, 0, 'INITCODEADMIN'))
        conn.commit()
        print(f"Utilisateur admin '{ADMIN_PSEUDO}' créé avec succès !")
    conn.close()

if __name__ == "__main__":
    main()
