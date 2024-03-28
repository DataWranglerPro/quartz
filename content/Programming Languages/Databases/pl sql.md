At some point you have to touch the database and this means you need to learn SQL. My recent jobs mainly used Oracle, so this is what we will learn today.

# How to clear screen (sqlplus)
``` sql
clear screen
```

# How to find the name of the schema
``` sql
SELECT user FROM DUAL;
```

# How to select n number of rows
``` sql
SELECT *
FROM (SELECT * FROM suppliers ORDER BY supplier_name DESC) suppliers2
WHERE rownum <= n
ORDER BY rownum;
```

# How to declare variables
``` plsql
DECLARE
	Num NUMBER;
	Num2 NUMBER(n);
	Num3 NUMBER(10,2);
	Num4 NUMBER := 50; -- add default value
	Num5 CONSTANT NUMBER := 10; – constant means the value can never be changed
	Text VARCHAR2(n);
	Text2 CHAR(n);
	Bool BOOLEAN;
	Datez DATE;

-- the begin/end blocks need to be present
BEGIN
	DBMS_OUTPUT.PUT_LINE('hello');
END;
/ -- this has to be placed here for the script to work
```

# How to set variables
``` plsql
DECLARE
	v_num NUMBER(9);

BEGIN
	SELECT col1
	  INTO v_num
	  FROM tbl1;
	    
	DBMS_OUTPUT.PUT_LINE(v_num);
END;
/
```

# How to print
``` sql
DBMS_OUTPUT.PUT_LINE('hello');
PROMPT hello
SELECT 'hello' FROM DUAL;
```

# How to declare dictionary type variables
``` plsql
DECLARE
	TYPE rec is RECORD (
		a NUMBER;
		b NUMBER;
	);
	
	var1 rec;
BEGIN
	var1.a := 10;
	var2.b := 20;
	DBMS_OUTPUT.PUT_LINE('----> ' || var1.a || ' ' || var1.b);
END;
/
```

# How to get first of month or last day of month
``` sql
LAST_DAY(somedatevalue);
FIRST_DAY(somedatevalue);
```

# How to get the current date
``` sql
SELECT SYSDATE, current_date FROM DUAL;
```

# How to extract year, month, and day
``` sql
EXTRACT(year from somedatevalue);
EXTRACT(month from somedatevalue);
EXTRACT(day from somedatevalue);
```

# How to get Monday/Sunday of previous week
``` sql
SELECT next_day (sysdate-7, 'MONDAY') Last_Monday, 
	   next_day (sysdate-7, SUNDAY) Last_Sunday
  FROM DUAL;
```

# How to get the next monday
``` sql
SELECT next_day (sysdate, 'MONDAY') as Next_Monday
  FROM dual;
```

# How to convert to number
``` sql
TO_NUMBER('100');
```

# How to select unique values (no duplicates)
``` sql
SELECT DISTINCT col1
  FROM tbl1
 WHERE rownum < 5;
```

# How to redirect output to a file (sqlplus)
``` sql
SPOOL file_name.txt
	-- stuff
SPOOL OFF;
```

# How to create a cursor
``` plsql
/*
	Cursor Attributes
	-- C1%ISOPEN (Boolean)
	-- C1%FOUND (Boolean)
	-- C1%NOTFOUND (Boolean)
	-- C1%ROWCOUNT (similar to enumerate, a row count)
*/

DECLARE 
	nm as VARCHAR2(45);
	CURSOR c1 is SELECT * FROM tbl;
BEGIN  
	OPEN c1;
	LOOP
		FETCH c1 INTO nm;
		EXIT WHEN c1%NOTFOUND;
		DBMS_OUTPUT.PUT_LINE(nm);
	END LOOP;
	CLOSE c1;
END;
-----------------------------------------
-----------------------------------------
DECLARE 
	CURSOR c1 is SELECT * FROM tbl;
BEGIN  
	FOR x in c1 
	LOOP
		DBMS_OUTPUT.PUT_LINE(x.ColumnName);
	END LOOP;
END;
-----------------------------------------
-----------------------------------------
DECLARE 
	CURSOR c1(num NUMBER) IS 
	SELECT * 
	  FROM tbl 
      WHERE col=num;
BEGIN  
	FOR x in c1 (n)
	LOOP
		DBMS_OUTPUT.PUT_LINE(x.ColumnName);
	END LOOP;
END;
-----------------------------------------
-----------------------------------------
DECLARE 
	TYPE arr1  IS TABLE OF NUMBER;
	One arr1;	

	CURSOR c1 IS 
	SELECT * 
	  FROM tbl;
BEGIN  
	OPEN c1;
	FETCH c1 BULK COLLECT INTO one;
	CLOSE c1;

	FOR x in one.FIRST .. one.LAST
	LOOP
		EXIT WHEN c1%NOTFOUND;
		DBMS_OUTPUT.PUT_LINE(x.ColumnName);
	END LOOP;
END;
```

# How to create a variable table
``` plsql
DECLARE
	-- we delcare our table columns here
	TYPE rec is RECORD (
		a NUMBER;
		b NUMBER;
	);
	
	-- we declare our table type
	TYPE t_rec IS TABLE of rec INDEX BY BINARY_INTEGER;

	-- this is the actual table named c_rec
	c_rec t_rec;
BEGIN
	-- insert into our variable
	SELECT col1
	  BULK COLLECT INTO c_rec
	  FROM tbl1
	 WHERE rownum < 5;

	-- loop through the table if it has data
	IF c_rec.FIRST IS NOT NULL THEN
		FOR i in c_rec.FIRST .. c_rec.LAST
			LOOP
				-- print record
				DBMS_OUTPUT.PUT_LINE(c_rec(i).col1);
			END LOOP;
	END IF;
END;
/
```

