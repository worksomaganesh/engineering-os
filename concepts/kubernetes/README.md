# Kubernetes — The Complete Beginner-to-Engineering Guide

> **The one-sentence idea:** Kubernetes helps run and manage containerized applications across a group of machines by continuously working to keep the actual system close to the state you declare.

**Who this guide is for:** a developer or AI/ML student learning how applications move from "it works on my laptop" to reliable services, background jobs, and production AI systems.

**Scope note:** Kubernetes is a large ecosystem. This guide builds a practical mental model and links to the official documentation for details. It does not mean every application needs Kubernetes, and it is not a replacement for understanding Linux, networking, containers, software design, or cloud fundamentals.

## The answer up front

- **What is Kubernetes?** An open-source platform for orchestrating containerized workloads and services. It lets you declare how applications should run and automates much of the work of scheduling, restarting, scaling, and exposing them. [Official overview](https://kubernetes.io/docs/concepts/overview/)
- **Why is it useful?** It helps operate many application instances, services, workers, and infrastructure components in a repeatable way across a cluster.
- **Why learn it?** It is useful when your work involves cloud-native backend systems, platform engineering, DevOps/SRE, data platforms, or production AI/ML workloads. It also teaches important systems concepts.
- **Is it needed for every project?** No. For a small API or a student prototype, a simpler managed service or one container may be cheaper and easier.
- **Why does it matter in the AI era?** AI/ML systems may need repeatable batch jobs, GPU-aware scheduling, model-serving replicas, resource allocation, pipelines, and scalable service infrastructure. Kubernetes provides some of that infrastructure; projects such as Kubeflow and KServe build AI-specific capabilities on top.

## 1. Start with the problem Kubernetes solves

Imagine you build an AI study assistant with a web frontend, a Python API, a background document-processing worker, and a database.

At the beginning you can run everything on your laptop. Later, more students use it. You may need several API copies, a worker queue, a model-inference service, and a way to replace a failed instance. Then questions appear:

- Which machine should run each application?
- What happens if one application process crashes?
- How do users reach a service when its instances change?
- How do you deploy a new version without unnecessarily interrupting users?
- How do you add replicas when traffic grows and reduce them later?
- How do you reserve CPU and memory so one workload does not consume everything?
- How do you provide configuration and credentials without baking them into images?
- How do you recover if a machine disappears?
- How do you manage many related services consistently?

You could write scripts to manage these tasks. But as the number of workloads and machines grows, custom scripts can become fragile. Kubernetes is designed to manage this operational complexity using a declarative API and controllers.

**Kubernetes is not primarily a tool for writing the application. It is a platform for managing how containerized applications run.**

## 2. What does "orchestration" mean?

A container runtime can start a container. Orchestration coordinates containers across a larger system.

A simplified example:

1. You package the API in a container image.
2. You declare that three interchangeable API instances should run.
3. Kubernetes schedules those instances as Pods on suitable machines.
4. A controller notices if fewer healthy replicas exist than requested.
5. A stable Service gives other applications one way to reach the replicas.
6. A deployment update replaces old replicas with new ones according to its strategy.
7. A health check can stop sending traffic to an instance that is not ready.
8. An autoscaler may adjust the desired replica count based on supported metrics.

This does not mean every problem fixes itself. Kubernetes can restart a process that repeatedly crashes, but it cannot automatically debug faulty code. A Deployment can maintain three Pods, but it cannot make a database query correct or guarantee the application has no bugs.

## 3. What Kubernetes is—and is not

### Kubernetes is
- An API for declaring and managing workloads and resources.
- A scheduler that places Pods on eligible nodes.
- A set of controllers that reconcile desired and observed state.
- A platform for service discovery and cluster networking abstractions.
- A mechanism for configuring workloads, attaching storage, and controlling resource allocation.
- An extensible foundation for platform engineering and cloud-native systems.
- A widely used building block for AI/ML infrastructure, often combined with other tools.

### Kubernetes is not
- A programming language or application framework.
- A container image builder; Docker or another build tool is often used for that step.
- A cloud provider, though it can run on cloud infrastructure or on-premises machines.
- Automatically a complete CI/CD system.
- A database or message queue by itself.
- A guarantee of zero downtime, security, correctness, or unlimited scaling.
- Mandatory for every web app.
- A machine-learning framework or an AI model.

The official project describes Kubernetes as a portable and extensible open-source platform for managing containerized workloads and services, with declarative configuration and automation. [Official Kubernetes overview](https://kubernetes.io/docs/concepts/overview/).

## 4. The mental model: desired state vs actual state

This is the most important concept in Kubernetes.

You declare **desired state** in a resource, such as "run three replicas of my API." Kubernetes observes **actual state**, such as "two replicas are currently healthy," and controllers keep working to reconcile the difference.

```text
You declare desired state
        |
        v
Kubernetes API stores the desired configuration
        |
        v
Controllers and scheduler observe resources
        |
        v
Kubernetes takes actions to move toward the desired state
        |
        v
Actual state changes (Pods start, become ready, or fail)
        |
        └── Controllers observe again and reconcile continuously
```

This is a feedback loop, not a one-time command sequence.

### Example

You declare that a stateless API needs three replicas. One Pod crashes.

- The controller sees fewer healthy/desired replicas than expected.
- Kubernetes creates or schedules a replacement Pod.
- The replacement may be placed on a suitable node.
- Readiness checks determine when it should receive traffic.

Kubernetes does not typically "repair" the broken process inside the same failed Pod and preserve its exact identity. It replaces or recreates workload instances according to the resource's controller and policy.

### Why declarative configuration is useful

Instead of writing instructions such as "start a process, wait five seconds, then start another," you describe the intended result and let controllers continuously reconcile it.

This allows the system to recover from many forms of ordinary failure. The configuration also becomes reviewable and versionable as code.

## 5. Kubernetes architecture

A Kubernetes cluster has a **control plane** and one or more **worker nodes**. In a managed Kubernetes service, the provider often operates some or most control-plane components for you.

### Control plane

| Component | Plain-English job |
|---|---|
| **kube-apiserver** | The front door to the Kubernetes API. Tools and components communicate through it. |
| **etcd** | Consistent key-value store holding Kubernetes API data and cluster state. It is a critical component to protect and back up appropriately. |
| **kube-scheduler** | Chooses a suitable node for Pods that do not yet have a node assignment. It considers resource requests and scheduling constraints. |
| **kube-controller-manager** | Runs controllers that compare desired state with observed state and take corrective action. |
| **cloud-controller-manager** (where used) | Connects Kubernetes to cloud-specific resources such as load balancers or nodes. |

### Worker node

| Component | Plain-English job |
|---|---|
| **kubelet** | Node agent that ensures assigned Pods and their containers run according to the Pod specification. |
| **Container runtime** | Pulls images and starts/stops containers. Examples include containerd and CRI-O; Docker is commonly used to build images but is not the only Kubernetes runtime. |
| **Networking components** | Implement Pod networking and Service traffic routing; exact implementation depends on the cluster setup. |

Official reference: [Kubernetes components](https://kubernetes.io/docs/concepts/overview/components/) and [Nodes](https://kubernetes.io/docs/concepts/architecture/nodes/).

### A normal deployment, step by step

Suppose you run:

```bash
kubectl apply -f deployment.yaml
```

A simplified sequence is:

1. `kubectl` sends an API request to the API server.
2. The API server authenticates and authorizes the caller and validates the resource.
3. The API object is persisted in the cluster's state store.
4. A Deployment controller notices the new desired Deployment and creates/updates a ReplicaSet.
5. The ReplicaSet controller ensures the desired number of Pods exist.
6. The scheduler assigns unscheduled Pods to suitable nodes.
7. The kubelet on each assigned node asks the container runtime to pull images and start containers.
8. Readiness/liveness/startup probes and other status signals affect how the workload is considered healthy.
9. Controllers continue reconciling if the Pod or node state changes.

This is a conceptual sequence. Internally, Kubernetes controllers operate asynchronously; it is not one synchronous script where every step happens instantaneously.

## 6. Important Kubernetes objects

Kubernetes resources are objects with a declared specification and an observed status. You interact with them using the Kubernetes API.

### Cluster
The collection of control-plane components and worker nodes that manage workloads. Your application does not usually run "inside the cluster" as one monolithic program; its containers are scheduled into Pods.

### Node
A physical or virtual machine that can run Pods. A node has finite CPU, memory, storage, network, and possibly specialized resources such as GPUs.

### Pod
The smallest deployable unit in Kubernetes. A Pod contains one or more containers that share certain resources, such as a network namespace and optionally volumes.

Most applications use one main application container per Pod. Sidecars may be appropriate when a helper must share lifecycle or local resources with the app.

Pods are replaceable workload instances—not durable identities to depend on for ordinary application data.

### Deployment
A common controller for stateless applications. You describe the Pod template and replica count; the Deployment manages ReplicaSets and supports controlled rollouts and rollbacks of Deployment revisions.

Typical use cases: web API, frontend server, model-inference API.

### ReplicaSet
Maintains a requested number of matching Pods. You will usually manage Deployments, not create ReplicaSets directly.

### StatefulSet
Runs Pods that need stable identities and often persistent storage or ordered scaling/update behavior. Stateful workloads need careful storage, replication, backup, and recovery design; a StatefulSet does not magically make a database highly available.

Examples: certain distributed databases, clustered systems, or components whose identity matters. For managed production databases, using a managed database service may be simpler.

### DaemonSet
Ensures a Pod runs on each eligible node. Useful for node-level agents such as logging, monitoring, or networking components.

### Job and CronJob
- **Job:** runs a task to completion, such as a one-off data import or batch processing task.
- **CronJob:** creates Jobs on a schedule.

These are especially relevant to AI/ML data preprocessing, offline evaluation, scheduled reports, and maintenance work.

### Namespace
A logical boundary for grouping resources inside a cluster—for example, `development`, `staging`, `production`, or a team's namespace. A Namespace is useful for organization and policy, but does not by itself provide complete security or isolate workloads like a separate cluster.

### Labels and selectors
Labels are key-value metadata; selectors identify matching objects. Controllers and Services use labels/selectors to group and discover Pods. A typo between a Service selector and Pod labels can leave a service with no usable backends.

### ConfigMap
Stores non-confidential configuration such as a feature setting or log level. It helps separate configuration from the container image. Do not store passwords or API keys in ConfigMaps.

### Secret
Intended for confidential data such as tokens or passwords. A Kubernetes Secret is not automatically safe just because it is named "Secret": by default, secret data is not necessarily encrypted at rest in etcd unless encryption is configured. Anyone with powerful enough API or etcd access can expose it. Use least-privilege access, encryption at rest, limited mounting, and external secret systems where appropriate. [Official Secret guidance](https://kubernetes.io/docs/concepts/configuration/secret/).

### Service
Gives a stable endpoint for a set of Pods. Pods may be replaced and receive different IPs; other workloads should generally access the application through a Service instead of hard-coding individual Pod addresses.

### Ingress / Gateway API
Ways to route external traffic into services. Ingress remains widely used, but the Kubernetes documentation says the Ingress API is frozen and recommends considering Gateway API for new capabilities. A functioning controller or gateway implementation is required; creating an Ingress object alone does not install the traffic-routing implementation. [Service and networking documentation](https://kubernetes.io/docs/concepts/services-networking/).

### PersistentVolume and PersistentVolumeClaim
Represent storage made available to the cluster and a workload's request for storage. Storage behavior depends on the provisioner, storage class, access modes, and underlying infrastructure. Persistent storage still needs backup, restore tests, and an understanding of failure modes.

### Custom Resource and Operator
A Custom Resource Definition (CRD) extends the Kubernetes API with a new kind of object. An Operator adds controllers that automate a particular application's operational tasks through those objects. For example, an operator may coordinate a database's backups and upgrades. [Official Operator pattern](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/).

## 7. How Kubernetes connects applications

In a multi-component application, Pods need to communicate without depending on the identity of a particular Pod instance.

- **Pod networking** gives each Pod an address within the cluster network under Kubernetes' network model; the actual networking implementation is supplied by the cluster.
- **Service discovery** lets a component find a stable service endpoint.
- **Service** routes connections to eligible backend Pods.
- **Cluster DNS** commonly lets workloads reach a Service by name.
- **NetworkPolicy** can restrict allowed Pod traffic, but it only works as intended if the installed networking implementation enforces it.
- **Gateway API or Ingress** can route external HTTP/HTTPS requests to internal services.
- **LoadBalancer Service** can use supported infrastructure to expose a service externally.

Example: a frontend Pod calls `http://student-api` via the API's Service name instead of calling Pod IP `10.x.x.x`. Kubernetes can replace API Pods and update the service's backing endpoints while the logical service name remains stable.

Do not expose every Service publicly. Internal APIs, databases, queues, and metrics endpoints usually should remain private.

Official references: [Services, load balancing, and networking](https://kubernetes.io/docs/concepts/services-networking/) and [Services](https://kubernetes.io/docs/concepts/services-networking/service/).

## 8. Scaling and resource management

### Resource requests and limits

Containers can declare CPU and memory requests and limits.

- A **request** helps the scheduler decide where a Pod fits and contributes to CPU/memory utilization calculations for some autoscaling modes.
- A **limit** places a cap on supported resources such as CPU or memory, with behavior depending on the resource and runtime.
- Missing or unrealistic settings can cause poor placement, contention, memory termination, or inefficient capacity use.

For example, if a model server requires 2 CPU cores and 4 GiB of memory to operate well, its resource request should reflect realistic needs rather than be copied blindly from a tutorial.

### Horizontal Pod Autoscaler (HPA)

The HPA adjusts the number of replicas of a scalable workload using observed metrics. Common configurations use CPU or memory; custom/external metrics can be used when a metrics pipeline supports them.

An HPA is not magic:
- Metrics need to be available.
- Targets must reflect the workload.
- New Pods need capacity to be scheduled.
- Startup time and readiness behavior affect scaling.
- Scaling Pods does not always mean the underlying cluster gains more machines automatically; a cluster autoscaler or cloud capacity mechanism may be needed.

Official reference: [Horizontal Pod Autoscaling](https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/).

### Cluster scaling
A node autoscaling component or cloud provider can add/remove worker capacity based on pending workloads and configured rules. Node scaling and Pod scaling are different controls. A Pod can request more replicas while the cluster still lacks resources to schedule them.

### Scheduling constraints
Affinity/anti-affinity, topology spread, taints/tolerations, priority, resource requests, and device constraints can influence where workloads run. These are powerful tools, but they can also leave workloads pending if the constraints cannot be satisfied.

## 9. A simple Deployment + Service example

This example shows the general shape of deploying a web API. The container image and port must be changed to match your application. It is a learning example, not a production-ready manifest.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: student-api
  labels:
    app: student-api
spec:
  replicas: 2
  selector:
    matchLabels:
      app: student-api
  template:
    metadata:
      labels:
        app: student-api
    spec:
      containers:
        - name: api
          image: ghcr.io/example/student-api:1.0.0
          ports:
            - name: http
              containerPort: 8000
          resources:
            requests:
              cpu: "250m"
              memory: "256Mi"
            limits:
              cpu: "1"
              memory: "512Mi"
          readinessProbe:
            httpGet:
              path: /health/ready
              port: http
            initialDelaySeconds: 3
            periodSeconds: 5
          livenessProbe:
            httpGet:
              path: /health/live
              port: http
            initialDelaySeconds: 10
            periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: student-api
spec:
  selector:
    app: student-api
  ports:
    - name: http
      port: 80
      targetPort: http
  type: ClusterIP
```

Understand the important lines:
- `replicas: 2` requests two interchangeable Pods.
- The label selector connects the Deployment to its Pods and the Service to its backends.
- `image` identifies the application artifact to run.
- Resource requests/limits inform placement and constrain resource use.
- A readiness probe checks whether the application should receive traffic.
- A liveness probe checks whether Kubernetes should restart an unresponsive container, based on the configured probe.
- `ClusterIP` makes the Service reachable inside the cluster by default, not directly public.

To try a manifest in a disposable cluster, first ensure the image exists and exposes the expected port and health endpoints. For real production use, add an explicit supported image tag/digest strategy, non-root/security context, appropriate NetworkPolicies, ServiceAccount permissions, secrets, rollout/readiness settings, monitoring, and deployment review.

## 10. Health checks: startup, readiness, liveness

These probes have different meanings:

- **Startup probe:** gives a slow-starting application time to initialize before liveness checks take effect.
- **Readiness probe:** determines whether a Pod should receive traffic.
- **Liveness probe:** helps detect a container that is stuck and should be restarted.

Using a liveness check that fails whenever an external dependency is temporarily unavailable may cause unnecessary restarts. A readiness check should reflect whether the app can serve requests; probe design is application-specific. [Official probe guide](https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/).

## 11. Deploying a new version

A typical workflow is:

1. Build and test the application.
2. Build a container image.
3. Publish the image to a registry.
4. Update the Deployment's image/version.
5. Kubernetes creates new Pods according to the update strategy.
6. Readiness checks determine when new Pods are suitable for traffic.
7. Old Pods are gradually removed as the rollout proceeds.
8. Observe rollout and application health; pause or roll back when necessary.

Commands you will use frequently:

```bash
kubectl get nodes
kubectl get pods
kubectl get deployments
kubectl get services
kubectl describe pod <pod-name>
kubectl logs <pod-name>
kubectl apply -f deployment.yaml
kubectl rollout status deployment/student-api
kubectl rollout history deployment/student-api
kubectl rollout undo deployment/student-api
kubectl get events --sort-by=.metadata.creationTimestamp
```

A rollout rollback can restore a previous Deployment revision, but it cannot automatically undo external database changes or remote side effects. Database migrations should be designed with compatibility and recovery in mind.

## 12. Real-life use case 1 — E-commerce website

Imagine a retailer has a storefront, product API, checkout service, inventory service, and background email worker.

A Kubernetes deployment may use:
- Deployments for stateless storefront/API services.
- Services for stable internal communication.
- Gateway API or an external load balancer to accept web traffic.
- HPA for stateless services whose demand varies, provided metrics and capacity are available.
- Jobs for one-time backfills or data repair in an isolated workflow.
- ConfigMaps for non-secret config and a proper secret store for credentials.
- Monitoring and rollout health checks to detect regressions.

On a festival sale day, request traffic increases. The HPA may increase replicas based on the configured metric, while node autoscaling can add worker capacity if the cluster supports it. A database or payment provider may still be the bottleneck; scaling API Pods alone does not remove every bottleneck.

Kubernetes is useful when the service topology and traffic justify its complexity. A small online store may be more economical on a managed application platform.

## 13. Real-life use case 2 — Video or document processing

Suppose users upload PDFs, images, or videos. Request handlers should not perform hours of work during a single HTTP request. Instead, the system can place a task into a queue and run background workers.

Kubernetes may run:
- A Deployment for the API.
- A worker Deployment that consumes queued jobs.
- Jobs for isolated one-off processing.
- CronJobs for scheduled cleanup or re-indexing.
- Persistent object storage for uploaded files and outputs.
- Metrics-driven scaling of workers based on queue depth, if a supported custom-metrics path exists.
- Resource limits so a single large document does not consume unbounded memory.

Kubernetes schedules and manages the containers; the queue provides durable task messaging, and object storage persists the files. Kubernetes itself is not the message queue or file store.

## 14. Real-life use case 3 — a production AI chat application

Imagine an AI study assistant that accepts a question, retrieves relevant notes, calls a model, and streams a response.

Possible workloads:
- Frontend or backend API Deployments.
- Retrieval service Deployment.
- Background ingestion Jobs for document parsing and embedding generation.
- A queue for slow or retryable tasks.
- A managed database and object storage.
- A model server or external model API integration.
- HPA or custom-metric autoscaling for components whose load can be measured meaningfully.
- Network policy and secrets management to protect internal services and provider credentials.

Kubernetes can help coordinate deployment and operations. It does not make retrieval accurate, improve the model's reasoning, or automatically ensure responses are safe. Those require AI-specific evaluation, design, and monitoring.

## 15. When should you learn Kubernetes—and when should you not?

### Kubernetes becomes valuable when
- You need multiple related services to run consistently.
- You need repeatable rollouts and replica management.
- You have background workers or scheduled Jobs.
- You need resource requests, limits, and policy-controlled scheduling.
- You operate containers across nodes or environments.
- You work in platform engineering, cloud-native DevOps/SRE, or production ML infrastructure.
- Your team needs a common deployment API across many services.

### Kubernetes may be overkill when
- You have a single small web application.
- You are still validating the idea with very low traffic.
- Your hosting platform already provides deployment, HTTPS, health checks, and scaling with little operations work.
- You do not have the time or expertise to maintain clusters securely.
- You have not yet learned containers, HTTP, Linux processes, networking, and basic deployment.

A useful career strategy is to understand what problem Kubernetes solves and build one small app on it after learning Docker and basic deployment. You do not need to start with a complex multi-node cluster.

## 16. Why Kubernetes matters in the AI era

AI workloads are not only web APIs. They may include dataset preparation, scheduled inference, large distributed training, fine-tuning, model serving, GPU allocation, autoscaling, and workflow orchestration.

Kubernetes helps by providing:
- **Scheduling:** place workloads on nodes that have suitable resources.
- **Resource declarations:** request CPU, memory, and supported specialized devices.
- **Batch execution:** run Jobs for preprocessing, evaluation, and other tasks.
- **Service operation:** manage and expose long-running inference APIs.
- **Scaling:** adjust replicas or capacity when supported metrics and infrastructure allow.
- **Isolation and controls:** namespaces, RBAC, network policies, admission controls, and workload security settings.
- **Extensibility:** operators and custom resources can automate higher-level workflows.

Kubernetes is an infrastructure layer, not an AI platform by itself. Teams often use additional tools:
- **Kubeflow Pipelines** defines repeatable ML workflows composed of components that run as Pods and other Kubernetes resources. [Official concepts](https://www.kubeflow.org/docs/components/pipelines/concepts/pipeline/).
- **Kubeflow Trainer** provides Kubernetes-native orchestration for distributed training and fine-tuning across frameworks and GPU resources. [Official overview](https://www.kubeflow.org/docs/components/trainer/overview/).
- **KServe** provides a Kubernetes-based model-inference platform, including predictive and generative inference deployment modes. [Official admin overview](https://kserve.github.io/website/docs/admin-guide/overview).
- **Dynamic Resource Allocation (DRA)** provides Kubernetes APIs for requesting and allocating specialized devices such as GPUs or FPGAs. Its availability and feature state depend on the Kubernetes version and device integration. [Kubernetes v1.34 DRA announcement](https://kubernetes.io/blog/2025/09/01/kubernetes-v1-34-dra-updates/).
- **Workload-aware scheduling** is an evolving area for AI and batch workloads. The Kubernetes v1.37 release blog from September 2026 described Workload and PodGroup APIs, gang scheduling, workload-aware preemption, and composite Pod groups advancing to Beta. Verify current feature gates and support before using these features in production. [Official v1.37 update](https://kubernetes.io/blog/2026/09/08/kubernetes-v1-37-advancing-workload-aware-scheduling/).

### Example: GPU inference service

A team wants to serve a model on GPU nodes.

1. Build a versioned model-serving container image.
2. Make model weights available through an appropriate storage mechanism.
3. Use a GPU-enabled cluster and the device plugin/runtime integration required by that hardware.
4. Request appropriate GPU resources in the workload specification; use the method supported by the cluster.
5. Configure readiness/health checks, resource budgets, and safe rollout policy.
6. Expose only the intended inference endpoint.
7. Measure latency, throughput, queueing, GPU utilization, and errors.
8. Scale based on measured demand and available GPU capacity.
9. Keep credentials, model artifacts, and data access under least-privilege controls.

Having Kubernetes does not mean GPUs are automatically available or that model serving is automatically efficient. The hardware drivers, device integration, model runtime, memory requirements, batching, scheduling and cost all matter.

### Example: model-training pipeline

A workflow might:
1. Validate incoming dataset metadata.
2. Preprocess and tokenize data in batch Jobs.
3. Start a distributed training job.
4. Evaluate the resulting model against a benchmark.
5. Store the artifact and metrics.
6. Register the candidate model only if the quality gate passes.
7. Deploy it to staging for inference evaluation.

Kubernetes can schedule and manage the containers/jobs. Kubeflow Pipelines or another workflow system can express step dependencies and artifacts. Experiment tracking and model registry may come from separate tools. Each component has a distinct responsibility.

### AI era: should every AI developer learn Kubernetes?

No. If you are primarily exploring models in notebooks or using managed model APIs, you can make valuable AI applications without operating Kubernetes.

Learn Kubernetes when your work moves toward:
- Hosting inference services yourself.
- Operating distributed training or fine-tuning.
- Scheduling GPU workloads.
- Serving several AI-related services reliably.
- Building data/ML pipelines that need containerized execution.
- Working in ML platform engineering, MLOps, infrastructure, or production engineering.

Even if managed services hide the cluster from you, the concepts of resource allocation, health, scaling, networking, rollout, observability and access control remain useful.

## 17. Kubernetes security basics

Kubernetes gives you powerful automation; a poorly configured cluster can also magnify a mistake.

Start with these principles:

- **Least privilege:** grant a workload only the API permissions it needs. Use RBAC roles and service accounts intentionally.
- **Protect Secrets:** enable encryption at rest where required, restrict who can read/create Pods and Secrets, mount credentials only where needed, and consider an external secrets provider.
- **Use non-root containers:** avoid privileged containers unless a clearly justified requirement exists.
- **Apply Pod Security Standards:** consider the Baseline or Restricted profile where compatible, instead of leaving everything privileged.
- **Control network paths:** use NetworkPolicies where the network implementation enforces them; declare intended communication.
- **Use trusted images:** pin and scan images, track provenance where available, and update vulnerable dependencies.
- **Keep API access secure:** protect control-plane credentials and avoid broad cluster-admin access.
- **Separate environments:** use appropriate namespace, cluster, and identity boundaries.
- **Set resource limits:** reduce the impact of faulty or abusive workloads.
- **Audit and monitor:** inspect events, logs, metrics, configuration changes, and access patterns.
- **Plan recovery:** test backups and restore procedures for stateful data and critical configuration.

Important nuance: Kubernetes Secrets are not automatically encrypted at rest by default in every configuration. The official documentation recommends encryption at rest, least-privilege RBAC, limiting Secret access, and considering external Secret stores. [Official Secret guidance](https://kubernetes.io/docs/concepts/configuration/secret/). Also review the [Kubernetes security overview](https://kubernetes.io/docs/concepts/security/), [RBAC good practices](https://kubernetes.io/docs/concepts/security/rbac-good-practices/), and [Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/).

## 18. Common mistakes beginners make

1. **Learning Kubernetes before Docker and Linux basics.** Start with processes, ports, images, containers, and HTTP.
2. **Thinking a Pod is permanent.** Design for replacement; persist needed data outside ephemeral container filesystems.
3. **Using `latest` tags without an image strategy.** Make releases traceable and repeatable.
4. **Putting passwords in a Docker image, source code, or ConfigMap.** Use appropriate secret management.
5. **Exposing every Service externally.** Keep internal APIs internal and explicitly configure entry points.
6. **Ignoring resource requests and limits.** Poor settings affect scheduling, performance, and noisy-neighbor behavior.
7. **Using liveness probes as dependency checks.** A temporary database outage should not necessarily cause every API container to restart.
8. **Assuming HPA adds machines.** HPA changes workload replicas; cluster capacity may require separate autoscaling.
9. **Assuming an Ingress object works by itself.** A suitable controller is required; evaluate Gateway API for new designs.
10. **Running a stateful database in Kubernetes without a backup plan.** Persistence, replication, upgrades, and restore need a deliberate design.
11. **Treating Kubernetes as a CI/CD tool.** It runs and manages workloads; a pipeline usually builds/tests/publishes artifacts and invokes deployment.
12. **Starting with a large production-like cluster for a tiny student project.** Learn the core objects locally, then add complexity as the need becomes real.
13. **Believing Kubernetes makes a system automatically highly available.** Application design, replica placement, dependencies, data replication, capacity, and monitoring still determine reliability.
14. **Ignoring cloud costs.** Idle node pools, GPUs, load balancers, disks, and observability can create significant cost.

## 19. How to learn Kubernetes step by step

### Stage 0 — prerequisites
Understand:
- Linux processes and files.
- Basic networking, IP addresses, DNS, HTTP, ports.
- Git.
- What a container image and container are.
- Environment variables and application configuration.
- Basic YAML.

### Stage 1 — Docker and one application
Create a small API, package it in an image, and run it locally. Learn ports, environment variables, logs, and container exit status.

### Stage 2 — local Kubernetes
Use a local cluster tool such as kind or minikube. Understand that local clusters still run real Kubernetes components, but resource constraints and some cloud integrations differ from managed production clusters.

### Stage 3 — core resources
Create a Namespace, Deployment, Service, and ConfigMap. Inspect Pods, logs, Events, and rollout status. Change the image version and observe rollout behavior.

### Stage 4 — health and resource control
Add readiness/liveness/startup probes where appropriate, resource requests/limits, and safe termination behavior. Observe why a Pod can be Running but not Ready.

### Stage 5 — networking and external access
Make one service internally reachable, then expose it through an appropriate local ingress/gateway or LoadBalancer implementation. Study DNS and NetworkPolicy.

### Stage 6 — persistence and background work
Run a Job and CronJob. Understand persistent volumes and storage claims. Do a controlled experiment where a Pod is replaced and observe what data persists.

### Stage 7 — security
Create a ServiceAccount and narrowly scoped RBAC Role/RoleBinding. Practise Secrets safely with fake credentials. Explore non-root containers, Pod Security Standards, and network restrictions.

### Stage 8 — observability and deployment automation
Automate checks and image build with CI, deploy a versioned artifact, track rollout status, inspect metrics/logs, and test a rollback or recovery path.

### Stage 9 — AI/ML extension
Containerize a simple inference API or a batch evaluation job. Only after learning the core, explore Kubeflow Pipelines, Kubeflow Trainer, KServe, and GPU scheduling.

## 20. Practical projects to prove your understanding

### Project A — containerized REST API
- Build a small Python API.
- Add health endpoints and tests.
- Build an image and run it locally.
- Deploy it to a local Kubernetes cluster using a Deployment and Service.
- Change the image and watch a rollout.

**You learn:** images, Pods, Deployments, Services, YAML, rollout mechanics.

### Project B — scalable background worker
- Create an API that adds tasks to a queue.
- Run the worker as a Deployment.
- Define CPU/memory requests/limits.
- Add HPA when the metrics path is configured.
- Measure queue depth and throughput before choosing an autoscaling signal.

**You learn:** asynchronous work, scaling, resource allocation, and metrics.

### Project C — secure multi-service application
- Deploy frontend and API separately.
- Keep the database private.
- Configure a ServiceAccount and minimum RBAC permissions.
- Use a fake secret through a proper Secret/external secret mechanism.
- Add NetworkPolicy and verify it is enforced in your cluster.

**You learn:** service discovery, configuration, identity, and network controls.

### Project D — scheduled ML evaluation
- Create a container that evaluates a small model on a dataset.
- Run it as a Job or CronJob.
- Store versioned output artifacts outside the ephemeral container filesystem.
- Make failures and exit status visible.
- Run a quality gate before a report is accepted.

**You learn:** batch workloads, reproducibility, job lifecycle, and MLOps basics.

### Project E — model inference service
- Containerize a small inference API.
- Deploy with resource requests and health probes.
- Keep model API credentials out of images and Git.
- Measure latency, throughput, errors and memory use.
- Add replicas only after understanding bottlenecks.
- Explore KServe only after ordinary Kubernetes deployment is clear.

**You learn:** serving, resource management, safe rollout, observability, and AI infrastructure.

## 21. Important commands to know

```bash
# Cluster and context
kubectl config get-contexts
kubectl config current-context
kubectl get nodes

# Resources
kubectl get namespaces
kubectl get pods -A
kubectl get deployments
kubectl get services
kubectl get jobs
kubectl get cronjobs

# Inspect a resource and why it is unhealthy
kubectl describe pod <pod-name>
kubectl get events --sort-by=.metadata.creationTimestamp
kubectl logs <pod-name>
kubectl logs <pod-name> --previous

# Apply and validate changes
kubectl apply -f ./k8s/
kubectl diff -f ./k8s/
kubectl rollout status deployment/student-api
kubectl rollout history deployment/student-api
kubectl rollout undo deployment/student-api

# Execute/debug in a container (only where authorized)
kubectl exec -it <pod-name> -- /bin/sh

# Resource and scaling views
kubectl top pods
kubectl top nodes
kubectl get hpa
```

A few cautions:
- `kubectl top` requires a suitable metrics pipeline, commonly Metrics Server.
- Not every container image includes `/bin/sh`; minimal images may intentionally omit a shell.
- The active Kubernetes context matters. Before applying or deleting resources, verify the current cluster and namespace.
- Use `kubectl delete` carefully, especially in shared/production environments.
- Commands may require different parameters depending on the resource and cluster configuration.

## 22. Kubernetes vs Docker vs cloud services

| Technology | Main job |
|---|---|
| Docker / image tools | Build and run container images in local/development workflows |
| Kubernetes | Coordinate containerized workloads across a cluster |
| Managed container platform (for example, a serverless container service) | Run application containers while the provider abstracts more infrastructure |
| Virtual machines | Provide general-purpose compute machines and operating-system environments |
| Terraform / IaC | Provision cloud and infrastructure resources through declared configuration |
| CI/CD system | Build, test, package, and release changes |
| Observability tools | Collect and analyze logs, metrics, traces, and alerts |
| Kubeflow / KServe | Add ML workflow/training/model-serving capabilities on Kubernetes |

These tools can complement one another. In some cases a managed serverless/container service is the better choice because the team does not need Kubernetes' degree of control.

## 23. Glossary

- **Cluster:** control plane plus worker nodes that run workloads.
- **Control plane:** components that expose the API and manage desired state.
- **Node:** a machine capable of running Pods.
- **Pod:** smallest deployable unit; one or more cooperating containers.
- **Deployment:** declarative management for stateless replicas and rollouts.
- **Replica:** one running instance of a workload template.
- **Service:** stable endpoint for selected Pods.
- **Namespace:** logical grouping of resources and a scope for many policies.
- **Ingress:** Kubernetes API for HTTP/HTTPS routing; its API is frozen, and Gateway API is the newer direction for evolving routing features.
- **Gateway API:** APIs for more expressive traffic routing, with implementation provided by a controller/gateway.
- **ConfigMap:** non-secret configuration.
- **Secret:** object intended for confidential data; needs appropriate encryption/access controls.
- **PV/PVC:** storage resource and a workload's request for storage.
- **HPA:** controller/API that changes replica count based on metrics.
- **Request/limit:** declared resource needs and supported caps for a container.
- **Job/CronJob:** run-to-completion task / scheduled task.
- **CRD:** extends the Kubernetes API with a new resource kind.
- **Operator:** controller that automates a specialised application's lifecycle.
- **CNI:** common term for the container network integration layer used by a cluster.
- **CSI:** common term for the container storage integration layer.
- **RBAC:** role-based access control.
- **Pod Security Standards:** graduated profiles for workload security.
- **Helm:** package manager commonly used to distribute/configure Kubernetes applications.
- **Kustomize:** tool for customizing Kubernetes YAML resources.
- **GitOps:** workflow in which version-controlled declarations are reconciled into environments by automation.
- **MLOps:** operational practices for the ML lifecycle, including data/model evaluation, deployment, and monitoring.

## 24. Recommended official resources

### Core
- [Kubernetes documentation](https://kubernetes.io/docs/home/)
- [Kubernetes overview](https://kubernetes.io/docs/concepts/overview/)
- [Kubernetes components](https://kubernetes.io/docs/concepts/overview/components/)
- [Workloads](https://kubernetes.io/docs/concepts/workloads/)
- [Services and networking](https://kubernetes.io/docs/concepts/services-networking/)
- [Configuration](https://kubernetes.io/docs/concepts/configuration/)
- [Storage](https://kubernetes.io/docs/concepts/storage/)
- [Resource management](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)
- [Security](https://kubernetes.io/docs/concepts/security/)
- [Tasks and tutorials](https://kubernetes.io/docs/tasks/)

### AI/ML
- [Kubeflow](https://www.kubeflow.org/docs/)
- [Kubeflow Pipelines concepts](https://www.kubeflow.org/docs/components/pipelines/concepts/pipeline/)
- [Kubeflow Trainer](https://www.kubeflow.org/docs/components/trainer/overview/)
- [KServe](https://kserve.github.io/website/)
- [Kubernetes v1.34 Dynamic Resource Allocation update](https://kubernetes.io/blog/2025/09/01/kubernetes-v1-34-dra-updates/)
- [Kubernetes v1.37 workload-aware scheduling update](https://kubernetes.io/blog/2026/09/08/kubernetes-v1-37-advancing-workload-aware-scheduling/)

## 25. Quick self-test

1. What problem does Kubernetes solve that a container runtime alone does not?
2. Explain desired state and actual state in your own words.
3. What is the difference between a Pod and a Deployment?
4. Why should applications connect through Services instead of relying on individual Pod IPs?
5. What is the difference between readiness and liveness probes?
6. What is the difference between HPA scaling replicas and a node autoscaler adding capacity?
7. Why does a Kubernetes Secret still need security configuration?
8. What is the difference between a Job and a CronJob?
9. How would you deploy a small inference API safely?
10. When might a managed container platform be a better choice than Kubernetes?

### Answer key
1. Kubernetes orchestrates scheduling, desired state, replica management, networking, rollout, and related operations across workloads/nodes.
2. Desired state is what you declare; actual state is what is currently running. Controllers try to reconcile them.
3. A Pod is a deployable instance; a Deployment manages a set of interchangeable Pod replicas and their rollout.
4. Pods can be replaced and their IPs can change; a Service supplies a stable logical endpoint.
5. Readiness controls whether the Pod should receive traffic; liveness detects certain unhealthy states where a restart may help.
6. HPA changes the number of workload replicas; node autoscaling changes available machine capacity. They work at different layers.
7. Secret data may be exposed to principals with API/etcd access if access and encryption are not configured correctly.
8. A Job runs to completion; a CronJob schedules Jobs according to a time-based schedule.
9. Use a versioned image, least-privilege configuration, no baked-in secrets, resource settings, probes, limited network exposure, logs/metrics, and a tested rollout/recovery path.
10. When one or a few applications need easy deployment and the team's needs do not justify the operational complexity of managing Kubernetes.

## Final recommendation

Learn Kubernetes by understanding the problem first, then using it on a small app. Do not memorize YAML without understanding Pods, controllers, scheduling, networking, resource limits, security, and failure behavior. For AI/ML, start with ordinary containerized services and batch jobs; move to Kubeflow, KServe, GPU scheduling, or distributed training only when you understand what those layers add.
