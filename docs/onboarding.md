# Shuffle Onboarding Draft

For reference, use:

- [Architecture](/docs/architecture)
- [Configuration](/docs/configuration)
- [Troubleshooting](/docs/troubleshooting)
- [Getting started](/docs/getting_started)

## Architecture overview

Shuffle is split into a server layer and a runtime layer.

The server layer handles the UI, API, authentication, workflow storage, app metadata, files, and database access. In the default Docker deployment this is mainly:

- `shuffle-frontend`: serves the web UI and routes browser/API traffic.
- `shuffle-backend`: runs the REST API, workflow validation, app metadata loading, file handling, and OpenSearch communication.
- `shuffle-opensearch`: stores users, organizations, workflows, executions, apps, files metadata, health data, and other platform state.

The runtime layer executes workflows. In the default Docker deployment this is:

- `shuffle-orborus`: polls the backend for workflow execution jobs and starts workers.
- `shuffle-worker`: controls one workflow execution.
- App containers: run individual workflow actions, such as HTTP, Shuffle Tools, or third-party integrations.

The usual execution flow is:

1. A user or trigger starts a workflow.
2. The backend validates and queues the execution.
3. Orborus polls the backend and starts a worker.
4. The worker starts app containers for workflow actions.
5. Apps return action results and logs to the worker/backend.
6. The execution ends as `FINISHED`, `ABORTED`, or `FAILURE`.

For Docker, Orborus and the backend use the Docker socket to start workers and app containers. Orborus deploys workers and apps into the Swarm execution network so runtime containers can run across multiple Docker nodes. For Kubernetes, Orborus and workers use Kubernetes API permissions to create worker/app deployments and services in the `shuffle` namespace.

## Deployment models

Docker Compose is the default deployment entrypoint for Shuffle. The Compose stack starts the core services and Orborus. Orborus automatically creates the Swarm execution network and deploys worker and app services. You can scale the runtime layer by changing replica/concurrency settings and by adding more nodes to the Docker Swarm.

Kubernetes is the cluster-native deployment model. In Kubernetes, the Helm chart deploys the core services, and Orborus/Worker create worker and app deployments through Kubernetes API permissions in the `shuffle` namespace.

For production, plan these items before deployment:

- Persistent storage for OpenSearch data.
- Persistent storage for Shuffle files and app hotload folders.
- Backup and restore process for OpenSearch and Shuffle files.
- Resource requests/limits or VM sizing.
- Network path from Shuffle apps to internal tools such as SIEM, EDR, ticketing,identity, and mail systems.
- Outbound internet/proxy path for downloading apps and Docker images.
- A stable `SHUFFLE_ENCRYPTION_MODIFIER`. If it is lost or changed, app authentications must be recreated.

## Docker requirements

Minimum lab requirements:

- Linux host or Windows with WSL2.
- Docker and Docker Compose.
- Git, unless using a release zip.
- At least 4 GB RAM for testing.

Recommended production starting point:

- 2 vCPU or more.
- 8 GB RAM or more.
- 100 GB SSD or more.
- Internal-only access to Docker/Swarm ports when scaling across nodes.
- Monitoring for CPU, memory, disk, OpenSearch heap, and container restarts.

OpenSearch prerequisites on Linux:

```bash
sudo chown -R 1000:1000 shuffle-database
sudo swapoff -a
sudo sysctl -w vm.max_map_count=262144
```

Important Docker environment variables:

- `FRONTEND_PORT`: default UI HTTP port, usually `3001`.
- `FRONTEND_PORT_HTTPS`: default UI HTTPS port, usually `3443`.
- `BACKEND_PORT`: backend API port, usually `5001`.
- `OUTER_HOSTNAME`: hostname/IP that Orborus and workers should use to reach the backend.
- `BASE_URL`: internal/backend URL used by Shuffle services.
- `SHUFFLE_ENCRYPTION_MODIFIER`: required secret for encrypting app authentication data.
- `SHUFFLE_OPENSEARCH_PASSWORD`: OpenSearch password used by Shuffle.
- `OPENSEARCH_INITIAL_ADMIN_PASSWORD`: initial OpenSearch admin password.
- `HTTP_PROXY` / `HTTPS_PROXY`: outbound proxy if the host cannot reach GitHub, GHCR, Docker Hub, or internal APIs directly.
- `SHUFFLE_PASS_WORKER_PROXY` / `SHUFFLE_PASS_APP_PROXY`: pass proxy settings to workers and app containers.
- `SHUFFLE_LOGS_DISABLED`: commonly `true` at scale to reduce memory pressure from app log forwarding.
- `SHUFFLE_ORBORUS_EXECUTION_CONCURRENCY`: soft limit for concurrent executions.

## Docker setup draft

Clone and start Shuffle:

```bash
git clone https://github.com/Shuffle/Shuffle
cd Shuffle
```

