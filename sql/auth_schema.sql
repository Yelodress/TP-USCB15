-- Schéma minimal pour le service d'authentification
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(255) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Utilisateur par défaut simple (mot de passe en clair pour test)
INSERT IGNORE INTO users (username, password) VALUES
  ('user1', 'pass1');