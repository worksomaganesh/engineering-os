# AWS — Amazon Web Services

## 1. What Is AWS?

**AWS stands for Amazon Web Services.** It is a cloud-computing platform that provides services for running applications, storing files, managing databases, networking, monitoring systems, and building AI workloads.

Instead of buying and maintaining all the physical computers yourself, you can provision resources hosted in Amazon's cloud infrastructure and configure them for your application.

AWS is a collection of services rather than a programming language, a version-control tool, or one single server.

## 2. Why Does AWS Exist?

Imagine that you build an AI-powered website on your laptop. The application works locally, but you want other people to access it at any time, even when your laptop is shut down.

A real application may need:
- A computer to run the backend code
- Storage for uploaded files and generated content
- A database for structured application records
- Networking so users can reach the application
- Identity and access controls
- Logs, monitoring, backup, and recovery mechanisms

You could buy and operate physical servers yourself, but that involves hardware, electricity, networking, maintenance, capacity planning, and other responsibilities.

Cloud platforms let you provision computing resources on demand. You configure the services you need, and the provider operates the underlying infrastructure according to the service model.

## 3. What Is Cloud Computing?

Cloud computing means using computing resources and services over a network instead of relying exclusively on equipment you own and operate yourself.

Resources may include:
- Compute capacity for running programs
- Object and block storage
- Managed databases
- Virtual networks and load balancers
- Monitoring and logging services
- Identity, permissions, and security tools
- Data processing and AI services

Cloud doesn't mean everything is automatically free, secure, highly available, or maintenance-free. You still choose configurations, manage your application, control access, monitor usage, and understand the cost model.

## 4. Important AWS Services to Know First

AWS has many services. Begin with the following core building blocks rather than attempting to learn the entire catalogue at once.

### 4.1 Amazon EC2 — Virtual servers

Amazon Elastic Compute Cloud (EC2) provides virtual server instances.

You can use an EC2 instance to:
- Run a Python or Node.js backend
- Host an API
- Install packages and configure a runtime
- Run background jobs
- Test server-side software

Mental model: EC2 gives you a configurable computer in the cloud. You remain responsible for the operating system and software you install, as well as system updates and security settings appropriate to your setup.

Documentation: https://docs.aws.amazon.com/ec2/

### 4.2 Amazon S3 — Object storage

Amazon Simple Storage Service (S3) stores objects in buckets.

Typical uses include:
- User-uploaded PDFs and images
- Datasets and exported reports
- Static files and backups
- Training artifacts and generated files

S3 is object storage, not the same thing as a general-purpose virtual server disk. Access permissions, bucket configuration, lifecycle rules, and data-transfer costs should be considered.

Documentation: https://docs.aws.amazon.com/s3/

### 4.3 Amazon RDS — Managed relational databases

Amazon Relational Database Service (RDS) helps you operate supported relational database engines without managing every infrastructure and database-administration task yourself.

Typical uses include:
- User and organisation records
- Orders and transactions
- Structured application data
- Relational data queried with SQL

A managed database still needs appropriate schema design, authentication, authorisation, backups, connectivity restrictions, and cost monitoring.

Documentation: https://docs.aws.amazon.com/rds/

### 4.4 AWS Lambda — Run code in response to events

AWS Lambda runs code in response to events or requests, while AWS manages the underlying execution infrastructure.

Possible uses:
- Process a file when it is uploaded
- Run a scheduled task
- Respond to an API request
- Transform data when an event occurs

Lambda is often called a serverless compute service. **Serverless does not mean there are no servers**; it means you do not manage the servers directly in the same way you would with a conventional virtual machine.

Documentation: https://docs.aws.amazon.com/lambda/

### 4.5 AWS IAM — Identity and Access Management

AWS Identity and Access Management (IAM) controls which identities can access AWS resources and which actions they can perform.

IAM is relevant when:
- Giving a developer access to a particular resource
- Allowing an application to access an S3 bucket
- Restricting which actions a role can take
- Applying least-privilege permissions

