-- Script that creates a function SafeDiv that divides
-- and returns the first by the second number or returns
-- 0 if second number == 0
DELIMITER $$ ;
CREATE FUNCTION SafeDiv(
	a INT,
	b INT
)
RETURNS FLOAT
DETERMINISTIC
BEGIN
	DECLARE result FLOAT;
	IF b = 0 THEN
		RETURN 0;
	END IF;
	SET result = (a * 1.0) / b;
	RETURN result;
END;$$
DELIMITER ;
