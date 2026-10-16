# Database Learning Roadmap

This path takes you from understanding what a database is to integrating one into a real application. It is a sequence, not a deadline.

## Stage 1 — Understand the purpose

Learn:
- persistence vs in-memory variables;
- database vs DBMS vs server;
- relational vs non-relational data models;
- OLTP vs OLAP;
- application database vs object storage.

Practice: draw the architecture for a task app and identify what data must persist after a restart.

**Ready to continue when:** you can explain why a backend might need both a database and object storage.

## Stage 2 — Learn SQL basics

Learn:
- tables, rows, columns, data types;
- SELECT, WHERE, ORDER BY, LIMIT;
- INSERT, UPDATE, DELETE;
- COUNT, SUM, AVG, GROUP BY;
- NULL and its behavior;
- basic filtering and sorting.

Practice:
- create a students table;
- insert 10 students;
- find students by course/status;
- count records by category;
- update one record and verify it.

**Ready when:** you can write simple queries without copying them line by line.

## Stage 3 — Relational modelling

Learn:
- primary and foreign keys;
- unique, not-null, and check constraints;
- one-to-one, one-to-many, many-to-many;
- joins;
- normalization and update anomalies;
- timestamps and identifiers.

Project: design students, courses, and enrollments tables. Insert sample data and query enrollments with student and course names.

**Ready when:** you can explain why a many-to-many relationship usually needs a junction table.

## Stage 4 — Transactions and data integrity

Learn:
- transactions and ACID;
- commit and rollback;
- concurrent updates and isolation at a conceptual level;
- idempotency for retried application requests;
- how to handle partial failures.

Practice: implement a transfer or inventory-reservation exercise in a disposable database. Ensure insufficient balance/stock causes the whole transaction to fail safely.

**Ready when:** you can explain why two related updates should not always be run independently.

## Stage 5 — Indexes and query performance

Learn:
- B-tree indexes at a high level;
- composite indexes and leftmost-prefix behavior where relevant;
- selectivity and query plans;
- how indexes affect writes;
- pagination and avoiding unnecessarily large result sets.

Practice: create sample data, run a filter query, inspect the query plan, add an appropriate index, and compare. Use realistic data and avoid claiming a performance improvement from tiny/noisy samples.

**Ready when:** you can describe why an index helps one query but may not help another.

## Stage 6 — Connect a backend

Choose a backend you are learning, such as:
- Python + FastAPI/Django;
- JavaScript/TypeScript + Express/NestJS;
- Java + Spring Boot.

Use a suitable database driver or ORM. Build create/read/update/delete endpoints. Validate inputs, bind query parameters safely, return controlled errors, and enforce authorization.

**Ready when:** the app persists data across restarts and does not expose database credentials to the browser.

## Stage 7 — Migrations and tests

Learn:
- schema migration tools;
- version-controlled schema changes;
- test database setup and cleanup;
- constraint and authorization tests;
- integration tests;
- migration compatibility and rollback/recovery planning.

Practice: add a field through a migration, test it on a clean database and an existing test database, then verify application behavior.

**Ready when:** a teammate can clone the project and create the expected schema from documented commands.

## Stage 8 — Security and operations

Learn:
- least-privilege database users;
- secrets management;
- encrypted connections;
- backups and restore tests;
- logs, metrics, slow-query investigation;
- connection pools;
- retention and deletion;
- patching and upgrade planning.

Practice: create a disposable database, backup it, restore it elsewhere, and document each step. Keep all secrets out of source control.

**Ready when:** you can explain what happens if the database server fails and how you would recover the data.

## Stage 9 — Learn other models by comparison

After SQL foundations, explore:
- MongoDB/Firestore for document-oriented data;
- Redis for caching and fast data structures;
- Elasticsearch/OpenSearch for full-text search;
- pgvector or a vector database for semantic retrieval;
- Neo4j for graph traversal;
- InfluxDB/TimescaleDB for time-series workloads;
- BigQuery/Snowflake/ClickHouse/DuckDB for analytics;
- Oracle Database or SQL Server if relevant to your courses or target roles.

For each product, ask what query model it supports, what trade-offs it makes, and why a relational database might not be the best fit for the target workload.

## Three hands-on project milestones

### Project A — Task tracker
- users and tasks;
- CRUD API;
- filtering and pagination;
- schema constraints;
- migrations and tests.

### Project B — Invoice reconciliation
- import CSV/XLSX rows;
- store normalized invoice data;
- compare invoice records;
- record discrepancies and review decisions;
- export a report.
- Keep original uploaded files in object storage or a protected file store where appropriate.

### Project C — RAG document assistant
- store document metadata and permissions in a relational database;
- store originals in object storage;
- split documents into chunks;
- generate embeddings;
- retrieve relevant chunks through pgvector or a vector service;
- log citations, feedback, and evaluation results.
- Verify that retrieval never bypasses user/document permissions.

## How to study efficiently

- Write queries yourself before reading the answer.
- Use a local disposable database for experiments.
- Read official docs for the product/version you actually use.
- Keep notes on why a schema or index exists.
- Practise backup/restore and migrations, not only SELECT statements.
- Learn one product well enough to build a complete app before sampling many others.
- When AI generates SQL, inspect the query, test edge cases, and understand the transaction and authorization behavior.

## Suggested official learning resources

- PostgreSQL tutorial: https://www.postgresql.org/docs/current/tutorial.html
- MySQL documentation: https://dev.mysql.com/doc/
- Oracle Database documentation: https://docs.oracle.com/en/database/oracle/oracle-database/
- SQLite documentation: https://www.sqlite.org/docs.html
- MongoDB learning resources: https://www.mongodb.com/docs/
- SQLBolt interactive SQL lessons: https://sqlbolt.com/
- Use the product's official documentation to verify syntax, current features, and operational recommendations.

## Final checkpoint

You have a solid beginner foundation when you can:
- model related data;
- write SQL queries and joins;
- use constraints and transactions;
- explain index trade-offs;
- integrate the database into a backend;
- protect credentials and enforce access;
- create migrations and tests;
- back up and restore data;
- justify why you chose a particular database for a real project.
