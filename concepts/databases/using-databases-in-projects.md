# Where a Database Fits When Building a Project

A database is not only a place to save records. It affects the application's architecture, API design, data model, validation, tests, deployment, security, and maintenance.

## 1. Typical web application architecture

```text
Browser / mobile app
       |
       | HTTPS request
       v
Backend API (FastAPI, Django, Express, Spring, etc.)
       |
       | validate request, authenticate user, enforce business rules
       v
Database driver / ORM
       |
       v
Database (PostgreSQL / MySQL / etc.)
       |
       v
Backend maps result to response
       |
       v
Client renders UI
```

The browser should normally call your backend, not connect directly to a traditional database using privileged credentials. The backend is the place to check permissions, validate data, run business rules, and control what data is returned.

Exceptions exist: Firebase and other backend-as-a-service products provide client SDKs and security-rule systems. If clients access data directly, security rules and identity/authorization configuration must be designed and tested carefully.

## 2. What should be stored in a database?

Good candidates:
- accounts, profiles, roles, and permissions;
- business records such as tenders, invoices, leads, tasks, and orders;
- workflow status and deadlines;
- references to uploaded documents;
- job status, audit events, and processing results;
- model evaluation results and metadata;
- application settings that must persist.

Not every file should be stored as a database row. Large PDFs, images, videos, model files, and exports are often better in object storage or a file system, with the database holding metadata and a secure reference. Small binary fields can be suitable in some cases, but choose intentionally.

## 3. Example: a task manager

Suppose the application needs users and tasks. A simple relational model:

```sql
CREATE TABLE app_users (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    display_name TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tasks (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    owner_id BIGINT NOT NULL REFERENCES app_users(id),
    title TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'todo'
        CHECK (status IN ('todo', 'in_progress', 'done')),
    due_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

This example uses PostgreSQL-style syntax. Other databases use different identity and timestamp syntax.

Why this model?
- every task has an owner;
- an owner must exist;
- email is unique;
- status is constrained to known values;
- creation time is persisted;
- task rows are separate from user rows to avoid repeating user information.

A production application would also consider indexes, access rules, lifecycle/soft deletion needs, audit history, and whether status should be a lookup table or enum.

## 4. A typical request lifecycle

Imagine a user clicks “Create task.”

1. The frontend sends an HTTPS request to the backend.
2. The backend authenticates the user.
3. The backend validates the request body.
4. The backend checks that the user is allowed to create this task.
5. The application uses a driver or ORM to send a parameterized insert.
6. The database checks types, constraints, and transaction rules.
7. The database commits the change if successful.
8. The backend receives the result and creates a safe response.
9. The frontend updates its view.
10. Logs and metrics help diagnose failures without exposing secrets.

This flow explains why database work is not just a frontend concern. The application must decide who can change which records and what happens if the insert fails.

## 5. Driver, ORM, and query builder

- **Driver:** connects application code to the database and sends queries/results.
- **ORM:** maps application-level objects/models to database records and can generate queries.
- **Query builder:** helps construct queries programmatically while retaining more explicit SQL control.

Examples include psycopg for PostgreSQL in Python, SQLAlchemy as a Python ORM/toolkit, Prisma for TypeScript/JavaScript, and JDBC for Java.

An ORM does not remove the need to understand SQL. You still need to reason about joins, transactions, indexes, query counts, and the actual SQL generated. For complex analytics or performance-critical paths, explicit SQL can be appropriate.

## 6. Connection pooling

Opening a new database connection for every small request can be expensive. A connection pool reuses a bounded set of connections.

Think about:
- maximum connection count;
- application instance count multiplied by pool size;
- idle and timeout behavior;
- serverless or short-lived workloads;
- transaction boundaries;
- what happens when the database is unavailable.

A pool should be configured for the database's capacity and deployment topology. More connections do not always mean more throughput.

## 7. Migrations: evolving the schema safely

Applications change. You may add a column, create a table, add an index, or backfill data. A migration records that change in a repeatable, reviewable way.

A safe workflow:
1. Make a migration file under version control.
2. Review how it behaves on existing data.
3. Test it against a disposable database with realistic data.
4. Consider whether it locks or rewrites a large table.
5. Deploy in a compatible order if old and new application versions may run together.
6. Back up important data and have a recovery plan.
7. Verify after deployment.

Avoid manually editing production schema in ways that are not recorded. A migration should be idempotent or managed by a migration tool's tracking system as appropriate.

## 8. Transactions and business logic

A single request may update multiple rows. For example, a purchase could create an order and reserve inventory. Those changes often belong in one transaction so the database does not commit only half the operation.

However, payment providers, email, and third-party APIs cannot normally join your local database transaction. Use reliable workflow designs, idempotency keys, retries, an outbox pattern, or compensating actions when necessary. Do not assume one SQL transaction can roll back an external payment.

## 9. Database in an AI/ML project

A typical AI application may use multiple storage systems because they serve different roles:

```text
User request
   |
   v
