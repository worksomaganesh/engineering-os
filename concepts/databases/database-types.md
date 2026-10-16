# Types of Databases: Understand the Families

There is no single official number of database types. Categories overlap because a product can support several data models or workloads. The purpose of this guide is to understand the trade-offs and recognize when a category is useful.

## 1. Relational databases (SQL)

**Model:** data is represented in tables with rows and columns, and relationships are represented through keys. SQL is used to define, query, and manipulate data.

Examples: PostgreSQL, MySQL, Oracle Database, Microsoft SQL Server, SQLite.

Good for:
- users, orders, inventory, payments, attendance, booking systems;
- business data with relationships and integrity rules;
- applications that need joins and transactions;
- records where constraints such as unique email or valid foreign keys matter.

Strengths:
- explicit schema and integrity constraints;
- joins and expressive queries;
- mature transaction support;
- widely understood tooling and operational practices.

Trade-offs:
- schema changes need planning;
- complicated distributed scaling can be challenging depending on the product and architecture;
- careless queries and indexes can still cause poor performance.

**Use when:** records have meaningful relationships and correctness matters. This is the best default family to learn first for many application projects.

## 2. Document databases

**Model:** records are stored as documents, often JSON-like objects with nested fields. Documents may not all have exactly the same shape.

Examples: MongoDB, Cloud Firestore, Couchbase.

Good for:
- content and catalog records with nested attributes;
- applications whose records naturally form documents;
- some mobile/web apps that need flexible schemas or real-time synchronization.

Strengths:
- natural fit for JSON-shaped data;
- flexible document structures;
- can make aggregate records easy to retrieve as one unit.

Trade-offs:
- relationships and cross-document queries may require extra modelling or additional reads;
- duplicated data can complicate updates;
- flexible schema does not mean “no data design needed.”

**Use when:** the application's common operations revolve around whole documents and their nested data. Do not choose it just because JSON is familiar.

## 3. Key-value stores

**Model:** retrieve a value by a key. Values may be strings, counters, hashes, lists, sets, streams, or other supported structures.

Examples: Redis, Amazon DynamoDB (also document-oriented), Valkey.

Good for:
- caching;
- session state;
- rate limits and counters;
- short-lived coordination state;
- fast lookups with known keys.

Strengths:
- simple access model;
- very fast operations for suitable workloads;
- specialized data structures can avoid building coordination logic from scratch.

Trade-offs:
- arbitrary relational joins are not the main strength;
- eviction, persistence, expiration, and consistency need deliberate configuration;
- cached values can become stale.

**Use when:** key-based access is the dominant operation. Often a supporting system beside a primary database.

## 4. Wide-column databases

**Model:** data is organized around partition keys and clustering/sort keys, with rows that can have flexible columns within a column family/table model. This is different from an analytics-oriented columnar warehouse.

Examples: Apache Cassandra, ScyllaDB, Google Cloud Bigtable.

Good for:
- large distributed write workloads;
- event histories and telemetry;
- applications with predictable query patterns across many nodes;
- high availability across regions when designed appropriately.

Strengths:
- horizontal scaling and high write throughput for suitable workloads;
- partitioning is central to the data model;
- can support large datasets distributed across machines.

Trade-offs:
- queries must be designed around partition keys and known access patterns;
- ad hoc joins and arbitrary queries are not the main strength;
- data modelling and consistency trade-offs need careful understanding.

**Use when:** scale, write volume, distribution, and known query patterns justify the operational complexity.

## 5. Graph databases

**Model:** entities are nodes, and relationships are edges; both can have properties. Traversing relationships is a first-class operation.

Examples: Neo4j, Amazon Neptune.

Good for:
- fraud rings and connected-account investigations;
- recommendation relationships;
- knowledge graphs;
- dependency mapping and network analysis.

Strengths:
- expressive relationship traversal;
- can make multi-hop connections natural to query.

Trade-offs:
- not automatically faster for every relationship query;
- data ingestion, graph shape, and query design matter;
- simple tabular workloads may be better served by relational databases.

**Use when:** relationships and paths are central to the questions the application asks.

## 6. Time-series databases

**Model:** optimized for measurements/events indexed by time, often with tags or dimensions.

Examples: InfluxDB, TimescaleDB (built on PostgreSQL), Prometheus for metrics.

Good for:
- server CPU/memory metrics;
- IoT sensors;
- industrial telemetry;
- monitoring and time-stamped measurements.

Strengths:
- time-based queries, retention, downsampling, and aggregation;
- optimized storage/querying for particular time-series patterns.

Trade-offs:
- not every event table needs a separate time-series product;
- cardinality, retention, and ingestion design matter;
- general business transactions may belong in a relational database.

**Use when:** large volumes of timestamped measurements and time-window analytics dominate.

## 7. Search engines and search-oriented stores

Examples: Elasticsearch, OpenSearch, Apache Solr.

Good for:
- full-text search;
- relevance ranking;
- faceted filtering;
- log search and investigation;
- hybrid lexical and vector retrieval where supported.

Strengths:
- text analysis, relevance scoring, and search-oriented indexing;
- suitable for exploring and filtering large document collections.

