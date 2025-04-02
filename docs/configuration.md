# Configure Shuffle

Documentation for configuring Shuffle. Most information is related to onprem and hybrid versions of Shuffle.

## Table of contents

* [Introduction](#introduction)
* [Updating Shuffle](#updating-shuffle)
* [Production readiness](#production-readiness)
* [Shuffle Scaling](#scaling-shuffle)
* [Distributed Caching](#distributed-caching)
* [Kubernetes](#kubernetes)
* [No Internet Install](#no-internet-install)
* [Proxy Configuration](#proxy-configuration)
* [App Certificates](#app-certificates)
* [HTTPS](#https)
* [IPv6](#ipv6)
* [Database](#database)
* [Database Change](#change-the-database-from-opensearch-to-elasticsearch)
* [Network Configuration](#network-configuration)
* [Docker Version error](#docker-version-error)
* [Database indexes](#database-indexes)
* [Uptime monitoring](#uptime-monitoring)
* [Debugging](#debugging)
* [Execution Debugging](#execution-debugging)
* [Known Bugs](#known-bugs)
* [Shuffle Server Healthcheck](#shuffle-server-healthcheck)
* [Using podman](#using-podman)
* [Marketplace setup](#marketplace-setup)

## Introduction

With Shuffle being Open Source, there is a need for a place to read about configuration. There are quite a few options, and this article aims to delve into those.

Shuffle is based on Docker and is started using docker-compose with configuration items in a .env file. .env has the configuration items to be used for default environment changes, database locations, port forwarding, github locations and more.

## Installation

Check out the [installation guide](https://github.com/frikky/shuffle/blob/master/.github/install-guide.md), however if you're on linux:

System requirements may be found further down in the [Servers](#servers) section.

```
git clone https://github.com/shuffle/Shuffle
cd Shuffle
docker-compose up -d
```

![image](https://user-images.githubusercontent.com/5719530/169809608-325b5e9f-af44-45ab-83e1-c2acbcaf206a.png)

### Updating Shuffle

`From version v1.1 onwards, we are using ghcr.io/shuffle/* registry instead of ghcr.io/frikky/*`

As long as you use Docker, updating Shuffle is straight forward. To use a specific version of Shuffle, check out [specific version](/docs/configuration#specific-versioning). We recommend always sticking to the `latest` tag, and if you want experimental changes, use the `nightly` tag. You may however in specific cases want to use a static tag, such as `2.0.0`

While being in the main repository, here is how to update Shuffle:

```
docker-compose down
git pull
docker-compose pull
docker-compose up -d
```

**PS: This will NOT update your apps, meaning they may be outdated. To update your apps, go to /apps and click both buttons in the top right corner (reload apps locally & Download from Github)**

### Specific Versioning

To use a specific version of Shuffle, you'll need to manually edit the Docker-Compose.yml file to reflect the version - usually for the frontend and backend, but sometimes also the other containers. You can [see all our released versions here](https://github.com/orgs/Shuffle/packages). We recommend keeping the same version for the frontend and backend, and **not** to keep them separate, as seen in the image below.

### Marketplace Setup

Using cloud marketplaces ([AWS Marketplace](https://aws.amazon.com/marketplace/), [Google Cloud Marketplace](https://console.cloud.google.com/marketplace), [Azure Marketplace](https://azuremarketplace.microsoft.com/)), you should be able to deploy Shuffle onprem with a few clicks. This is a great way to get started with Shuffle, as it's a fully managed service and test it out in your own environment without worrying about the setup. We are working with our cloud partners to get this up and running as soon as possible. 

## Server configuration

Shuffle is by default configured to be easy to start using. This means we have had to make some tradeoffs which can be enabled/disabled to make it easier to use, or scale better. The following section outlines a lot of what is necessary to make Shuffle's security, availability and scalability better. 

![image](https://github.com/user-attachments/assets/1bf288e0-fbd7-47c1-aba2-5269acaa4f8d)

**Here are the things we'll dive into**
- [Environment Variables](#environment_variables)
- [High Availability](#high-availability)

### Environment Variables
With Shuffle being a very technical system, it is important to understand that you have a lot of control mechanisms available to you in your local installation. 

[Check the .env file on your server](https://github.com/Shuffle/Shuffle/blob/main/.env) to see what the default values are. They are broadly split into the following:

- Setup Configuration (default usernames & download locations for easy deployments)
- Network Configuration (e.g. how does the frontend route to the correct backend, or Orborus->Frontend->Backend through Nginx)
- Container Control (Registries, Docker & K8s-specific configs etc.)
- Health and Stability (Enable/Disable health checks, Log forwarding, automatic Reruns and Aborts etc.)
- Opensearch Configuration (Networking, password & security systems etc)

**PS:** Most of our environment variables start with `SHUFFLE_`

### Servers
When setting up Shuffle for production, we always recommend two or more servers (VMs), but it works fine with one to start. These are MINIMUM requirements, and we recommend adding more to avoid congestion.

The webserver is where your users and Shuffle's API is. Opensearch is a RAM heavy database, and we are doing A LOT of caching with to ensure scalable stability.

- Services: Frontend, Backend, Orborus, Opensearch (All)
- CPU: 2vCPU
- RAM: 8Gb
- Disk: >100Gb (SSD)

The [default docker-compose file](https://github.com/shuffle/Shuffle/blob/main/docker-compose.yml) works well to scale on a single server. 

### Hybrid Cloud Configuration

* Onprem: If you want to try using Hybrid Shuffle, see [Cloud sync documentation](/docs/organizations#cloud_synchronization)
* Cloud: If you want access to on-premises resources and API's, [set up extra Environments](/docs/organizations#environments)

### High Availability
When running Shuffle on multiple servers, you need to take multiple things into account. Among them are:
- Can the servers talk to each other?
- Do you want all Shuffle services on all servers?
- Do you want distributed storage?
- Do you already have a cluster, or does it need to be made?
- Do you want Docker or Kubernetes? Or containerless?

![image](https://github.com/user-attachments/assets/5248417c-c47b-4397-95c5-b01e1f5b4082)

Here is a breakdown of the previous High Availability image of Shuffle, and how it works:
1. All the **Green** colored services are our providers, meaning they are built by someone else than Shuffle, but used in the Shuffle stack. Here is our recommendation on scaling these services:
   * [Opensearch (Database)](https://opensearch.org/docs/latest/tuning-your-cluster/). Elasticsearch also works. If you are using more than one entrypoint to Opensearch/Elasticsearch, [add the URL's comma separated in the .env file](https://github.com/Shuffle/Shuffle/blob/c5ef50f523c041efaf53a1e285c1b19a30201e67/.env#L104). 
   * [Memcached (Shared Memory)](#distributed_caching): We recommend starting with memcached on a single server, and only scaling up as need be. When scaling, this memcached is only required for the Workers to communicate, and is not required for Shuffle itself to work. Add multiple [comma separated URL's here](https://github.com/Shuffle/Shuffle/blob/c5ef50f523c041efaf53a1e285c1b19a30201e67/.env#L84) to configure multiple instances.
  
2. **NFS** is Network File Storage. This is for you to be able to store files across multiple servers. This is required if you are running multiple instances of the Shuffle backend, and for them to have consistent access to the Files that you store. Only configure this if you are storing files in Shuffle. When NFS is set up, [mount your NFS storage to ./shuffle-files](https://github.com/Shuffle/Shuffle/blob/c5ef50f523c041efaf53a1e285c1b19a30201e67/docker-compose.yml#L28).

3. The **Blue** services are YOUR services. These can be in your Cloud, Onprem etc. The service in Shuffle that needs access to this are the `Apps`, which have their network configuration copied from the `Orborus` container. If you have on-premises services that Shuffle needs access to, set up an Orborus instance in the same network, which has access to your Shuffle instance + the service in question.

4. The **orange** services are Shuffle's containers. Below is a breakdown of what and how to use them.
* **Backend:** Handles all of Shuffle's API requests, and are typically routed through the Frontend service. This means that it usually does NOT expose a port. **Scale across ALL available servers.** Available on shuffle-http://backend:5001 in the container network. 
* **Frontend:** Handles frontend & backend routing, as well as the default certificates. **Scale across ALL available servers.** Available on http://shuffle-frontend:3001 or https://shuffle-frontend:3443 in the container network.
* **Orborus / Worker / Apps:** Orborus is in charge of this stack, and is how you control all three services. Orborus receives jobs from the Backend, and does NOT expose any port. Read more about configuring, scaling and managing them in your instance on the [/admin?tab=locations](/admin?tab=locations) page, or in the next section.

### Scaling Runtime Locations
Orborus can run in Docker-swarm mode, and in early 2023, with Kubernetes. This makes the workflow executions **A LOT** faster, use less resources, making it more scalable both on a single, as well as across multiple servers. Since September 2024, scale has been partially open source, and can be achieved with changing environment variables in the "Orborus" container for Shuffle. [Click here for Kubernetes details](https://github.com/Shuffle/Shuffle/tree/2.0.0/functions/kubernetes#instructions). If you have received a licensed version, don't forget step 3 to load in the correct worker. 

Let's begin with setting up Docker, Docker Compose, and creating a Docker Swarm network with two manager nodes involves several steps. Below is a step-by-step guide to achieve this:

**Step 1: Install Docker**

Install Docker on both machines by following the official Docker installation guide for your operating system.
Docker Installation Guide: https://docs.docker.com/get-docker/

**Step 2: Install Docker Compose**

Install Docker Compose on both machines by following the official Docker Compose installation guide.
Docker Compose Installation Guide: https://docs.docker.com/compose/install/

Step 3: Load the license **(skip if not a customer)**

You should have received a license from the Shuffle team, which comes in form of a URL. This URL can be used to download the licensed version of the Worker as many times as you want. After downloading it, you need to docker load the file. 
```
wget <url>
docker load -i shuffle-worker.zip
```

After these have been ran, it should be clear what the docker image is. This docker image needs to be used in the `SHUFFLE_WORKER_IMAGE` environment variable in step 4. 

**Step 4: Configure Orborus Environment Variables:**
1. Add and change the following environment variables for Orborus in the docker-compose.yml file. `BASE_URL` is the external URL of the server you're running Shuffle on (the one you visit Shuffle with in your browser):
```
# Required:
- SHUFFLE_SWARM_CONFIG=run      # Enables SWARM scaling
- SHUFFLE_LOGS_DISABLED=true    # Ensures we don't have memory issues
- BASE_URL=http://YOUR-BACKEND-IP:3001   # replaced by the backend's public IP
- SHUFFLE_WORKER_IMAGE=ghcr.io/shuffle/shuffle-worker:latest

# Optional configuration:
- SHUFFLE_AUTO_IMAGE_DOWNLOAD=false                       # This should be set to false IF images are already downloaded
- SHUFFLE_WORKER_SERVER_URL=http://shuffle-workers        # Internal Docker Worker URL (don't modify if not necessary)
- SHUFFLE_SWARM_NETWORK_NAME=shuffle_swarm_executions     # If you want a special network name in the executions
- SHUFFLE_SCALE_REPLICAS=1                                # The amount of worker container replicas PER NODE  (since 1.2.0)
- SHUFFLE_APP_REPLICAS=1                                  # The amount of app container replicas PER NODE     (since 1.2.1)
- SHUFFLE_MAX_SWARM_NODES=1                               # The max amount of swarm nodes shuffle can use     (since 1.3.2)
- SHUFFLE_SKIPSSL_VERIFY=true                             # Stops Shuffle's internal services from validating TLS/SSL certificates. Good to use if BASE_URL is a domain.
    
```

If this is configured properly, the "Status" and "Scale" section on your [Runtime Locations in the Admin panel](https://shuffler.io/admin?tab=locations) should show as "Running" and a green checkmark respectively.
![image](https://github.com/user-attachments/assets/9fbfdf29-0a3f-4926-bf93-da70226e30b1)

To make swarm work, Please make sure that [these ports are open](https://docs.docker.com/engine/swarm/swarm-tutorial/#open-protocols-and-ports-between-the-hosts) on all your machines (to at least, both of these machines internally): 2377, 7946 and 4789

**It is recommended to make sure that these ports are ONLY open internally to be sure that everything is secure.**

2. When step 1 is configured, take down the stack and pull it back up AFTER initializing swarm:
```
docker swarm init
docker-compose down
docker-compose up -d
docker swarm join-token manager # copy the command given
```

PS: In certain scenarios you may need extra configurations, e.g. for network MTU's, docker download locations, proxies etc. See more in the [production readiness](/docs/configuration#production_readiness) section.

### Adding another machine to the swarm network:

Start by making sure docker works here. Then paste the output from the previous docker command to `docker join`. It adds the network in the docker swarm network as a manager (It is required to orchestrate the app containers).

It should look something like this:

```
docker swarm join --token SWMTKN-1-{token} {internal IP}:2377
```

### Verify swarm

Run the following command to get logs from Orborus:

```
docker logs -f shuffle-orborus
```

And to check if services have started:

```
docker service ls
```

If the list is empty, or you see any of the "replicas" have 0/1, then something is wrong. In case of any swarm issues, contact us at [support@shuffler.io](mailto:support@shuffler.io) or contact your account representative.

If you get EOFs or timeouts for workers in machine B, look [here](https://shuffler.io/docs/troubleshooting#TLS_timeout_error/Timeout_Errors/EOF_Errors).

![](Aspose.Words.81096d25-bbff-47b2-a5ee-1ac38ad8ca4e.001.jpeg)

### Environment Variables

Shuffle has a few toggles that makes it straight up faster, but which removes a lot of the checks that are being done during your first tries of Shuffle.

Backend:

```
# Set the encryption key to ensure all app authentication is being encrypted. If this is NOT defined, we do not encrypt your apps. If this is defined, all authentications - both old and new will start using this key. 
# Do NOT lose this key if specified, as that means you will need to reset all keys.

SHUFFLE_ENCRYPTION_MODIFIER=YOUR KEY HERE

# **PS: Encryption is available from Shuffle backend version >=0.9.17.**
# **PPS: There's a [known bug](https://github.com/frikky/Shuffle/issues/528) with Proxies and git**

# Set up distributed memcaching. See "Distributed Caching" for more.
SHUFFLE_MEMCACHED=<IP>:PORT

```

Orborus:

```
# Cleans up all containers after they're done. Necessary to help Docker scale. Default=false
CLEANUP=true     

# Cleans up any containers related to Shuffle that have been up for more than 600 seconds.
SHUFFLE_ORBORUS_EXECUTION_TIMEOUT=600

# Decides the max amount of workflows to concurrenly run. Defaults to 10.
# Example math: 10 workflows * WITH 10 apps / second = 110 containers per second.
# We recommend starting with 10 and going higher as need be.
SHUFFLE_ORBORUS_EXECUTION_CONCURRENCY=10

# Configures a HTTP proxy to use when talking to the Shuffle Backend
HTTP_PROXY=     
# Configures a HTTPS proxy when speaking to the Shuffle Backend
HTTPs_PROXY=     

# Decides if the Worker should use the same proxy as Orborus (HTTP_PROXY). Default=true
SHUFFLE_PASS_WORKER_PROXY=true

# Decides if the Apps should use the same proxy as Orborus (HTTP_PROXY). Default=false
SHUFFLE_PASS_WORKER_PROXY=true


### PAID: The environment variables below only work when you've acquired a paid license of Shuffle (not required, but VERY useful when scaling Shuffle):
SHUFFLE_WORKER_IMAGE=ghcr.io/shuffle/shuffle-worker-scale:latest
SHUFFLE_SWARM_NETWORK_NAME=shuffle_swarm_executions
SHUFFLE_SCALE_REPLICAS=1
SHUFFLE_SWARM_CONFIG=run

# Set up distributed caching for Orborus & Worker(s). See "Distributed Caching" for more.
SHUFFLE_MEMCACHED=<IP>:PORT
```

### Distributed Caching
Once you have a Scalable version of Shuffle, using Docker swarm, it becomes important for data to flow correctly throughout the platform. In version 1.1 of Shuffle, we introduce distributed caching [in the form of Memcached](https://hub.docker.com/_/memcached). Memcached helps reduce the load on the database, as well as to ensure all executions are handled adequately. These services are supported:

- Backend
- Orborus
- Worker

To make use of Memcached, you have to start a memcached service locally on a host Shuffle can access, before configuring each service to use it with a single environment variable. The default port is 11211. Here is a quickstart that reserves 1024 Mb of memory:
```
docker run --name shuffle-cache -p 11211:11211 -d memcached -m 1024
```

**PS: This requires swap limit capabilities on the Docker host. [More about running it in Docker here](https://hub.docker.com/_/memcached)**

Once this is up, it will be listening on port 11211. From here, you may set up the `SHUFFLE_MEMCACHED` environment variable on the previously mentioned services. We recommend starting with the backend. Here's an example that fits into your docker-compose file:
```
services:
  image: ghcr.io/shuffle/shuffle-backend:latest
  environment:
    - SHUFFLE_MEMCACHED=10.0.0.1:11211
    ...
  ...
  
```

You can additionally add this do your docker compose with the following setting:
```
  memcached:
    image: memcached:latest
    container_name: shuffle-cache
    hostname: shuffle-cache
    mem_limit: 1024m
    restart: unless-stopped
    environment:
      - MEMCACHED_MEMORY=1024
      - MEMCACHED_MAX_CONNECTIONS=2500
    ports:
      - 11211:11211
```

### Multi-server memcached
You can run Memcached on multiple servers as well, but may run into key inconsistency. This should however not affect how things run in Shuffle, as we verify and fix request data. To do this, simply add multiple memcached instances to the environment variable, comma separated.

Example:
```
- SHUFFLE_MEMCACHED=10.0.0.1:11211,10.0.0.2:11211,10.0.0.3:11211
```

If you need help with this, [please contact us](mailto:support@shuffler.io).

### Disaster Recovery/High Availability

In a production system within a high-criticality environment concerning requirements and security, it is crucial that all our tools possess the property of High Availability or, at least, Disaster Recovery.

The following architecture illustrates how Shuffle should be deployed in its On-Premise free mode to achieve at least Disaster Recovery, which ensures that even if one node of the system fails, there will be no loss of information. In the worst case scenario, if it was a critical node, it should be able to resume operation promptly.

The first step to ensure this is to distribute the database in a way that guarantees the property that even if one node fails, there will be no data loss.

The second point to consider is that for Workflows to continue running even if one Orborus node goes down, there should be another node of the same type to ensure this.

In this manner, we can ensure that, in the worst case, the backend+frontend may experience negative consequences due to being in a Docker container. However, its automatic restart can be configured, and in any case, bringing this node back into operation is swift.

The resulting architecture that emerges after applying these properties is as follows:

![DisasterRecovery On Premmise Deploy](https://github.com/Shuffle/Shuffle-docs/blob/master/assets/configuration-disaster-recovery-onprem-deploy.png?raw=true)

To implement this, follow these steps:

- Define in all your nodes the list of hostnames in /etc/hosts so all the machines can do the necessary IP resolutions when they have a hostname.

- Configure an OpenSearch database cluster. For this step, it is recommended to follow the official documentation [https://opensearch.org/docs/latest/tuning-your-cluster/index/](https://opensearch.org/docs/latest/tuning-your-cluster/index/). Anyways to achieve this in a easy way you just need to change this settings in each opensearch node and reload the service:
```
cluster.name -> Set its new value to "shuffle-cluster".
node.name -> Set its new value to the hostname of the current node.
network.host -> Set its new value to the IP of your node(you need to be able to ping this IP from each one of the opensearch nodes and also from the backend+frontend one).
discovery.seed_hosts -> Set its new value to a list that contains each one of the hostnames of the OpenSearch nodes for example like this: ['opensearchReplica0', 'opensearchReplica1', 'opensearchReplica2']
cluster.initial_cluster_manager_nodes -> All the nodes should be able to be masters so as done before use that list of hostnames like: ['opensearchReplica0', 'opensearchReplica1', 'opensearchReplica2']
```

- Deploy a node containing both the frontend and backend components. In the configurations of this node, all nodes of the database cluster should be included to experience the effects of the previous step. The dockerfile should look like this:

```Dockerfile
version: '3'
services:
  frontend:
    image: ghcr.io/shuffle/shuffle-frontend:latest
    container_name: shuffle-frontend
    hostname: shuffle-frontend
    ports:
      - "${FRONTEND_PORT}:80"
      - "${FRONTEND_PORT_HTTPS}:443"
    networks:
      - shuffle
    environment:
      - BACKEND_HOSTNAME=${BACKEND_HOSTNAME}
    restart: unless-stopped
    depends_on:
      - backend
  backend:
    image: ghcr.io/shuffle/shuffle-backend:latest
    container_name: shuffle-backend
    hostname: ${BACKEND_HOSTNAME}
    # Here for debugging:
    ports:
      - "${BACKEND_PORT}:5001"
    networks:
      - shuffle
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ${SHUFFLE_APP_HOTLOAD_LOCATION}:/shuffle-apps     
      - ${SHUFFLE_FILE_LOCATION}:/shuffle-files
      #- ${SHUFFLE_OPENSEARCH_CERTIFICATE_FILE}:/shuffle-files/es_certificate
    env_file: .env
    environment:
      - SHUFFLE_APP_HOTLOAD_FOLDER=/shuffle-apps
      - SHUFFLE_FILE_LOCATION=/shuffle-files
    restart: unless-stopped
networks:
  shuffle:
    driver: bridge
```
Also for this step you need to change the value of a variable inside the .env so it looks like this:`SHUFFLE_OPENSEARCH_URL=SHUFFLE_OPENSEARCH_URL=https://192.168.0.30:9200,https://192.168.0.31:9200,https://192.168.0.32:9200`. Each one of that IPs is the corresponding one to each opensearch node.

- Deploy as many Orborus nodes as desired. At a minimum, it is recommended to deploy 2 nodes. If scaling is required regarding the maximum number of concurrently executing Workflows, the number of these nodes can be increased. The dockerfile of each one of the orborus nodes should look like this:

```Dockerfile
version: '3'
services:
  orborus:
    #build: ./functions/onprem/orborus
    image: ghcr.io/shuffle/shuffle-orborus:latest
    container_name: shuffle-orborus
    hostname: shuffle-orborus
    networks:
      - shuffle
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      - BASE_URL=http://192.168.0.49:5001
      - SHUFFLE_APP_SDK_VERSION=1.1.0
      - SHUFFLE_WORKER_VERSION=latest
      - ORG_ID=Shuffle
      - ENVIRONMENT_NAME=Shuffle
      - DOCKER_API_VERSION=1.40
      - SHUFFLE_BASE_IMAGE_NAME=frikky
      - SHUFFLE_BASE_IMAGE_REGISTRY=ghcr.io
      - SHUFFLE_BASE_IMAGE_TAG_SUFFIX="-1.0.0"
      - CLEANUP=true
      - SHUFFLE_ORBORUS_EXECUTION_TIMEOUT=600
    restart: unless-stopped
networks:
  shuffle:
    driver: bridge
```

You need to change the value of the environment `BASE_URL` of this Dockerfile, so it aims to the IP of your Shuffle frontend+backend node.

### Kubernetes

Shuffle use with Kubernetes is now possible due to help from our contributors. You can read more about how it works on our [Github page](https://github.com/Shuffle/Shuffle/tree/main/functions/kubernetes), which includes extensive helm charts and configuration possibilities.

Due to Kubernetes not being capable of building Shuffle Apps directly, an additional container for building them is available.

### Orborus with Kubernetes
To configure Kubernetes, you need to specify a single environment variable for Orborus: RUNNING_MODE. By setting the environment variable RUNNING_MODE=kubernetes, execution should work as expected!

### Scaling Kubernetes
To scale Shuffle in Kubernetes, use the following environment variables in the Orborus container:
```bash
SHUFFLE_SCALE_REPLICAS=3 # HPA coming soon. This is for static scaling.
SHUFFLE_WORKER_IMAGE=ghcr.io/shuffle/shuffle-worker-scale:nightly
IS_KUBERNETES=true
SHUFFLE_SWARM_CONFIG=run
SHUFFLE_MEMCACHED=shuffle-memcached:11211 # this depends on your setup.
```

## Networking
Networking with Shuffle is pretty straight forward. What we check for are the following:

- Can Shuffle reach your services? 
- Can the Shuffle services reach each other (frontend/backend/database/Orborus)

There are however many things that can go wrong with these simple mechanisms, leading to a need for network configuration changes. Shuffle is however built on HTTP, and can be easily modified and made to work both in air-gapped locations as well as with enterprise proxy environments. 

### Proxy configuration

Proxies are another requirement to many enterprises, hence it's an important feature to support. There are two places where proxies can be implemented:

* Shuffle Backend: Connects to Github and Dockerhub.
* Shuffle Orborus: Connects to Dockerhub and Shuffle Backend.

**PS: Orborus settings are also set for the Worker**

To configure these, there are two options:

* Internal vs External proxy (shuffle vs apps)
* Individual containers
* Globally for Docker

To **DISABLE** proxy for **internal** Shuffle traffic (between internal containers), add the following environment variable to Orborus ([origin](https://jamboard.google.com/d/1KNr4JJXmTcH44r5j_5goQYinIe52lWzW-12Ii_joi-w/edit?usp=sharing)):
```
- SHUFFLE_INTERNAL_HTTP_PROXY=noproxy
- SHUFFLE_INTERNAL_HTTPS_PROXY=noproxy
```

To disable proxy use for specific domains, use NO_PROXY with comma separation between domains:
```
NO_PROXY=myinternal-domain.com,random.org
```

#### Global Docker proxy configuration

Follow this guide from Docker: https://docs.docker.com/network/proxy/

### Internal Proxy settings

The main proxy issues may arise with the "Backend", along with 3the "Orborus" container, which runs workflows. This has to do with how this server can contact the backend (Orborus), along with how apps can be downloaded (Worker), down to how apps engage with external systems (Apps).

Environment variables to be sent to the Orborus container:

```
# Configures a HTTP proxy to use when talking to the Shuffle Backend
HTTP_PROXY=     
# Configures a HTTPS proxy when speaking to the Shuffle Backend
HTTPs_PROXY=     

# Decides if the Worker should use the same proxy as Orborus (HTTP_PROXY). Default=true
SHUFFLE_PASS_WORKER_PROXY=true

# Decides if the Apps should use the same proxy as Orborus (HTTP_PROXY). Default=false
SHUFFLE_PASS_WORKER_PROXY=true
```

Environment variables for the Backend container:

```
# A proxy to be used if Opensearch / Elasticsearch (database) is behind a proxy.
SHUFFLE_OPENSEARCH_PROXY

# Configures a HTTP proxy for external downloads
HTTP_PROXY=     
# Configures a HTTPS proxy for external downloads
HTTPs_PROXY=     
```

### Opensearch / Elasticsearch proxies
Connections from Shuffle's backend to the Opensearch database **does NOT** follow normal HTTP_PROXY and NOPROXY environment variables. 

Opensearch and Elasticsearch proxy configuration can be set using the `SHUFFLE_OPENSEARCH_PROXY` environment variable. 

#### Individual container proxy

To set up proxies in individual containers, open docker-compose.yml and add the following lines with your proxy settings (http://my-proxy.com:8080 in my case).

**PS: Make sure to use uppercase letters, and not lowercase (HTTP_PROXY, NOT http_proxy)**

![Proxy containers](https://github.com/shuffle/shuffle-docs/blob/master/assets/proxy-containers.png?raw=true)

### Orborus running on a different network
All you'll need to do is allow orborus to have access to the backend OR frontend of Shuffle.

### Internal vs External proxy
As of November 2023, we added another way to configure a difference between these two:
- Internal tools like Backend -> Orborus -> Worker <-> Apps
- Apps -> External tools

This is in order to make it possible to have the an internal proxy different from those apps use for external services. These environment variables should be added to the "Orborus" container.

```
HTTP_PROXY=<external proxy>                     # used by default for everything

SHUFFLE_INTERNAL_HTTP_PROXY=<internal proxy>     # Overrides HTTP_PROXY, making internal services in Shuffle use this proxy instead of HTTP_PROXY.
```

**PS: This is in beta. Reach out to support@shuffler.io if you have any trouble with this.**

### HTTPS

HTTPS is enabled by default on port 3443 with a self-signed certificate for localhost. If you would like to change this, the only way (currently) is to add configure and rebuild the frontend. If you don't have HTTPS enabled, check [updating shuffle](#updating_shuffle) to get the latest configuration. Another workaround is to set up an [Nginx reverse proxy](https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/) you can control yourself. See further down for more details

```
After setting this up, make sure to change the BASE_URL for Orborus to talk to your new HTTPS url if you want encrypted traffic everywhere.
Default Routing: Orborus -> Backend:5001.
New Routing: Orborus -> Nginx -> Frontend -> Backend.

The New Routing steps are automatic as long as you update the BASE_URL to point to your new reverse proxy URL.
```

Necessary info for the truststore to create TLS/SSL certificates:

* Certificates are located in ./frontend/certs.
* ./frontend/README.md contains information on generating a self-signed cert
* (default): Privatekey is named privkey.pem
* (default): Fullchain is named fullchain.pem

If you want to change this, edit ./frontend/Dockerfile and ./frontend/nginx.conf.

After changing certificates, you can rebuild the entire frontend by running (./frontend)

```
./run.sh --latest
```

Make sure that the output image is the same in your docker-compose.yml file. This should work seemlessly for you next.

### App Certificates
As of November 2023, it's now possible to mount folders into apps. This is in order for you to have better control of what Shuffle Apps can do, with the main reason being to manage certificates. 

To mount in certificates, add the following environment variable to the "Orborus" container, but change the source and destination folder. The item BEFORE the colon (:) is the source folder on your machine, with the one AFTER the colon (:) being for the destination folder in the app itself.

If you want more folders mounted, add them with a comma.
```
SHUFFLE_VOLUME_BINDS="/etc/ssl/certs:/usr/local/share/ca-certificates,srcfolder2:dstfolder2"
```

**PS: This is in beta. Reach out to support@shuffler.io if you have any trouble with this.
**

### Using the Nginx Reverse Proxy for TLS/SSL
If you intend to use Nginx as a Reverse Proxy, the main steps are below. [Here is a basic single-server architecture for it](https://jamboard.google.com/d/1zJU8yMzbsu-XWeZnch_5MoDwmMNkkN8ZmoGNLCaHPlU/edit?usp=sharing). The Docker version is further down.

1. [Install Nginx](https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-20-04) on your server (find the correct distro), or in a [Docker container by itself](https://www.theserverside.com/blog/Coffee-Talk-Java-News-Stories-and-Opinions/Docker-Nginx-reverse-proxy-setup-example).
2. Make sure you have a VALID certificate that matches your domain/hostname and [add this to your Nginx server](https://phoenixnap.com/kb/install-ssl-certificate-nginx)
3. In the nginx.conf file (/etc/nginx/conf.d/default.conf or similar), under "server", add the information below. Make sure to change the "proxy_pass" part. This is how it will redirect all /api requests.
```
location / {
    proxy_pass SHUFFLE FRONTENDIP;
    proxy_buffering off;
    proxy_http_version 1.1;

    proxy_connect_timeout 900;
    proxy_send_timeout 900;
    proxy_read_timeout 900;
    send_timeout 900;
    proxy_ssl_verify off;
}
```
4. Restart Nginx! `systemctl restart nginx`

### Nginx in Docker
1. Add the following service to your docker-compose.yml
```
  nginx-proxy:
    image: nginx:latest
    container_name: shuffle-nginx-proxy
    networks:
      - shuffle
    ports:
      - "80:80"
    volumes:
      - ./nginx-conf:/etc/nginx/conf.d
      - ./certs:/etc/nginx/certs
    restart: always
```

2. Add a new nginx configuration file called `nginx-conf` with the following (you may add additional Nginx configuration to this):
```
server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate /etc/nginx/certs/cert.crt;
    ssl_certificate_key /etc/nginx/certs/cert.key;

    location / {
        proxy_pass http://shuffle-frontend:80;

        proxy_buffering off;
        proxy_http_version 1.1;

        proxy_connect_timeout 900;
        proxy_send_timeout 900;
        proxy_read_timeout 900;
        send_timeout 900;
        proxy_ssl_verify off;
    }
}
```

3. Add a folder called "certs" with **your certificates** named `cert.crt` and `cert.key`.
4. Restart everything: `docker-compose down; docker-compose up -d`

### Internal Certificate Authority
By default, certificates are not being verified when outbound traffic goes from Shuffle. This is due to the massive use of self-signed certificates when using internal services. You may ignore certificate warnings by adding `SHUFFLE_SKIPSSL_VERIFY=true` to the environment of each relevant service - most notably used for Orborus.  If you want to accept your Certificate Authority for all requests, there are a few ways to do this:

1. Mount your CA certificates (recommended): Add the `./certs:/certs` mount to the Orborus service in your docker-compose.yml. Ensure that the shuffle directory contains a certs subdirectory with all the necessary certificate files. This will automatically append all certificates in `./certs` to the system's root CA.
2. Docker Daemon level  - point to your cert: `$ dockerd --tlscacert=/path/to/custom-ca-cert.pem`
3. Add it to every app (per-image configuration). You can do this by modifying the Dockerfile for an app and manually building it with the certificate in the Dockerfile of each Docker image. Restart Shuffle after this is done.

As this may require advanced Docker understanding, reach out to ask us about it: [support@shuffler.io](mailto:support@shuffler.io) 

### IPv6

Shuffle supports IPv6 in Docker by default, but your docker engine may not. IPv6 can be enabled in Docker by adding it to the /etc/docker/daemon.json file on the host as per this article by Docker:

[https://docs.docker.com/config/daemon/ipv6/](https://docs.docker.com/config/daemon/ipv6/)


### Enterprise Environments

In most enterprise environments, Shuffle will be behind firewalls, proxies and other networking equipment. If this is the case, below are the requirements to make Shuffle work anywhere. The most common issue has to do with downloads from Alpine linux's Docker images while Shuffle is running.

**PS:** If external connections are blocked, you may further have issues running Apps. Read more about [manual image transfers here](#manual_docker_image_transfers).

### Change the Database from OpenSearch to Elasticsearch

-	Open the Docker-compose.yml file in the Shuffle directory. Find the OpenSearch container section and either comment out or remove the details. Save your modifications to the file.
  
 	![image](https://github.com/yogeshgurjar127/Shuffle-docs/assets/118437260/5a9ff541-14f4-4ddc-8c04-08a874ffc3ff)

- Now open the .env file and change the below value in the .env  from false to true for Elasticsearch database enable.
  
  ![image](https://github.com/yogeshgurjar127/Shuffle-docs/assets/118437260/f1116c97-daa2-48ba-80f4-f14803c1629d)

-	Find the part in the .env file that defines database configurations. Update the Elasticsearch host configuration using your Elasticsearch IP address.
  
  ![image](https://github.com/yogeshgurjar127/Shuffle-docs/assets/118437260/13277ad5-269d-44a7-ab3b-13916bb9ce0e)




### Domain Whitelisting

These URL's are used to get Shuffle up and running. Whitelisting them for the Shuffle services should make all processes work seamlessly.  

PS: We do intend to make this JUST https://shuffler.io in the future.

```
# Can be closed after install with working Workflows
shuffler.io                                                      # Initial setup & future app/workflow sync
github.com                                                        # Downloading apps, workflows and documentation
pkg-containers.githubusercontent.com     # Downloads from Github Container registry (ghcr.io)
raw.githubusercontent.com                         # Downloads our Documentation raw from github (https://github.com/shuffle/shuffle-docs)

# Should stay open
dl-cdn.alpinelinux.org                        # Used for building apps in realtime
registry.hub.docker.com                     # Downloads apps if they don't exist locally
ghcr.io                                                        # Github Docker registry
auth.docker.io                                        # Dockerhub authentication
registry-1.docker.io                            # Dockerhub registry (for apps)
production.cloudflare.docker.com     # Protects of DockerHub
```

### Incoming IP Whitelisting

When using Shuffle in the cloud (*.shuffler.io), the incoming IP to your services by default will be be from our cloud functions, if you are not using [Runtime Locations](/admin?tab=locations). The range is **not static**, and may wary based on region. Here's a list (mostly IPv6 as of 2025):

```
Default (London): 2600:1900:2000:2a:400::0 -> 2600:1900:2000:2a:400::ffff
```

If you want direct access with ANY app in your on-premises environment, we recommend setting up a new environment on a server in the same network. Steps to set this up:

1. Go to [/admin?tab=locations](/admin?tab=locations) and create a new runtime location
2. Click the Copy button in the "Command" tab to copy the relevant Docker command. This requires Docker installed on the server in question.
3. Run the copied command on your server on-premises.
4. Change the Environment a workflow runs with to the new environment. When ran, it will automatically run on YOUR server, instead of on our cloud.
5. Your server will now be reaching out to Shuffle cloud for jobs every few seconds. This requires outbound access from YOUR network to the domains shuffler.io and shuffle-backend-stbuwivzoq-nw.a.run.app.

Environment page:
<img width="1072" alt="image" src="https://github.com/user-attachments/assets/037ade5c-680f-4144-97ff-d117cb29035c">

Architecture connecting from cloud to onprem (hybrid):
![image](https://github.com/user-attachments/assets/7f0b6146-ebae-4133-bbc7-8b158d48c3a9)

### Static inbound IPs for cloud
As a customer of Shuffle we can provide you with a static **IP range** with secondary domains that can be used for cloud routing. Contact support@shuffler.io for more info

### Manual Docker image transfers

In certain cases you may not have access to download or build images at all. If that's the case, you'll need to manually transfer them to the appropriate server. If the image to transfer is an app, it should be moved to the "Orborus" server. Otherwise; backend server.

```
# 1. Download the image you want. Go to [hub.docker.com](https://hub.docker.com/r/frikky/shuffle/tags?page=1&ordering=last_updated) and find the image. Download with docker pull. E.g. for Shuffle-tools:
docker pull frikky/shuffle:shuffle-tools_1.1.0

# 2. Save the image to a file to be transferred.
docker save frikky/shuffle:shuffle-tools_1.1.0 > shuffle_tools.tar

# 3. Transfer the file to a remote server
scp shuffle_tools.tar username@<server>:/path/to/destination/shuffle_tools.tar

# 4. Log into the remote server and find the repository
ssh username@<server>
cd /path/to/destination #same path as above

# 5. Load the file!
docker load shuffle_tools.tar

## All done!

# Transfer between 2 remote hosts:
#scp -3 centos@10.0.0.1:/home/user/wazuh.tar centos@10.0.0.2:/home/user/wazuh.tar
```

### No Internet Install
This procedure will help you export what you need to run Shuffle on a no internet host.

**The following features will not work without internet:**
- Cloud Sync
- Automatic Health System (/health page)
- UI app activations
- Automatic App generation AI
- Depending on your network: Search engine. This is a frontend feature, if you are in a no-internet zone, it will stop working. 

1. Prerequise
* Both machines has Docker and Docker Compose installed already

* Your host machine already needs the images on it to make them exportable
2. Pull images on original machine

Shuffle need a few base images to work:

- shuffle-frontend
- shuffle-backend
- shuffle-orborus
- shuffle-worker
- shuffle:app_sdk
- opensearch
- shuffle-subflow

```
 docker pull ghcr.io/frikky/shuffle-backend & docker pull ghcr.io/frikky/shuffle-frontend & docker pull ghcr.io/frikky/shuffle-orborus &  docker pull frikky/shuffle:app_sdk & docker pull ghcr.io/frikky/shuffle-worker & docker pull opensearchproject/opensearch:2.5.0 & docker pull registry.hub.docker.com/frikky/shuffle:shuffle-subflow_1.0.0
```

Be careful with the versioning for opensearch, all other are going to use the tag "latest". 
You will also need to download and transfer ALL the apps you want to use. These can be discovered as such:

```
docker images | grep -i shuffle
```

3. Save images and archive them

```
mkdir shuffle-export & cd shuffle-export

docker save ghcr.io/frikky/shuffle-backend > backend.tar
docker save ghcr.io/frikky/shuffle-frontend > frontend.tar
docker save ghcr.io/frikky/shuffle-orborus > orborus.tar
docker save frikky/shuffle:app_sdk > app_sdk.tar
docker save ghcr.io/frikky/shuffle-worker:latest > worker.tar
docker save opensearchproject/opensearch:2.5.0 > opensearch.tar
docker save registry.hub.docker.com/frikky/shuffle:shuffle-subflow_1.0.0 > sublow.tar

git pull https://github.com/Shuffle/python-apps.git

wget https://raw.githubusercontent.com/Shuffle/Shuffle/master/.env
wget https://raw.githubusercontent.com/Shuffle/Shuffle/master/docker-compose.yml

cd .. & tar cvf shuffle-export.tar.gz shuffle-export
```

4. Export data to the targeted machine

Use scp, usb key, ..., to copy the previous archive to the machine. [More about manual transfers here](http://localhost:3002/docs/configuration#manual_docker_image_transfers)

5. Import docker images to host without internet
   
   ```
   tar xvf shuffle-export.tar.gz & cd shuffle-export
   find -type f -name "*.tar" -exec docker load --input "{}" \;
   ```

6. Deploy Shuffle without Internet

Create folders to add the python apps

```
mkdir shuffle-apps
cp -a python-apps/ * shuffle-apps/
```

Now, you just need to configure and install Shuffler like in normal procedure

### Database

To modify the database location, change "DB_LOCATION" in .env (root dir) to your new location.

### Database indexes (opensearch)

- workflowapp
- workflowexecution
- workflowapp
- workflow
- apikey
- app_execution_values
- environments
- files
- hooks
- openapi3
- organizations
- schedules
- sessions
- syncjobs
- trigger_auth
- workflowappauth
- users
- workflowqueue-*

PS: workflowqueue-* is based on the runtime location used for workflow execution (Orborus).

## Debugging

As Shuffle has a lot of individual parts, debugging can be quite tricky. To get started, here's a list of the different parts, with the latter three being modular / location independent.

| Type                                        | Container name        | Technology       | Note                                                                                                       |
| ------------------------------------------- | --------------------- | ---------------- | ---------------------------------------------------------------------------------------------------------- |
| Frontend                                    | shuffle-frontend      | ReactJS          | Cytoscape graphs & Material design                                                                         |
| Backend                                     | shuffle-backend       | Golang           | Rest API that connects all the different parts                                                             |
| Database                                    | shuffle-database      | Google Datastore | Has all non-volatile information. Will probably move to elastic or similar.                                |
| Orborus                                     | shuffle-orborus       | Golang           | Runs workers in a specific environment to connect locations. Defaults to the environment "Shuffle" onprem. |
| Worker                                      | worker-id             | Golang           | Deploys Apps to run Actions defined in a workflow                                                          |
| app sdk                                     | appname_appversion_id | Python           | Used by Apps to talk to the backend                                                                        |
| worker-8a666e4f-e544-440e-bf0f-4220e7cc9e25 |                       |                  |                                                                                                            |

### Disabling Image downloads
There are cases where automatic image downloads may occur, such as when you restart Orborus. You can disable this with `SHUFFLE_AUTO_IMAGE_DOWNLOAD=false`


### Execution debugging

Execution debugging might be the most notable issue you might explain. This is because there are a ton of reasons that it might crash. Before going into techniques to find what's going on, you'll need to understand what exactly happens when you click the big execution button.

**Frontend click -> Backend verifies and deploys executions -> (based on environments) orborus deploys a new worker -> worker finds actions to execute -> your app is executed.**

1. A workflow is executed
2. The backend verifies whether you can execute and deploys to environment
3. Orborus is listening to environment and deploys worker if it's the correct one
4. Worker deploys actions if they have the right environment
5. App executes and returns data back to the execution

As previously stated, a lot can go wrong. Here's the most common issues:

* Networking (firewalls / proxies)
* Badly formed apps.
* Bad environment

### General debugging

This part is mean to describe how to go about finding the issue you're having with executions. In most cases, you should start from the top of the list previously described in the following way:

1. Find out what environment your action(s) are running under by clicking the App and seeing "Environment" dropdown. In this case (and default) is "Shuffle". Environments can be specified / changed under the path /admin
   ![Check execution 3](https://github.com/shuffle/shuffle-docs/blob/master/assets/check_execution_3.png?raw=true)

2. Check if the workflow executed at all by finding the execution line in the shuffle-backend container. Take note that it mentions environment "Shuffle", as found in the previous step.
   
   ```
   docker logs -f shuffle-backend
   ```

![Check execution 1](https://github.com/shuffle/shuffle-docs/blob/master/assets/check_execution_1.png?raw=true)

3. If it executed, check whether Orborus is running, before checking it's logs for "Container \<container_id\> is created. The container_id is the worker it has deployed. Take not of the environment again at the end of the line. If you don't see this line, it's most likely because it's running in the wrong environment.

Check if shuffle-orborus is running

```
docker ps # Check if shuffle-orborus is running
```

Find whether it was deployed or not

```
docker logs -f shuffle-orborus  # Get logs from shuffle-orborus
```

![Check execution 2](https://github.com/shuffle/shuffle-docs/blob/master/assets/check_execution_2.png?raw=true)

Check environment of running shuffle-orborus container.

```
docker inspect shuffle-orborus | grep -i "ENV"
```

Expected env result where "Shuffle" corresponds to the environment
![Check execution 4](https://github.com/shuffle/shuffle-docs/blob/master/assets/check_execution_4.png?raw=true)

4. Check whether the worker executed your app. Remember that we found \<container_id\> previously by checking the logs of shuffle-orborus? Now we need that one. Workers are and will always be verbose, specifically for the reason of potential debugging.

Find logs from a docker container

```
docker logs -f CONTAINER_ID
```

![Check execution 5](https://github.com/shuffle/shuffle-docs/blob/master/assets/check_execution_5.png?raw=true)

As can be seen in the image above, is shows the exact execution order it takes. It starts by finding the parents, before executing the child process after it's finished. Take note of the specific apps being executed as well. It says "Time to execute \<app_id\> with app \<app_name:app_version\>. This indicates the app THAT WILL be executed. The following lines saying "Container \<container_id\> is the container created with this app.



5. App debugging in itself might be the trickiest. There are a lot of factors like branches, bad workflow building etc that might come into play. This builds on the same concept as the worker, where you pass the container ID it specified.

Get the app logs

```
docker logs -f CONTAINER_ID # The CONTAINER_ID found in the previous worker logs
```

As you will notice, app logs can be quite verbose (optional in a later build). In essence, if you see "RUNNING NORMAL EXECUTION" in the end, there's a 99.9% chance that it worked, otherwise some issue might have occurred.

Please [notify me](https://twitter.com/frikkylikeme) if you need help debugging app executions ASAP, as I've done a lot of it, but it's more tricky than the other steps.

### Hybrid docker image handling

We currently don't have a Docker Registry for Shuffle, meaning you need some minor configuration to get Orborus running remotely with the right containers. This only applies to containers not on dockerhub, as we automatically push PYTHON containers there when updated (not OpenAPI)

Here's an example of how to handle this with two different servers and Docker

```
ssh user@10.0.0.1
docker save frikky/shuffle:wazuh_api_rest_1.0.0 > wazuh.tar
exit
scp -3 centos@10.0.0.1:/home/user/wazuh.tar centos@10.0.0.2:/home/user/wazuh.tar
ssh user@10.0.0.2
docker load wazuh.tar
```

## Docker socket

For now, the docker socket is required to run Shuffle. Whether you run with Kubernetes or another clustering technology, Shuffle WILL need access to ContainerD, which is what the docker socket provides. If this is against internal policies and you want a single point of contact for controlling permissions, please have a look at [docker socket proxy](#docker_socket_proxy) farther down.

**Usage of the socket**:

* Backend (Not required, but used for app management)
* Orborus (Required, deploying Workers)
* Worker    (Required, deploying Apps. Apps DONT have access to the socket.)

**API's in use**

* Backend: Create, Make, Export docker images. No direct container management.
* Orborus: Download and Remove images. Make, List and Remove containers. Make, List and Remove services.
* Worker: Download and Remove images. Make, List and Remove containers. Make, List and Remove services.

### Docker Socket Proxy
In certain scenarios or environments, you may find the docker socket to not have the right permissions, or running the socket directly on your software to be against internal policies. To solve this problem, we've built support for the [docker socket proxy](https://github.com/Tecnativa/docker-socket-proxy), which will give the containers the same permissions, but without the socket being directly mounted in the same container. Another good reason to use the docker socket proxy is to control the docker permissions required.

To use the docker socket proxy, add the following to your docker-compose.yml as a service. This will lauch it together with the rest:
```
  docker-socket-proxy:
    image: tecnativa/docker-socket-proxy
    privileged: true
    environment:
      - SERVICES=1
      - TASKS=1
      - NETWORKS=1
      - NODES=1
      - BUILD=1
      - IMAGES=1
      - GRPC=1
      - CONTAINERS=1
      - PLUGINS=1
      - SYSTEM=1
      - VOLUMES=1
      - INFO=1
      - DISTRIBUTION=1
      - POST=1
      - AUTH=1
      - SECRETS=1
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    networks:
      - shuffle

```

When done, remove the "/var/run/docker.sock" volume from the backend and orborus services in the docker-compose. To enable the docker rerouting, add this environment variable to both of them
```
      - DOCKER_HOST=tcp://docker-socket-proxy:2375
```

This will route all docker traffic through the docker-socket-proxy giving you granular access to each API. 

## Uptime Monitoring

Uptime monitoring of Shuffle can be done by periodically polling the API for userinfo located at /api/v1/getinfo. This is an API that connects to our database, and which will be stuck if we any platform issues occur, whether in your local instance or in our Cloud instance on https://shuffler.io. 

Shuffle has and will not have any planned downtime for services on https://shuffler.io, and have built our architecture around being able to upgrade and roll back without any downtime at all. If this occurs in the future for our Cloud platform, we will make sure to notify any active users. We plan to launch a status monitor for our services in 2022.

**Basic monitoring** can be done with a curl request + sendmail + cronjob as [seen in this blogpost](https://www.programcreek.com/2017/06/automatically-detect-server-downtime-using-linux-cron-job/) with the curl command below. Your personal API key can be found on [https://shuffler.io/settings](https://shuffler.io/settings) or in the same location (/settings) in your local instance.

```
curl https://shuffler.io/api/v1/getinfo -H "Authorization: Bearer apikey"
```

### Shuffle Server Healthcheck

There are multiple things to check in the Shuffle server to ensure that the health of server is in a good state:  

- Disk Space 
- Memory 
- Elasticsearch service state 

For this, the scripts have been prepared with the alerting mechanism which will check if everything is proper or not. 

### Disk Space Script 

This script will determine whether or not the disc space is more than 75% full. If so, an alert will be sent to your Webhook URL. Replace the script's <Webhook-URL> with your Webhook URL. 


```
#!/bin/sh
df -H | grep -vE '^Filesystem|tmpfs|cdrom' | awk '{ print $5 " " $1 }' | grep -v overlay | while read output;
do
  #echo $output
  usep=$(echo $output | awk '{ print $1}' | cut -d '%' -f1  )
  partition=$(echo $output | awk '{ print $2 }' )
  if [ $usep -ge 75 ]; then
    curl -X POST -H 'Content-type: application/json' --data '{"Alert":"Almost out of disk space","Server":"Local-Lab Shuffle Server"}' <Webhook-URL>
  fi
done
```

### Memory Check Script 

This script will determine whether or not the memory utilization is more than 70%. If so, an alert will be sent to your Webhook URL. Replace the script's <Webhook-URL> with your Webhook URL. 


```
#check server health
STATUS="$(curl http://172.17.14.102:3001/api/v1/_ah/health)"
if [ "${STATUS}" = "OK" ]; then
    :
else
    curl -X POST -H 'Content-type: application/json' --data '{"Alert":"There is a problem with this server(172.17.14.102), status is not OK"}' <Webhook-URL>
    exit 1
fi
```

### Elasticsearch Service Script 

This script will determine whether or not the Elasticsearch service is running or not. If not so, an alert will be sent to your Webhook URL. Replace the script’s <Elasticsearch-IP> with the Elasticsearch IP of your environment. Replace the script's <Webhook-URL> with your Webhook URL. 

```
#check server health
STATUS="$(curl <Elasticsearch-IP>)"
if [ "${STATUS}" = "OK" ]; then
    :
else
    curl -X POST -H 'Content-type: application/json' --data '{"Alert":"There is a problem with this server(172.17.14.102), status is not OK"}' <Webhook-URL>
    exit 1
fi
~
```

### Cron Jobs to automate the Process 

You can set a cron job to execute the scripts on every 15 minutes and the whole process can be automated. 

```
*/15 * * * * bash /root/diskspacecheck.sh
*/15 * * * * bash /root/healthchech.sh
*/15 * * * * bash /root/memorycheck.sh
```

### Using podman

Our main goal is to provide stable support for docker. But a lot of members from our community run podman (Especially because RHEL 8 uses it). We have tested Shuffle with podman and it works for most parts. While it's not our main focus, The way to run Shuffle with podman is nearly the same.

1. Make sure to remove the usage of double quotes from .env after you git clone Shuffle. This is because podman doesn't support double quotes in the .env file.

You can do it like this:



```
sed -E "s/(.*)=['\"]?([^'\"]*)['\"]?/\1=\2/" .env -i
```


2. Edit the existing docker-compose.yml to support podman by:

In shuffle-backend, comment back in the volume: /var/run/docker.sock:/var/run/docker.sock
And in environments, Comment back out:  # DOCKER_HOST=tcp://docker-socket-proxy:2375


So that the shuffle-backend service block ends up looking like this:



```yaml
  backend:
    image: ghcr.io/shuffle/shuffle-backend:latest
    container_name: shuffle-backend
    hostname: ${BACKEND_HOSTNAME}
    # Here for debugging:
    ports:
      - "${BACKEND_PORT}:5001"
    networks:
      - shuffle
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ${SHUFFLE_APP_HOTLOAD_LOCATION}:/shuffle-apps:z
      - ${SHUFFLE_FILE_LOCATION}:/shuffle-files:z
    env_file: .env
    environment:
      #- DOCKER_HOST=tcp://docker-socket-proxy:2375 # we commented this out
      - SHUFFLE_APP_HOTLOAD_FOLDER=/shuffle-apps
      - SHUFFLE_FILE_LOCATION=/shuffle-files
```



3. Run Shuffle with podman by:



```bash
sudo podman-compose -f docker-compose.yml pull
sudo podman-compose -f docker-compose.yml up
```
