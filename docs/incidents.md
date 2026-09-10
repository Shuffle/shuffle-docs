# Incidents in Shuffle Security

Documentation for managing incidents, alerts, cases, and automated response workflows in Shuffle Security.

## Table of contents
* [Why Shuffle Security?](#why-shuffle-security)
* [Ingest: Getting alerts into Shuffle](#ingest-getting-alerts-into-shuffle)
* [Schemaless ingest & translation to OCSF](#schemaless-ingest--translation-to-ocsf)
* ["Automation for Incidents"](#automation-for-incidents)
  * [Incident Automation Readiness](#4-incident-automation-readiness)
* [SOC use cases](#soc-use-cases)
* [Investigation workspace & tools](#investigation-workspace--tools)
  * [Tasks & Kanban board](#tasks--kanban-board)
  * [Observables & IOC management](#observables--ioc-management)
  * [Email threads & alert deduplication](#email-threads--alert-deduplication)
* [AI Agents in Incidents](#ai-agents-in-incidents)
* [Terminology & preferences](#terminology--preferences)
* [API & Datastore access](#api--datastore-access)

---

## Why Shuffle Security?

Shuffle is an open-source security orchestration, automation, and response (SOAR) platform. **Shuffle Security** ([shuffle.security](https://shuffle.security)) is our dedicated SecOps application built directly on top of Shuffle Core.

If you've ever worked in a Security Operations Center (SOC), you know how fragmented incident response can be: an alert fires in your SIEM or EDR, a webhook triggers an automation workflow, and then you have to flip over to Jira, TheHive, ServiceNow, or a heavy ticketing system just to track what's happening, assign tasks, or paste in indicators.

We built **Shuffle Security** because we wanted a dedicated, lightning-fast security operations workspace that lives directly alongside your automations. It gives you one place for triage, case management, observables, [Host Monitors](/docs/monitors), [Vulnerabilities](/docs/vulnerabilities), and automated response actions—without needing a separate database or extra external tooling.

> [!NOTE]
> **Available to Everyone — Zero License Paywalls**  
> Incident and case management is a native feature included for **everyone**—whether you use Shuffle Cloud or run self-hosted Shuffle Open Source via Docker Compose or Kubernetes.  
> There are no separate per-analyst licenses, no seat fees, and no ticket caps. It doesn't cost anything extra except standard **app runs** when your automations execute (e.g. ingesting alerts from a SIEM, running threat intelligence enrichment, or executing an endpoint isolation workflow). If an incident is handled manually or sits in your queue, it costs zero app runs.

### Seamlessly Engrained in Shuffle Core

Under the hood, all incidents, alerts, and cases are stored directly in **`shuffle-security_incidents`** inside Shuffle Core's Datastore (OpenSearch) formatted according to the **OCSF 2005 (Incident Finding)** specification. 

Because they share the exact same datastore as the rest of Shuffle:
- Workflows can directly read from, mutate, or create incidents using native Datastore nodes.
- AI Agents and Python apps have instant access to incident timelines, raw observables, and related cases without external database drivers.
- Self-hosted setups don't need to spin up a secondary database—your existing OpenSearch cluster handles everything.

If you are self-hosting on Docker or Kubernetes, see [Self-hosting Shuffle Security in Configuration](/docs/configuration#self-hosting-shuffle-security) and our [Architecture overview](/docs/architecture#server-vs-runtime) to see how the server components connect.

---

## Ingest: Getting alerts into Shuffle

The first step in any SOC workflow is getting alerts from your detection sources into your queue without friction. Shuffle supports both push (webhook) and pull (scheduled polling) ingestion:

<!-- component:ingest workflow="Ingest Tickets" category="cases" -->

### 1. Ingestion Webhooks (Instant Push)
Every organization in Shuffle Security gets a dedicated inbound webhook URL to receive push alerts from your detection stack (Splunk, Wazuh, Elastic, CrowdStrike, AWS GuardDuty, custom scripts).

> [!TIP]
> **Where is the Ingestion Webhook located in the UI?**  
> 1. Go to **`/incidents`** in Shuffle Security.  
> 2. Look at the top header bar directly above the incidents table: you'll see the **Ingest** pill row.  
> 3. Click the **"Webhook"** button next to "+".  
> 4. A modal opens showing your unique **Webhook URL** (`https://<instance>/api/v1/hooks/webhook_<org_id>_cases`), an enable/disable toggle switch, and a **"Copy Webhook URL"** button.  
> 5. You can copy this URL directly into your SIEM, EDR, or alert script. The modal also provides a sample `curl` command with authentication headers to test sending an alert.

<!-- TODO: Screenshot Needed: Ingestion Webhook Dialog
- Route / UI Location: /incidents -> Click "Webhook" button in the Ingest pill row above the table.
- What to capture: The open Webhook modal showing the organization webhook URL (webhook_<org_id>_cases), enable/disable toggle, "Copy Webhook URL" button, and sample curl command.
- Recommended filename: assets/incidents-webhook-modal.png
- Inject syntax: ![Ingestion Webhook Modal](https://raw.githubusercontent.com/Shuffle/Shuffle-docs/master/assets/incidents-webhook-modal.png)
-->

### 2. Polling Workflows (Scheduled Pull)
If your tools don't support webhooks or sit behind private network perimeters, you can use Shuffle's built-in **Ingest Tickets** workflow. It runs on a schedule (e.g. every 2 minutes), queries your alert source APIs (like Microsoft Defender, Email inboxes, or cloud SIEMs), and streams new detections directly into Incidents. You can click the **Sync Now** button in the Ingest pill row to immediately trigger polling.

### 3. The Incidents Dashboard (`/incidents`)
All ingested events land in the unified incident queue at `/incidents`:

<!-- component:incident-status title="Live Incident Queue & Health" subtitle="Real-time findings and queue telemetry from your active Shuffle incident pipeline." -->

The incident queue tracks events through standardized lifecycle stages:

| Status Stage | Meaning | Primary Owner | Expected Action |
| :--- | :--- | :--- | :--- |
| **New / Open** | Freshly ingested alert awaiting initial triage | Triage Analyst / Automation | Evaluate observables, execute enrichment, escalate or resolve. |
| **In Progress** | Active investigation underway | Assigned SOC Analyst | Inspect case canvas, correlate IOCs, trigger response playbooks. |
| **Under Review** | Containment executed, pending sign-off | Incident Lead / Team Lead | Verify eradication, confirm post-incident RCA. |
| **Resolved / Closed** | Threat neutralized or confirmed false positive | SOC Analyst | Archive case; feedback IOCs to detection rules. |

> [!TIP]
> **Querying Incidents via REST API / CLI**  
> You can programmatically query the incidents queue from any script or CI pipeline:  
> ```bash
> curl -s -X POST "https://<your-shuffle-instance>/api/v1/datastore/search" \
>   -H "Authorization: Bearer $SHUFFLE_API_KEY" \
>   -H "Content-Type: application/json" \
>   -d '{"category": "shuffle-security_incidents", "query": "*", "size": 10}' | jq .
> ```

- **Header Bar & Controls**:
  - **Ingest Row**: Contains the Webhook button, connected detection sources, and the `+` button to connect additional alert tools via the App Search Drawer.
  - **Search & Quick Filters**: Search incidents by keyword, title, or observable, or filter by status (`All`, `Open`, `In Progress`, `Under Review`, `Closed`) and severity.
- **Incident Table Columns**:
  - **Severity**: Color-coded badges (`Critical` red, `High` orange, `Medium` yellow, `Low` green, `Info` blue).
  - **Title & Incident ID**: Clear alert description and unique tracking ID.
  - **Status**: Current lifecycle stage pill.
  - **Assignee**: Assigned SOC analyst avatar or unassigned badge.
  - **Observables Count**: Badge showing the number of extracted IOCs (IPs, domains, hashes, CVEs).
  - **Created & Age**: Relative timestamp tracking time elapsed against your SLA.
- **Bulk Actions**: Select multiple incidents via row checkboxes to bulk-assign analysts, change statuses, or purge noise.
- **Case Canvas (`/incidents/:id`)**: Clicking any row navigates directly to the interactive investigation workspace.

<!-- TODO: Screenshot Needed: Incidents Dashboard Table
- Route / UI Location: /incidents
- What to capture: Full view of the /incidents dashboard with sample detections, showing the top Ingest pill row, search and status filter tabs (Open, In Progress), severity badges (Critical, High, Medium), assignee avatars, and observables count badges.
- Recommended filename: assets/incidents-dashboard-table.png
- Inject syntax: ![Incidents Dashboard Overview](https://raw.githubusercontent.com/Shuffle/Shuffle-docs/master/assets/incidents-dashboard-table.png)
-->

---

## Schemaless ingest & translation to OCSF

One of the biggest headaches in security engineering is schema rigidity. Every vendor formats alerts differently:
- Wazuh uses a nested JSON structure with `data.vulnerability`
- CrowdStrike passes `event.ComputerName` and `event.SHA256`
- AWS GuardDuty uses `detail.service.action`
- A custom internal webhook might just send `{ "host": "srv1", "ip": "10.0.0.5" }`

In traditional SOAR and SIEM tools, if an API changes a single field name or sends unexpected keys, the ingestion pipeline crashes or silently drops the alert.

### Schemaless by Design
Shuffle is **schemaless at ingest**. That means Shuffle accepts *any* valid JSON payload from any tool, sensor, or API without requiring you to pre-define table columns or schema mappings beforehand. Nothing is ever dropped due to schema validation errors.

### Dynamic Translation to OCSF
While schemaless ingestion gives you zero-friction data capture, analysts and playbooks still need predictable, standardized fields during investigation. Shuffle solves this by acting as a dynamic translation layer to **OCSF (Open Cybersecurity Schema Framework)**:

1. **Observable Extraction**: Shuffle inspects the schemaless payload and automatically extracts indicators of compromise (IOCs):
   - IP addresses (IPv4 & IPv6)
   - Hostnames and fully qualified domain names (FQDNs)
   - File hashes (MD5, SHA1, SHA256)
   - Email addresses and URLs
   - User identities and CVE identifiers
2. **Standardized Severity & Status**: Maps heterogeneous vendor levels into consistent OCSF severity ratings and investigation states.
3. **Preserving Raw Data Fidelity**: The original, un-modified raw alert is always preserved alongside the normalized finding. You get the convenience of standardized OCSF fields for playbooks and analytics, while retaining 100% forensic fidelity for deep investigations.
4. **Traffic Light Protocol (TLP)**: Observables automatically inherit or can be assigned TLP markings (`TLP:RED`, `TLP:AMBER`, `TLP:GREEN`, `TLP:CLEAR`) to control safe external threat intel sharing.

---

## "Automation for Incidents"

In Shuffle, Incidents and Automations are not two separate products tacked together—they share the exact same execution engine and Datastore:

```
┌──────────────────┐       Ingest Pipeline       ┌──────────────────┐
│  Alert Sources   │ ─────────────────────────▶ │ Shuffle Security │
│ (SIEM/EDR/Email) │                             │   (/incidents)   │
└──────────────────┘                             └────────┬─────────┘
                                                          │
                                         Click Playbook / │ Passes
                                         Status Changed   │ $incident
                                                          ▼
┌──────────────────┐      Update Tasks & Notes   ┌──────────────────┐
│ Containment &    │ ◀────────────────────────── │ Shuffle Workflow │
│ Remediation Apps │                             │ (Response Engine)│
└──────────────────┘                             └──────────────────┘
```

### 1. The `$incident` Context
When you trigger an automation from an incident (or when an incident status change triggers a workflow), Shuffle automatically injects the entire case context into the workflow execution as `$incident`.

Inside your workflow, you can reference:
- `$incident.title` — Title of the alert
- `$incident.severity` — Severity level (Critical, High, Medium, Low)
- `$incident.observables` — Array of extracted IOCs (IPs, hashes, domains)
- `$incident.description` — Incident summary or raw finding
- `$incident.id` — Unique identifier for callbacks

### 2. Bi-Directional Updates
Workflows don't just consume incident data; they report back into the incident in real time:
- Post timeline notes and analyst comments
- Add or check off Kanban tasks
- Attach sandbox analysis reports or memory dumps
- Update incident status or resolution reasons upon completion

### 3. Human-in-the-Loop Approvals
For high-impact response actions (such as taking a critical server offline or revoking domain admin credentials), Shuffle allows you to insert approval nodes. The workflow will pause, send an interactive approval request to Slack, Teams, or the incident workspace, and wait for an analyst's explicit confirmation before executing.

### 4. Incident Automation Readiness

Before handling production alerts, Shuffle Security evaluates whether your core incident automation pipeline is active. The **Automation Readiness** console inspects four foundational pillars required for automated SecOps triage and response:

<!-- component:automation-readiness category="cases" -->

| Readiness Pillar | Verification Check | Default Flow / Key | Purpose & Manual Configuration |
| :--- | :--- | :--- | :--- |
| **Ingestion Webhook** | Inbound webhook active | `webhook_<org_id>_cases` | Listens for inbound alert payloads from SIEM, EDR, or alert forwarders. Toggle at `/incidents` -> **Webhook** in the header. |
| **Threat Intel Enrichment** | Active workflow | `threat_intel_case_management_1` | Automatically enriches extracted observables (IPs, hashes, domains) against threat feeds. Activate in [`/usecases`](/usecases). |
| **Assign & Escalate** | Active workflow | `case_management_assign_escalate_1` | Routes newly ingested incidents to on-call analysts and escalates unhandled alerts on SLA breach. Activate in [`/usecases`](/usecases). |
| **Incident Configuration** | Datastore cache present | `shuffle-security_incidents_default` | Initializes standard IOC regex types, default threat feeds, and security routing rules. Seeded via `/preferences` -> **Incidents**. |

```
┌────────────────────────────────────────────────────────────────────────┐
│                     Incident Automation Readiness                      │
├────────────────────────┬───────────────────────────────────────────────┤
│ Ingestion Webhook      │ [Active]    api/v1/hooks/webhook_<org_id>_cases │
│ Threat Intel Enrich    │ [Active]    threat_intel_case_management_1    │
│ Assign & Escalate      │ [Active]    case_management_assign_escalate_1 │
│ Incident Configuration │ [Active]    shuffle-security_incidents_default│
└────────────────────────┴───────────────────────────────────────────────┘
```

> [!TIP]
> **Inspecting and Toggling Readiness in the UI**  
> 1. In the web application, this readiness card appears docked directly above the incident queue at **`/incidents`** and in the sidebar of **`/usecases`**.  
> 2. Clicking any row in the card opens the specific use case drawer to view the live workflow diagram, configured apps, and execution history without navigating away from your active page.  
> 3. Click **"Enable all"** on the card to activate all unconfigured checks in a single batch, or manage them individually via REST API:  
>    ```bash
>    # Trigger initial incident configuration seeding
>    curl -s -X POST "https://<your-shuffle-instance>/api/v1/usecases/setup_defaults" \
>      -H "Authorization: Bearer $SHUFFLE_API_KEY" \
>      -H "Content-Type: application/json" \
>      -d '{"category": "cases"}' | jq .
>    ```

<!-- TODO: Screenshot Needed: Incident Automation Readiness Card
- Route / UI Location: /incidents -> Top of queue or below KPI summary
- What to capture: The Automation Readiness card showing all 4 green check status rows (Ingestion Webhook, Threat Intel Enrichment, Assign & Escalate, Incident Configuration) and the "Enable all" button.
- Recommended filename: assets/incidents-automation-readiness.png
- Inject syntax: ![Incident Automation Readiness Card](https://raw.githubusercontent.com/Shuffle/Shuffle-docs/master/assets/incidents-automation-readiness.png)
-->

---

## SOC use cases

Shuffle Security comes with pre-built flows and templates designed for real SOC operational scenarios:

<!-- component:usecases category="cases" -->

Here are a few common patterns:

### 1. Phishing Triage & Auto-Purge
- **Ingest**: Ingest reported emails via Microsoft 365 or Google Workspace.
- **Analysis**: Parse `.eml` and `.msg` headers, evaluate SPF/DKIM/DMARC alignment, sandbox URLs with urlscan.io, and check attachments against VirusTotal.
- **Deduplication**: If 50 employees report the same phishing blast, Shuffle groups them into a single parent incident.
- **Response**: With one click, search and purge the malicious email from all mailboxes across the entire tenant.

### 2. EDR Detection & Endpoint Containment
- **Ingest**: Ingest suspicious process execution alerts from CrowdStrike, SentinelOne, or Wazuh.
- **Triage**: Extract executable hashes and C2 network connections.
- **Action**: Analysts click **"Isolate Host"** from the Response Actions panel. The workflow triggers the EDR API to sever network connectivity while keeping the management channel alive for live response.

### 3. Cloud Identity Abuse & Impossible Travel
- **Ingest**: Okta or Azure AD logs an impossible travel anomaly or multiple failed MFA attempts.
- **Verification**: Shuffle automatically pings the user via Slack or Microsoft Teams asking: *"Did you just attempt to log in from Berlin?"*
- **Containment**: If the user responds *"No"*, the workflow instantly revokes active OAuth tokens, resets user sessions, and assigns an urgent review task to the SOC team.

### 4. Automated IOC Threat Hunting
- **Ingest**: Detect a compromised internal host communicating with an unknown external IP.
- **Enrichment**: Query AbuseIPDB, AlienVault OTX, and your internal MISP instance.
- **Block**: Push the confirmed malicious IP directly to your perimeter firewalls (Palo Alto Networks, Fortinet, Cloudflare) via an automated blocklist workflow.

Explore and activate all available flow templates at [`/usecases`](/usecases).

---

## Investigation workspace & tools

Clicking into an incident opens the interactive investigation canvas:

<!-- TODO: Screenshot Needed: Incident Investigation Workspace Canvas
- Route / UI Location: /incidents/:id (click any incident from the table)
- What to capture: The interactive investigation canvas showing the header (title, severity, status dropdown, assignee), the Kanban task board lanes, and case timeline.
- Recommended filename: assets/incidents-investigation-workspace.png
- Inject syntax: ![Incident Investigation Canvas](https://raw.githubusercontent.com/Shuffle/Shuffle-docs/master/assets/incidents-investigation-workspace.png)
-->

### Tasks & Kanban board
Coordinate multi-step investigations without losing track of progress:
- **Kanban Lanes**: Drag and drop tasks between **To Do**, **In Progress**, and **Done** (or configure custom status lanes in `/preferences`).
- **Checklists**: Break response plans into discrete steps (e.g. *"Isolate endpoint"*, *"Dump LSASS memory"*, *"Revoke Kerberos ticket"*).
- **Automated Tasks**: Attach a workflow directly to a task card so an analyst can execute it with a single click.

### Observables & IOC management
- **Central Repository**: Search and filter all organization-wide observables centrally at `/incidents/observables`.
- **Threat Intelligence Feeds**: Integrated with threat feeds at `/incidents/threat-feeds` to automatically cross-reference indicators with VirusTotal, AbuseIPDB, AlienVault OTX, and MISP. When an IP, domain, or file hash is extracted from an alert, Shuffle queries your configured threat feeds in real time to calculate reputation scores and populate threat context directly on the incident canvas.
- **CVE Correlation**: CVE identifiers extracted from alerts are cross-referenced with your [Vulnerabilities](/docs/vulnerabilities) backlog and real-world exploitation signals (EPSS and CISA KEV).
- **TLP Controls**: Assign Traffic Light Protocol levels (`TLP:RED`, `TLP:AMBER`, `TLP:GREEN`, `TLP:CLEAR`) to prevent sensitive internal observables from leaking to external lookup services.

<!-- TODO: Screenshot Needed: Observables & Threat Intel Enrichment
- Route / UI Location: /incidents/:id -> Observables tab (or /incidents/observables)
- What to capture: Observables list showing IOC types (IP, domain, hash), reputation score badges (VirusTotal / AbuseIPDB), TLP tags, and the one-click response action button.
- Recommended filename: assets/incidents-observables-enrichment.png
- Inject syntax: ![Observables & Threat Intel Correlation](https://raw.githubusercontent.com/Shuffle/Shuffle-docs/master/assets/incidents-observables-enrichment.png)
-->

### Email threads & alert deduplication
- **Conversation Threading**: Groups related emails and alert floods into clean conversation threads based on Message-IDs and subjects.
- **Anti-Fatigue Deduplication**: Prevents alert storms from cluttering your queue by clustering identical alerts into one actionable investigation.

---

## AI Agents in Incidents

Shuffle Security includes deep integration with **Shuffle AI** and the autonomous agent loop via the `shuffle_incidents` MCP tool:

<!-- component:ask-ai label="Ask AI about Incidents" input="Analyze this incident and suggest an automated containment plan" -->

- **Context-Aware Assistant**: Clicking **"Ask about this Incident"** opens the AI panel with the current incident's title, severity, timeline, email threads, and observables pre-loaded into the prompt context.
- **Automated IOC Triage**: Instruct the agent to *"Check these three IPs against threat intel and summarize the findings."*
- **Executive Summaries**: Generate executive incident summaries and Post-Incident Reviews (PIR) in Markdown with one click.
- **Containment Recommendations**: Ask the agent to draft a response plan. It evaluates the indicators, drafts actions, and can trigger the corresponding playbooks upon your approval.

---

## Terminology & preferences

Every security team uses different lingo. Some teams work with **Alerts**, some work with **Incidents**, MSSPs often prefer **Tickets** or **Cases**, and DevOps teams might say **Jobs**.

Instead of forcing you into our definitions, you can change the name of everything in the platform with a single toggle!

Head to **`/preferences`** (or click your organization settings) to pick your preferred entity terminology:

| Terminology | Singular | Plural | Route | Best for |
| :--- | :--- | :--- | :--- | :--- |
| **Incidents** *(default)* | Incident | Incidents | `/incidents` | SOC incident triage and multi-step investigation. |
| **Alerts** | Alert | Alerts | `/alerts` | High-volume detection pipelines and noise reduction. |
| **Cases** | Case | Cases | `/cases` | Formal case management and digital forensics. |
| **Tickets** | Ticket | Tickets | `/tickets` | Helpdesk, IT, or MSSP customer ticketing. |
| **Jobs** | Job | Jobs | `/jobs` | Scheduled batch tasks and operations. |

When you change this setting, all navigation bars, page titles, buttons, and even AI prompts automatically update to match your chosen wording.

---

## API & Datastore access

Under the hood, incidents are stored directly in Shuffle Core's Datastore (OpenSearch) under the **`shuffle-security_incidents`** category formatted according to OCSF 2005. This means you have full programmatic control via the Shuffle REST API or from custom Python apps:

### REST API Endpoints

- **List Incidents from Datastore**: `GET /api/v1/orgs/{org_id}/list_cache?category=shuffle-security_incidents&top=100`
- **Filter by Status & Severity**: `GET /api/v1/incidents?status=open&severity=high`
- **Get Incident Details**: `GET /api/v1/incidents/{id}` (or `GET /api/v1/orgs/{org_id}/get_cache?category=shuffle-security_incidents&key={id}`)
- **Create an Incident**: `POST /api/v1/incidents` (or `POST /api/v2/incidents`)
- **Add a Task**: `POST /api/v1/incidents/{id}/tasks`
- **Attach Observables**: `POST /api/v1/incidents/{id}/observables`
- **Trigger a Response Action**: `POST /api/v1/incidents/{id}/actions/{action_id}`

### In Custom Python Apps & Workflows

In custom Shuffle Python apps and automation nodes, you can query, enrich, or resolve incidents directly using the datastore cache helpers:

```python
# Query an incident by key from the OCSF incident datastore
incident = self.get_cache("incident_id_123", category="shuffle-security_incidents")

# Inspect observables
if incident and len(incident.get("observables", [])) > 0:
    for obs in incident["observables"]:
        print(f"Extracted {obs.get('type')}: {obs.get('value')}")

# Update or save the enriched incident record
self.set_cache("incident_id_123", incident, category="shuffle-security_incidents")
```

For more details on backend API endpoints and authentication, check out our [API documentation](/docs/API).
