# AzTop - Starter Pack

**Lancement rapide Railway/local :**

1. Crée ta base PostgreSQL (Railway ou local).
2. Configure un `.env` avec PGHOST, PGDATABASE, PGUSER, PGPASSWORD, PGPORT, SECRET_KEY.
3. `python init_db.py` pour créer les tables et le premier utilisateur admin AzTop.
4. `python app.py` pour lancer le serveur.
5. Connecte-toi avec AzTop / azertyuiop.

**Champs User** : pseudo, password (hashé), is_admin, level, prestige, last_ip, user_agent, money, donations, invite_code, created_at
**Tables** : user, invite_code, user_log

Pour ajouter d'autres admins, utilise `init_admin.py`.

v.0.1a