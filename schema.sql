-- Table principale des utilisateurs
CREATE TABLE IF NOT EXISTS "user" (
    id SERIAL PRIMARY KEY,
    pseudo VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    level INTEGER DEFAULT 1,
    prestige INTEGER DEFAULT 0,
    last_ip VARCHAR(45),
    user_agent VARCHAR(256),
    money INTEGER DEFAULT 0,
    donations INTEGER DEFAULT 0,
    invite_code VARCHAR(16),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des codes d’invitation générés
CREATE TABLE IF NOT EXISTS invite_code (
    id SERIAL PRIMARY KEY,
    code VARCHAR(16) UNIQUE NOT NULL,
    generated_by INTEGER REFERENCES "user"(id) ON DELETE SET NULL,
    used_by INTEGER REFERENCES "user"(id) ON DELETE SET NULL,
    is_used BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    used_at TIMESTAMP
);

-- Table de log de connexions utilisateur
CREATE TABLE IF NOT EXISTS user_log (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES "user"(id) ON DELETE CASCADE,
    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip VARCHAR(45),
    user_agent VARCHAR(256)
);
