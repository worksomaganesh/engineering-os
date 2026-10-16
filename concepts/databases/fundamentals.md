# Database Fundamentals: From Zero to Understanding

## 1. What is data?

Data is information represented in a form a computer can store and process: a student's ID, a product price, a message, an image's metadata, a sensor reading, or a model evaluation result.

An application often needs to remember data after its process exits. That requires persistent storage. A database is one structured way to manage it.

## 2. Database vs DBMS vs database server

These terms are related but not identical:

- **Data:** the facts being stored.
- **Database:** the organized collection of data.
- **DBMS:** software that manages databases, queries, concurrency, constraints, and storage.
- **Database server:** a running service that accepts database client connections; common for PostgreSQL, MySQL, Oracle, and SQL Server.
- **Database client/driver:** software used by an application or tool to send queries and receive results.
- **Managed database service:** a cloud provider operates some infrastructure and maintenance tasks for you, but you still own data modelling, permissions, query design, and many operational decisions.

SQLite is different from the common client-server setup: it is an embedded database engine that reads and writes a database file through a library.

## 3. Why not store everything in variables or text files?

A variable normally exists only while the program is running. A text or JSON file can persist data, but an application must then build many capabilities itself: safe concurrent updates, indexing, filtering, transactions, constraints, recovery, and access controls.

Files are still useful—for uploaded documents, images, exports, backups, and configuration. A database is often used for structured records and metadata. A real application commonly uses both.

## 4. Relational database vocabulary

Consider a simple college application.

### Table

A table stores records with a consistent set of columns.

```sql
CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);
```

### Row

One record in the table, for example one student.

### Column

A field in each record, such as `full_name`.

### Primary key

A value (or set of values) that uniquely identifies each row. A primary key must be unique and not null.

### Foreign key

A rule connecting a column to a key in another table, helping preserve referential integrity.

```sql
CREATE TABLE courses (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL
);

CREATE TABLE enrollments (
    student_id INTEGER NOT NULL REFERENCES students(id),
    course_id INTEGER NOT NULL REFERENCES courses(id),
    PRIMARY KEY (student_id, course_id)
);
```

This design says that an enrollment must reference an existing student and course, and that the same student-course pair cannot be entered twice.

### Schema

The structure of the database: tables, columns, data types, constraints, indexes, views, and relationships.

### Query

A request to read or change data. SQL is a language for defining and querying relational data. Each product has dialect differences.

## 5. Basic SQL example

Create a table and insert a record:

```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'todo',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO tasks (id, title, status)
VALUES (1, 'Learn database basics', 'in_progress');

SELECT id, title, status
FROM tasks
WHERE status = 'in_progress'
ORDER BY created_at DESC;

UPDATE tasks
SET status = 'done'
WHERE id = 1;

DELETE FROM tasks
WHERE id = 1;
```

The exact syntax and data types can differ between PostgreSQL, MySQL, SQLite, and other engines. Do not run destructive commands against important data just to experiment.

Common SQL operations:
- `SELECT`: read rows.
- `INSERT`: create rows.
- `UPDATE`: modify rows.
- `DELETE`: remove rows.
- `CREATE` / `ALTER`: define or change schema.
- `JOIN`: combine related records.
- `GROUP BY`: aggregate rows into groups.
- `WHERE`: filter rows.
- `ORDER BY`: sort results.

## 6. Relationships and joins

A relational database lets you store related entities separately and combine them in queries.

Example: list enrollments with student and course names:

```sql
SELECT s.full_name, c.title
FROM enrollments e
JOIN students s ON s.id = e.student_id
JOIN courses c ON c.id = e.course_id;
```

The join conditions explain how the records relate. Without suitable conditions, a join can create a huge Cartesian product. Indexes and query plans can influence performance, but the first priority is a correct query and sound model.

Common relationships:
- **One-to-one:** one profile per user.
- **One-to-many:** one customer has many orders.
- **Many-to-many:** many students take many courses, represented through a junction table such as enrollments.

## 7. Constraints protect data

Constraints encode rules in the database:
- `NOT NULL`: a value must be present.
- `UNIQUE`: values cannot duplicate within the defined constraint.
- `PRIMARY KEY`: uniquely identifies a row.
- `FOREIGN KEY`: enforces a relationship to referenced data.
- `CHECK`: enforces a boolean condition where supported.
- suitable data types: avoid storing every value as arbitrary text.

Application validation is still useful for helpful error messages and business rules, but critical integrity rules should not depend solely on a single UI path. Data can be written through scripts, jobs, or other APIs too.

## 8. Transactions and ACID

A transaction groups related database operations into one logical unit. For example, placing an order may require creating the order and reserving inventory.

ACID describes four commonly discussed transaction properties:

- **Atomicity:** either the transaction's operations take effect as a unit, or they are rolled back.
- **Consistency:** a committed transaction preserves the database's defined integrity rules.
- **Isolation:** concurrent transactions are controlled according to the database's isolation level.
- **Durability:** committed changes survive failures according to the system's durability guarantees and configuration.

Conceptual example:

```sql
BEGIN;

UPDATE inventory
SET quantity = quantity - 1
WHERE product_id = 42 AND quantity > 0;

INSERT INTO orders (customer_id, product_id)
VALUES (7, 42);

COMMIT;
```