# How to create a function
``` plsql
DECLARE
	-- create function
	FUNCTION f_add(v_num IN NUMBER) RETURN NUMBER
	/* receives number, adds 1,000 and returns the result */
	IS
	BEGIN
		RETURN v_num + 1000;
	END f_add;
	
BEGIN
	-- run and print function output
	DBMS_OUTPUT.PUT_LINE(f_add(28));
END;
/
```

# How to create a procedure
``` plsql
DECLARE
	-- variable that holds the final result
	v_result NUMBER;
	
	-- create procedure
	PROCEDURE p_add(v_num IN NUMBER, v_dummy OUT NUMBER)
	/* receives number, adds 1,000 and returns the result 
	   in a variable named v_result
	*/
	IS
	BEGIN
		-- add 1000 to output
		v_dummy := v_num + 1000;
	END;
	
BEGIN
	-- run proc, save the results in the variable v_result
	p_add(28, v_result);

	-- print proc output
	DBMS_OUTPUT.PUT_LINE(v_result);
END;
/
```

# How to create a CTE
``` plsql
WITH test
AS (SELECT * FROM tbl1 WHERE ROWNUM < 5)
SELECT * from test;
```

# How to delete the execution plan table
``` sql
DELETE plan_table;
COMMIT;
```

# How to do date math
``` sql
SELECT TO_DATE('01/10/2008', 'mm/dd/yyyy') - TO_DATE('01/10/2007', 'mm/dd/yyyy') FROM DUAL;

SELECT TRUNC(TO_DATE('01/10/2008', 'mm/dd/yyyy')) - TRUNC(TO_DATE('01/10/2007', 'mm/dd/yyyy')) FROM DUAL;
```

# How to search within stored procedures
``` sql
SELECT * FROM user_source WHERE UPPER('some_text') LIKE '%BLAH%';
```
# How to pick a random sample from a table
``` sql
SELECT * FROM tbl1(10) ORDER BY DBMS_RANDOM.VALUE;
```

# How to create a temp table
``` sql
DECLARE LOCAL TEMPORARY TABLE tbl1( 
  supplier_id number(10) not null,
  supplier_name varchar2(50) not null,
  contact_name varchar2(50)
);
```

# How to update a table
``` sql
UPDATE t1
	SET COL = 1
  FROM tbl t1
 WHERE COL2 = 6;
```

# How to insert into a table
``` sql
INSERT INTO suppliers (supplier_id, supplier_name)
SELECT account_no, name
  FROM customers
  WHERE customer_id > 5000;
```

# How to join two tables
``` sql
SELECT t1.column
  FROM table1 t1
  JOIN table2 t2 ON (t1.column = t2.column);
```


# How to select rows in ascending order
``` sql
SELECT * FROM suppliers ORDER BY supplier_name;
```

# How to select rows in descending order
``` sql
SELECT * FROM suppliers ORDER BY supplier_name DESC;
```

# How to write IF/THEN statements
``` sql
IF (condition) THEN
	-- do stuff
END IF;

IF (condition) THEN
	-- do stuff
ELSE
	-- do stuff
END IF;

IF (condition) THEN
	-- do stuff
ELSIF (condition) THEN
	-- do stuff
END IF;
```

# How to write Loops
``` sql
LOOP
   monthly_value := daily_value * 31;
   EXIT WHEN monthly_value > 4000;
END LOOP;
--
WHILE monthly_value <= 4000
LOOP
   monthly_value := daily_value * 31;
END LOOP;
--
FOR loop_counter IN [REVERSE] lowest_number..highest_number
LOOP
   {...statements...}
END LOOP;
--
FOR Lcntr IN 1..20
LOOP
   LCalc := Lcntr * 31;
END LOOP;
```

# How to check for NULL values
``` sql
SELECT *
FROM suppliers
WHERE supplier_name IS NULL;
```

# How to write an update statement with a sub query
``` sql
UPDATE customers
SET c_details = (SELECT contract_date
                 FROM suppliers
                 WHERE suppliers.supplier_name = customers.customer_name)
WHERE customer_id < 1000;
```

# How to use the Keyword "IN"
``` sql
SELECT *
FROM customers
WHERE customer_name IN ('IBM', 'Hewlett Packard', 'Microsoft');
```

# How to count all of the rows in a table
``` sql
SELECT COUNT(*) AS 'Number of employees'
FROM employees;
```

# How to delete contents of a table
``` sql
DELETE FROM customers
 WHERE last_name = 'Smith';
```

# How to select the smallest/largest value in a column
``` sql
SELECT department, MIN(salary) AS "Lowest salary"
  FROM employees
 GROUP BY department;
```

# How to pause for n number of seconds
``` sql
dbms_lock.sleep( Number_of_seconds );
```

# How to string match
``` sql
SELECT supplier_name
  FROM suppliers
 WHERE supplier_name LIKE 'Sm_th'
   AND last_name LIKE '%er%';
```

# How to permanently delete a table
``` sql
DROP TABLE table_name;
```

# How to cast a string into a date
``` sql
TO_DATE(‘1/1/2015’, ‘MM/DD/YYYY’)
```


