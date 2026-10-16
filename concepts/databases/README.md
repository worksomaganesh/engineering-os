# Databases — A Beginner-to-Engineering Guide

> **This guide answers:** What is a database, what kinds exist, what are Oracle, MySQL, PostgreSQL and other database products used for, and how does a database fit into building a real project?

## The short answer

A **database** is an organized place to store data so an application or person can create it, retrieve it, change it, and manage it reliably. A **database management system (DBMS)** is the software that manages that data, provides ways to query it, and handles concerns such as concurrent access, integrity, storage, permissions, and recovery.

A database is useful whenever an application must remember information beyond the current execution: user accounts, orders, assignments, messages, uploaded-file metadata, payment records, model evaluations, job status, and much more.

There is no single universal count of database types. Databases can be categorized by their **data model**, **workload**, **storage layout**, **deployment model**, and **specialized purpose**. These categories overlap: PostgreSQL is relational but can also store JSON and, using extensions, vectors; Elasticsearch supports search, analytics, and vector retrieval; SQLite is a relational SQL engine designed to be embedded into an application.

**For many beginner full-stack projects, PostgreSQL or MySQL is a sensible starting point.** SQLite is excellent for local applications and small prototypes. MongoDB can fit document-shaped data. Redis is commonly an additional cache or fast data structure service, not a default replacement for the system of record. Specialized databases are worth learning when a specific query or workload requires them.

## Read the documents in this order

1. [Database Fundamentals](fundamentals.md) — what databases do, tables, keys, SQL, transactions, indexes, backups, and terminology.
2. [Types of Databases](database-types.md) — relational, document, key-value, graph, time-series, search, vector, analytics, distributed, and embedded models.
3. [Database Products Compared](database-products.md) — Oracle, PostgreSQL, MySQL, SQLite, SQL Server, MongoDB, Redis, Cassandra, DynamoDB, Firestore, Neo4j, Elasticsearch, InfluxDB, BigQuery, Snowflake, ClickHouse, DuckDB, and vector tools.
4. [Where a Database Fits in a Project](using-databases-in-projects.md) — architecture, data modelling, SQL example, backend integration, migrations, tests, and lifecycle.
5. [How to Choose a Database](choosing-a-database.md) — decision process, trade-offs, common mistakes, and practical recommendations.
6. [Database Learning Roadmap](learning-roadmap.md) — what to learn first and how to practise.

## A simple way to think about it

Imagine building a college attendance application. It needs to remember students, courses, class sessions, and attendance records. If all the information exists only in a Python list, it disappears when the process stops. If you write it all into arbitrary text files, you must invent your own query, concurrency, integrity, and recovery rules.

A database gives you a managed data store. Depending on the database and its configuration, it can help:
- persist data across application restarts;
- search, filter, sort, join, and aggregate records;
- enforce rules such as unique IDs and valid relationships;
- let many users and application instances access data safely;
- group related updates into transactions;
- create indexes for common queries;
- control who is allowed to read or change the data;
- support backups, recovery, replication, and larger workloads.

A database does not automatically make data secure, correct, backed up, or fast. Those outcomes depend on schema design, queries, permissions, deployment, testing, and operations.

## How databases fit into a typical project

```text
User / browser / mobile app
          |
          | HTTPS request
          v
Backend application / API
          |
          | validated query via a database driver or ORM
          v
Database
  ├── users
  ├── products / records
  ├── transactions
  └── application state
          |
          v
Backend returns a response to the client
```

For a traditional custom backend, the browser normally talks to the backend API, and the backend connects to the database. This keeps database credentials on the server and allows the application to enforce its business rules. Backendless platforms such as Firebase provide a different architecture where clients may access data through SDKs and security rules; those rules then become a critical authorization boundary.

The database is part of the application from early data modelling through deployment, monitoring, backups, and migrations. It is not merely a box you add at the end.

## The most important distinctions

| Question | Example distinction |
|---|---|
| What is the data model? | Relational tables vs JSON-like documents vs graph relationships |
| What kind of queries dominate? | Small record updates vs analytical scans vs similarity search |
| Where does it run? | Embedded local file vs self-managed server vs managed cloud service |
| How is it stored/processed? | Row-oriented operational database vs columnar analytics engine |
| How is access exposed? | SQL client, document query API, key lookup API, graph query language, or vector search API |

The category alone does not decide the answer. A database's query model, consistency guarantees, scaling behavior, pricing, availability, ecosystem, and your team's skills all matter.

## Beginner recommendations

- Learn **SQL and relational modelling** first, even if your first project later uses a NoSQL database. Tables, keys, joins, constraints, and transactions teach foundational data concepts.
- Use **PostgreSQL** as a strong general-purpose learning choice, or **MySQL** if it matches your course, stack, or target environment.
- Use **SQLite** for small local apps, command-line tools, prototypes, and embedded data.
- Learn **MongoDB** when the document model has a real advantage for your data and access patterns.
- Learn **Redis** for caching, rate-limiting, queues, sessions, and other fast in-memory data-structure use cases.
- Learn **vector search** when building semantic retrieval or RAG; start by understanding embeddings, similarity, metadata filters, and evaluation. You may be able to begin with PostgreSQL plus pgvector before operating a dedicated vector database.
- Learn **Oracle Database**, SQL Server, cloud data warehouses, wide-column stores, graph databases, and time-series databases in relation to their workloads and the roles you want.

## Official sources used in this guide

- [Oracle AI Database Concepts](https://docs.oracle.com/en/database/oracle/oracle-database/26/cncpt/introduction-to-oracle-database.html)
- [PostgreSQL documentation and overview](https://www.postgresql.org/docs/current/)
- [MySQL 8.4 Reference Manual](https://dev.mysql.com/doc/refman/8.4/en/)
- [SQLite — About](https://www.sqlite.org/about.html)
- [Microsoft SQL Server documentation](https://learn.microsoft.com/sql/sql-server/what-is-sql-server)
- [MongoDB Manual](https://www.mongodb.com/docs/manual/)
- [Redis data types](https://redis.io/docs/latest/develop/data-types/)
- [Apache Cassandra architecture](https://cassandra.apache.org/doc/latest/cassandra/architecture/overview.html)
- [Amazon DynamoDB overview](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html)
- [Cloud Firestore documentation](https://firebase.google.com/docs/firestore)
- [Neo4j graph database concepts](https://neo4j.com/docs/getting-started/graph-database/)
- [Elasticsearch search documentation](https://www.elastic.co/docs/solutions/search)
- [InfluxDB 3 documentation](https://docs.influxdata.com/influxdb3/)
- [BigQuery overview](https://docs.cloud.google.com/bigquery/docs/introduction)
- [Snowflake key concepts](https://docs.snowflake.com/en/en/user-guide/intro-key-concepts)
- [ClickHouse columnar database guide](https://clickhouse.com/resources/engineering/what-is-columnar-database)
- [pgvector](https://github.com/pgvector/pgvector)
- [Qdrant vector search](https://qdrant.tech/documentation/overview/vector-search/)
- [Milvus overview](https://milvus.io/docs/overview.md)

Use the product documentation for the exact version and deployment model you are using. Features, pricing, support windows, and managed-service offerings can change.

## Final takeaway

A database is a core part of a software system's memory. Choosing one is not a popularity contest: start with the data you need to store and the operations you must perform, select the simplest suitable system, and evolve only when evidence shows that you need something different.
