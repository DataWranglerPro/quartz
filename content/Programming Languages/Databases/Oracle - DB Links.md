There are times where tables are not able to be accessed with a regular select statement. These tables might be available via db link.

For example let's say I have a table named:
- my_tbl

If I try to query this table I get an error.
``` sql
SQL> select * from my_tbl where ROOWNUM < 2;

Error starting at line : 1 in command -
select * from my_tbl where ROOWNUM < 2
Error at Command Line : 1 Column 15
Error report - 
SQL Error: ORA-00942L table or view does not exist
00942. 00000 - "table or view does not exist"
*Cause:
*Action:
```

Let's find the correct DB link:
``` sql
select * from all_db_links;
```

Now what I do is try the select statement with every db link name from the query above and see which one works.

For example:
``` sql
select @ from my_tbl@paste_db_link_here where rownum < 2;
```

