-- A SQL script that creates a trigger that decreases the quantity of items
-- after adding a new order. The quantity of the items can be negative
CREATE TRIGGER decrease_items_quantity AFTER INSERT ON orders FOR EACH ROW
UPDATE items SET quantity = quantity - NEW.number WHERE name=NEW.item_name;
