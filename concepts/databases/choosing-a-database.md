# How to Choose a Database for a Project

Choosing a database is a design decision, not a popularity vote. Start from the application's data and query requirements, then choose the simplest system that can meet them.

## 1. Ask these questions in order

### A. What data must be stored?
Examples: users, orders, invoices, document metadata, messages, sensor readings, graph relationships, embeddings, or analytics events.

### B. What are the main operations?
- Look up one record by ID?
- Search/filter records?
- Join related entities?
- Update multiple records atomically?
- Traverse multi-hop relationships?
- Search full text?
- Find semantically similar embeddings?
- Aggregate billions of events?

Write down the five or ten most important queries before choosing a product.

### C. What correctness guarantees matter?
Ask whether duplicate records are harmful, whether several updates must commit together, whether reads may be slightly stale, and what consistency behavior the application requires.

### D. What scale and availability do you actually expect?
Estimate record counts, read/write rate, payload size, growth, latency needs, downtime tolerance, and geographic requirements. Do not build for hypothetical billions of users before validating the product.

### E. What can you operate?
A self-managed distributed database adds deployment, patching, monitoring, backups, upgrades, and incident response. A managed service can reduce some work but brings provider coupling, pricing, and configuration decisions.

### F. What does it cost?
Include more than the headline price:
- compute and storage;
- backups and replicas;
- request/read/write charges;
- network transfer;
- index and log storage;
- engineering/operations time;
- migration and lock-in costs.

Use the current provider pricing page for actual estimates. Costs change by region, tier, and workload.

## 2. A quick decision guide

| Project requirement | Sensible starting candidate | Why / caution |
|---|---|---|
| Typical web app with users and related records | PostgreSQL or MySQL | SQL, relationships, transactions, mature tooling |
| Small local app or prototype | SQLite | Minimal setup; evaluate concurrency/deployment needs |
| Flexible nested document records | MongoDB or Firestore | Fits document-shaped access; model queries and security carefully |
| Firebase-centric mobile/web app | Firestore | SDK and real-time integration; understand rules and pricing |
| Fast cache, sessions, rate limits | Redis | Supporting system for suitable ephemeral/fast state |
| Full-text relevance search | Elasticsearch/OpenSearch | Often a derived search index, not the sole source of truth |
| Semantic search/RAG | PostgreSQL + pgvector or dedicated vector service | Start simple; evaluate retrieval quality and scale |
| Relationships/path traversal are central | Neo4j or another graph DB | Graph queries are first-class |
| Large-scale timestamped metrics | InfluxDB, TimescaleDB, or suitable metrics system | Retention and time-window queries |
| Large-scale analytical reports | BigQuery, Snowflake, Redshift, ClickHouse, DuckDB | Analytics-oriented execution/storage |
| Distributed high-write workloads with known query patterns | Cassandra/ScyllaDB/Bigtable | Requires query-first partition design |
| Enterprise stack already standardizes on Oracle or SQL Server | That ecosystem's database | Existing skills, support, integration, and requirements matter |

These are starting points, not rigid rules. PostgreSQL can cover many workloads through core features and extensions; specialized products can be justified when they solve a demonstrated problem.

## 3. Why SQL is a strong first foundation

Learning relational databases teaches:
- modelling entities and relationships;
- keys and constraints;
- joins;
- filtering and aggregation;
- transactions and isolation;
- indexes and query plans;
- schema migrations;
- permissions and recovery.

These ideas help even if you later use document, graph, key-value, or vector systems. Learn SQL before collecting database brand names.

## 4. Why “NoSQL is more scalable” is too simplistic

Some NoSQL systems are designed for horizontal distribution and predictable access patterns. Relational systems can also scale vertically, use replicas, partition data, and support distributed variants. Scalability depends on the product, architecture, workload, consistency needs, and engineering effort.

A design that needs joins, transactions, and flexible ad hoc queries may be simpler and safer in a relational database. A workload that needs massive distributed writes with known partition-key queries may suit a wide-column store. Choose from evidence.

## 5. Primary database vs supporting stores

A mature application may use more than one system:

- **System of record:** authoritative business records, often PostgreSQL/MySQL/Oracle.
- **Cache:** derived values for faster reads, often Redis.
- **Search index:** derived text/search representation, often Elasticsearch/OpenSearch.
- **Object storage:** large PDFs, images, videos, and model artifacts.
- **Vector index:** embedding retrieval, possibly pgvector or a dedicated vector database.
- **Warehouse:** analytical copy for reporting, such as BigQuery or Snowflake.
- **Queue/stream:** asynchronous event processing, using a suitable messaging system.

Each additional component creates operational and consistency work. Add it when a requirement justifies it, not because a diagram looks sophisticated.

## 6. Example: choose for a GeM Tender Copilot

MVP requirements:
- users and organizations;
- tender metadata and deadlines;
- extracted requirements and evidence references;
- bid-readiness report and review state;
- uploaded PDF files;
- asynchronous extraction jobs;
- perhaps semantic retrieval later.

A sensible initial architecture:
- PostgreSQL for users, organizations, tenders, extracted structured requirements, and report status;
- object storage for tender PDFs and generated reports;
- a queue/background worker if extraction is slow or retryable;
- optionally pgvector or a separate vector service only if semantic retrieval adds measured value.

Why not start with five databases? The main records have clear relationships and need reliable updates. PostgreSQL plus object storage and a simple background job mechanism may be enough. Add more systems only after measuring a real limitation.

## 7. Example: choose for an AI RAG assistant

Potential data:
- users and document permissions;
- source document metadata;
- chunks and citations;
- embeddings;
- conversation and feedback history.

Start with a relational database for users, permissions, document metadata, and application state. Store original files in object storage. For retrieval, evaluate PostgreSQL plus pgvector or a dedicated vector database. The vector index must respect document permissions; similarity alone is not authorization.

If you later need large-scale hybrid search or advanced ranking, evaluate a search engine. If you need analytics over usage events, evaluate a warehouse. Keep the architecture proportional to actual needs.

## 8. A practical evaluation checklist

For the two or three strongest candidates, build a small proof of concept:
- create representative schema and data;
- run the real queries;
- include realistic data volume and skew;
- test concurrent updates;
- test failure/recovery paths;
- inspect query plans;
- measure latency and throughput;
- test backup and restore;
- estimate cost at expected usage;
- check driver/library support and hosting options.

Do not rely on an isolated synthetic benchmark. Benchmark the workload your project will actually run.

## 9. Common selection mistakes

- Choosing a database because a famous company uses it.
- Choosing a specialized system before understanding SQL.
- Treating every JSON-shaped API payload as proof that MongoDB is needed.
- Using Redis as the only permanent store without understanding persistence and recovery.
- Assuming vector search automatically produces accurate RAG answers.
- Using a data warehouse as the primary store for interactive transactional updates without checking suitability.
- Introducing multiple databases for a portfolio MVP when one database and object storage would suffice.
- Ignoring backups, authorization, schema migrations, and total cost.
- Assuming moving to another database later is effortless. Data migration, SQL dialects, indexes, transactions, and application assumptions can make it substantial.

## The practical default

For many beginner projects, use PostgreSQL (or MySQL if your ecosystem calls for it), learn SQL deeply, and keep the initial architecture simple. Add specialized databases when a real workload—not hype—shows why you need them.
