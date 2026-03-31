# Getting Started with Shuffle
Welcome to the Shuffle documentation! This guide will help you get up and running with Shuffle quickly and effectively.


## Table of contents
* [Introduction](#introduction)
* [Usage Models](#usage_models)
* [First workflow](#first_workflow)
* [Shuffle 101](#shuffle_101)
* [Shuffle Videos](#shuffle_videos)
* [Community Videos](#community_videos)
* [Learn about Shuffle](#learn_about_shuffle)
* [Environment Variables](#environment-variables-env)

## Overview
Shuffle is an open-source automation platform designed specifically for the security industry. You can start using it for free with the following options:

- [Open Source (On-Premises)](https://github.com/shuffle/shuffle/blob/main/.github/install-guide.md)  
  Download and install Shuffle in your infrastructure.

- [Cloud Signup (SaaS)](https://shuffler.io/register)  
  Sign up for Shuffle's cloud-based service and get started quickly. Allows for Multi-Tenant and  
  [stores data in a location near you](https://shuffler.io/legal/privacy_policy#data-location).

- [Hybrid Cloud](https://shuffler.io)  
  Use Local Shuffle Agents connected to your Shuffle Cloud Organizations.


**Need help? Check out these resources:**
- **[Training](https://shuffler.io/training)**  
  Access training resources to get up to speed with Shuffle.
- **[Old Training Videos](https://drive.google.com/drive/folders/1MtVfkCXDMSZ9yBwLDiVb0lj1H-oAK5RZ?usp=sharing)**  
  In case you would like to watch older on-demand training videos. The platform however has significantly improved since then and the [current training](https://shuffler.io/training) would be a better match.

## Workflow Development
Workflows run the automated processes in Shuffle by connecting Triggers and Actions/APIs. 

If you want some practice, check out our [default intro to Workflow development](https://github.com/Shuffle/shuffle-docs/blob/master/handbook/engineering/workflow_development.md)

### Finding Usecases
[Usecases are auto-generated workflows](/usecases) that perform a task together. This can be things like handling EDR alerts, doing phishing analysis or using detection rules with Sigma with your SIEM. 

### Finding Workflows
[Workflows](/docs/workflows) connect [Apps](/docs/apps) together to perform an action, typically getting and setting data with API's and using Shuffle's built in tools like Shuffle Tools to modify or format the data. They can be ran and stopped according to your needs, and typically have one starting point and multiple outputs. 

### Finding Apps
[Apps](/docs/apps) are API's or Python scripts, and can be [modified and built by anyone](https://shuffler.io/docs/app_creation). To use an existing public app in a Workflow, you must first activate it. Public apps can be forked, meaning you can have your own version of them.

### Introduction Blogposts
* [1. Introducing Shuffle - an Open Source SOAR platform](https://medium.com/security-operation-capybara/introducing-shuffle-an-open-source-soar-platform-part-1-58a529de7d12)
* [2. Getting started with Shuffle](https://medium.com/@Frikkylikeme/getting-started-with-shuffle-an-open-source-soar-platform-part-2-1d7c67a64244)
* [3. Creating your first app - Virustotal and TheHive](https://medium.com/@Frikkylikeme/integrating-shuffle-with-virustotal-and-thehive-open-source-soar-part-3-8e2e0d3396a9)
* [4. On webhooks and loops - TheHive, Cortex and MISP](https://medium.com/swlh/indicators-and-webhooks-with-thehive-cortex-and-misp-open-source-soar-part-4-f70cde942e59)
* [5. Deploying Shuffle :)](https://medium.com/@stasis_/soar-deploying-shuffle-ad26173525d2)
* [6. Automation with Shuffle SOAR](https://medium.com/@Romser/final-part-configuring-shuffle-soar-28e3674ede22)
* [7. Simplify Your SOAR Implementation with Shuffle](https://medium.com/@socfortress/simplify-your-soar-implementation-with-shuffle-and-seim-integration-d1d32728515e)

### Workflow Principles
1. Variables & nodes
2. JSON autocompletion
3. Loops
4. Nestedloops
5. [Start nodes](https://shuffler.io/workflows/0285a05e-8dc0-4614-840b-88606d6a1e59)
6. Triggers
7. Subflows
8. [App Authentication](https://shuffler.io/workflows/d65d228a-f406-4227-9fa7-f7d9303f8411)
9. Loop filtering
10. [Shuffle File storage](https://shuffler.io/workflows/dd5e3800-2f2e-4089-8055-b500e3b8b349)
11. [Shuffle Datastore (Cache)](https://shuffler.io/workflows/f39a3c37-4f38-4ca0-952a-a9425080b44e)
12. Deduplication
13. [Liquid formatting](https://shuffler.io/workflows/0d604c52-1b3f-49d8-a57e-480baf07ab8d)
14. [HTTP & Rest APIs](https://shuffler.io/workflows/b8a3a70a-f3f9-459f-99b3-7a2723a1a4b8)

### Shuffle 101
- [Learning Startnodes](https://shuffler.io/workflows/0285a05e-8dc0-4614-840b-88606d6a1e59?queryID=5775af43ac103d34ff77f11d27ea5bed)
- [Learning the HTTP app](https://shuffler.io/workflows/b8a3a70a-f3f9-459f-99b3-7a2723a1a4b8?queryID=5775af43ac103d34ff77f11d27ea5bed)
- [Cache Tutorial](https://shuffler.io/workflows/f39a3c37-4f38-4ca0-952a-a9425080b44e?queryID=5775af43ac103d34ff77f11d27ea5bed)
- [File Tutorial](https://shuffler.io/workflows/dd5e3800-2f2e-4089-8055-b500e3b8b349?queryID=5775af43ac103d34ff77f11d27ea5bed)
- [App Authentication](https://shuffler.io/workflows/d65d228a-f406-4227-9fa7-f7d9303f8411?queryID=5775af43ac103d34ff77f11d27ea5bed)
- [Learning Liquid Formatting](https://shuffler.io/workflows/0d604c52-1b3f-49d8-a57e-480baf07ab8d?queryID=5775af43ac103d34ff77f11d27ea5bed)
- [JSON within Shuffle](https://shuffler.io/workflows/ee334515-0224-4a09-af8c-ebc60886f154?queryID=7571057f529c8a4a9aabd5800c0d2b29)

### Shuffle YouTube Videos
**Learn about Shuffle - in-depth**  
Here's a training session we did on Shuffle.

- **00:00 - 00:30**: Introduction to Shuffle and what we're building
- **00:30 - 02:00**: Feature walkthrough of organizations, app creator, and workflows
- **02:00 - end**: Real-time demo, creating use-cases for attendees

[![Shuffle the SOC walkthrough](https://img.youtube.com/vi/PNuXCixYwDc/0.jpg)](https://www.youtube.com/watch?v=PNuXCixYwDc)

## Community Videos

### 1. Understanding Shuffle
Our friends at [OpenSecure](https://www.youtube.com/watch?v=_riaZjLnoXo&t=317s) have created excellent videos to help you learn about Shuffle. Be sure to check them out!

### 2. What is SOAR?
Learn the basics of SOAR (Security Orchestration, Automation, and Response) and how Shuffle fits into this ecosystem.  
**Watch now:** [Shuffle Getting Started - Understanding Shuffle](https://www.youtube.com/watch?v=_riaZjLnoXo)

### 3. Installing Shuffle
Ready to install Shuffle? Follow this step-by-step guide to get Shuffle up and running quickly.  
**Watch now:** [How to Install Shuffle](https://www.youtube.com/watch?v=YDUKZojg0vk)

## Environment Variables (.env)

The root `.env` file configures how Shuffle starts, connects services, and executes workflows. Use the table below as a reference for each variable.

> Recommended: replace all default passwords and set `SHUFFLE_ENCRYPTION_MODIFIER` before production use.

### Core and bootstrap

| Variable | Default | Description |
| --- | --- | --- |
| `ENVIRONMENT_NAME` | `Shuffle` | Name of the execution environment used by workers. |
| `LIQUID_SANITIZE_INPUT` | `true` | Sanitizes Liquid template input to reduce unsafe input handling. |
| `SHUFFLE_DOWNLOAD_WORKFLOW_LOCATION` | `` | Remote repository URL/location for downloading workflows on first load. |
| `SHUFFLE_DOWNLOAD_WORKFLOW_USERNAME` | `` | Username for workflow repository authentication. |
| `SHUFFLE_DOWNLOAD_WORKFLOW_PASSWORD` | `` | Password/token for workflow repository authentication. |
| `SHUFFLE_DOWNLOAD_WORKFLOW_BRANCH` | `` | Branch to pull workflows from during bootstrap. |
| `SHUFFLE_APP_DOWNLOAD_LOCATION` | `https://github.com/shuffle/python-apps` | Repository location used to download apps. |
| `SHUFFLE_DOWNLOAD_AUTH_USERNAME` | `` | Username for app repository authentication. |
| `SHUFFLE_DOWNLOAD_AUTH_PASSWORD` | `` | Password/token for app repository authentication. |
| `SHUFFLE_DOWNLOAD_AUTH_BRANCH` | `` | Branch to pull apps from. |
| `SHUFFLE_APP_FORCE_UPDATE` | `false` | Forces app updates even when apps already exist locally. |
| `SHUFFLE_DEFAULT_USERNAME` | `` | Default admin username created on first startup (min length 3). |
| `SHUFFLE_DEFAULT_PASSWORD` | `` | Default admin password created on first startup (min length 3). |
| `SHUFFLE_DEFAULT_APIKEY` | `` | Optional default API key for initial user bootstrap. |

### Local paths and encryption

| Variable | Default | Description |
| --- | --- | --- |
| `SHUFFLE_APP_HOTLOAD_FOLDER` | `./shuffle-apps` | Local app folder used for hotloading apps. |
| `SHUFFLE_APP_HOTLOAD_LOCATION` | `./shuffle-apps` | Local app location used by Shuffle for loading/saving apps. |
| `SHUFFLE_FILE_LOCATION` | `./shuffle-files` | Base path for Shuffle file storage. |
| `SHUFFLE_ENCRYPTION_MODIFIER` | `` | Required secret used in authentication encryption. Changing/loss requires reauth for apps. |

### Backend/frontend and network

| Variable | Default | Description |
| --- | --- | --- |
| `BASE_URL` | `http://shuffle-backend:5001` | Internal backend base URL used by services. |
| `SSO_REDIRECT_URL` | `http://localhost:3001` | Redirect URL used in SSO flows. |
| `BACKEND_HOSTNAME` | `shuffle-backend` | Backend hostname for service communication. |
| `BACKEND_PORT` | `5001` | Backend service port. |
| `FRONTEND_PORT` | `3001` | Frontend HTTP port. |
| `FRONTEND_PORT_HTTPS` | `3443` | Frontend HTTPS port. |
| `AUTH_FOR_ORBORUS` | `` | Optional auth value used by Orborus when talking to backend. |
| `OUTER_HOSTNAME` | `shuffle-backend` | Public/outer hostname used for local execution callbacks and service routing. |
| `DB_LOCATION` | `./shuffle-database` | Local database/emulator storage location. |
| `DOCKER_API_VERSION` | `1.40` | Docker API version used by Shuffle components. |

### Proxy, timezone, and runtime mode

| Variable | Default | Description |
| --- | --- | --- |
| `HTTP_PROXY` | `` | Outbound HTTP proxy for Orborus/worker/app traffic. |
| `HTTPS_PROXY` | `` | Outbound HTTPS proxy for Orborus/worker/app traffic. |
| `SHUFFLE_PASS_WORKER_PROXY` | `TRUE` | Passes proxy environment variables into workers. |
| `SHUFFLE_PASS_APP_PROXY` | `TRUE` | Passes proxy environment variables into app containers. |
| `SHUFFLE_INTERNAL_HTTP_PROXY` | `noproxy` | Internal HTTP proxy override for Shuffle internal communication. |
| `SHUFFLE_INTERNAL_HTTPS_PROXY` | `noproxy` | Internal HTTPS proxy override for Shuffle internal communication. |
| `TZ` | `Europe/Amsterdam` | Timezone used by Orborus, workers, and apps. |
| `ORBORUS_CONTAINER_NAME` | `` | Explicit Orborus container name (used for container detection, including cgroup v2 cases). |
| `SHUFFLE_ORBORUS_STARTUP_DELAY` | `` | Startup delay before Orborus begins processing. |
| `SHUFFLE_SKIPSSL_VERIFY` | `true` | Disables SSL verification for configured Shuffle calls. |
| `IS_KUBERNETES` | `false` | Enables Kubernetes runtime mode when set to true. |

### Image and deployment behavior

| Variable | Default | Description |
| --- | --- | --- |
| `SHUFFLE_BASE_IMAGE_REPOSITORY` | `frikky` | Docker image repository namespace used for base images. |
| `SHUFFLE_USE_GCHR_OVERRIDE_FOR_AUTODEPLOY` | `true` | Uses GHCR override behavior for autodeploy to avoid re-updating core apps (HTTP, subflow, tools). |

Optional variables (commented by default in `.env`):

| Variable | Default | Description |
| --- | --- | --- |
| `SHUFFLE_BASE_IMAGE_NAME` | `shuffle` | Base image name override. |
| `SHUFFLE_BASE_IMAGE_REGISTRY` | `ghcr.io` | Base image registry override. |
| `SHUFFLE_BASE_IMAGE_TAG_SUFFIX` | `"-1.4.0"` | Optional suffix appended to base image tag. |

### Orborus execution and scaling

| Variable | Default | Description |
| --- | --- | --- |
| `SHUFFLE_SWARM_BRIDGE_DEFAULT_INTERFACE` | `eth0` | Interface used to resolve container IP in Docker/swarm networking. |
| `SHUFFLE_SWARM_BRIDGE_DEFAULT_MTU` | `1500` | MTU used for bridge networking assumptions. |
| `SHUFFLE_MEMCACHED` | `` | Optional memcached endpoint/configuration for caching. |
| `SHUFFLE_CONTAINER_AUTO_CLEANUP` | `true` | Automatically removes execution containers after runs. |
| `SHUFFLE_ORBORUS_EXECUTION_CONCURRENCY` | `5` | Soft limit for concurrent executions handled by Orborus. |
| `SHUFFLE_HEALTHCHECK_DISABLED` | `false` | Disables healthcheck endpoints/processes when true. |
| `SHUFFLE_ELASTIC` | `true` | Enables elastic/OpenSearch-related logging/index behavior. |
| `SHUFFLE_LOGS_DISABLED` | `true` | Disables log collection/storage when true. |
| `SHUFFLE_CHAT_DISABLED` | `false` | Disables chat features when true. |
| `SHUFFLE_DISABLE_RERUN_AND_ABORT` | `false` | Disables rerun and abort controls for executions when true. |
| `SHUFFLE_RERUN_SCHEDULE` | `300` | Interval/schedule used for rerun handling. |
| `SHUFFLE_WORKER_SERVER_URL` | `` | Explicit backend URL for workers if autodetection points to wrong server. |
| `SHUFFLE_ORBORUS_PULL_TIME` | `` | Poll/pull interval for Orborus execution queue handling. |
| `SHUFFLE_MAX_EXECUTION_DEPTH` | `` | Maximum recursion depth for subflow execution. |
| `SHUFFLE_APP_REPLICAS` | `3` | Number of app replicas to run. |

### Datastore and search

| Variable | Default | Description |
| --- | --- | --- |
| `DATASTORE_EMULATOR_HOST` | `shuffle-database:8000` | Datastore emulator host used by Shuffle backend. |
| `SHUFFLE_OPENSEARCH_URL` | `https://shuffle-opensearch:9200` | OpenSearch endpoint URL. |
| `SHUFFLE_OPENSEARCH_CERTIFICATE_FILE` | `` | Path to custom OpenSearch certificate file. |
| `SHUFFLE_OPENSEARCH_APIKEY` | `` | API key for OpenSearch authentication. |
| `SHUFFLE_OPENSEARCH_CLOUDID` | `` | OpenSearch Cloud ID for managed deployments. |
| `SHUFFLE_OPENSEARCH_PROXY` | `` | Proxy value used for OpenSearch traffic. |
| `SHUFFLE_OPENSEARCH_INDEX_PREFIX` | `` | Prefix added to generated OpenSearch index names. |
| `SHUFFLE_OPENSEARCH_SKIPSSL_VERIFY` | `true` | Skips SSL verification for OpenSearch connections. |
| `SHUFFLE_OPENSEARCH_USERNAME` | `"admin"` | Username for OpenSearch auth. |
| `SHUFFLE_OPENSEARCH_PASSWORD` | `"StrongShufflePassword321!"` | OpenSearch password used by Shuffle backend and first-time setup. |
| `OPENSEARCH_INITIAL_ADMIN_PASSWORD` | `"StrongShufflePassword321!"` | Initial OpenSearch admin password used during first-time OpenSearch setup. |

### Other runtime settings

| Variable | Default | Description |
| --- | --- | --- |
| `SHUFFLE_TENZIR_URL` | `` | Endpoint for Tenzir integration. |
| `SHUFFLE_PROTECTED_CLEANUP_DISABLED` | `true` | Disables protected cleanup safeguards when true. |
| `DEBUG_MODE` | `false` | Enables debug mode and verbose behavior when true. |
