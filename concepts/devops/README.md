# DevOps — What It Is, Why It Matters, and How It Works

## The short answer

**DevOps is a way of building, releasing, operating, and improving software by bringing development and operations together through shared ownership, automation, fast feedback, and reliable processes.**

It is not just a tool, a job title, or a collection of YAML files. GitHub Actions, Docker, Kubernetes, Terraform, and monitoring tools can support DevOps—but installing those tools does not automatically mean a team practises DevOps.

The goal is to help a team deliver useful software **more safely, reliably, and repeatably**, while learning from how that software behaves after release. Microsoft's [DevOps overview](https://learn.microsoft.com/en-us/devops/what-is-devops) and AWS's [DevOps explanation](https://aws.amazon.com/devops/what-is-devops/) describe DevOps as a combination of culture, practices, and tools across the software lifecycle.

## 1. Understand the problem DevOps solves

Imagine four people working on one application.

- A **developer** writes code and says, "It works on my laptop."
- A **tester** tries to find bugs.
- An **operations engineer** is responsible for running the application reliably.
- A **security engineer** wants credentials and infrastructure to be protected.

Without good collaboration, the process may look like this:

1. A developer finishes a feature and sends the code to another team.
2. The test environment is configured differently from the developer's laptop.
3. The application fails to build or behave correctly.
4. The release team manually fixes configuration.
5. The deployment breaks production.
6. People disagree about who owns the incident.
7. Fixes take longer because the process is manual and hard to reproduce.

The problem is not necessarily that any individual did a bad job. The workflow contains fragile handoffs and hidden assumptions.

**DevOps changes the workflow:** the people building the application take shared responsibility for how it is built, tested, delivered, observed, and improved. Repeatable steps are automated where practical; feedback arrives earlier; security and reliability are considered throughout the process.

### A simple analogy

Think of a restaurant opening a new branch.

- Development is designing the menu and preparing the food.
- Operations is making sure the kitchen, supplies, equipment, staffing, and service work every day.
- Quality checks test that the meal is safe and consistent.
- Monitoring reveals customer waits, equipment problems, and recurring complaints.
- Automation and documented processes help every branch follow reliable procedures.

DevOps is the collaboration and operating system connecting all of those activities—not one machine in the kitchen.

## 2. The software lifecycle DevOps connects

A common way to visualize the process is as a repeating loop:

```text
PLAN
  ↓
CODE
  ↓
BUILD
  ↓
TEST
  ↓
RELEASE
  ↓
DEPLOY
  ↓
OPERATE
  ↓
MONITOR AND LEARN
  └──────────────→ back to PLAN
```

The loop is continuous because a release is not the end of software development. Once users use the application, the team learns about bugs, performance, cost, usability, and new needs. Those observations become the next improvements.

| Stage | What happens | Example |
|---|---|---|
| Plan | Decide the problem, work, risks, and acceptance criteria | Define a password-reset feature and its security conditions |
| Code | Write and review application or infrastructure code | Implement the reset endpoint |
| Build | Turn source into a repeatable artifact | Build a package or container image |
| Test | Validate behavior and quality | Run unit, integration, security, and relevant UI tests |
| Release | Decide which version is ready | Approve a tested build for release |
| Deploy | Put that version into a target environment | Deploy to staging, then production |
| Operate | Keep the service functioning | Manage configuration, capacity, backups, and incidents |
| Monitor and learn | Observe real behavior and use feedback | Detect elevated errors and investigate a slow endpoint |

Not every team uses these exact stage names or separates them into distinct steps. The important idea is the feedback loop and shared responsibility.

## 3. The core principles of DevOps

### 3.1 Shared ownership instead of isolated teams

Developers consider how code will run in production. Operations engineers contribute to design and automation before release. Security and quality checks are integrated into the workflow rather than appearing only at the end.

Shared ownership does not mean everyone must do every job. It means handoffs are clear, feedback is early, and teams work toward the same user and service outcomes.

### 3.2 Automate repeatable work

If developers repeatedly run the same build, tests, packaging, deployment, and validation steps manually, those steps are candidates for automation.

Automation makes the process more repeatable and reduces avoidable human error. But **automating a bad process makes the bad process run faster**. The team must still design the correct checks and keep them maintained.

### 3.3 Make changes small and observable

Smaller changes are usually easier to understand, test, review, and recover from than one enormous release. Version control and code review provide traceability.

Small changes do not automatically mean safe changes; tests, access controls, observability, and sound release design still matter.

### 3.4 Get feedback early

A formatting error should ideally be caught before a deployment. A broken API contract should be caught during development or CI rather than after customers depend on it. A production error should produce enough telemetry to investigate it.

The earlier a problem is detected, the less expensive and disruptive it may be to diagnose and correct.

### 3.5 Design for reliability and recovery

Software will fail sometimes. A mature delivery process plans for failure using health checks, controlled rollouts, alerts, backups, rollback or roll-forward procedures, and blameless learning after incidents.

A deployment pipeline is not reliable merely because it can deploy quickly; it must also help the team notice and recover from problems.

### 3.6 Integrate security throughout the lifecycle

Security belongs in code review, dependencies, secrets management, infrastructure configuration, build pipelines, deployment permissions, and monitoring. This integration is commonly called **DevSecOps**. Security still needs specialists and thoughtful risk assessment; it should not be reduced to a single automated scanner.

## 4. The most important DevOps practices

### 4.1 Version control

Version control—often Git—tracks changes to application and infrastructure code.

It helps the team:
- Understand who changed what and why.
- Review changes before they are merged.
- Work in parallel using branches.
- Identify which commit produced a build.
- Revert or investigate changes when something breaks.

Git is foundational, but Git alone is not DevOps. It is one of the enabling practices.

### 4.2 Continuous Integration (CI)

**Continuous Integration** means developers integrate changes frequently into a shared codebase, and automated checks help validate those changes.

A CI workflow commonly:
1. Starts when code is pushed or a pull request is opened.
2. Installs the required dependencies in a controlled environment.
3. Runs formatting or lint checks.
4. Runs tests and type checks.
5. Builds the application.
6. Publishes clear pass/fail results.

A small example: every pull request to your GitHub repository could trigger GitHub Actions to install dependencies, run tests, and stop a merge from proceeding if required checks fail.

Benefits include earlier defect detection, repeatable checks, and fewer surprises when changes are integrated. CI cannot guarantee correctness; it can only run the checks that have been designed and configured.

### 4.3 Continuous Delivery vs Continuous Deployment

These names are similar but have an important distinction.

| Practice | Meaning |
|---|---|
| Continuous Integration (CI) | Frequently integrate code and validate it with automated checks |
| Continuous Delivery | Keep the software in a tested, deployable state; production release may still require a human approval |
| Continuous Deployment | Automatically deploy every change that passes the defined pipeline to production |

A team can practise CI and continuous delivery without automatically deploying every commit to users. Continuous deployment requires confidence in testing, observability, release safety, and recovery. Microsoft's [continuous delivery guide](https://learn.microsoft.com/en-us/devops/deliver/what-is-continuous-delivery) explains staged validation and approaches for limiting release risk.

### 4.4 Build artifacts and reproducible builds

Source code is not always the thing directly deployed. A build process may produce a compiled binary, a package, a static web bundle, or a container image.

A good workflow records which source commit and build process produced the artifact. Ideally, the same tested artifact is promoted through staging and production, rather than rebuilt differently at each stage.

This reduces the chance that "the code we tested" differs from "the thing we deployed."

### 4.5 Infrastructure as Code (IaC)

Applications need environments: compute, storage, databases, networks, permissions, DNS, and other resources.

**Infrastructure as Code** defines infrastructure in version-controlled files or programs instead of relying entirely on manually clicking through a console.

For example, instead of documenting "create a database, choose these settings, then open this network port" and repeating it manually, an IaC configuration describes the intended environment so a tool can provision and update it consistently.

Popular examples include Terraform and cloud-native infrastructure templates. IaC can improve repeatability and review, but a dangerous configuration can also be repeated automatically. Review changes, protect secrets, and use least privilege.

Reference: [AWS — Infrastructure as Code](https://docs.aws.amazon.com/whitepapers/latest/introduction-devops-aws/infrastructure-as-code.html).

### 4.6 Configuration and secrets management

The same application may need different settings in local development, testing, staging, and production. Configuration should be explicit and appropriately separated from source code.

Sensitive values—database passwords, API keys, signing keys, and cloud credentials—should be kept in suitable secret stores or protected runtime configuration, not committed to Git or embedded in public frontend code.

A deployment that works only because one developer's laptop has undocumented settings is not repeatable.

### 4.7 Containers and orchestration

A **container** packages an application and its dependencies into a standardized runtime unit. Docker is a widely used tool in this area.

Containers can reduce "works on my machine" differences, but they do not automatically provide complete security or guarantee that the application is portable across every environment.

**Container orchestration**, often using Kubernetes for more complex deployments, helps manage groups of containers: scheduling, health checks, scaling, service discovery, and rolling updates. You do not need Kubernetes for every project. For many student projects, a simple managed platform or one container is enough.

### 4.8 Monitoring and observability

Once software is deployed, the team needs to understand how it behaves.

- **Logs** describe events, errors, and context.
- **Metrics** measure values over time, such as request rate, error rate, latency, resource use, and queue depth.
- **Traces** follow a request through multiple services.
- **Alerts** notify the responsible team when conditions need attention.
- **Dashboards** help people investigate trends and service health.

Monitoring can tell you that an endpoint's error rate increased; useful logs and traces help explain where the requests failed.

Observability is not just collecting huge quantities of data. Signals must answer useful questions while avoiding unnecessary sensitive information.

### 4.9 Release strategies

A deployment can be technically successful while still harming users. Common techniques help reduce the impact of a bad release:

- **Rolling deployment:** gradually replace old instances with new ones.
- **Blue-green deployment:** maintain two environments and switch traffic after validating the new version.
- **Canary release:** expose a new version to a small portion of traffic before expanding.
- **Feature flags:** enable or disable specific functionality without necessarily deploying new code.

These strategies do not replace tests and monitoring. They help reduce the blast radius and can support recovery when combined with good operational practices.

### 4.10 DevSecOps

DevSecOps brings security checks and controls into normal delivery workflows.

Examples:
- Dependency vulnerability checks.
- Secret scanning.
- Static application security testing (SAST).
- Container and infrastructure configuration scanning.
- Least-privilege deployment identities.
- Approval gates for production changes.
- Audit logs and monitoring.

Automated tools can find classes of problems, but they produce false positives and have coverage limits. Important findings still need context and appropriate review.

## 5. What does a CI/CD pipeline actually do?

Imagine you push a change to a web application.

1. You push a Git commit or open a pull request.
2. A workflow runner checks out the specific revision.
3. It installs the dependencies in the configured environment.
4. It runs linting, type checks, and automated tests.
5. It builds a deployable artifact.
6. Required checks determine whether the change can proceed.
7. The artifact is deployed to a staging environment.
8. Smoke tests check that key endpoints and user flows work.
9. An approval or policy gate may permit production deployment.
10. The release system deploys using the configured strategy.
11. Monitoring checks health and alerts the team if important signals deteriorate.
12. If a problem occurs, the team follows the tested rollback or roll-forward procedure and investigates the cause.

The key chain is:

**Commit → Build → Test → Package → Release gate → Deploy → Observe → Learn**

A CI/CD pipeline is an automated workflow, not the whole DevOps culture. It cannot compensate for weak tests, unsafe permissions, unreviewed production changes, or missing monitoring.

## 6. A real-world example: deploying an AI study assistant

Suppose you build an AI study assistant with a frontend, a backend API, a database, and a model-provider API.

Without a repeatable DevOps workflow, you might deploy manually, forget an environment variable, break a database migration, or discover that the production logs do not contain enough information to debug a failure.

A basic DevOps workflow might look like this:

**Development**
- Keep the source in Git.
- Store local secrets outside the repository.
- Create a pull request for each meaningful change.

**CI checks**
- Install pinned dependencies.
- Run unit tests for business logic.
- Run API integration tests using a test database.
- Check formatting and types.
- Scan for accidentally committed secrets.

**Build and package**
- Build the frontend.
- Package the backend or create a container image.
- Tag the artifact with the commit SHA or immutable version.

**Staging**
- Deploy to a test environment.
- Use test credentials and synthetic data.
- Run health checks and a browser smoke test.
- Validate the database migration.

**Production**
- Use protected production secrets.
- Require the configured review/approval.
- Deploy the tested artifact.
- Monitor request latency, error rates, AI provider failures, and database health.

**Learning**
- An alert detects that model calls are failing.
- Logs and traces identify the provider timeout.
- You apply a safe fix and test it in the next pipeline run.
- You improve timeouts, retries, and alerts based on the incident.

This is DevOps because the whole path from code to a service users can depend on is intentionally designed—not just because the app is running in Docker.

## 7. How is DevOps useful?

### Faster, more repeatable releases
Automation reduces manual handoffs and lets teams release changes more frequently when their tests and controls are reliable.

### Earlier defect detection
CI tests and build checks can catch certain issues before the code reaches production, when diagnosing and fixing them is often easier.

### Fewer environment surprises
Explicit configuration, containers, and infrastructure definitions reduce undocumented setup differences.

### Better reliability and recovery
Monitoring, controlled deployments, and tested recovery procedures make it easier to notice and address problems.

### More effective collaboration
Developers and operations people share context and responsibility rather than discovering each other's constraints at the final handoff.

### Improved security and auditability
Reviewed infrastructure changes, secret management, limited permissions, and deployment logs improve control over how software reaches production.

### Better feedback from real users
Monitoring and operational incidents reveal whether a feature is useful, reliable, fast, and affordable after deployment.

These are potential outcomes, not automatic guarantees. DevOps can add complexity if a team installs tools without improving its workflow, tests, or ownership.

## 8. Common DevOps tools and what they do

Learn the category first, then choose one tool to practise. You do not need to learn every product listed here.

| Category | Examples | Purpose |
|---|---|---|
| Version control | Git, GitHub | Track changes and collaborate |
| CI/CD workflows | GitHub Actions, GitLab CI/CD, Jenkins, Azure Pipelines | Automate build, test, and release steps |
| Containers | Docker | Package applications and dependencies |
| Orchestration | Kubernetes | Operate containerized workloads at scale |
| Infrastructure as Code | Terraform, cloud-native templates | Define and provision infrastructure repeatably |
| Configuration automation | Ansible and similar tools | Apply repeatable system configuration |
| Cloud platform | AWS, Google Cloud, Azure | Run compute, storage, networking, databases, and managed services |
| Secrets management | Cloud secret managers, Vault-style systems | Store and control access to sensitive values |
| Static/security scanning | CodeQL, Semgrep, dependency scanners | Detect selected code, dependency, and configuration risks |
| Monitoring | Prometheus, Grafana, cloud monitoring products | Observe system health and performance |
| Distributed tracing | OpenTelemetry-compatible tools | Follow requests across service boundaries |
| Incident/alert management | Cloud alerts and on-call tooling | Notify responsible people and coordinate response |

Tool choice depends on the organization, codebase, budget, compliance requirements, and existing stack. Do not choose Kubernetes just because a tutorial uses it, and do not deploy a dozen tools to prove you know DevOps.

## 9. DevOps vs related terms

| Term | Main emphasis | Relationship to DevOps |
|---|---|---|
| DevOps | Shared ownership and practices across development, delivery, and operations | Broad working model |
| CI/CD | Automated integration, testing, packaging, and delivery/deployment workflows | A set of important DevOps practices |
| DevSecOps | Security integrated into software delivery and operations | Security-focused extension of the same lifecycle |
| SRE (Site Reliability Engineering) | Reliability engineering, service objectives, incident response, and reducing operational toil | Often complements DevOps and makes reliability goals measurable |
| Platform Engineering | Internal platforms and reusable capabilities that make teams more productive and safer | Can provide shared infrastructure and self-service workflows for DevOps teams |
| MLOps | Operationalizing ML systems: data/model pipelines, evaluation, deployment, monitoring, and lifecycle | Applies DevOps ideas to machine-learning systems, with ML-specific needs |

These terms overlap in practice. They are not mutually exclusive teams or competing philosophies.

## 10. DevOps and an AIML student

DevOps is useful for an AIML student because an AI/ML project is more than a notebook or a model that produces one output.

A model-based application may need:
- A reproducible environment and dependency versions.
- Dataset and model version tracking.
- Tests for preprocessing and API behavior.
- A repeatable way to package and deploy inference code.
- Secrets management for external model APIs.
- Monitoring for failures, latency, cost, and sometimes prediction/data quality.
- A rollback or redeployment path when a model or application release is faulty.

**MLOps** extends operational practices to the particular lifecycle of machine-learning systems, including data/model evaluation and model drift where relevant. Traditional DevOps remains useful for the API, frontend, infrastructure, authentication, CI/CD, observability, and runtime around the model.

DevOps is therefore especially useful when you move from "my model works in this notebook" to "another person can run the same version, use it reliably, and access it as a deployed service."

## 11. A beginner roadmap for learning DevOps

Learn enough to ship and operate one small project before chasing advanced infrastructure.

### Stage 1 — foundation
Learn Git, Linux command-line basics, environment variables, processes, networking basics, and how an application starts.

**Goal:** be able to run, inspect, and debug a small application locally.

### Stage 2 — automated checks
Create a repository with a small test suite. Configure GitHub Actions or another CI tool to run tests automatically on a pull request.

**Goal:** a broken test produces a failed check and a clear reason.

### Stage 3 — environment and packaging
Use a dependency lockfile and package the app consistently. Learn Docker after understanding the application process and its dependencies.

**Goal:** another developer can run the app using documented commands or a container.

### Stage 4 — deploy a small application
Deploy a simple API or full-stack app to one managed hosting/cloud platform. Configure environment variables and secrets safely.

**Goal:** a public or private test deployment can be updated through a repeatable workflow.

### Stage 5 — monitor it
Add health checks, structured logs, error tracking, and basic latency/error metrics. Trigger a test failure and learn how to investigate it.

**Goal:** you can answer "Is the service healthy? If not, how do I know what failed?"

### Stage 6 — infrastructure and release safety
Learn basic Infrastructure as Code and a safe deployment strategy. Add a staging step, smoke tests, and a manual approval before production if appropriate.

**Goal:** you can recreate a simple environment and explain how you would recover from a bad release.

### Stage 7 — security and reliability
Learn least privilege, secret scanning, dependency updates, backups, incident response, and cost awareness. Add resource limits and safe failure handling.

**Goal:** your pipeline protects against common mistakes, not only happy-path failures.

You do not need to master Kubernetes, service meshes, multi-region clusters, or complex deployment architectures before you can build something useful.

## 12. Beginner projects that teach DevOps

### Project A — CI for a Python API
- Create a small FastAPI/Flask application.
- Add unit tests.
- Configure CI for pull requests.
- Make a test fail intentionally and observe the result.

**You learn:** Git workflow, CI triggers, dependency installation, testing, and pipeline failures.

### Project B — Dockerize an application
- Package the API.
- Use a small base image and a non-root runtime where practical.
- Configure environment variables correctly.
- Keep secrets out of the image.

**You learn:** images, containers, configuration, reproducibility, and basic runtime security.

### Project C — deploy with a pipeline
- Deploy the app to a managed cloud platform.
- Keep test and production config separate.
- Use a health endpoint and a smoke test.
- Store credentials as protected platform secrets.

**You learn:** deployment automation, environment configuration, permissions, and release validation.

### Project D — add observability
- Emit structured application logs.
- Track latency and errors.
- Add an alert for an intentionally triggered failure.
- Write a short incident note describing diagnosis and prevention.

**You learn:** operational feedback, debugging, and recovery.

### Project E — deploy an AI endpoint
- Expose a small model or model-provider API through an authenticated endpoint.
- Add request limits, timeout/retry policy, secret management, and cost/error metrics.
- Use CI for tests and deploy a versioned artifact.
- Evaluate the model response separately from API uptime.

**You learn:** the bridge between DevOps and MLOps. A healthy server does not prove the model is accurate; monitor both service reliability and model/data quality where appropriate.

## 13. Common misconceptions

**"DevOps is a tool."**  
No. It is a way of working supported by practices and tools.

**"DevOps means CI/CD."**  
CI/CD is important, but DevOps also includes culture, infrastructure, security, operations, feedback, reliability, and improvement.

**"If I use Docker, I am doing DevOps."**  
Docker supports packaging and runtime consistency. It does not by itself give you automated tests, safe releases, observability, shared ownership, or recovery practices.

**"Everyone should use Kubernetes."**  
No. Choose the simplest infrastructure that reliably meets the requirements. Orchestration has operational cost.

**"Continuous deployment means every change must automatically go live."**  
No. Continuous delivery can keep changes ready for release with a manual approval. Continuous deployment automates production release after the defined checks.

**"Automation removes the need for testing."**  
Automation runs tests consistently; it does not make weak tests meaningful.

**"A green pipeline guarantees a bug-free application."**  
A green pipeline means the configured checks passed. Missing or poorly designed tests can miss important problems.

**"DevOps is only for large companies."**  
A solo developer can use version control, CI, reproducible environments, safe deployment, and logs. The scale of the implementation changes with the project.

**"DevOps and MLOps are the same."**  
They overlap. ML systems also need attention to data, model versions, evaluation, drift, and experiment reproducibility.

## 14. Measuring whether DevOps is helping

Do not measure success only by number of deployments or lines of automation.

Useful measures can include:
- **Deployment frequency:** how often changes are successfully released.
- **Lead time for changes:** how long it takes for a change to go from committed work to running in production.
- **Change failure rate:** how frequently deployments cause a failure or require remediation, using a clearly defined formula.
- **Time to restore service:** how long it takes to recover from a service-impacting failure.
- **Reliability and user impact:** error rates, availability, latency, and customer-impacting incidents.
- **Delivery friction:** time spent waiting for reviews, environments, or manual handoffs.
- **Security and recovery:** time to address important vulnerabilities, restore backups, or recover from an incident.

DORA's [research and Core Model](https://dora.dev/research/) provides evidence-based capabilities and measures for improving software delivery and organizational performance. Use metrics to improve the system, not to rank individuals or encourage teams to ship risky changes faster. Interpret them in the context of the service and the people doing the work.

## 15. How DevOps relates to AI coding agents

AI agents may increasingly write code, update tests, or propose infrastructure changes. The organization still needs to answer:
- Did the change pass the required tests?
- Were the right permissions used?
- Is the artifact traceable to the source commit?
- Did the deployment happen in the intended environment?
- Did the service remain healthy?
- Can we detect and recover from a bad change?

DevOps provides the automation and operational feedback around AI-assisted coding. An agent can help author a pipeline, but the pipeline's permissions, secrets, tests, deployment gates, and recovery behavior still require engineering judgment and verification.

A sensible principle is: **automate routine steps, keep permissions narrow, make critical changes observable, and require appropriate human approval for risky actions.**

## 16. Official learning resources

- [Microsoft Learn — What is DevOps?](https://learn.microsoft.com/en-us/devops/what-is-devops)
- [AWS — What is DevOps?](https://aws.amazon.com/devops/what-is-devops/)
- [Google Cloud — DevOps and DORA research](https://cloud.google.com/devops)
- [Google Cloud — DevOps capabilities](https://docs.cloud.google.com/architecture/devops)
- [Microsoft Learn — Continuous delivery](https://learn.microsoft.com/en-us/devops/deliver/what-is-continuous-delivery)
- [AWS — Infrastructure as Code](https://docs.aws.amazon.com/whitepapers/latest/introduction-devops-aws/infrastructure-as-code.html)
- [DORA — Research](https://dora.dev/research/)
- [GitHub Actions documentation](https://docs.github.com/en/actions)
- [Docker documentation](https://docs.docker.com/)
- [Terraform documentation](https://developer.hashicorp.com/terraform/docs)
- [Kubernetes documentation](https://kubernetes.io/docs/home/)
- [OpenTelemetry documentation](https://opentelemetry.io/docs/)

Use current official documentation for commands, service pricing, security requirements, and certification details; cloud and tool behavior can change.

## 17. Quick self-test

1. In your own words, what is DevOps, and why is it more than a tool?
2. What problem does CI solve?
3. What is the difference between continuous delivery and continuous deployment?
4. Why is Infrastructure as Code useful?
5. Why does a container not automatically make an application secure?
6. What information do logs, metrics, and traces provide?
7. Why can a passing CI pipeline still ship a bug?
8. How can staging, canary releases, or feature flags reduce deployment risk?
9. What additional lifecycle concerns does MLOps have for machine-learning systems?
10. If an application is slow in production, what evidence would help you investigate it?

### Answer key

1. DevOps connects development, delivery, operations, security, and feedback through shared ownership and repeatable practices.
2. CI integrates code frequently and automatically runs checks to identify problems early.
3. Continuous delivery keeps changes ready to release, often with a human gate; continuous deployment automatically releases changes that pass the defined pipeline.
4. IaC makes infrastructure repeatable, reviewable, versioned, and easier to recreate.
5. Containers package software and dependencies but still rely on runtime, kernel, permissions, network, image, and configuration security.
6. Logs show events, metrics show numeric behavior over time, and traces connect work across services.
7. Tests can be incomplete, assertions can be weak, and untested behavior can still fail.
8. They limit exposure, validate a version gradually, or disable a feature without necessarily rolling back the whole application.
9. MLOps also considers model/data versioning, evaluation, reproducibility, drift, and model quality.
10. Metrics can show latency, traces can locate slow service boundaries, and logs can provide failure context.

## Final takeaway

**DevOps helps turn code into a service that can be built, tested, released, operated, and improved reliably.** Start small: use Git, automate tests, deploy one project, add monitoring, and learn how to recover from a failure. Understand the purpose of each tool before adding another one.
