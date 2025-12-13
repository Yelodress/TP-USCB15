-- Création de la table "question"
CREATE TABLE IF NOT EXISTS question (
  id INT AUTO_INCREMENT PRIMARY KEY,
  content VARCHAR(255) NOT NULL,
  answer BOOLEAN NOT NULL DEFAULT 0
);
INSERT INTO question (content, answer) VALUES
  ('Does the company offer a psychological support program?', 1),
  ('Do employees have a dedicated rest area?', 1),
  ('Are stress management trainings available?', 1),
  ('Is remote work prohibited in the company?', 0),
  ('Do managers receive specific training on workplace well-being?', 1),
  ('Can employees adjust their working hours freely?', 0),
  ('Are sporting activities organized regularly?', 1),
  ('Does the company enforce more than 50 hours of work per week?', 0),
  ('Is personalized monitoring of workload implemented?', 1),
  ('Are employees encouraged to take all their breaks?', 1),
  ('Do the offices have ergonomic equipment?', 1),
  ('Does the company refuse any diversity and inclusion policy?', 0),
  ('Can employees report an issue anonymously?', 1),
  ('Is an annual budget allocated to well-being and quality of work life?', 1),
  ('Are meetings routinely scheduled during lunch break?', 0);

CREATE TABLE IF NOT EXISTS api_keys (
  id INT AUTO_INCREMENT PRIMARY KEY,
  api_key VARCHAR(255) NOT NULL UNIQUE,
  description VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT IGNORE INTO api_keys (api_key, description) VALUES
  ('cle1', 'default key for testing');

-- Création de la table "user_answers" pour stocker les réponses des utilisateurs
CREATE TABLE IF NOT EXISTS user_answers (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL, -- Référence à l'ID de l'utilisateur
  question_id INT NOT NULL,
  reponse BOOLEAN NOT NULL,
  FOREIGN KEY (question_id) REFERENCES question(id) ON DELETE CASCADE,
  UNIQUE(user_id, question_id) -- Un utilisateur ne peut répondre qu'une seule fois à une question
);