Avoid using overly broad permissions as a convenience. Grant only the access required for a user's or application's task, and follow current AWS guidance for credentials and roles.

Documentation: https://docs.aws.amazon.com/iam/

### 4.6 Other service categories

As your projects grow, you may encounter services for:
- Virtual networking, routing, and load balancing
- DNS and content delivery
- Logs, metrics, and operational monitoring
- Container images and container orchestration
- Data warehouses and analytics
- Machine-learning development and model hosting
- Secrets and encryption management

You do not need all of these services for every application. Choose them based on the architecture and requirements.

## 5. How AWS Fits into an AI Application

Imagine building an AI study assistant that lets students upload PDFs and ask questions about them.

One possible architecture is:

```text
Student's browser
       |
       v
Frontend application
       |
       v
Backend API hosted on AWS
       |
       +------> S3: stores uploaded documents
       |
       +------> RDS: stores structured application records
       |
       +------> External AI API or an appropriate AWS AI service
       |
       v
Backend returns the answer
       |
       v
Frontend displays the response
```

A request might follow this path:

1. The student submits a question.
2. The frontend sends it to the backend.
3. The backend validates the request and checks the user's permissions.
4. The backend retrieves any required data or document content.
5. The backend calls the chosen AI service.
6. The backend applies the necessary checks and returns the answer.
7. The frontend displays it.

This is only one possible design. A small application may not need a separate relational database, and a static site may not need a traditional backend server at all.

### AWS and the AI model are not necessarily the same service

You can host the application on AWS and call an external model provider's API. You can also use suitable AWS AI services for parts of the workload.

In either design, keep private credentials on the server or in an appropriate secret-management facility. Do not embed private provider keys into JavaScript delivered to a user's browser.

## 6. AWS vs. Your Computer, Git, and GitHub

| Tool or platform | Main role |
|---|---|
| Your computer | Write and run code locally |
| Git | Track file changes and project history |
| GitHub | Host Git repositories and support collaboration |
| AWS | Provide cloud infrastructure and managed services to deploy and operate software |

These tools complement each other.

A developer can write code locally, commit it with Git, publish it to GitHub, and deploy the application to AWS. A continuous integration/deployment workflow can automate some of those steps.

Uploading source code to GitHub does not by itself deploy an application to AWS. Deployment requires the appropriate build and deployment process, credentials, configuration, and target service.

## 7. Is AWS Free?

AWS is not an entirely free platform. It offers free usage options and offers that depend on the services, account eligibility, usage limits, and current terms. Other usage is billable.

Cost may depend on factors such as:
- Time a compute resource is running
- Storage consumed
- Number and type of requests
- Database capacity and configuration
- Data transfer
- Region
- Monitoring, backups, and other related resources

Do not assume that a running server is free just because it receives no visitors. A resource may incur charges while it remains provisioned.

### Cost-control habits for beginners

1. Read current pricing for the specific service and region.
2. Check which free offers apply to the account and how long they last.
3. Set up billing notifications or budget alerts where available.
4. Stop or delete resources when no longer needed.
5. Inspect related resources such as disks, snapshots, IP addresses, databases, and logs.
6. Review the bill or usage dashboard after experiments.

A billing alert is a warning mechanism, not necessarily a strict spending cap. Verify which controls the service actually enforces.

Pricing and free-tier rules can change; consult the current official pricing pages before deploying anything that may incur charges.

## 8. Security Basics

Cloud services do not secure every aspect of an application automatically. Security is shared between the provider and the customer, with responsibilities varying by service.

Useful habits include:
- Use IAM roles and scoped permissions appropriately.
- Avoid exposing database ports to the entire internet.
- Keep software and operating systems updated where you manage them.
- Store secrets in appropriate secret-management facilities.
- Avoid committing API keys or credentials to GitHub.
- Enable suitable logging and monitoring.
- Protect backups and sensitive data.
- Check who can access each resource.
- Understand the security responsibilities of managed services.

For example, an S3 bucket containing private documents should not be made public merely to fix an application's access problem. Configure the required access path and permissions instead.

## 9. When Should You Use AWS?