This example is incomplete as production order logic: the application must verify that the inventory update actually affected a row and roll back if no item was available. It illustrates why the updates should be treated as one unit. Transaction syntax and behavior vary by database.

A database transaction is not the same thing as a business process that may involve an external payment provider, email service, and warehouse. Those distributed workflows need additional patterns such as idempotency, retries, outbox/saga designs, or compensating actions.

## 9. Indexes: a trade-off, not magic

An index is an additional data structure that helps the database locate or order matching records without scanning every row in some query plans.

For example, if the application frequently looks up users by email, an index or unique constraint on email can help. The exact implementation depends on the engine.

Benefits:
- can speed up filters, joins, ordering, and certain range queries;
- can support uniqueness constraints.

Costs:
- consumes disk or memory;
- must be maintained when data changes;
- too many or poorly chosen indexes can slow writes and complicate maintenance.

Create indexes based on real query patterns, inspect query plans, and measure. Do not index every column automatically.

## 10. Normalization and denormalization

**Normalization** organizes relational data to reduce unnecessary duplication and update anomalies. For example, store a customer's canonical address in one appropriate record rather than repeating inconsistent copies in every order.

**Denormalization** intentionally duplicates or precomputes data to improve a specific access pattern or simplify reads. It may be appropriate for analytics, caching, or document-oriented designs, but adds synchronization and consistency work.

Neither should be treated as an absolute rule. Start with a clear model, then denormalize only for a justified reason.

## 11. SQL vs NoSQL

“SQL” often refers to relational systems and their query language. “NoSQL” is a broad umbrella for non-relational models such as document, key-value, graph, and wide-column systems. Some NoSQL products support SQL-like query languages, and relational products may support JSON or other non-tabular features.

Do not interpret NoSQL as “no schema,” “no transactions,” or “more scalable in every case.” Different systems make different trade-offs. Choose based on data model and access patterns.

## 12. OLTP vs OLAP

- **OLTP:** frequent operational transactions—creating an account, submitting an order, recording attendance.
- **OLAP:** analysis over large amounts of data—monthly revenue trends, cohort analysis, or operational dashboards.

PostgreSQL/MySQL/Oracle often power operational systems. BigQuery, Snowflake, Redshift, ClickHouse, and DuckDB are examples used for analytical workloads, although the product boundaries vary. Many organizations use both and move data through an ETL/ELT pipeline.

## 13. Durability, backups, replication, and availability

These concepts solve different problems:
- **Backup:** a recoverable copy of data.
- **Restore test:** proof that a backup can actually be recovered.
- **Replication:** maintaining copies on other nodes or systems.
- **High availability:** design intended to keep service running during certain failures.
- **Disaster recovery:** restoring service and data after a major incident.
- **Point-in-time recovery:** restoring to a chosen moment when supported and correctly configured.

Replication is not a substitute for backups: accidental deletion or malicious changes may replicate too. Define recovery objectives, keep protected backups, and test restores.

## 14. Database security basics

- Use least-privilege accounts and separate application credentials from administrator credentials.
- Never put production database passwords in public repositories or browser-delivered frontend code.
- Store secrets in environment configuration or a managed secret store; avoid logging credentials.
- Use encrypted connections when appropriate and supported.
- Validate and parameterize SQL inputs; do not concatenate untrusted strings into query text.
- Apply authorization in the correct layer and test it.
- Keep dependencies and database versions maintained.
- Monitor access and protect backups as sensitive data.
- Plan retention and deletion according to legal and business requirements.

Parameterized query example in generic form:

```sql
SELECT id, full_name
FROM students
WHERE email = ?;
```

Placeholder syntax differs by driver/database. Use the driver's parameter-binding API; do not replace the placeholder with string concatenation.

## 15. Database performance: where time goes

A slow query can result from:
- scanning more rows than needed;
- missing or unsuitable indexes;
- returning too much data;
- inefficient joins or sorting;
- locks and contention;
- too many network round trips;
- poor connection management;
- resource limits or noisy neighbors;
- an unsuitable data model.

Use query plans, metrics, realistic data, and load tests. Do not assume the database is the bottleneck until measured.

## 16. Important vocabulary

| Term | Meaning |
|---|---|
| DBMS | Software that manages databases |
| SQL | Language for defining and querying relational data |
| Schema | Data structure and constraints |
| Primary key | Unique row identifier |
| Foreign key | Referential-integrity relationship |
| Transaction | Group of operations treated as one logical unit |
| ACID | Atomicity, consistency, isolation, durability |
| Index | Data structure that can accelerate suitable queries |
| Migration | Versioned change to schema/data structure |
| Connection pool | Reuse/manage database connections |
| Replication | Keeping data copies on other nodes/systems |
| Sharding/partitioning | Splitting data across partitions/nodes according to a strategy |
| Backup/restore | Recovery copy and the process of recovering it |
| ORM | Object-relational mapper that maps application objects to relational records |
| OLTP / OLAP | Operational transactions / analytical processing |

## What to practise

1. Create three related tables.
2. Add primary keys, foreign keys, and unique constraints.
3. Insert sample records.
4. Write SELECT queries with filters and joins.
5. Aggregate with COUNT, SUM, and GROUP BY.
6. Update records inside a transaction.
7. Add an index for a demonstrated query and compare the query plan.
8. Write a migration and test it on a disposable database.
9. Create a backup and restore it to a fresh environment.
10. Practise parameterized queries and least-privilege access.
