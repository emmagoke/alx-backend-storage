-- This query creates a trigger that resets the attribute valid_email
-- only when the email has been changed.
DROP TRIGGER IF EXISTS `valid_email_change`;
DELIMITER $$$
CREATE TRIGGER `valid_email_change`
BEFORE UPDATE ON `users` FOR EACH ROW
BEGIN
  IF NEW.email != OLD.email THEN SET NEW.valid_email = 0;
  ELSE
    SET NEW.valid_email = NEW.valid_email
  END IF;
END $$$
DELIMITER;