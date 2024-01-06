* 03/05/2014 - Created tutorial
`Cursors?`
`	C1%ISOPEN (Boolean)`
`	C1%FOUND (Boolean)`
`	C1%NOTFOUND (Boolean)`
`	C1%ROWCOUNT (similar to enumerate, a row count)`
`DECLARE` 
`nm as VARCHAR2(45);`
`CURSOR c1 is SELECT * FROM tbl;`
`BEGIN`  
`OPEN c1;`
`LOOP`
`FETCH c1 INTO nm;`
`EXIT WHEN c1%NOTFOUND;`
`DBMS_OUTPUT.PUT_LINE(nm);`
`END LOOP;`
`CLOSE c1;`
`END;`
`DECLARE` 
`CURSOR c1 is SELECT * FROM tbl;`
`BEGIN`  
`FOR x in c1` 
`LOOP`
`DBMS_OUTPUT.PUT_LINE(x.ColumnName);`
`END LOOP;`
`END;`
`DECLARE` 
`CURSOR c1(num NUMBER) IS` 
`SELECT *` 
`FROM tbl WHERE col=num;`
`BEGIN`  
`FOR x in c1 (n)`
`LOOP`
`DBMS_OUTPUT.PUT_LINE(x.ColumnName);`
`END LOOP;`
`END;`
`DECLARE` 
	`TYPE arr1  IS TABLE OF NUMBER;`
	`One arr1;`	
`CURSOR c1 IS` 
`SELECT *` 
`FROM tbl;`
`BEGIN`  
`OPEN c1;`
`FETCH c1 BULK COLLECT INTO one;`
`CLOSE c1;`
`FOR x in one.FIRST .. one.LAST`
`LOOP`
	`EXIT WHEN c1%NOTFOUND;`
`DBMS_OUTPUT.PUT_LINE(x.ColumnName);`
`END LOOP;`
`END;`

`-- How to update a table`
`UPDATE t1`
`SET COL = 1`
`FROM tbl t1`
`WHERE COL2 = 6;`

`-- How to declare variables`
`DECLARE`
	`Num NUMBER;`
`Num2 NUMBER(n);`
	`Num3 NUMBER(10,2);`
	`Num4 NUMBER := 50; -- add default value`
	`Num5 CONSTANT NUMBER := 10; – constant means the value can never be changed`
	`Text VARCHAR2(n);`
	`Text2 CHAR(n);`
	`Bool BOOLEAN;`
	`Datez DATE;`

`-- How to declare dictionary type variables`
`DECLARE`
	`TYPE rec is RECORD (`
`a NUMBER;`
`b NUMBER;`
	`)`
	
	`var1 rec;`
`BEGIN`
	`var1.a := 10;`
	`var2.b := 20;`
`END`

`-- How to get first of month or last day of month`
`LAST_DAY(somedatevalue);`
`FIRST_DAY(somedatevalue);`


`-- How to extract year from date`
`EXTRACT(year from somedatevalue);`

`-- How to convert to number`
`TO_NUMBER(somevalue);`

`-- How to get Monday/Sunday of previous week`
`SELECT next_day (sysdate-7, 'MONDAY') Last_Monday,` 
`next_day (sysdate-7, SUNDAY) Last_Sunday`
`FROM dual;`

`-- How to get monday of current week`
`SELECT next_day (sysdate, 'MONDAY') as Current_Monday`
`FROM dual;`
`-- How to create a temp table`
`DECLARE LOCAL TEMPORARY TABLE tbl1(` 
  `supplier_id number(10) not null,`
  `supplier_name varchar2(50) not null,`
  `contact_name varchar2(50)`
`);`

`-- How to insert into a table`
`INSERT INTO suppliers (supplier_id, supplier_name)`
`SELECT account_no, name`
`FROM customers`
`WHERE customer_id > 5000;`

`-- How to join two tables`
`SELECT columns`
`FROM table1 t1`
`LEFT JOIN table2 t2 ON (t1.column = t2.column);`

`-- How to select n number of rows`
`SELECT *`
`FROM (select * from suppliers ORDER BY supplier_name DESC) suppliers2`
`WHERE rownum <= n`
`ORDER BY rownum;`

`-- How to select rows in ascending order`
`select * from suppliers ORDER BY supplier_name`

`-- How to select rows in descending order`
`select * from suppliers ORDER BY supplier_name DESC`
`-- How to select unique vales (no dups)`
`SELECT DISTINCT state`
`FROM customers`
`WHERE last_name = 'Smith';`

`-- How to write IF statements`

`IF (condition) THEN`
	`-- do stuff`
`END IF`
`IF (condition) THEN`
	`-- do stuff`
`ELSE`
	`-- do stuff`

`END IF`

`IF (condition) THEN`
	`-- do stuff`
`ELSIF (condition) THEN`
	`-- do stuff`
`END IF`

`-- How to write Loops`
`LOOP`
   `monthly_value := daily_value * 31;`
   `EXIT WHEN monthly_value > 4000;`
`END LOOP;`
`WHILE monthly_value <= 4000`
`LOOP`
   `monthly_value := daily_value * 31;`
`END LOOP;`
`FOR loop_counter IN [REVERSE] lowest_number..highest_number`
`LOOP`
   `{...statements...}`
`END LOOP;`
`FOR Lcntr IN 1..20`
`LOOP`
   `LCalc := Lcntr * 31;`
`END LOOP;`

`-- How to check for NULL values`
`SELECT *`
`FROM suppliers`
`WHERE supplier_name IS NULL;`

`-- How to write an update statement with a sub query`
`UPDATE customers`
`SET c_details = (SELECT contract_date`
                 `FROM suppliers`
                 `WHERE suppliers.supplier_name = customers.customer_name)`
`WHERE customer_id < 1000;`

`-- How to use the Keyword "IN"`
`SELECT *`
`FROM customers`
`WHERE customer_name IN ('IBM', 'Hewlett Packard', 'Microsoft');`

`-- How to count all of the rows in a table`
`SELECT COUNT(*) AS "Number of employees"`
`FROM employees;`

`-- How to delete contents of a table`
`DELETE FROM customers`
`WHERE last_name = 'Smith';`

`-- How to select the smallest/largest value in a column`
`SELECT department, MIN(salary) AS "Lowest salary"`
`FROM employees`
`GROUP BY department;`

`-- How to pause for n number of seconds`
`dbms_lock.sleep( Number_of_seconds );`

`-- How to string match`
`SELECT supplier_name`
`FROM suppliers`
`WHERE supplier_name LIKE 'Sm_th'`
	`AND last_name LIKE '%er%';`


`-- How to permanently delete a table`
`DROP TABLE table_name;`

`-- How to cast a string into a date`
`D = to_date(‘1/1/2015’, ‘DD/MM/YYYY’)`

`-- How to declare a stored procedure`
`PROCEDURE name`
`IS`
`BEGIN`
`-- enter stuff`
`END;`

`-- How to declare a function`
`FUNCTION name`
`RETURN datatype`
`IS`
`BEGIN`
`-- enter stuff`
`RETURN value;`
`END;`
