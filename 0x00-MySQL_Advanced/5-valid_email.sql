-- This query creates a trigger that resets the attribute valid_email
-- only when the email has been changed.
DELIMITER $$$
CREATE TRIGGER `valid_email_change`
AFTER UPDATE ON `users` FOR EACH ROW
BEGIN
  IF
    NEW.email != OLD.email SET NEW.valid_email
  END IF
END $$$
DELIMITER;