Edit `.env` before first start. Set at least:

```bash
SHUFFLE_ENCRYPTION_MODIFIER=<random-long-secret>
SHUFFLE_OPENSEARCH_PASSWORD=<strong-password>
OPENSEARCH_INITIAL_ADMIN_PASSWORD=<same-strong-password-for-first-start>
OUTER_HOSTNAME=<server-ip-or-dns-name>
SSO_REDIRECT_URL=http://<server-ip-or-dns-name>:3001
```

Start the stack:

```bash
docker compose up -d
```

Check containers:

```bash
docker compose ps
docker logs -f shuffle-backend
docker logs -f shuffle-orborus
docker logs -f shuffle-opensearch
```

Open Shuffle:

```text
http://<server-ip-or-dns-name>:3001
https://<server-ip-or-dns-name>:3443
```

After first login:

1. Create the first admin user, unless `SHUFFLE_DEFAULT_USERNAME` and `SHUFFLE_DEFAULT_PASSWORD` were configured.
2. Go to `/apps`.
3. Verify that default apps are present.
4. If apps are missing, check outbound access to GitHub and proxy settings.
5. Create a basic workflow with Start node and HTTP or Shuffle Tools to test execution.

Useful Docker commands:

```bash
docker compose pull
docker compose up -d
docker compose down
docker compose restart backend
docker compose restart orborus
docker ps
docker network ls
docker volume ls
```

## Docker scale notes

The default Docker Compose file starts the core services and Orborus with Swarm execution settings. For multi-node Docker execution, initialize/join the Docker Swarm nodes so Orborus can deploy workers and apps as Swarm services on the execution network.

Common Swarm ports between nodes:

- `2377/tcp`: cluster management.
- `7946/tcp` and `7946/udp`: node communication.
- `4789/udp`: overlay networking.

Keep these ports internal to the cluster.

Basic Swarm flow:

```bash
docker compose up -d
docker service ls
```

Orborus automatically creates the Docker Swarm execution network and deploys worker and app services. Use these settings to scale the runtime layer:

- `SHUFFLE_ORBORUS_EXECUTION_CONCURRENCY`: maximum number of executions Orborus should actively schedule at the same time.
- `SHUFFLE_SCALE_REPLICAS`: worker service replicas per Swarm node.
- `SHUFFLE_APP_REPLICAS`: app service replicas per Swarm node.
- Docker Swarm nodes: add more nodes when the current hosts do not have enough CPU, memory, network reachability, or isolation for the workload.

After changing these settings, restart Orborus and verify that Swarm services are created:

```bash
docker compose restart orborus
docker service ls
docker network ls
docker logs -f shuffle-orborus
```

## Kubernetes requirements

Minimum requirements:

- A working Kubernetes cluster.
- `kubectl` access to the cluster.
- Helm.
- Permission to create namespace-scoped deployments, services, roles, role bindings, service accounts, PVCs, secrets, and network policies.
- A default storage class, or explicit storage class values.
- Image pull access to `ghcr.io` and required app registries.

Production planning:

- Use the `shuffle` namespace for one Shuffle deployment.
- Do not deploy unrelated applications in the same namespace because Shuffle-created worker/app resources are managed there.
- Decide whether to use the chart-provided single-node OpenSearch or an external OpenSearch cluster.
- Decide whether Orborus/Worker may dynamically create app deployments, or whether apps should be pre-deployed with Helm.
- Configure ingress/TLS or a LoadBalancer service for frontend access.
- Store secrets outside Helm values where possible.

Important Kubernetes/Helm values:

- `shuffle.baseUrl`: external URL where users access Shuffle.
- `shuffle.org`: default organization, usually `Shuffle`.
- `backend.replicaCount`: number of backend replicas.
- `frontend.replicaCount`: number of frontend replicas.
- `orborus.replicaCount`: number of Orborus replicas.
- `opensearch.enabled`: whether the chart deploys OpenSearch.
- `backend.openSearch.url`: external OpenSearch URL if not using chart OpenSearch.
- `backend.extraEnvVarsSecret`: mount backend secrets as environment variables.
- `orborus.extraEnvVarsSecret`: mount Orborus secrets as environment variables.
- `worker.enableHelmDeployment`: deploy worker through Helm instead of Orborus dynamic creation.
- `apps.enabled`: pre-deploy selected apps through Helm.

Secrets to prepare:

```yaml
SHUFFLE_OPENSEARCH_PASSWORD: "<strong-password>"
SHUFFLE_DEFAULT_USERNAME: "admin"
SHUFFLE_DEFAULT_PASSWORD: "<strong-admin-password>"
SHUFFLE_DEFAULT_APIKEY: "<uuid-v4>"
SHUFFLE_ENCRYPTION_MODIFIER: "<random-long-secret>"
```