Backend API
   ├── PostgreSQL: users, permissions, jobs, metadata, billing state
   ├── Object storage: uploaded PDFs, images, datasets, model artifacts
   ├── Queue: asynchronous document/model jobs
   ├── Vector index: embedding similarity retrieval, if needed
   └── Model API / inference service
           |
           v
      Results stored with status, provenance, and timestamps
```

Examples:
- a tender copilot stores tender metadata, extraction results, checklists, and review status in a relational database; the original PDF often lives in object storage;
- a GST reconciliation tool stores invoice records and discrepancy decisions, while uploaded spreadsheets and reports may live in object storage;
- a RAG application stores document metadata and access permissions, with chunk text/embeddings in a relational or vector-capable store;
- an ML experiment tracker stores experiment configuration, metrics, and artifact locations; large artifacts belong in appropriate object storage.

Do not store every model weight or uploaded PDF directly in a relational table by default. Keep references, metadata, ownership, retention, and access controls consistent.

## 10. A practical database setup workflow

For a new project:

1. **List entities:** what real-world things does the application need to remember?
2. **List operations:** create, read, update, delete, search, aggregate, relate, and audit.
3. **Choose a model:** relational by default for structured related business records; choose another family when it fits a specific workload.
4. **Draw relationships:** identify one-to-one, one-to-many, and many-to-many relationships.
5. **Define constraints:** keys, uniqueness, required fields, valid ranges, and relationships.
6. **Choose a product:** consider query requirements, hosting, skills, cost, and expected scale.
7. **Create migrations:** make schema changes reproducible.
8. **Connect securely:** use drivers/ORMs, secret management, least privilege, and encrypted connections where appropriate.
9. **Build data-access code:** keep queries and transactions testable.
10. **Test:** include constraints, authorization, transaction failure, edge cases, and realistic queries.
11. **Observe:** monitor latency, errors, slow queries, connection usage, and storage.
12. **Operate:** automate backups, test restores, patch, plan retention, and document recovery.

## 11. Local development and deployment

For local development, a developer may run PostgreSQL or MySQL through a local installer or Docker, or use SQLite for an embedded setup. A managed database can reduce server administration in production, but still requires network restrictions, credentials, backup settings, monitoring, and cost control.

Keep development, test, and production data separate. Never point experiments at a production database. Do not commit database passwords or connection strings containing secrets.

## 12. Testing strategy

Test more than whether the API returns HTTP 200:
- schema constraints reject invalid data;
- users cannot read or modify another user's records;
- transactions roll back correctly after failure;
- duplicate requests do not create duplicate business actions where idempotency is required;
- migrations work from a clean database and an existing database;
- common queries perform acceptably with realistic volumes;
- backup restore procedures work;
- database outages and timeouts produce controlled errors.

Use isolated test databases or containers and clean up test data. Avoid relying on a developer's personal database state.

## 13. Common mistakes

- Choosing MongoDB, Redis, or a vector database because it is fashionable rather than because the workload fits.
- Treating a database as a replacement for object storage.
- Storing credentials in Git or frontend bundles.
- Building SQL by concatenating untrusted input.
- Forgetting authorization in queries and APIs.
- Using an ORM without understanding generated queries.
- Adding indexes without measuring or never adding indexes at all.
- Skipping migrations and editing production by hand.
- Assuming replication means backups are unnecessary.
- Ignoring data retention and deletion.
- Using one database for both operational transactions and heavy analytics without measuring the impact.
- Adding many infrastructure services to an MVP before proving they are needed.

## A small project to practise

Build a personal task API:
- backend: FastAPI, Express, Spring Boot, or another stack you are learning;
- database: PostgreSQL or SQLite;
- tables: users and tasks;
- API: create, list, update, complete, and delete tasks;
- safety: parameterized queries, validation, authentication/authorization if users are supported;
- quality: migrations, tests, indexes for actual query patterns, and a backup/restore note.

Once it works, add search/filtering, pagination, audit history, and a background job. This teaches more about database engineering than creating a table and stopping there.