AWS can be useful when you need to:
- Host an application for users beyond your own laptop
- Run a backend API or background job
- Store uploaded files
- Operate a relational database
- Provision cloud networking
- Scale compute or storage according to a workload
- Monitor and operate deployed software
- Use cloud services for suitable data or AI workloads

AWS may be unnecessary for a very small demo that can be hosted more simply. The right option depends on required control, complexity, expected traffic, budget, security needs, and operational skills.

## 10. A Beginner Learning Path

For an AI/ML engineering student, a sensible progression is:

1. **Understand basic prerequisites:** Linux, Git, Python, HTTP, APIs, and basic networking.
2. **Learn cloud vocabulary:** regions, availability, compute, storage, networking, IAM, and billing.
3. **Start with one simple deployment:** learn how to deploy a small application and reach it securely.
4. **Explore a storage service:** practise uploading and retrieving a non-sensitive sample file.
5. **Understand identity and permissions:** give an application only the access it needs.
6. **Add data storage when needed:** learn managed databases if your application has structured persistent data.
7. **Learn monitoring and cost control:** inspect logs, measure resources, and remove unused services.
8. **Explore advanced services when a project requires them:** containers, load balancing, queues, data engineering, or managed AI services.

Do not try to memorise every AWS service. Learn the building blocks through a small project and expand your knowledge when you have a concrete need.

## 11. Questions for Revision

1. What does AWS stand for?
2. What is cloud computing?
3. What problem does EC2 solve?
4. What is S3 designed to store?
5. What does RDS help you manage?
6. What does Lambda do, and what does serverless mean?
7. What is IAM used for?
8. Does uploading code to GitHub automatically deploy it to AWS?
9. Does hosting an application on AWS mean the AI model must also come from AWS?
10. Why can an AWS resource cost money when user traffic is low?
11. Why are billing alerts not necessarily a hard spending limit?
12. Why should cloud credentials and IAM permissions be restricted?
13. What is the difference between GitHub and AWS?
14. Name two reasons a small application might not need AWS yet.

### Answer Key

1. Amazon Web Services.
2. Using computing resources and services over a network rather than relying exclusively on infrastructure that you own and operate.
3. EC2 provides configurable virtual server instances for running software.
4. S3 provides object storage for items such as documents, images, datasets, and backups.
5. RDS helps operate supported relational database engines as a managed service.
6. Lambda runs code in response to events or requests while AWS manages the underlying execution infrastructure; serverless does not mean servers do not exist.
7. IAM manages identities and access permissions for AWS resources.
8. No. Deployment needs an appropriate build/deploy process and target configuration.
9. No. The application may call an external AI provider or use an appropriate AWS AI service.
10. Some provisioned resources incur charges while running or allocated, independent of visitor traffic.
11. An alert notifies you about usage; it may not automatically prevent all future spending.
12. Restricted access reduces the chance and impact of misuse.
13. GitHub hosts source repositories and collaboration tools; AWS provides cloud infrastructure and services to run applications.
14. Hosting may be unnecessarily complex, and a simpler or local setup may already meet the application's needs.

## 12. Key Takeaway

> **AWS is a collection of cloud services for building, deploying, and operating software. It gives developers access to compute, storage, databases, networking, security, monitoring, and AI-related services without requiring them to own all the underlying physical infrastructure.**

A useful mental model:

```text
Write code locally
       |
       v
Track the code with Git
       |
       v
Store and collaborate through GitHub
       |
       v
Deploy the application to AWS (when appropriate)
       |
       v
Monitor security, reliability, and cost
```

## Further Reading

- [AWS Getting Started](https://docs.aws.amazon.com/getting-started/)
- [Amazon EC2 documentation](https://docs.aws.amazon.com/ec2/)
- [Amazon S3 documentation](https://docs.aws.amazon.com/s3/)
- [Amazon RDS documentation](https://docs.aws.amazon.com/rds/)
- [AWS Lambda documentation](https://docs.aws.amazon.com/lambda/)
- [AWS IAM documentation](https://docs.aws.amazon.com/iam/)