## Kubernetes setup draft

Create namespace and secrets:

```bash
kubectl create namespace shuffle

kubectl create secret generic shuffle-backend-env \
  --namespace shuffle \
  --from-literal=SHUFFLE_OPENSEARCH_PASSWORD='<strong-password>' \
  --from-literal=SHUFFLE_ENCRYPTION_MODIFIER='<random-long-secret>' \
  --from-literal=SHUFFLE_DEFAULT_USERNAME='admin' \
  --from-literal=SHUFFLE_DEFAULT_PASSWORD='<strong-admin-password>' \
  --from-literal=SHUFFLE_DEFAULT_APIKEY='<uuid-v4>'
```

Create a draft values file:

```yaml
shuffle:
  baseUrl: "https://shuffle.example.com"
  org: "Shuffle"

backend:
  extraEnvVarsSecret: shuffle-backend-env

ingress:
  enabled: true
  hostname: shuffle.example.com
```

Install with Helm:

```bash
helm install shuffle oci://ghcr.io/shuffle/charts/shuffle \
  --namespace shuffle \
  --create-namespace \
  --values values.yaml
```

Verify:

```bash
kubectl get pods -n shuffle
kubectl get svc -n shuffle
kubectl get ingress -n shuffle
helm status shuffle -n shuffle
```

Upgrade:

```bash
helm upgrade shuffle oci://ghcr.io/shuffle/charts/shuffle \
  --namespace shuffle \
  --values values.yaml
```

Uninstall:

```bash
helm uninstall shuffle --namespace shuffle

kubectl delete svc --namespace shuffle \
  -l "app.kubernetes.io/managed-by in (shuffle-orborus,shuffle-worker)"

kubectl delete deploy --namespace shuffle \
  -l "app.kubernetes.io/managed-by in (shuffle-orborus,shuffle-worker)"
```

## Collecting logs

When reporting an issue, collect logs from the server layer and the runtime layer.

Docker compose:

```bash
docker compose ps
docker logs --tail 300 shuffle-frontend
docker logs --tail 300 shuffle-backend
docker logs --tail 300 shuffle-orborus
docker logs --tail 300 shuffle-opensearch
```

Follow logs while reproducing:

```bash
docker logs -f shuffle-backend
docker logs -f shuffle-orborus
```

Find active workers and app containers:

```bash
docker ps --format "table {{.ID}}\t{{.Image}}\t{{.Status}}\t{{.Names}}"
docker ps | grep -i worker
docker ps | grep -i tools
```

Worker/app logs:

```bash
docker logs --tail 200 <container_id_or_name>
docker inspect <container_id_or_name>
```

Kubernetes:

```bash
kubectl get pods -n shuffle -o wide
kubectl get deploy -n shuffle
kubectl get svc -n shuffle
kubectl get events -n shuffle --sort-by=.lastTimestamp
```

Kubernetes service logs:

```bash
kubectl logs -n shuffle deploy/shuffle-backend --tail=300
kubectl logs -n shuffle deploy/shuffle-frontend --tail=300
kubectl logs -n shuffle deploy/shuffle-orborus --tail=300
```

Kubernetes worker/app logs:

```bash
kubectl get pods -n shuffle | grep -i worker
kubectl get pods -n shuffle | grep -i app
kubectl logs -n shuffle <pod-name> --tail=200
kubectl describe pod -n shuffle <pod-name>
```

Health checks:

```bash
curl http://<shuffle-host>:3001/api/v1/_ah/health
curl http://<shuffle-host>:3001/api/v1/health
```

OpenSearch health from Docker:

```bash
docker exec -it shuffle-opensearch bash
curl -k -u admin:'<password>' https://localhost:9200/_cluster/health?pretty
```

OpenSearch health from Kubernetes depends on whether OpenSearch is chart-managed or external. For chart-managed OpenSearch, first find the pod/service:

```bash
kubectl get pods -n shuffle | grep -i opensearch
kubectl get svc -n shuffle | grep -i opensearch
```

## Basic debugging checklist

### UI does not load

Check:

- `shuffle-frontend` container/pod is running.
- Port `3001` or ingress is reachable.
- Frontend can resolve and reach backend.
- Browser is using the expected HTTP/HTTPS URL.

Commands:

```bash
docker logs --tail 200 shuffle-frontend
docker logs --tail 200 shuffle-backend
curl http://<shuffle-host>:3001/health
```

Kubernetes:

```bash
kubectl describe ingress -n shuffle
kubectl logs -n shuffle deploy/shuffle-frontend --tail=200
kubectl logs -n shuffle deploy/shuffle-backend --tail=200
```

### Backend starts but login/setup fails

Check:

- OpenSearch is running and healthy.
- `SHUFFLE_OPENSEARCH_PASSWORD` matches the OpenSearch password.
- Persistent volume permissions are correct.
- `SHUFFLE_ENCRYPTION_MODIFIER` is set before app authentication is used.

