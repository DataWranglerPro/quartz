As you may know, a lot of the code we write is repetitive. Yes, it is much better if you know exactly what most of the code is doing, but in general a lot of the code follows a similar pattern or template. Here are some [[pl sql]] templates I have used over the years.

# Basic pl sql block
``` sql
SET SERVEROUTPUT ON

DECLARE
BEGIN
	-- print
	dbms_output.put_line('hello world');
END;
/
```

# Select into
``` sql
SET SERVEROUTPUT ON

DECLARE
	-- declare variables
	v_name VARCHAR(20);
BEGIN
	-- get last name of one record
	SELECT col1
	  INTO v_name
	  FROM tbl1
	 WHERE ROWNUM < 2;
	 
	-- print
	dbms_output.put_line('last name is: ' || v_name);
END;
/
```

# Select into exception
``` sql
SET SERVEROUTPUT ON

DECLARE
	-- declare variables
	v_name VARCHAR(20);
BEGIN
	-- get last name of one record
	SELECT col1
	  INTO v_name
	  FROM tbl1
	 WHERE col2 = 5;

	EXCEPTION 
	WHEN NO_DATA_FOUND THEN
		v_name := NULL;
	 
	-- print
	dbms_output.put_line('last name is: ' || COALESCE(v_name, 'MISSING'));
END;
/
```


# Simple for loop
``` sql
SET SERVEROUTPUT ON

DECLARE
BEGIN
	-- loop through 9 records in tbl1
	FOR REC IN (SELECT col1
				  FROM tbl1
				 WHERE ROWNUM < 10)
		LOOP
			-- print
			dbms_output.put_line('last name is: ' || REC.col1);
		END LOOP;
END;
/
```


# For loop with cursor
``` sql
SET SERVEROUTPUT ON

DECLARE
	-- declare cursor
	CURSOR c1 IS
		SELECT col1
		  FROM tbl1
		 WHERE ROWNUM < 10;
BEGIN
	-- loop through 9 records in tbl1
	FOR REC IN c1
		LOOP
			-- print
			dbms_output.put_line('last name is: ' || REC.col1);
		END LOOP;
END;
/
```


# Simple function
``` sql
SET SERVEROUTPUT ON

DECLARE
	-- declare function
	FUNCTION get_num(p_par1 IN NUMBER) RETURN NUMBER
	IS
		v_num NUMBER := NULL;
	BEGIN
		SELECT col1
		  INTO v_num
		  FROM tbl1
		 WHERE col2 = p_par1;
	RETURN v_num;
	END get_num;
BEGIN
	-- call function and print
	dbms_output.put_line('number is: ' || get_num(10));
END;
/
```

# Simple procedure
``` sql
SET SERVEROUTPUT ON

DECLARE
	-- declare variables
	v_out NUMBER;

	-- declare function
	PROCEDURE get_num(p_par1 IN NUMBER, p_par2 OUT NUMBER)
	IS
	BEGIN
		SELECT col1
		  INTO p_par2
		  FROM tbl1
		 WHERE col2 = p_par1;
	END;
BEGIN
	-- call proc and print
	get_num(10, v_out);
	dbms_output.put_line('number is: ' || v_out);
END;
/
```


# Commit every n rows
``` sql
SET SERVEROUTPUT ON

DECLARE
	-- declare variables
	v_LIMIT_IN PLS_INTEGER DEFAULT 1000; -- commit every 1000 updates

	-- declare cursor
	CURSOR c1 IS
		SELECT col1
		  FROM tbl1
		 WHERE ROWNUM < 10;

	TYPE tt_tbl1 IS TABLE OF c1%ROWTYPE INDEX BY PLS_INTEGER;
	t_tbl1 tt_tbl1;
BEGIN
OPEN c1;
	LOOP
		FETCH c1
		BULK COLLECT INTO t_tbl1 LIMIT v_LIMIT_IN;
	
		FOR indx IN 1 .. t_tbl1.COUNT
		LOOP
			-- do stuff
			-- here is how you get your data: t_tbl1(indx).col1
		END LOOP;

		commit;

		EXIT WHEN c1%NOTFOUND;
	END LOOP;
CLOSE c1;
END;
/
```


# record table
``` plsql
DECLARE

	-- declare variables
	v_id NUMBER :=0;

	-- declare cursor
	CURSOR c2 IS
		SELECT col1
		  FROM tbl1
		 WHERE ROWNUM < 10;
		 
	-- we delcare our table columns here
	TYPE rec is RECORD (
		a NUMBER;
		b NUMBER;
	);
	
	-- we declare our table type
	TYPE t_rec IS TABLE of rec INDEX BY BINARY_INTEGER;

	initrec rec;
	c_rec t_rec;
BEGIN
	FOR REC in c2
		LOOP
			-- initialize table
			IF NOT c_rec.exists(REC.col1) THEN
				c_rec(REC.col1) := initrec;
			END IF;

			-- add data to table
			c_rec(REC.col1) := REC.col2;
		END LOOP;

	-- loop through the table if it has data
	IF c_rec.FIRST IS NOT NULL THEN
		v_id := c_rec.FIRST;

		LOOP
			EXIT WHEN v_id IS NULL;
				DBMS_OUTPUT.PUT_LINE(c_rec(v_id).col1);
			v_id := c_rec.NEXT(v_id);
		END LOOP;
	END IF;
END;
/
```