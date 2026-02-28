-- Création de la table "question"
CREATE TABLE IF NOT EXISTS question (
  id INT AUTO_INCREMENT PRIMARY KEY,
  content VARCHAR(255) NOT NULL,
  answer BOOLEAN NOT NULL DEFAULT 0
);
INSERT INTO question (content) VALUES
  ('Does the company offer a psychological support program?'),
  ('Do employees have a dedicated rest area?'),
  ('Are stress management trainings available?'),
  ('Is remote work prohibited in the company?'),
  ('Do managers receive specific training on workplace well-being?'),
  ('Can employees adjust their working hours freely?'),
  ('Are sporting activities organized regularly?'),
  ('Does the company enforce more than 50 hours of work per week?'),
  ('Is personalized monitoring of workload implemented?'),
  ('Are employees encouraged to take all their breaks?'),
  ('Do the offices have ergonomic equipment?'),
  ('Does the company refuse any diversity and inclusion policy?'),
  ('Can employees report an issue anonymously?'),
  ('Is an annual budget allocated to well-being and quality of work life?'),
  ('Are meetings routinely scheduled during lunch break?');

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
  response BOOLEAN NOT NULL,
  image_path VARCHAR(255) DEFAULT NULL, -- Path to an optional image for the answer
  FOREIGN KEY (question_id) REFERENCES question(id) ON DELETE CASCADE,
  UNIQUE(user_id, question_id) -- Un utilisateur ne peut répondre qu'une seule fois à une question
);