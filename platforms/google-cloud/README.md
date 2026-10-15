# Google Cloud Platform (GCP)

Google Cloud is Google's cloud computing platform. It provides services for running applications, storing files, managing databases, analyzing data, deploying AI systems, and securing production infrastructure.

You will often hear it called **Google Cloud Platform (GCP)**. "Google Cloud" is the current product branding, while GCP remains a common abbreviation.

This guide explains the platform from a beginner's point of view: how it is organized, which services matter first, how they fit together, how billing works, and how to start learning it safely.

## 1. What Is Cloud Computing?

Imagine you build an app on your own computer. To make it available to other people, the app needs a computer that stays online, networking, storage, security, and often a database. Operating all of this yourself takes time.

Cloud computing lets you rent computing resources and use managed services over the internet instead of buying and maintaining every server yourself.

With Google Cloud, you can:
- Run a website, API, background worker, or scheduled job.
- Store images, documents, backups, and other files.
- Use a managed SQL or NoSQL database.
- Analyze large datasets.
- Train, evaluate, and serve machine-learning models.
- Manage identities, permissions, networking, logs, and deployments.

Official starting point: [Google Cloud documentation](https://cloud.google.com/docs).

## 2. The Mental Model: How Google Cloud Is Organized

The basic hierarchy is:

- **Organization (optional for many individual learners):** often represents a company, school, or institution.
- **Folders (optional):** group projects by team, department, or environment.
- **Projects:** organize cloud resources and settings.
- **Resources:** individual services or objects, such as a Cloud Run service, virtual machine, database, or storage bucket.

A simple hierarchy looks like this:

Organization → Folders → Projects → Resources

Individual learners may not need an organization or folders. Projects are the most important starting point. A project has a project ID, settings, enabled APIs, permissions, and a billing relationship.

For example, you could maintain separate projects for a learning sandbox, a portfolio app, and a production app. Keeping experiments separate from production can make access controls, cost tracking, and cleanup easier.

A **billing account** pays for eligible usage. A project may exist without billing being active, but many services and actions require billing. Treat billing as part of the setup, not as an afterthought.

Many services also require you to enable the corresponding API in the project before using them.

## 3. The Most Useful Services to Know

You do not need to memorize every Google Cloud product. Start by understanding which problem each major service solves.

| Service | What it does | Example use |
|---|---|---|
| [Compute Engine](https://cloud.google.com/compute) | Virtual machines that you manage | A custom server or workload needing operating-system control |
| [Cloud Run](https://cloud.google.com/run) | Runs applications, containers, services, and jobs on managed infrastructure | Deploying a Python API or web backend |
| [Cloud Storage](https://cloud.google.com/storage) | Stores objects such as files and media | PDFs, images, exports, and backups |
| [Cloud SQL](https://cloud.google.com/sql) | Managed relational databases, including PostgreSQL and MySQL | Users, orders, and structured application records |
| [Firestore](https://cloud.google.com/firestore) | Managed NoSQL document database | Flexible document-oriented application data |
| [BigQuery](https://cloud.google.com/bigquery) | Analytics data warehouse for SQL-based analysis at scale | Analyzing large datasets and event records |
| [Vertex AI](https://cloud.google.com/vertex-ai/docs) | Machine-learning and AI development, evaluation, and deployment tools | Building AI/ML applications and model workflows |
| [Pub/Sub](https://cloud.google.com/pubsub) | Messaging between independent services | Sending an event from one service to another |
| [Identity and Access Management (IAM)](https://cloud.google.com/iam/docs/overview) | Controls which identities can do which actions on which resources | Giving an application permission to access a bucket |
| [Secret Manager](https://cloud.google.com/secret-manager/docs) | Stores and manages sensitive values | API tokens, credentials, and private configuration |
| [Cloud Build](https://cloud.google.com/build/docs) | Runs builds and automation workflows | Building and testing code as part of CI/CD |
| [Artifact Registry](https://cloud.google.com/artifact-registry/docs) | Stores build artifacts and container images | Keeping the image that Cloud Run deploys |
| [Cloud Logging](https://cloud.google.com/logging/docs) | Collects and searches logs from applications and services | Diagnosing errors after deployment |
| [VPC networking](https://cloud.google.com/vpc/docs/overview) | Provides networking and network controls | Connecting resources securely |

### Important distinctions

**Compute Engine vs Cloud Run:** Compute Engine gives you a virtual machine and more control over its operating system, which also means more maintenance and configuration. Cloud Run is a managed application platform: you provide code or a container, and Google manages much of the underlying infrastructure. Choose based on the control your workload needs.

**Cloud Storage vs a database:** Cloud Storage is for objects such as PDFs, photos, and files. Cloud SQL and Firestore hold application data. An app might store a PDF in Cloud Storage and put its owner, filename, and metadata in a database.

**Cloud SQL vs BigQuery:** Cloud SQL is generally for application transactions, such as creating a user or updating an order. BigQuery is for analytics across large datasets. They solve different problems.

**Vertex AI vs Cloud Run:** Vertex AI provides AI/ML capabilities and tooling. Cloud Run hosts your application code and services. An AI application can run its API on Cloud Run and call a model through an appropriate AI service.

## 4. Example: An AI Study Assistant

Suppose you build an app where a student uploads notes and asks questions about them. One possible architecture is:

- **Frontend:** the student's browser or web interface.
- **Cloud Run:** the backend API that validates requests and coordinates the work.
- **Cloud Storage:** stores uploaded PDFs and other files.
- **Firestore or Cloud SQL:** stores users, file metadata, and application records.
- **Vertex AI or another approved model API:** generates AI responses, depending on the design.
- **Secret Manager:** stores sensitive credentials when needed.
- **Cloud Logging:** helps diagnose failures.

A typical request might work like this:

1. The student uploads a PDF through the app.
2. The backend stores the file in Cloud Storage.
3. The database records who owns the file and its metadata.
4. When the student asks a question, the backend retrieves relevant information and calls the configured model or retrieval pipeline.
5. The backend sends the answer to the frontend.
6. Logs help with troubleshooting, while IAM determines which resources the backend may access.

This is an example, not a requirement to use every service. A first prototype might need only Cloud Run and one data store. Add services when they solve a real need.

## 5. Regions and Zones

Cloud resources may be associated with a **region** or a **zone**.

- A **region** is a geographic area containing Google Cloud resources.
- A **zone** is an isolated deployment area within a region.

Some products are regional, some zonal, and some global. Availability, latency, data residency, resilience, and pricing can depend on the location you choose.

For a learning project, choose a location supported by the services you need and appropriate for your users and data requirements. Do not assume every service is available in every region.

Official reference: [Google Cloud locations](https://cloud.google.com/about/locations).

## 6. IAM and Security Basics

IAM determines **who can do what on which resource**. An identity could be a human user or a service account used by an application.

Follow these beginner-safe practices:

1. **Apply least privilege.** Give an identity only the permissions it needs.
2. **Prefer service identities for workloads.** Configure the application's service account with required access instead of embedding a personal credential in code.
3. **Keep secrets out of Git.** Do not commit API keys, passwords, service-account private keys, or files containing secrets.
4. **Use Secret Manager where appropriate.** Restrict access to each secret to the workloads that need it.
5. **Be careful with public access.** Do not make a storage bucket or service public unless that is explicitly required and understood.
6. **Separate experiments from production.** Different projects can help isolate resources and permissions.
7. **Review access periodically.** Remove permissions and resources that are no longer needed.

A credential committed to a public repository should be treated as exposed: revoke or rotate it, then remove it from active code and configuration. Deleting it in a later commit does not guarantee that the old value is gone from Git history or copies.

Official references: [IAM overview](https://cloud.google.com/iam/docs/overview) · [Secret Manager](https://cloud.google.com/secret-manager/docs).

## 7. Billing and the Free Tier — Read Before Deploying

Cloud services can incur charges. "Serverless" does not mean every usage pattern is free, and stopping one resource does not necessarily delete all other billable resources in a project.

### Free Trial

According to Google's current documentation when this guide was prepared, eligible new customers can receive **US$300 in welcome credit for 90 days** and access eligible Free Tier products. Eligibility, covered products, and program conditions apply. Check the official [Google Cloud Free Program](https://cloud.google.com/free) before signing up.

Important distinctions:
- Free Tier products have specific monthly usage limits.
- Usage beyond those limits may be billable, depending on billing status and remaining credit.
- Trial resources may stop when the trial ends unless the account is upgraded under the program's terms.
- The trial credit **does not pay for Gemini API costs in Google AI Studio**. Google's documentation points users toward the applicable Gemini API free tier or billing options.
- Prices, eligibility, and free limits may change. Always confirm the current official terms.

### Cost-control checklist

- Read the pricing information for every service before using it.
- Use a separate sandbox project for experiments.
- Create a [billing budget and alerts](https://cloud.google.com/billing/docs/how-to/budgets).
- Remember that **budget alerts are notifications, not a guaranteed hard spending cap**.
- Avoid leaving unused VMs, disks, databases, addresses, or other resources running.
- Check storage, networking, and data-transfer costs as well as compute costs.
- After a tutorial, inspect the resources it created and delete what you no longer need.
- Use the [Google Cloud pricing calculator](https://cloud.google.com/products/calculator) to estimate costs.

Understand the billing terms before adding payment details or deploying billable resources. Treat every service as potentially chargeable until you verify its current free allowance and pricing.

## 8. Google Cloud vs Google AI Studio vs Firebase

These products are related, but they are **not interchangeable**.

| Product | Main purpose | Think of it as |
|---|---|---|
| Google AI Studio | Experimenting with Gemini prompts and building with the Gemini API | An AI model experimentation and prototyping environment |
| Google Cloud | Hosting apps and managing infrastructure, data, networking, security, and production services | The broader cloud platform |
| Firebase | App-development services such as authentication, databases, hosting options, and analytics | A developer-focused app platform that integrates with Google Cloud |

For example, you can prototype a Gemini prompt in Google AI Studio, then build a backend running on Cloud Run and store uploaded documents in Cloud Storage. Firebase can be a good choice for specific app features, depending on your architecture.

Choosing Google Cloud does not mean you must use Vertex AI. Using Gemini through AI Studio does not automatically mean you need to deploy on Google Cloud. Pick each component according to the application's requirements, data handling, and billing model.

## 9. Google Cloud and AWS: Rough Service Equivalents

These are useful mental comparisons, not claims that the services have identical features or pricing.

| Google Cloud | Rough AWS comparison | Main category |
|---|---|---|
| Compute Engine | Amazon EC2 | Virtual machines |
| Cloud Run | AWS App Runner or other managed container/serverless options, depending on workload | Managed application execution |
| Cloud Storage | Amazon S3 | Object storage |
| Cloud SQL | Amazon RDS | Managed relational databases |
| Google Kubernetes Engine (GKE) | Amazon EKS | Managed Kubernetes |
| BigQuery | Amazon Redshift | Data warehousing and analytics |
| Pub/Sub | Amazon SNS/SQS, depending on messaging pattern | Messaging |
| Vertex AI | Amazon SageMaker AI | AI/ML platform capabilities |
| IAM | AWS IAM | Identity and permissions |

When comparing providers, look beyond product names. Consider the workload, regional availability, security configuration, operational effort, integrations, quotas, and total cost.

## 10. Beginner Learning Path

Follow this sequence instead of trying to learn the entire platform at once.

### Stage 1 — Understand the foundation
- Learn projects, billing, regions, zones, resources, and APIs.
- Explore the [Google Cloud Console](https://console.cloud.google.com/).
- Understand IAM roles and service accounts before granting permissions.

### Stage 2 — Deploy a small application
- Build a simple Python or Node.js HTTP API.
- Follow a [Cloud Run quickstart](https://docs.cloud.google.com/run/docs/quickstarts).
- Learn environment configuration, logs, request handling, and service access controls.
- Check billing implications before deploying.

### Stage 3 — Add persistence
- Store uploaded files in Cloud Storage.
- Add Cloud SQL or Firestore only if your application needs a database.
- Learn how to grant your application access without hard-coding credentials.

### Stage 4 — Operate the app responsibly
- Inspect logs in Cloud Logging.
- Understand IAM, Secret Manager, and network access.
- Set budget alerts and clean up unused resources.
- Learn how to roll out and verify a new version.

### Stage 5 — Explore AI/ML services
- Learn Vertex AI concepts through its [official documentation](https://cloud.google.com/vertex-ai/docs).
- Start with a small, clearly scoped AI feature.
- Compare model/API suitability, latency, data handling, and pricing before settling on an architecture.

### Official entry points
- [Google Cloud documentation](https://cloud.google.com/docs)
- [Cloud Run documentation](https://docs.cloud.google.com/run/docs)
- [Cloud Storage documentation](https://cloud.google.com/storage/docs)
- [Cloud SQL documentation](https://cloud.google.com/sql/docs)
- [Vertex AI documentation](https://cloud.google.com/vertex-ai/docs)
- [Google Cloud Free Program](https://cloud.google.com/free)
- [Google Cloud pricing calculator](https://cloud.google.com/products/calculator)

## 11. Quick Self-Test

1. What is the difference between a project and a resource?
2. When might Cloud Run be simpler than managing a virtual machine?
3. When should a file go into Cloud Storage rather than Cloud SQL?
4. How is a relational database workload different from a BigQuery analytics workload?
5. What problem does IAM solve, and what does least privilege mean?
6. Why should secrets never be committed to a public GitHub repository?
7. Why does a free trial not guarantee that every service or usage pattern is free?
8. How do Google AI Studio, Google Cloud, and Firebase differ?

### Answers to check your understanding

1. A project organizes resources and settings; a resource is an individual cloud object or service instance.
2. When you want Google to manage much of the underlying application infrastructure and the workload fits Cloud Run.
3. Use Cloud Storage for files and objects; use a database for structured or document-style application records and queries.
4. An operational database handles application transactions; BigQuery is optimized for large-scale analytics.
5. IAM controls access; least privilege means granting only the permissions required for a task.
6. A committed secret can be copied or preserved in history, so treat it as exposed and rotate it if leaked.
7. Free offers apply only to eligible products and specified limits; other usage may be chargeable.
8. AI Studio is for model experimentation, Google Cloud is the broader cloud platform, and Firebase provides app-development services that integrate with Google Cloud.

---

**Guiding principle:** deploy only what you understand, give it only the permissions it needs, monitor its cost, and clean up resources when an experiment is finished.