Trade-offs:
- a search index is often a derived copy, not the authoritative source of business records;
- indexes may update asynchronously and lag behind the primary database;
- operating a cluster adds cost and complexity.

**Use when:** users need rich text search, relevance ranking, or log exploration beyond simple SQL filters.

## 8. Vector databases and vector search

**Model:** stores or indexes embedding vectors and finds vectors similar to a query vector, commonly using approximate nearest-neighbor techniques. Usually supports metadata filters too.

Examples: Pinecone, Qdrant, Milvus, Weaviate, Chroma; PostgreSQL can add vector search through pgvector.

Good for:
- semantic search;
- retrieval-augmented generation (RAG);
- finding similar text, images, or other embedded content;
- recommendation and deduplication systems.

Strengths:
- vector similarity search at scale;
- can combine semantic similarity with metadata filtering and hybrid search.

Trade-offs:
- retrieval quality depends on embedding model, chunking, filters, ranking, and evaluation;
- similarity does not guarantee factual relevance;
- a vector index does not replace application permissions or authoritative source data;
- a dedicated service may be unnecessary for a small MVP.

**Use when:** your application actually needs embedding similarity. First understand embeddings and retrieval; do not add a vector database merely because a project uses an LLM.

## 9. Analytical databases, data warehouses, and OLAP engines

Examples: BigQuery, Snowflake, Amazon Redshift, ClickHouse, DuckDB.

These systems are optimized for analytical queries over large datasets, such as scanning many rows, aggregating metrics, and comparing trends. Columnar storage and vectorized processing are common techniques.

Good for:
- business intelligence dashboards;
- product analytics;
- financial or operational reports;
- large-scale SQL analytics;
- data pipelines and machine-learning feature preparation.

**OLTP vs OLAP:**
- **OLTP** (online transaction processing) handles many small, current-record operations: creating an order, changing an address, recording attendance.
- **OLAP** (online analytical processing) handles larger analytical queries: monthly sales by region, churn trends, cohort analysis.

A data warehouse is not simply “a bigger application database.” It has a different workload and often receives data from several operational sources.

## 10. Embedded and file-based databases

Example: SQLite; DuckDB is also commonly embedded for analytical workflows.

The database engine runs inside the application process or is used as a library rather than requiring a separately managed database server for common deployments.

Good for:
- local-first applications;
- desktop/mobile apps;
- command-line tools;
- prototypes and tests;
- small services where a single local database file is appropriate;
- local analytical workflows with DuckDB.

Strengths:
- simple setup and low operational overhead;
- excellent for local development and many single-user/single-node use cases.

Trade-offs:
- concurrency and network access characteristics differ from server databases;
- a local file is not automatically shared or backed up;
- multi-instance server deployment may need a server database instead.

## 11. Distributed SQL / NewSQL systems

Examples include CockroachDB and YugabyteDB, which aim to combine SQL/relational semantics with distributed operation across nodes.

Good for:
- applications needing relational transactions and horizontal distribution;
- deployments with multi-region or resilience requirements.

Trade-offs:
- distribution adds latency and operational/data-modelling considerations;
- not every application needs this complexity;
- exact transaction and compatibility guarantees differ by product.

## 12. In-memory databases

“In-memory” describes a storage/performance approach, not one uniform data model. Redis is a common example; some relational systems also use memory-optimized features.

Good for:
- low-latency cache and session state;
- ephemeral state;
- fast counters and queues;
- specialized real-time workloads.

Important: understand persistence, replication, eviction, and recovery settings before trusting an in-memory service with valuable data.

## 13. Ledger and immutable-record systems

Some databases and specialized services are designed to provide tamper-evident or append-only histories.

Good for:
- audit records;
- regulated workflows that need verifiable history;
- tracking changes where modification detection is important.

A normal database can also support audit tables and append-only patterns. A specialized ledger is justified only when its integrity guarantees and operational model are required.

## 14. Multi-model databases

Some products support more than one data model in a single engine, for example relational tables plus JSON, or document and graph capabilities. PostgreSQL extensions and JSON support are examples of adding capabilities to a relational core.

The existence of multiple features does not mean all models perform equally well for all workloads. Test the specific query pattern and deployment.

## Quick comparison

| Family | Best-known strength | Example |
|---|---|---|
| Relational SQL | Relationships, constraints, transactions | PostgreSQL |
| Document | Nested JSON-like records | MongoDB |
| Key-value | Fast lookup by key, cache/data structures | Redis |
| Wide-column | Distributed, high-volume access patterns | Cassandra |
| Graph | Relationship traversal | Neo4j |
| Time-series | Timestamped measurements | InfluxDB |
| Search | Full-text search and relevance | Elasticsearch |
| Vector | Embedding similarity retrieval | Qdrant / pgvector |
| Analytics/warehouse | Large aggregations and reporting | BigQuery |
| Embedded | Local storage with little setup | SQLite |
| Distributed SQL | Relational model across distributed nodes | CockroachDB |

## A critical rule

**Do not select a database from the product name or trend. Start from the queries, integrity needs, data shape, expected scale, latency, operational skills, and budget.** Then test the likely candidate with realistic data and representative queries.