Commands:

```bash
docker logs --tail 300 shuffle-backend
docker logs --tail 300 shuffle-opensearch
docker exec -it shuffle-opensearch curl -k -u admin:'<password>' https://localhost:9200/_cluster/health?pretty
```

### Apps are missing

Check:

- Backend can reach `https://github.com/shuffle/python-apps`.
- Proxy settings are configured if required.
- `SHUFFLE_APP_DOWNLOAD_LOCATION` points to the correct repository.
- The local `shuffle-apps` directory is mounted and writable.

Commands:

```bash
docker logs -f shuffle-backend
docker exec -it shuffle-backend sh
```

Inside the container, test DNS and outbound access if tools are available:

```bash
nslookup github.com
curl -I https://github.com/shuffle/python-apps
```

### Executions stay queued or never start

Check:

- Orborus is running.
- Orborus can reach backend using `BASE_URL`.
- `OUTER_HOSTNAME` points to an address reachable from Orborus/workers.
- Docker socket or Kubernetes RBAC permissions are available.
- Execution concurrency is not set too low.

Docker commands:

```bash
docker logs -f shuffle-orborus
docker inspect shuffle-orborus
docker ps | grep -i worker
```

Kubernetes commands:

```bash
kubectl logs -n shuffle deploy/shuffle-orborus --tail=300
kubectl auth can-i create deployments --as=system:serviceaccount:shuffle:shuffle-orborus -n shuffle
kubectl get events -n shuffle --sort-by=.lastTimestamp
```

### Worker starts but app actions fail

Check:

- App image exists or can be pulled.
- Worker/app can reach backend.
- Worker/app can reach the target internal API.
- Required app authentication is configured.
- Proxy and custom CA settings are correct.
- App container logs show the real API error.

Commands:

```bash
docker ps | grep -i worker
docker logs --tail 200 <worker-container>
docker logs --tail 200 <app-container>
```

Kubernetes:

```bash
kubectl get pods -n shuffle | grep -i worker
kubectl get pods -n shuffle | grep -i <app-name>
kubectl logs -n shuffle <worker-pod> --tail=200
kubectl logs -n shuffle <app-pod> --tail=200
```

### OpenSearch is unhealthy

Check:

- Host has enough RAM and disk.
- `vm.max_map_count` is set on Linux hosts.
- Data directory permissions are correct.
- Password values match between backend and OpenSearch.
- Persistent volume is not full.

Commands:

```bash
df -h
free -m
docker logs --tail 300 shuffle-opensearch
sudo sysctl vm.max_map_count
sudo chown -R 1000:1000 shuffle-database
```

### Server is slow or runs out of memory

Check:

- OpenSearch heap settings.
- App log forwarding volume. Set `SHUFFLE_LOGS_DISABLED=true` for Orborus/runtime if memory is high.
- Execution concurrency.
- Number of active workers and apps.
- Disk pressure from old containers/images/logs.

Commands:

```bash
docker stats
docker ps
docker system df
docker logs --tail 200 shuffle-orborus
```

Kubernetes:

```bash
kubectl top pods -n shuffle
kubectl describe pod -n shuffle <pod-name>
kubectl get events -n shuffle --sort-by=.lastTimestamp
```

## Information to include in an escalation

Before sending a problem to Shuffle, run the relevant debugging steps above and include the command output in the email or support request. Include logs from the same time window as the failure. Redact passwords, API keys, tokens, cookies, and customer data before sending.

At minimum, include:

- Deployment type: Docker Compose, Docker Swarm, Kubernetes, or hybrid.
- Shuffle version or image tags.
- Sanitized `.env` or Helm values.
- Frontend URL and whether TLS/ingress/proxy is used.
- Container/pod status.
- Backend, Orborus, Worker, App, and OpenSearch logs from the same reproduction window.
- Screenshot of the error.
- Whether the environment uses outbound proxy, custom CA, private registry, or no-internet mode.
- Recent changes: upgrade, password change, storage migration, DNS change, proxy change, node restart.

For Docker deployments, attach the output from:

```bash
docker compose ps
docker service ls
docker network ls
docker logs --tail 300 shuffle-backend
docker logs --tail 300 shuffle-orborus
docker logs --tail 300 shuffle-opensearch
docker service logs -tail 300 shuffle-workers
```

For Kubernetes deployments, attach the output from:

```bash
kubectl get pods -n shuffle -o wide
kubectl get deploy -n shuffle
kubectl get svc -n shuffle
kubectl get events -n shuffle --sort-by=.lastTimestamp
kubectl logs -n shuffle deploy/shuffle-backend --tail=300
kubectl logs -n shuffle deploy/shuffle-orborus --tail=300
```
