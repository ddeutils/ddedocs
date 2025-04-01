# SQL Script

Implementation of SQL scripting in a preview of Spark 4 is progressing well.
Although a few months are still ahead of us till we see Spark 4 in databricks,
thanks to the fact that Spark 4 Preview, as always, is also open source,
we can use the back door to see what is coming.

Compound Statements & Local Variables

```sql
BEGIN
  DECLARE counter INT DEFAULT 1;
  DECLARE total INT DEFAULT 0;

  WHILE counter <= 5 DO
    SET total = total + counter;
    SET counter = counter + 1;
  END WHILE;

  SELECT total AS sum_of_first_five;
END;
```

Condition Handling with `DECLARE HANDLER`

```sql
BEGIN
  DECLARE EXIT HANDLER FOR SQLSTATE '23505'  -- e.g. unique constraint
  BEGIN
    INSERT INTO error_logs VALUES('Duplicate key detected');
  END;

  -- Attempt to insert a duplicate row
  INSERT INTO users VALUES (42, 'alice@example.com');
  INSERT INTO users VALUES (42, 'alice@example.com');  -- triggers the handler

  SELECT 'Done' AS status;
END;
```

Looping Constructs: `FOR`, `REPEAT`, `WHILE`

```sql
BEGIN
  DECLARE even_count INT DEFAULT 0;

  FOR row AS
    SELECT val FROM (VALUES (1), (2), (3), (4), (5)) AS t(val)
  DO
    IF (row.val % 2 = 0) THEN
      SET even_count = even_count + 1;
    END IF;
  END FOR;

  SELECT even_count AS number_of_evens;
END;
```

Working with Cursors (`DECLARE`, `OPEN`, `FETCH`, `CLOSE`)

```sql
BEGIN
  DECLARE temp_val INT;
  DECLARE cur CURSOR FOR SELECT val FROM range(1, 4);

  OPEN cur;
  FETCH cur INTO temp_val;  -- fetch row1 => 1
  INSERT INTO cursor_demo VALUES (temp_val);

  FETCH cur INTO temp_val;  -- fetch row2 => 2
  INSERT INTO cursor_demo VALUES (temp_val);

  -- more FETCH operations ...

  CLOSE cur;
END;
```

Enhanced `SET VARIABLE` for Session or Script-Local Variables

```sql
DECLARE VARIABLE region STRING DEFAULT 'EMEA';
DECLARE VARIABLE sales_threshold DECIMAL(10,2) DEFAULT 1000.00;

-- Update a variable directly
SET VARIABLE region = 'APAC';

-- Assign the result of a query to a variable
SET VARIABLE sales_threshold = (
  SELECT avg(total_amount) FROM orders WHERE region = region
);

SELECT region AS current_region, sales_threshold AS threshold;
```

Creating and Calling Procedures

```sql
CREATE OR REPLACE PROCEDURE compute_bonus(
  IN base_salary DECIMAL(10,2),
  IN bonus_rate DECIMAL(5,4),
  OUT result DECIMAL(10,2)
)
LANGUAGE SQL
AS
BEGIN
  SET result = base_salary * bonus_rate;
END;

-- Call the procedure
CALL compute_bonus(1500.00, 0.10, ?);
-- Above call returns: result => 150.00
```

Signaling Errors and Retrieving Diagnostics

```sql
BEGIN
  DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
  BEGIN
    DECLARE err_state STRING;
    DECLARE err_message STRING;
    GET DIAGNOSTICS CONDITION 1
      err_state = RETURNED_SQLSTATE,
      err_message = MESSAGE_TEXT;
    INSERT INTO error_log VALUES(err_state, err_message, current_timestamp());
  END;

  -- Force an error to test logging
  SIGNAL SQLSTATE '45001' SET MESSAGE_TEXT = 'Custom error triggered';

  SELECT 'Script continued' AS status;  -- This won't run due to EXIT handler
END;
```

exceptions thrown from parser/interpreter

```sql
BEGIN
  DECLARE x INT;
  SET x = 'abc';  -- Error: type mismatch
END;
```

Support for labels

```sql
BEGIN label_one:
  BEGIN label_two:
    LEAVE label_one;  -- Jump out of label_one’s block
    SELECT 'Should not be reached' AS unreachable;
  END label_two;
  SELECT 'Reached' AS success;
END label_one;
```

Support for IF ELSE statement

```sql
BEGIN
  DECLARE test_value INT DEFAULT 2;
  IF test_value < 5 THEN
    SELECT 'Small' AS category;
  ELSE
    SELECT 'Large' AS category;
  END IF;
END;
```

Support for CASE statement

```sql
BEGIN
  DECLARE choice INT DEFAULT 3;
  CASE
    WHEN choice = 1 THEN SELECT 'One' AS result;
    WHEN choice = 3 THEN SELECT 'Three' AS result;
    ELSE SELECT 'Unknown' AS result;
  END CASE;
END;
```

Support for LOOP statement

```sql
BEGIN
  DECLARE counter INT DEFAULT 0;
  loop_block: LOOP
    IF counter >= 2 THEN
      LEAVE loop_block;
    END IF;
    INSERT INTO log VALUES (counter);
    SET counter = counter + 1;
  END LOOP loop_block;
END;
```

Support for REPEAT statement

```sql
BEGIN
  DECLARE x INT DEFAULT 0;
  REPEAT
    SET x = x + 2;
  UNTIL x >= 6 END REPEAT;
  SELECT x AS final_value;  -- 6
END;
```

Support for ITERATE statement

```sql
BEGIN
  DECLARE i INT DEFAULT 0;
  count_loop: WHILE i < 5 DO
    SET i = i + 1;
    IF i = 3 THEN
      ITERATE count_loop;  -- skip the rest for i=3
    END IF;
    INSERT INTO iteration_log VALUES (i);
  END WHILE;
END;
```

Exception handling

```sql
BEGIN
  DECLARE EXIT HANDLER FOR SQLSTATE '22012'  -- division by zero
  BEGIN
    INSERT INTO error_log VALUES('Division by zero occurred');
  END;

  SELECT 10 / 0;  -- triggers the handler
END;
```

Support for multiple variable declarations in the same statement

```sql
BEGIN
  DECLARE a INT, b STRING DEFAULT 'test', c DECIMAL(10,2);
  SELECT a, b, c;
END;
```

Support for RESIGNAL statement

```sql
BEGIN
  DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
  BEGIN
    RESIGNAL SQLSTATE '45001'
      SET MESSAGE_TEXT = 'Re-throwing a custom error';
  END;
  SIGNAL SQLSTATE '22012';  -- any error triggers the handler
END;
```

Support for PRINT/TRACE statement

```sql
BEGIN
  PRINT 'Starting script';  -- Not yet implemented
  SELECT 'Some logic here';
END;
```

## References

- [SQL scripting in Spark 4](https://databrickster.medium.com/sql-scripting-in-spark-4-296e22bf1f11)
