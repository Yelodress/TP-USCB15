-- ...existing code...
-- Création de la table "question"
CREATE TABLE IF NOT EXISTS question (
  id INT AUTO_INCREMENT PRIMARY KEY,
  content VARCHAR(255) NOT NULL,
  answer BOOLEAN NOT NULL DEFAULT 0
);

-- Insertion des questions sur le bien-être en entreprise
INSERT INTO question (content, answer) VALUES
  ('L’entreprise propose-t-elle un programme de soutien psychologique ?', 1),
  ('Les employés disposent-ils d’un espace de repos dédié ?', 1),
  ('Des formations sur la gestion du stress sont-elles disponibles ?', 1),
  ('Le télétravail est-il interdit dans l’entreprise ?', 0),
  ('Les managers reçoivent-ils une formation spécifique au bien-être au travail ?', 1),
  ('Les employés peuvent-ils ajuster leurs horaires librement ?', 0),
  ('Des activités sportives sont-elles organisées régulièrement ?', 1),
  ('L’entreprise impose-t-elle plus de 50 heures de travail par semaine ?', 0),
  ('Un suivi personnalisé de la charge de travail est-il mis en place ?', 1),
  ('Les salariés sont-ils encouragés à prendre toutes leurs pauses ?', 1),
  ('Les bureaux disposent-ils d’équipements ergonomiques ?', 1),
  ('L’entreprise refuse-t-elle toute politique de diversité et d’inclusion ?', 0),
  ('Les employés peuvent-ils signaler anonymement un problème ?', 1),
  ('Un budget annuel est-il alloué au bien-être et à la qualité de vie au travail ?', 1),
  ('Les réunions sont-elles systématiquement programmées pendant la pause déjeuner ?', 0);

-- ...existing code...
-- Création de la table api_keys et insertion d'une clé par défaut
CREATE TABLE IF NOT EXISTS api_keys (
  id INT AUTO_INCREMENT PRIMARY KEY,
  api_key VARCHAR(255) NOT NULL UNIQUE,
  description VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT IGNORE INTO api_keys (api_key, description) VALUES
  ('cle1', 'default key for testing');