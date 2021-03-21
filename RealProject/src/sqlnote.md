# Python to SQL
* open connection (MDP + AZURE)


* execute query
```python
query = "SELECT * FROM table"
pd.read_sql(query, cnxn)
```
* execute cursor
```python
cur = cnxn.cursor()
query = "DELETE FROM table;"
cur.execute(query)
cnxn.commit()
cur.close()   
```


# SQL

* Redshift grant

```sql
Grant select on schema.table TO abc
Grant ALL on data_mart_hdms.email_events TO group write_access
call preprod_data_mart_hdms.proc_grant ('event'); --> fast function
```

# date

often used cases 
```sql
to_char(created_date, 'YYYYMMDD')
TO_DATE( created_date,'YYYY-MM-DD')

create table schema.table1(
customer_number varchar(10),
sales_org varchar(4),
flagtype varchar(256),
created_date TIMESTAMP WITHOUT TIME ZONE	timestamp default CURRENT_TIMESTAMP);

```
transfer string to timestamp: `to_timestamp(schedtime, 'MM/DD/YYYY HH:MI:SS') `


* stop session

```sql
select * from stv_sessions where user_name = 'user1'
and process <> (select PG_BACKEND_PID());
select pg_terminate_backend(14358);
select pg_terminate_backend(14359);
select pg_terminate_backend(14358);
select pg_terminate_backend(14359);


SELECT
  current_time,
  c.relname,
  l.database,
  l.transaction,
  l.pid,
  a.usename,
  l.mode,
  l.granted
FROM pg_locks l
JOIN pg_catalog.pg_class c ON c.oid = l.relation
JOIN pg_catalog.pg_stat_activity a ON a.procpid = l.pid
--join pg_catalog.stv_sessions s on   s.process =l.procpid
WHERE l.pid <> pg_backend_pid()
and a.usename = 'hdms_admin';
```

* regular expression sql 

(`regexp` is for mysql, redshif `~` or `!=`)

The following is the query with regex when you want exactly 10 digits in a string and all must be a number:
```sql
select * from table
where id REGEXP '^[0-9]{10}$';
```
one or more number: `'^[0-9]*$'`

