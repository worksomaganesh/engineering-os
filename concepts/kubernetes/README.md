# Kubernetes — A Detailed Beginner-to-Engineering Guide

> **Purpose:** Understand what Kubernetes is, what problems it solves, how its components cooperate, how to deploy and operate applications with it, and why it matters for modern AI/ML systems.
>
> This guide is written for learning. Commands and manifests are illustrative; adapt images, versions, security settings, storage classes, networking, and cloud configuration to the environment you actually use.

## 1. The short answer

**Kubernetes (often shortened to K8s) is an open-source system for deploying, scheduling, scaling, and managing containerized applications across a cluster of machines.**

You tell Kubernetes the state you want—for example, "keep three healthy copies of this API running and make them reachable"—and its control loops continually work to make the real system match that desired state.

Kubernetes can:
- Schedule containers onto suitable machines.
- Restart or replace failed application instances.
- Scale workloads up or down.
- Give groups of Pods stable network identities through Services.
- Manage configuration, credentials, and persistent storage integrations.
- Perform controlled application rollouts and rollbacks.
- Coordinate batch jobs and, with the right hardware plugins and ecosystem tools, AI/ML workloads.
- Expose APIs so teams can automate operations and build higher-level platforms.

Kubernetes **does not** automatically make an application correct, secure, inexpensive, observable, or highly available. Those properties require appropriate application design, cluster configuration, policies, testing, and operational practices.

