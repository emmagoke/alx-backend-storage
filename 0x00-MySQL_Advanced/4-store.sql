-- This query creates a trigger that decreases the quantity
-- of an item after adding a new order.
DELIMITER $$$
CREATE TRIGGER `items_change`
AFTER INSERT ON `orders` FOR EACH ROW
BEGIN
  -- DECLARE old_quant INT;
  -- SELECT quantity INTO old_quant FROM items WHERE name = NEW.item_name;
  UPDATE items SET quantity = quantity - NEW.number
         WHERE name = NEW.item_name;
END $$$
DELIMITER ;