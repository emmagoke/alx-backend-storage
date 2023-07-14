-- This query creates a stored procedure AddBonus that adds a new correction for a student.
-- Procedure AddBonus is taking 3 inputs (in this order):
-- user_id, a users.id value (you can assume user_id is linked to an existing users)
-- project_name, a new or already exists projects - if no projects.name found in the table,
-- you should create it score, the score value for the correction

DROP PROCEDURE IF EXISTS AddBonus;
DELIMITER // ;
CREATE PROCEDURE AddBonus(
      IN user_id INTEGER,
      IN project_name VARCHAR(255), 
      IN score INTEGER)
BEGIN
  -- DECLARE project_id_new INT;
  IF NOT EXISTS (SELECT name FROM projects WHERE name=project_name) THEN
    INSERT INTO projects (name) VALUES (project_name);
  END IF;
--   SET project_id_new = LAST_INSERT_ID();
-- ELSE
--   SELECT id INTO project_id_new FROM projects WHERE name=project_name;
-- END IF;
  INSERT INTO corrections (user_id, project_id, score)
    VALUES (user_id, (SELECT id FROM projects WHERE name=project_name), score);
END; //
DELIMITER;