Official introduction: [Kubernetes — What is Kubernetes?](https://kubernetes.io/docs/concepts/overview/).

## 2. Why was Kubernetes created?

Imagine your application starts as one Python API on your laptop. At first, running it is simple. Then more users arrive and the system grows.

You may need to:
1. Run several copies of the API.
2. Put those copies on more than one machine.
3. send requests to healthy copies.
4. replace a crashed copy.
5. release a new version without taking the service down.
6. run background tasks separately from web requests.
7. attach storage for data that must survive a container restart.
8. restrict which workloads can access sensitive services.
9. allocate CPU, memory, and possibly GPUs.
10. know what is running, where it is running, and why it is unhealthy.

Doing all of this manually across many machines quickly becomes fragile. A shell script can help with a few steps, but a growing system needs a common API, a scheduler, health information, state reconciliation, networking, storage integrations, and consistent operational patterns.

Kubernetes provides a platform for those tasks. It grew from ideas about declarative cluster management and is now an open-source project maintained by the Kubernetes community under the Cloud Native Computing Foundation.

### A simple analogy: a fleet manager

Imagine a delivery company with 50 vans:
- You say how many vans must be operational.
- A dispatcher assigns work to available vans.
- If a van breaks, the dispatcher arranges a replacement.
- A dashboard tracks the fleet.
- Routes and policies determine where work can go.

Kubernetes is like a fleet manager for application workloads. A **Pod** is the basic unit it schedules; a **node** is a machine that can run Pods; the **scheduler** selects a suitable node; and **controllers** continually check whether the desired number and state of workloads exist.

The analogy has limits: Kubernetes does not understand your business logic automatically. It uses the health signals and desired state you configure.

## 3. First understand containers

A container is a way to run an application with its user-space dependencies in an isolated environment. A container image packages the filesystem layers and metadata needed to start the application. A container runtime—such as containerd—runs containers on a machine.

Docker is widely used to build images and run containers locally. Kubernetes usually works with a compatible container runtime on each worker node; it does not require you to use the Docker Engine as the runtime on every node.

### What a container solves—and what it doesn't

A container helps make the application environment more consistent across development, testing, and deployment. It does not automatically:
- Provide a cluster scheduler.
- Make a service reachable from the internet.
- Persist files safely after a container is replaced.
- Scale the number of instances.
- Protect secrets or enforce least privilege.
- Make a program bug-free.

Kubernetes manages workloads made from containers across a cluster. Docker and Kubernetes are therefore related, but they are not the same thing.

Read next: [Docker documentation](https://docs.docker.com/).

## 4. What exactly is a Kubernetes cluster?

A **cluster** is a set of machines managed as one Kubernetes environment. The machines are commonly called **nodes**.

At a high level:

```text
                 YOU / kubectl / CI pipeline
                           |
                           v
                 Kubernetes API Server
                           |
                 Desired state is stored
                           |
          +----------------+----------------+
          |                                 |
          v                                 v
    Scheduler / Controllers            etcd
          |
          v
   Choose a suitable node
          |
     +----+------------------------------+
     |                                   |
     v                                   v
 Worker Node A                      Worker Node B
 +----------------+                 +----------------+
 | kubelet        |                 | kubelet        |
 | container      |                 | container      |
 | runtime        |                 | runtime        |
 | Pods           |                 | Pods           |
 +----------------+                 +----------------+
```

This is a conceptual picture, not a promise that every component runs in a single process or machine. Managed Kubernetes services may operate the control plane for you, while you remain responsible for workloads and some configuration.

### Control plane

The control plane exposes the Kubernetes API and coordinates cluster state.

- **kube-apiserver:** the main API entry point. Tools and controllers communicate with the cluster through it.
- **etcd:** a consistent key-value store holding Kubernetes cluster state. It needs reliable protection and backups in self-managed environments.
- **kube-scheduler:** chooses a suitable node for newly created Pods that do not yet have one.
- **kube-controller-manager:** runs controllers that observe resources and reconcile actual state toward desired state.
- **cloud-controller-manager:** when applicable, integrates Kubernetes with a cloud provider for capabilities such as nodes, routes, and load balancers.

### Worker node

A worker node supplies compute resources to run workloads.

- **kubelet:** node agent that makes sure the Pods assigned to that node are running as specified and reports status.
- **Container runtime:** pulls images and runs containers.
- **Network implementation:** supplies Pod networking and connectivity, usually through a Container Network Interface (CNI) implementation.
- **kube-proxy or an equivalent implementation:** supports Service networking behavior. Some clusters use other implementations for portions of this functionality.

### Who runs the control plane?

- **Self-managed cluster:** your team is responsible for installing, securing, upgrading, backing up, and monitoring more of the control plane.
- **Managed Kubernetes:** a cloud provider manages much of the control plane, while you still need to understand worker capacity, workload configuration, security, networking, costs, and application operations.

Managed Kubernetes reduces some operational burden; it does not eliminate Kubernetes engineering.

Official reference: [Kubernetes components](https://kubernetes.io/docs/concepts/overview/components/).

## 5. The most important idea: declarative desired state

Kubernetes is commonly used declaratively. Instead of manually issuing a command every time an instance crashes, you describe what should exist.

For example:

> "Run three replicas of this container image. Each replica needs 250 millicores of CPU and 256 MiB of memory. Expose them through a stable Service."

A Deployment and related objects represent that intention. Kubernetes controllers observe the objects and work toward the desired state.

### Reconciliation loop

```text
Read desired state
       |
       v
Observe actual state
       |
       v
Compare desired vs actual
       |
       v
Take corrective action
       |
       v
Observe again (continuously)
```

If three replicas are desired but only two exist, the relevant controller works toward creating another. If the image cannot be pulled, the Pod may remain unhealthy or waiting; Kubernetes reports the condition but cannot invent the missing image or fix an invalid registry credential.

This is why Kubernetes is more than a deployment command. It is a set of APIs and controllers that continually reconcile state.

### Imperative vs declarative

- **Imperative:** "Start another instance now."
- **Declarative:** "The service should have three replicas; keep working toward that state."

Imperative commands remain useful for inspection and debugging. Declarative manifests are especially useful for repeatable environments, code review, and GitOps workflows.

## 6. The core Kubernetes objects you should understand

### 6.1 Pod

A **Pod** is Kubernetes' smallest schedulable workload unit. It contains one or more closely related containers that share networking and can share mounted volumes.

Most application Pods contain one main container. A multi-container Pod is appropriate when containers need to cooperate tightly—for example, an application container and a sidecar that handles a closely coupled task.

A Pod is not normally treated as a permanent server. It can be replaced and receive a different IP address. Use a controller and Service for typical long-running applications.

### 6.2 Deployment

A **Deployment** manages a stateless application through ReplicaSets and Pods. It is commonly used for APIs, web servers, and frontend services.

It helps manage:
- Desired replica count.
- Rolling updates.
- Rollback to a previous Deployment revision.
- Replacement of Pods that disappear.

A Deployment does not itself provide a public URL or a persistent database.

### 6.3 ReplicaSet

A **ReplicaSet** maintains a requested number of matching Pods. In ordinary application work, you usually create a Deployment and let it manage ReplicaSets instead of managing ReplicaSets directly.

### 6.4 Service

A **Service** provides a stable way to reach a set of matching Pods. Pods may be replaced and their IP addresses can change; clients should usually call the Service rather than hard-code Pod IPs.

Common Service types:
- **ClusterIP:** internal cluster access by default.
- **NodePort:** exposes a port on cluster nodes; often more of a building block than the preferred public production entry point.
- **LoadBalancer:** requests an external load balancer when supported by the environment/provider.

A Service selects matching Pods using labels and selectors. A Service is not the same as an application container.

### 6.5 Ingress and Gateway API

A web application often needs HTTP/HTTPS routing from outside the cluster to internal Services.

- **Ingress** is a widely used API for HTTP/HTTPS routing. It requires an Ingress controller; creating an Ingress object alone does not make routing happen.
- **Gateway API** is a newer, more expressive family of APIs for traffic management, with resources such as GatewayClass, Gateway, and HTTPRoute. Support depends on the chosen implementation.

For a new deployment, evaluate the Gateway API and the supported ingress/gateway implementation for your environment rather than assuming every cluster supports the same features.

References: [Services](https://kubernetes.io/docs/concepts/services-networking/service/), [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/), [Gateway API](https://gateway-api.sigs.k8s.io/).

### 6.6 ConfigMap and Secret

- **ConfigMap:** non-confidential configuration, such as a feature flag or service URL.
- **Secret:** sensitive data such as a credential or token.

Important: a Kubernetes Secret is not automatically a complete secrets-management solution. Configure access controls and encryption at rest appropriately, restrict who can read secrets, avoid printing them in logs, and consider an external secret manager. Do not put real API keys into public example manifests or Git repositories.

### 6.7 Namespace

A **Namespace** groups namespaced resources inside a cluster. Teams often use namespaces to separate applications, environments, or ownership boundaries.

Namespaces help organization, but they are not a complete security boundary on their own. Use RBAC, network policies, quotas, and appropriate admission controls where needed.

### 6.8 Job and CronJob

- **Job:** runs a task to completion, such as importing data, processing a batch, or evaluating a model.
- **CronJob:** creates Jobs on a schedule, such as a nightly report or periodic data cleanup.

They suit finite tasks better than keeping a permanent web server alive. Retrying a failed Job can be useful, but the task should be designed carefully for retries and idempotency to avoid duplicate side effects.

### 6.9 StatefulSet and persistent storage

A **StatefulSet** manages workloads that need stable identities and/or stable storage associations, such as certain databases or distributed systems.

Kubernetes storage abstractions include:
- **PersistentVolume (PV):** a storage resource available to the cluster.
- **PersistentVolumeClaim (PVC):** a workload's request for storage.
- **StorageClass:** describes classes of dynamically provisioned storage.
- **Volume:** storage mounted into a Pod.

A container's writable layer is not the same as durable storage. If data must survive Pod replacement, design and test persistence explicitly. StatefulSet does not magically make a database highly available or safe; backup, replication, consistency, recovery, and upgrades still matter.

### 6.10 DaemonSet

A **DaemonSet** ensures a Pod runs on selected nodes, often for node-level tasks such as log collection, monitoring agents, or networking components.

### 6.11 Custom Resource Definition and Operator

A **Custom Resource Definition (CRD)** extends the Kubernetes API with a new resource type. An **Operator** combines custom resources with controller logic to automate domain-specific operations.

For example, an ML platform might define a custom resource describing a training job. A controller can translate that high-level request into Pods, resource allocation, status reporting, retries, and cleanup. The exact behavior comes from that operator, not from Kubernetes core alone.

Official references: [Workloads](https://kubernetes.io/docs/concepts/workloads/), [Custom resources](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/), [Operators](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/).

## 7. A first working example: deploy a small web API

This example shows a Deployment and an internal Service. It uses a public demonstration image so you can learn the object relationships. For a real project, replace the image with your own tested image, pin it to an appropriate version or digest, and review image security.

Create a file named `web-demo.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-demo
  labels:
    app: web-demo
spec:
  replicas: 2
  selector:
    matchLabels:
      app: web-demo
  template:
    metadata:
      labels:
        app: web-demo
    spec:
      containers:
        - name: web
          image: nginx:1.28
          ports:
            - name: http
              containerPort: 80
          resources:
            requests:
              cpu: "100m"
              memory: "64Mi"
            limits:
              cpu: "500m"
              memory: "128Mi"
          readinessProbe:
            httpGet:
              path: /
              port: http
            initialDelaySeconds: 2
            periodSeconds: 5
          livenessProbe:
            httpGet:
              path: /
              port: http
            initialDelaySeconds: 10
            periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: web-demo
spec:
  selector:
    app: web-demo
  ports:
    - name: http
      port: 80
      targetPort: http
  type: ClusterIP
```

The example pins an image tag rather than using `latest`, but for production you should deliberately manage versions and consider digest pinning and image-update policy. Check the current image registry for a valid maintained tag before running this example; image tags change over time.

### Read the manifest

- `kind: Deployment` asks Kubernetes to manage the application replicas.
- `replicas: 2` describes the desired count.
- The Deployment's selector must match the Pod template labels.
- `image` identifies the container image.
- `resources.requests` influences scheduling and resource reservation.
- `resources.limits` places limits on resource use, subject to Kubernetes' resource semantics.
- `readinessProbe` tells Kubernetes when the container is ready to receive traffic.
- `livenessProbe` checks whether the process should be restarted if it is unhealthy according to the configured probe.
- The Service selects the Pods labelled `app: web-demo` and exposes port 80 inside the cluster.

### Try it

On a local Kubernetes environment such as kind or Minikube, after installing and selecting the correct cluster context:

```bash
kubectl apply -f web-demo.yaml
kubectl get deployments
kubectl get pods -o wide
kubectl get services
kubectl describe deployment web-demo
kubectl logs deployment/web-demo
kubectl port-forward service/web-demo 8080:80
```

Then visit `http://localhost:8080` while the port-forward command is running.

Clean up:

```bash
kubectl delete -f web-demo.yaml
```

Only run commands against a cluster you intend to modify. Always inspect `kubectl config current-context` before applying manifests, especially if you have access to production clusters.

## 8. What happens when you deploy a manifest?

Suppose you run `kubectl apply -f web-demo.yaml`.

1. **kubectl reads the file** and sends the desired resources to the Kubernetes API server.
2. **The API server authenticates and authorizes the request**, validates the objects, and applies relevant admission controls.
3. **The API stores the accepted state** in the cluster's backing store.
4. **Controllers notice the Deployment** and create or update a ReplicaSet, which requests the desired Pods.
5. **The scheduler selects nodes** that satisfy the Pod's scheduling constraints and resource requests.
6. **The kubelet on each selected node observes the assigned Pod** and instructs the container runtime to pull the image and start containers.
7. **Networking and storage components configure what the Pod needs**, depending on the cluster setup and manifest.
8. **The kubelet reports status and probe results.** The Service's endpoint information reflects eligible backends according to cluster behavior.
9. **You inspect the outcome** with `kubectl get`, `describe`, and `logs`.

These steps are asynchronous. A successful `kubectl apply` means the API accepted the desired resource configuration; it does **not** guarantee the application is already running or healthy. Check status and investigate events.

## 9. Scheduling: how Kubernetes decides where Pods run

The scheduler considers resource requests, node capacity, scheduling constraints, taints and tolerations, affinity rules, and other policies.

### CPU and memory requests vs limits

- **Request:** the amount used for scheduling and resource planning.
- **Limit:** the maximum resource use enforced according to the resource type and runtime behavior.

For CPU, a limit can throttle a container. For memory, exceeding the limit can result in the container being terminated (often observed as an OOM kill). Requests that are too low or too high can both cause problems: low requests can contribute to contention; high requests can leave capacity unusable.

### Labels, selectors, affinity, and taints

- **Labels:** key-value metadata attached to objects.
- **Selectors:** choose objects matching labels.
- **Node affinity / pod affinity:** express placement preferences or constraints.
- **Taints and tolerations:** keep workloads away from nodes unless the workload tolerates the relevant taint.

These features can separate general API workloads from specialized GPU nodes, isolate noisy batch workloads, or keep certain system services on appropriate machines. Placement rules should be as simple as the real requirement allows; overly strict constraints can leave Pods pending.

### GPU scheduling

Kubernetes can schedule supported GPU resources through device plugins and appropriate vendor drivers. Once a GPU device plugin advertises a resource, a Pod can request that resource. Different hardware may require labels, node selectors, affinity, or specialized scheduling policy.

Kubernetes schedules the resource; it does not automatically install all GPU drivers, optimize your model, or guarantee maximum utilization. See the official [GPU scheduling guide](https://kubernetes.io/docs/tasks/manage-gpus/scheduling-gpus/).

## 10. Health checks: readiness, liveness, and startup

These probes answer different questions.

- **Readiness:** should this Pod receive traffic right now?
- **Liveness:** should Kubernetes restart this container because it appears stuck or unhealthy?
- **Startup:** has a slow-starting application completed startup yet?

A poorly designed liveness probe can create restart loops. For example, if an application temporarily waits for a slow dependency and the liveness check treats that delay as a fatal failure, Kubernetes may repeatedly restart a process that could otherwise recover.

Readiness should reflect whether the instance can serve requests. Liveness should generally detect a failure the process cannot recover from on its own. Startup probes can protect slow initialization from premature liveness failures.

Reference: [Configure liveness, readiness, and startup probes](https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/).

## 11. Scaling and availability

### Replicas and horizontal scaling

A Deployment can run several Pods. Multiple replicas help distribute load and replace failed instances, provided the cluster has capacity and the application is designed to run concurrently.

The **Horizontal Pod Autoscaler (HPA)** adjusts replica count based on observed metrics, commonly CPU or memory utilization and, with suitable metrics adapters, application-specific metrics. HPA does not create unlimited machines. If the cluster has no capacity, Pods may remain pending unless node capacity can also grow.

A **Cluster Autoscaler** or cloud-specific node autoscaling mechanism can adjust the number of worker nodes, depending on the environment. Pod autoscaling and node autoscaling solve different problems and can work together.

### Rollouts and rollbacks

Deployments can gradually replace old Pods with new ones. You can monitor status and, when appropriate, roll back to an earlier revision. A rollback is not a complete recovery plan if the release also performed an irreversible database migration or changed external data.

### Availability needs more than replicas

Three Pods on one machine do not protect against that machine failing. High availability may require multiple nodes, failure-domain distribution, redundant infrastructure, working health checks, external dependency resilience, backups, and a recovery plan. Kubernetes provides mechanisms; your architecture determines the actual resilience.

References: [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/), [Horizontal Pod Autoscaling](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/).

## 12. Networking: how applications communicate

Kubernetes networking has multiple layers:

1. **Pod networking:** Pods communicate through cluster networking, subject to the CNI and network policies.
2. **Service discovery:** a Service gives a stable virtual address and DNS name for a selected set of backends.
3. **External entry:** a LoadBalancer, Ingress controller, Gateway API implementation, or another supported setup routes traffic from outside the cluster.
4. **Egress:** workloads may call databases, model APIs, storage, and other external services; network rules and policies determine what is allowed.

Example: a frontend may call `http://backend.default.svc.cluster.local` to reach a Service named `backend` in the `default` namespace, subject to cluster DNS and networking configuration.

A NetworkPolicy can express allowed ingress and egress patterns, but enforcement depends on the cluster's network implementation. Defining a policy in a cluster that does not enforce it does not provide the intended protection.

Reference: [Kubernetes networking concepts](https://kubernetes.io/docs/concepts/services-networking/).

## 13. Storage and databases

Kubernetes can connect workloads to persistent storage through PVs, PVCs, and StorageClasses. A workload can request a volume without hard-coding every provider-specific storage detail.

However, running a database inside Kubernetes is not automatically the best choice. Consider:
- Do you have a reliable backup and restore process?
- How are upgrades and schema changes handled?
- What is the recovery point and recovery time objective?
- How will replication and consistency work?
- Who owns database operations and incident response?
- Would a managed database reduce operational risk?

For many student projects and small production apps, a managed database outside the cluster may be simpler. Kubernetes can still run the API and background workers that use it.

## 14. Configuration and secrets safely

Keep non-sensitive environment-specific settings in configuration. Keep passwords, API keys, certificates, and tokens in a proper secrets-management workflow.

Practical rules:
- Never commit real secrets into Git.
- Do not bake secrets into container images.
- Avoid exposing secret values in logs, traces, command output, or screenshots.
- Restrict Secret read access with RBAC.
- Configure encryption at rest where required and available.
- Use workload identity or short-lived credentials where supported instead of long-lived cloud keys.
- Separate development and production credentials.
- Rotate credentials after suspected exposure.
- Consider a cloud secret manager and a maintained integration when it fits your platform.

Kubernetes Secrets are API objects, not magic encryption. The security of a Secret depends on cluster configuration, storage encryption, authorization, and how applications consume it.

References: [Secrets](https://kubernetes.io/docs/concepts/configuration/secret/), [RBAC good practices](https://kubernetes.io/docs/concepts/security/rbac-good-practices/).

## 15. Security: what a production-minded engineer checks

A Kubernetes deployment expands the set of things that must be secured: API access, worker nodes, container images, workload identities, secrets, network paths, admission policy, and the software itself.

A practical checklist:

- Use supported Kubernetes versions and plan upgrades.
- Give users and service accounts only the permissions they need.
- Avoid giving application Pods cluster-admin privileges.
- Prefer non-root containers where feasible.
- Set appropriate security contexts and avoid unnecessary Linux capabilities.
- Use trusted, maintained images and scan dependencies and images.
- Avoid privileged containers unless there is a justified, tightly controlled requirement.
- Apply Pod Security Standards or equivalent admission policy.
- Restrict network access with NetworkPolicy where the CNI enforces it.
- Protect the API endpoint and control-plane credentials.
- Store and rotate secrets properly.
- Monitor audit events and relevant workload activity.
- Back up required persistent data and test recovery.
- Treat manifests, Helm charts, and infrastructure code as code that requires review.

A cluster's security posture depends on its environment and threat model. Follow the managed provider's hardening guidance if you use a cloud service.

References: [Kubernetes security](https://kubernetes.io/docs/concepts/security/), [Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/).

## 16. Observability and troubleshooting

When a workload fails, start by asking what state Kubernetes reports before changing things at random.

Useful commands:

```bash
kubectl get nodes
kubectl get pods -A
kubectl get deployments
kubectl get services
kubectl get events --sort-by=.metadata.creationTimestamp
kubectl describe pod <pod-name>
kubectl logs <pod-name>
kubectl logs <pod-name> --previous
kubectl get pod <pod-name> -o yaml
kubectl top pods
kubectl top nodes
```

Some commands require metrics-server or other components to be installed. Replace placeholders such as `<pod-name>` with real resource names.

### Common failure states

| Symptom | What it often means | First checks |
|---|---|---|
| `Pending` | Pod has not been scheduled or is waiting on a dependency such as storage | `kubectl describe pod`, events, node capacity, PVC state |
| `ImagePullBackOff` | Image could not be pulled, and retries are backing off | Image name/tag, registry access, image pull credentials |
| `CrashLoopBackOff` | Container repeatedly exits and restart attempts are backing off | Current and previous logs, exit code, command, config, probes |
| `OOMKilled` | Container was terminated after memory pressure/limit exceedance | Memory usage, limit, leak or workload spike, node pressure |
| Service has no working backends | Service selector or Pod readiness may not match | Service selector, Pod labels, EndpointSlices, readiness |
| `Running` but app doesn't respond | Process may be unhealthy, wrong port, routing issue, or dependency failure | Logs, probes, container port, Service targetPort, network rules |
| Pods remain pending after scale-up | Insufficient schedulable capacity or restrictive placement rules | Requests, node capacity, taints, affinity, quotas, autoscaler |

Useful mental model: **observe → inspect events and logs → form a hypothesis → change one thing → verify**. Avoid deleting resources as the first response when you have not collected evidence.

## 17. Helm, Kustomize, GitOps, and operators

These are related but distinct ecosystem tools and patterns.

- **Helm:** packages and installs Kubernetes applications using charts with configurable values.
- **Kustomize:** customizes Kubernetes manifests using overlays without requiring a templating language.
- **GitOps:** keeps desired configuration in version control and uses a reconciler to apply it to an environment. Tools such as Argo CD and Flux are commonly associated with this approach.
- **Operators:** encode application-specific operational knowledge in controllers and custom resources.

For a beginner, start by reading and applying plain YAML manifests. Learn how labels, selectors, Pods, Deployments, Services, and probes work before relying on large charts or operators you cannot yet troubleshoot.

## 18. Kubernetes in the AI era (2026)

Kubernetes is relevant to AI because AI applications are not just model calls. Production AI systems can include APIs, model servers, embedding workers, retrieval pipelines, databases, object storage, evaluation jobs, asynchronous queues, observability, and GPU-backed workloads.

Kubernetes offers a common way to schedule and operate many of those components. It is **not required for every AI application**, and it does not make a model smarter by itself.

### 18.1 Hosting an AI inference API

Imagine you fine-tune or download a model and wrap it in an HTTP API.

Kubernetes can:
- Run multiple inference replicas.
- expose them through a Service and a supported gateway.
- allocate CPU, memory, and GPU resources.
- roll out a new model-serving image.
- restart failed instances and report health.
- scale replicas based on configured metrics.

But model startup time, GPU memory, batching, request queues, cold starts, and inference latency need workload-specific engineering. Autoscaling on CPU alone may be a poor signal for GPU inference; teams may need metrics such as queue depth, concurrent requests, GPU utilization, or latency, along with a suitable autoscaling mechanism.

### 18.2 Running scheduled data and ML jobs

An ML workflow may need to:
1. Validate incoming data.
2. Run preprocessing.
3. Train or fine-tune a model.
4. Evaluate it against a baseline.
5. Store the resulting artifact.
6. Register or promote the model only if quality gates pass.

Kubernetes Jobs and CronJobs can run finite and scheduled tasks. Higher-level tools can coordinate dependencies, artifacts, retries, and workflow metadata. Use the simplest orchestration that satisfies the workload; a collection of Jobs alone is not a complete ML pipeline system.

### 18.3 Distributed training and fine-tuning

Large training or fine-tuning tasks may span multiple machines and GPUs. Kubernetes can allocate the underlying cluster resources and coordinate Pods, while specialized training frameworks/operators handle distributed execution, worker coordination, rendezvous, and related details.

The relevant ecosystem includes:
- **Kubeflow:** modular, Kubernetes-native tooling for data and AI workflows.
- **Kubeflow Trainer:** Kubernetes-native APIs and operators for scalable training and distributed AI workloads.
- **KServe:** Kubernetes-native model serving abstractions for supported inference workloads.
- **GPU device plugins:** expose supported accelerator resources to the scheduler.
- **Queueing and scheduling extensions:** help manage shared, scarce GPU capacity in some environments.

These tools are not all built into Kubernetes. They add higher-level capabilities and introduce their own installation, compatibility, operational, and security considerations.

References: [Kubeflow introduction](https://www.kubeflow.org/docs/started/introduction/), [Kubeflow Trainer](https://www.kubeflow.org/docs/components/trainer/overview/), [KServe](https://kserve.github.io/website/docs/intro), [Kubernetes GPU scheduling](https://kubernetes.io/docs/tasks/manage-gpus/scheduling-gpus/).

### 18.4 Hosting AI agents and tool backends

An AI agent application may contain:
- A user-facing web app.
- An agent API/orchestrator.
- A queue for long-running tasks.
- Tool adapters for GitHub, documents, or business systems.
- A database for task state.
- A model-provider API connection.
- Workers that execute jobs.
- Logs, traces, and policy checks.

Kubernetes can run and scale these components separately. For example, a queue-backed worker pool can add replicas when work accumulates. A long-running task should not necessarily occupy a web request process for its entire lifetime.

However, Kubernetes is not an agent-security system. It does not automatically decide whether an agent is allowed to delete a file, read a secret, or call a tool. Enforce tool permissions, workload identities, network restrictions, approval gates, audit logs, sandboxing, and resource limits at the appropriate layers.

### 18.5 Serving retrieval-augmented generation (RAG)

A RAG application might use:
- An API that accepts a question.
- An embedding service or external embedding API.
- A retrieval service and vector database.
- Object storage for source documents.
- A model provider or self-hosted model.
- Background ingestion workers.

Kubernetes can run the API and workers and provide service discovery and rollout management. The vector database may be managed externally or run in the cluster depending on operational requirements. Kubernetes does not determine retrieval quality; chunking, embedding choice, indexing, evaluation, permissions, and source quality remain application responsibilities.

### 18.6 Why AI makes infrastructure skills valuable

As AI coding tools make it easier to generate application code, engineers still need to understand:
- How a service is packaged and deployed.
- Why it fails to start.
- How it gets configuration and secrets.
- How CPU, memory, storage, and GPUs are allocated.
- How to measure latency, throughput, errors, and cost.
- How to release a new model without breaking users.
- How to isolate workloads and restrict access.
- How to recover from a failed rollout.

Kubernetes is one way to learn these production concerns. It is especially valuable if you aim toward platform engineering, cloud infrastructure, MLOps, ML platform engineering, or production AI systems. It is not a substitute for programming, algorithms, ML fundamentals, databases, networking, or testing.

## 19. Real-world scenarios: when Kubernetes is useful

These are illustrative architectures, not claims about a particular company’s internal infrastructure.

### Scenario A — E-commerce site during a sale

**Problem:** Traffic rises sharply during a seasonal sale. A single application process becomes overloaded.

**Possible design:**
- Several web/API replicas behind a Service.
- An external gateway/load balancer routes incoming traffic.
- HPA scales replicas using appropriate metrics.
- Node autoscaling adds capacity when the cluster can expand.
- A queue and worker pool handle order emails or non-interactive work.
- Monitoring tracks latency, error rates, queue depth, and saturation.

**Why Kubernetes helps:** it provides workload scheduling, replica management, service discovery, and scaling mechanisms.

**What it does not solve alone:** database bottlenecks, poor caching, payment provider outages, unsafe retry logic, or insufficient capacity in a cloud account. Scaling the API can even worsen database overload if the architecture is not designed carefully.

### Scenario B — A clinic appointment system

**Problem:** A clinic wants to deploy a booking API, staff dashboard, notification worker, and scheduled reminders.

**Possible design:**
- API and dashboard as Deployments.
- Notification work processed by queue-backed workers.
- A CronJob for scheduled reminders, designed to avoid duplicate messages.
- A managed database for appointments.
- Secrets for external messaging credentials.
- Role-based access, audit logging, backups, and restricted network access.

**Why Kubernetes helps:** different components can be deployed and scaled separately, and scheduled work can be managed using familiar APIs.

**Important caveat:** healthcare data introduces privacy and compliance obligations. Kubernetes does not make the application compliant by default; the whole system, provider configuration, data handling, and operational procedures must be assessed.

### Scenario C — AI document assistant for tenders

**Problem:** Users upload tender PDFs and ask questions about eligibility, mandatory documents, and deadlines.

**Possible design:**
1. The frontend sends a file to a controlled upload API.
2. The API stores the document in object storage and creates a processing task.
3. A queue-backed worker extracts text and page-level evidence.
4. An embedding worker indexes passages.
5. A query API retrieves evidence and generates a structured answer.
6. A database stores task status and results.
7. Monitoring tracks processing time, failures, queue backlog, and model/API errors.

**Where Kubernetes fits:** it can run the API, workers, scheduled cleanup, and supporting services. If PDF processing spikes, workers may scale independently of the user-facing API.

**What needs extra design:** file-type validation, size limits, malware handling, tenant isolation, retention policy, prompt-injection defenses for uploaded documents, evidence citations, model evaluation, and cost limits. Kubernetes is infrastructure—not the tender-compliance logic.

### Scenario D — Model-training platform shared by a team

**Problem:** Multiple students or ML engineers want to run experiments, but GPUs are limited and workloads compete.

**Possible design:**
- A GPU-enabled node pool with vendor drivers and device plugins.
- Training workloads that declare GPU, CPU, and memory needs.
- Queueing or quotas so one experiment cannot consume all capacity.
- Persistent or object storage for datasets and model artifacts.
- Jobs or Kubeflow Trainer for training.
- Evaluation gates before a model is promoted.
- Metrics and logs to diagnose failures and utilization.

**Why Kubernetes helps:** it provides a shared scheduling and resource-management layer and can support reproducible, automated training workloads.

**What needs extra design:** distributed-training configuration, GPU memory, data locality, expensive idle accelerators, checkpoint recovery, and fair scheduling. A single student with a laptop GPU probably does not need a cluster for ordinary experiments.

### Scenario E — AI coding-agent service

**Problem:** A web service accepts a development task, starts a worker, runs tests, and returns a patch or report.

**Possible design:**
- API Deployment accepts tasks.
- Queue holds work that should not block HTTP requests.
- Worker Pods run isolated task containers.
- A controller or job runner tracks status and timeout.
- Logs and artifacts are stored separately.
- Resource quotas limit CPU, memory, execution time, and parallel tasks.

**Why Kubernetes helps:** worker jobs can be created, tracked, and scaled, and resource limits can be applied consistently.

**Critical security point:** untrusted code execution requires strong isolation and carefully restricted credentials/network access. A normal Pod is not automatically a complete security sandbox. Use an appropriate sandboxing design, keep privileges narrow, and do not expose production secrets to untrusted task code.

## 20. When should you use Kubernetes—and when should you not?

### Kubernetes may be a good fit when:
- You operate multiple services or many replicas.
- You need standardized deployment and operations across teams/environments.
- You have variable workload demand and need orchestration.
- You run batch jobs or distributed workloads.
- You need consistent workload APIs across supported cloud/on-premises environments.
- You have operational capacity to manage the cluster or use a managed offering.
- The benefits of the platform outweigh its cost and complexity.

### Kubernetes may be unnecessary when:
- You are learning Python or building your first API.
- You have one small website or a simple prototype.
- A serverless or managed app platform meets the requirement.
- A single VM and a well-managed process is sufficient.
- Your team cannot justify the operational burden.
- You have not yet validated whether the product solves a real problem.

For a first-year student, don't put Kubernetes in front of every project just to make the architecture look advanced. First build an application, test it, deploy it simply, and understand its real constraints. Add Kubernetes when you can explain what problem it solves in that project.

## 21. Kubernetes vs Docker vs serverless

| Technology | Main job | Best way to think about it |
|---|---|---|
| Docker / container tooling | Build and run container images | Package and run an application consistently |
| Kubernetes | Orchestrate containerized workloads across a cluster | Keep workloads running and coordinate resources, networking, rollout, and scaling |
| Serverless app platform | Run application code without requiring you to manage a full cluster | Deploy a service with less infrastructure management |
| Virtual machine (VM) | Provide a virtualized machine environment | Manage an operating-system-level runtime environment |
| Managed container service | Run containers with varying levels of infrastructure abstraction | Use containers without necessarily managing Kubernetes directly |

These options overlap. A managed serverless container platform may be simpler for a small API; Kubernetes can be preferable when you need its broader workload model and control. Compare operational burden, cost, portability, scaling behavior, networking, security, and team skills—not hype.

## 22. Kubernetes vs DevOps vs MLOps

- **Kubernetes** is a platform for orchestrating workloads.
- **DevOps** is a broader approach to shared ownership and reliable software delivery/operations.
- **MLOps** applies operational practices to machine-learning systems, including model/data versioning, evaluation, deployment, and monitoring.

A team can practise DevOps without Kubernetes. A team can use Kubernetes without having a mature DevOps culture. MLOps can use Kubernetes, managed cloud services, or simpler infrastructure depending on the workload.

Related guide in this repository: [DevOps](../devops/README.md).

## 23. The command-line tool: kubectl

`kubectl` is the standard command-line tool for interacting with a Kubernetes API server.

Common commands:

```bash
# Context and cluster
kubectl config get-contexts
kubectl config current-context
kubectl cluster-info
kubectl get nodes

# Workloads and services
kubectl get deployments
kubectl get pods -o wide
kubectl get services
kubectl get jobs
kubectl get namespaces

# Understand failures
kubectl describe pod <pod-name>
kubectl get events --sort-by=.metadata.creationTimestamp
kubectl logs <pod-name>
kubectl logs <pod-name> --previous

# Change and verify a manifest
kubectl diff -f web-demo.yaml
kubectl apply -f web-demo.yaml
kubectl rollout status deployment/web-demo
kubectl rollout history deployment/web-demo

# Port-forward and cleanup
kubectl port-forward service/web-demo 8080:80
kubectl delete -f web-demo.yaml
```

Before applying or deleting resources, confirm the current context and namespace. Commands can affect real environments. Do not copy production commands into a terminal without understanding their scope.

Reference: [kubectl reference](https://kubernetes.io/docs/reference/kubectl/).

## 24. A staged learning roadmap

Learn Kubernetes after you can build and run a simple application. This sequence avoids memorizing YAML without understanding the system.

### Stage 1 — foundations
Learn:
- Linux processes and command line.
- Git and basic networking (HTTP, ports, DNS).
- How a web server starts and listens on a port.
- Environment variables and configuration.
- Docker images and containers.

**Checkpoint:** build an API image and run it locally; explain its port, environment, and logs.

### Stage 2 — local cluster
Choose one local learning environment, such as kind or Minikube, and learn:
- Cluster and node.
- Pod.
- Deployment.
- Labels and selectors.
- Service.
- Namespaces.

**Checkpoint:** deploy a small app with two replicas and reach it through a Service.

### Stage 3 — lifecycle and debugging
Learn:
- ConfigMaps and Secrets.
- Requests and limits.
- Readiness, liveness, and startup probes.
- Events, logs, and `describe`.
- Rollouts and rollback.
- Jobs and CronJobs.

**Checkpoint:** intentionally break the image tag or configuration, diagnose the problem, and fix it using evidence.

### Stage 4 — networking and storage
Learn:
- ClusterIP and external exposure.
- Ingress or Gateway API concepts.
- DNS and network policies.
- PVCs and StorageClasses.
- How a managed database differs from a database running in the cluster.

**Checkpoint:** deploy an API with a database connection in a safe test environment and explain the request path.

### Stage 5 — automation and release
Learn:
- CI builds and tests.
- Image registry and versioning.
- Helm or Kustomize.
- GitOps concepts.
- Staging, smoke tests, and safe releases.

**Checkpoint:** a pull request runs checks and a controlled workflow deploys a tested image to a non-production cluster.

### Stage 6 — security and reliability
Learn:
- RBAC and service accounts.
- Pod Security Standards and security contexts.
- Secret management.
- Resource quotas and network policy.
- Monitoring and alerting.
- Backup, restore, upgrade, and recovery.

**Checkpoint:** document who can deploy, what the workload can access, how failures are detected, and how the system recovers.

### Stage 7 — AI/ML workloads
Learn:
- GPU requests and node selection.
- Jobs and worker queues.
- Model-serving APIs.
- Autoscaling metrics.
- Kubeflow or KServe only when a real use case needs them.
- Model versioning, evaluation, observability, and inference cost.

**Checkpoint:** deploy a small model API or a mock inference endpoint, measure latency and failures, and explain what would change when using a GPU.

Do not jump to advanced multi-cluster networking, service meshes, custom operators, or distributed GPU training until the core objects are understandable.

## 25. Beginner project ladder

### Project 1 — Two-replica web server
Deploy the example from this guide. Inspect Pods, Services, labels, and events.

### Project 2 — Python API with health probes
Build a tiny FastAPI application with a health endpoint. Containerize it, define resource requests, add readiness/liveness probes, and deploy it locally.

### Project 3 — API + background worker
Create an API that enqueues a task and a separate worker that processes it. Run the worker as a separate Deployment or Jobs depending on the task model. Add a queue appropriate to your application.

### Project 4 — scheduled data processing
Use a CronJob to run a harmless, idempotent data-processing task. Examine Job history, logs, failure behavior, and cleanup policies.

### Project 5 — CI to cluster
Configure CI to test the code and build an image. Deploy to a disposable local or test cluster. Avoid granting a public pull request unrestricted production credentials.

### Project 6 — AI inference endpoint
Deploy a simple inference API, initially on CPU. Measure request latency, throughput, and error rates. Add GPU scheduling only if the model and environment need it.

### Project 7 — GPU-aware batch training
In an environment where GPU resources are available, run a small training Job with explicit resource requests. Track duration, memory, utilization, artifacts, and failure recovery. Do not spend money on GPU infrastructure without a clear experiment and budget.

For each project, document the architecture, commands, decisions, failure cases, screenshots or logs that do not expose secrets, and what you would improve.

## 26. Cost and operational trade-offs

Kubernetes is open source, but operating a Kubernetes workload is not free. Costs can include:
- Control-plane or cluster management fees, depending on provider.
- Worker VMs and accelerator nodes.
- Persistent disks and object storage.
- Load balancers, public IPs, network traffic, and data transfer.
- Logging, metrics, tracing, and retention.
- Registry storage and image transfers.
- Engineering time spent on upgrades, incidents, security, and maintenance.

GPU nodes can be particularly expensive. Scaling a Deployment to zero may not remove the cost of reserved nodes or other infrastructure. HPA and node autoscaling require sensible minimums, limits, and metrics.

Before creating a cluster:
1. Identify the learning or product goal.
2. Choose a local cluster first when possible.
3. Set a budget and cost alerts in a cloud environment.
4. Use the smallest suitable resources.
5. Delete test infrastructure when finished.
6. Check current pricing and provider-specific billing details.

Kubernetes can improve resource utilization and automation at scale, but it does not guarantee lower costs. Complexity also has a cost.

## 27. Kubernetes versions and staying current

Kubernetes is actively developed. As of **October 2026**, the official release page lists v1.37, v1.36, and v1.35 among the three most recent minor release branches. The latest patch listed there for v1.37 is v1.37.1, released September 15, 2026. Check the official release page before choosing a version; support windows and patches change over time.

Do not blindly copy manifests from old tutorials. Confirm:
- The API version is supported by your target cluster.
- The tool and chart versions are compatible.
- Security defaults and deprecated APIs have not changed.
- The image tag exists and is maintained.
- The cloud provider supports the Kubernetes version you choose.

Official source: [Kubernetes releases](https://kubernetes.io/releases/).

## 28. Common misconceptions

**"Kubernetes is a programming language."**  
No. It is a platform and API ecosystem. You describe resources using YAML/JSON and interact with the API using tools and programs.

**"Kubernetes is the same as Docker."**  
No. Container tools build/run images; Kubernetes orchestrates workloads across a cluster.

**"Kubernetes automatically fixes every failure."**  
It can replace Pods and reconcile desired state, but it cannot correct every application bug, invalid configuration, broken dependency, or data corruption.

**"A Pod is a permanent machine."**  
No. Pods are replaceable workload instances. Use controllers and Services for resilient application patterns.

**"Three replicas guarantee high availability."**  
Not if all replicas depend on one node, one database, one region, or another single point of failure.

**"A running Pod means the application is healthy."**  
A process may run while its endpoint fails. Readiness probes, application checks, logs, metrics, and real tests provide additional evidence.

**"Kubernetes makes an AI model faster."**  
Not by itself. It can coordinate deployment and resources; inference performance depends on the model, serving runtime, hardware, batching, data path, and workload.

**"Kubernetes is required for production AI."**  
No. Serverless, managed model endpoints, VMs, or simpler container platforms may be better for a given use case.

**"Kubernetes Secrets are automatically safe."**  
No. Authorization, encryption at rest, access patterns, audit, and external integrations matter.

**"I should learn Kubernetes before building applications."**  
Usually not. Learn programming, HTTP, Git, Linux, testing, and containers first. Kubernetes becomes much easier when you understand the application it is supposed to operate.

## 29. Quick self-test

Try answering these before reading the key.

1. What problem does Kubernetes solve that Docker alone does not?
2. What is the difference between a Pod, a Deployment, and a Service?
3. What does the control plane do?
4. What does it mean for Kubernetes to reconcile desired and actual state?
5. Why can `kubectl apply` succeed while an application is still broken?
6. How do resource requests differ from limits?
7. What is the difference between readiness and liveness probes?
8. Why is a PVC different from a container's writable filesystem?
9. What must be installed/configured before Kubernetes can schedule GPU resources?
10. How could Kubernetes support a RAG application?
11. Why is Kubernetes not a complete sandbox for untrusted AI-agent code?
12. Name two cases where a managed serverless service may be a better choice.

### Answer key

1. Kubernetes coordinates scheduling, replicas, networking, rollout, and lifecycle across a cluster; Docker alone does not provide that cluster control plane.
2. Pod is the schedulable workload unit; Deployment manages stateless replicas and updates; Service provides stable access to selected Pods.
3. It exposes the API and runs components/controllers that coordinate desired cluster state.
4. Controllers repeatedly compare what should exist with what does exist and take action toward the target.
5. The API may accept valid configuration while an image pull, startup, dependency, networking, or application error remains.
6. Requests influence scheduling/resource planning; limits constrain resource use according to resource type.
7. Readiness determines whether an instance should receive traffic; liveness detects a failure that may require a restart.
8. A PVC requests persistent storage intended to survive Pod replacement; a container writable layer is not a durable-storage guarantee.
9. Compatible hardware, drivers, vendor device plugin, and correct node/resource configuration; advanced environments may need additional scheduling policy.
10. It can run APIs, ingestion workers, retrieval services, and model endpoints while managing their deployment, resources, networking, and scaling.
11. A Pod's default isolation and permissions may not safely contain arbitrary hostile code; use a deliberate sandbox, least privilege, network controls, and restricted credentials.
12. A small API with low operational needs, or a prototype where managing a cluster would outweigh the benefit.

## 30. Official references and further reading

Start with these primary sources. For current commands, API versions, security guidance, and compatibility, prefer the documentation matching your target Kubernetes release.

### Kubernetes fundamentals
- [What is Kubernetes?](https://kubernetes.io/docs/concepts/overview/)
- [Kubernetes components](https://kubernetes.io/docs/concepts/overview/components/)
- [Objects and desired state](https://kubernetes.io/docs/concepts/overview/working-with-objects/)
- [Workloads](https://kubernetes.io/docs/concepts/workloads/)
- [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Services](https://kubernetes.io/docs/concepts/services-networking/service/)
- [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/)
- [Gateway API](https://gateway-api.sigs.k8s.io/)
- [ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap/)
- [Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)
- [Persistent volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
- [Resource management for Pods and containers](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)
- [Container probes](https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/)
- [GPU scheduling](https://kubernetes.io/docs/tasks/manage-gpus/scheduling-gpus/)

### Security and operations
- [Kubernetes security concepts](https://kubernetes.io/docs/concepts/security/)
- [RBAC good practices](https://kubernetes.io/docs/concepts/security/rbac-good-practices/)
- [Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
- [Horizontal Pod Autoscaling](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)
- [kubectl command reference](https://kubernetes.io/docs/reference/kubectl/)
- [Kubernetes releases](https://kubernetes.io/releases/)

### AI/ML ecosystem
- [Kubeflow introduction](https://www.kubeflow.org/docs/started/introduction/)
- [Kubeflow Trainer](https://www.kubeflow.org/docs/components/trainer/overview/)
- [KServe documentation](https://kserve.github.io/website/docs/intro)
- [Kubernetes blog: operating AI/ML workloads with a Kubeflow Headlamp plugin (July 2026)](https://kubernetes.io/blog/2026/07/13/introducing-headlamp-plugin-for-kubeflow/)

### Tools for practice
- [kind — Kubernetes in Docker](https://kind.sigs.k8s.io/)
- [Minikube](https://minikube.sigs.k8s.io/docs/)
- [Helm](https://helm.sh/docs/)
- [Kustomize](https://kustomize.io/)
- [Argo CD](https://argo-cd.readthedocs.io/)
- [Docker documentation](https://docs.docker.com/)

## Final takeaway

Kubernetes is a **desired-state orchestration platform** for running and managing containerized workloads across a cluster. Its real value is not the YAML itself: it is the coordinated system of APIs, scheduling, controllers, networking, storage integrations, rollout mechanisms, and operational feedback.

For an AIML student in the AI era, learn Kubernetes after the foundations. Start with a small API and a local cluster; learn to deploy, inspect, debug, scale, and secure it. Then apply those skills to AI inference, data processing, model training, or agent-worker systems only when the workload genuinely benefits from orchestration.
