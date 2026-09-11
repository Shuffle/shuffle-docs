# Incidents in Shuffle Security

Documentation for managing incidents, alerts, cases, observables, and automated response workflows in Shuffle Security.

## Table of contents
* [Overview](#overview)
* [Datastore architecture & OCSF schema](#datastore-architecture--ocsf-schema)
* [Ingest: Getting alerts into Shuffle](#ingest-getting-alerts-into-shuffle)
* [Schemaless ingest & observable extraction](#schemaless-ingest--observable-extraction)
* [Automation for Incidents](#automation-for-incidents)
* [Incident Automation Readiness](#incident-automation-readiness)
* [SOC use cases](#soc-use-cases)
* [Investigation workspace & tools](#investigation-workspace--tools)
* [AI Agents in Incidents](#ai-agents-in-incidents)
* [Terminology & preferences](#terminology--preferences)
* [API & Datastore reference](#api--datastore-reference)

---

## Overview

Shuffle Security ([shuffle.security/incidents](https://shuffle.security/incidents)) provides an incident response and alert management workspace connected directly to Shuffle Core automations.

Instead of managing alerts in a separate ticketing system disconnected from your execution engine, Shuffle Security keeps investigations, tasks, observables, host telemetry, and automated playbooks in one unified environment.

> [!NOTE]
> **Zero License Paywalls**  
> Incident and case management is included in both Shuffle Cloud and self-hosted open-source instances. There are no per-seat licenses, analyst fees, or ticket caps. Standard app runs execute only when automation workflows run. Manual incident handling, triage, and queue management consume zero app runs.

---

## Datastore architecture & OCSF schema

All incidents, alerts, and cases are stored directly in Shuffle's Datastore under the **`shuffle-security_incidents`** category formatted according to the **OCSF 2005 (Incident Finding)** specification.

<!-- component:datastore category="shuffle-security_incidents" -->

<!-- component:datastore-link category="shuffle-security_incidents" -->

Inspect and query raw incident records directly:
- Shuffle Security Datastore: Navigate to [`/admin/datastore?category=shuffle-security_incidents`](/admin/datastore?category=shuffle-security_incidents) in Shuffle Security. If local datastore exists, it loads locally; otherwise, it automatically redirects to Shuffle Core.
- Shuffle Core Datastore: [Open in Shuffle Core Datastore](https://shuffler.io/admin?tab=datastore&category=shuffle-security_incidents) (`https://shuffler.io/admin?tab=datastore&category=shuffle-security_incidents` or `/admin?tab=datastore&category=shuffle-security_incidents` on self-hosted Core).
- Manual UI Navigation: Go to **Admin** -> **Datastore** -> select category **`shuffle-security_incidents`**.

### How Data is Added (OCSF 2005 Structure)

When a detection workflow, ingestion webhook, or custom script records an incident into `shuffle-security_incidents`, it populates an OCSF 2005 JSON payload:

| Field | Type | Description | Sample Value |
| :--- | :--- | :--- | :--- |
| `class_uid` | Integer | OCSF Class Identifier | `2005` (Incident Finding) |
| `category_uid` | Integer | OCSF Category Identifier | `2` (Findings) |
| `activity_id` | Integer | Action Identifier | `1` (Create) |
| `severity_id` | Integer | Severity Scale (1 to 5) | `4` (High) |
| `finding_info` | Object | Finding Title, Description, and Timestamps | `{"title": "Phishing detection with credential harvester URL"}` |
| `observables` | Array | Indicators (IP, hash, process, domain, user) | `[{"name": "process.name", "value": "mimikatz.exe"}]` |

```python
# Write incident finding directly from Python worker or app
self.set_cache(
    key="incident_2026_0942",
    value={
        "class_uid": 2005,
        "class_name": "Incident Finding",
        "activity_id": 1,
        "severity_id": 4,
        "severity": "High",
        "finding_info": {
            "title": "Phishing detection with credential harvester URL",
            "desc": "Inbound email flagged with credential harvesting link.",
            "created_time": 1773291000,
        },
        "observables": [
            {"name": "url.domain", "type": "domain", "value": "login-verify-account-update.xyz"},
            {"name": "email.sender", "type": "email", "value": "security-alert@external-notice.com"},
        ],
    },
    category="shuffle-security_incidents",
)
```

Because incidents live in the native datastore:
- Workflows read, update, or create incidents using standard datastore actions.
- AI Agents and custom Python scripts interact with incident timelines, observables, and tasks directly without external database drivers.
- Self-hosted deployments require no secondary database.

---

## Ingest: Getting alerts into Shuffle

<!-- component:ingest workflow="Ingest Tickets" category="cases" -->

### 1. Ingestion Webhook (Push)
Every organization gets a dedicated inbound webhook to receive alerts from detection systems (Splunk, Wazuh, Elastic, CrowdStrike, AWS GuardDuty, custom scripts):
- Navigate to **`/incidents`** in Shuffle Security.
- In the top header bar, click the **"Webhook"** button in the Ingest row.
- The modal displays your dynamic inbound endpoint:
  ```
  https://<instance>/api/v1/hooks/webhook_<hook_id>
  ```
- Send JSON payloads to this webhook to trigger alert normalization and incident creation.

### 2. Polling Workflows (Scheduled Pull)
For alert sources that do not push webhooks or reside behind firewalls, use scheduled workflows (such as the default `Ingest Tickets` flow). These workflows query external APIs on a regular cadence and write findings into `shuffle-security_incidents`. Click **"Sync Now"** in the Ingest row to trigger an immediate pull.

### 3. The Incidents Dashboard (`/incidents`)

<!-- component:incident-dashboard -->

Incidents progress through standardized lifecycle states:

| Status Stage | Meaning | Typical Handling |
| :--- | :--- | :--- |
| **New / Open** | Ingested alert awaiting triage | Evaluate observables, run automated enrichment, escalate or close. |
| **In Progress** | Active investigation | Inspect canvas, review observables, execute response playbooks. |
| **Under Review** | Containment executed | Verify remediation and post-incident documentation. |
| **Resolved / Closed** | Threat neutralized or confirmed false positive | Archive case; update detection rules if necessary. |

- **Filters & Search**: Filter by status (`All`, `Open`, `In Progress`, `Under Review`, `Closed`), severity, or search by keyword and observable value.
- **Table Columns**: Severity, Title & ID, Status, Assignee, Observables count, and Created timestamp.
- **Bulk Actions**: Select multiple incidents to reassign, change status, or purge false positives.

<!-- TODO: Screenshot Needed: Incidents Dashboard Table
- Route / UI Location: /incidents
- What to capture: Full view of the /incidents dashboard showing Ingest row, search bar, status filter tabs, and incident rows.
- Target path: assets/incidents-dashboard-table.png -->

---

## Schemaless ingest & observable extraction

Detection tools output vastly different payload formats (e.g. Wazuh nested JSON, CrowdStrike event schemas, GuardDuty actions).

### Schemaless Ingestion
Shuffle is schemaless at ingest. Payloads are accepted without pre-defined schema mappings, and the original raw alert is preserved alongside the normalized incident record for complete forensic fidelity.

### Observable Extraction & OCSF Mapping
During ingestion, Shuffle parses payloads to extract common indicators of compromise:
- IPv4 and IPv6 addresses
- Hostnames and fully qualified domain names
- File hashes (MD5, SHA1, SHA256)
- Email addresses and URLs
- User accounts and CVE identifiers

Extracted indicators populate the incident's observables list and can be tagged with Traffic Light Protocol levels (`TLP:RED`, `TLP:AMBER`, `TLP:GREEN`, `TLP:CLEAR`).

---

## Automation for Incidents

<!-- component:automation-for-incidents category="incidents" -->

Use the interactive rocket button above, or navigate to **/incidents** and click the **Automation for Incidents** (rocket) button in the header bar to configure triggers, AI agents, and response workflows for your tenant.

Incidents and workflows share the same execution engine:

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

### The `$incident` Context
When an incident triggers a workflow, Shuffle passes the incident context as `$incident`:
- `$incident.title` — Alert title
- `$incident.severity` — Severity level (Critical, High, Medium, Low, Info)
- `$incident.observables` — Array of extracted IOCs
- `$incident.description` — Incident description or summary
- `$incident.id` — Unique incident identifier

Workflows can update the incident by appending timeline notes, modifying tasks, or updating the incident status in the datastore.

---

## Incident Automation Readiness

Shuffle Security verifies whether foundational incident response workflows are configured:

<!-- component:automation-readiness category="cases" -->

| Readiness Pillar | Verification Check | Target Flow / Key | Purpose & Configuration |
| :--- | :--- | :--- | :--- |
| **Ingestion** | Inbound webhook trigger running | `Ingestion Webhook` (`webhook_<trigger_id>`) | Pushes alerts directly into incidents via webhook. Configure at `/incidents` -> **Webhook**. |
| **Enrichment** | Threat feeds, IOC extraction, and enrich automation active | `Enable Threat feeds`, `Realtime IOC extraction`, `threat_intel_case_management_1` | Matches extracted observables against threat intelligence feeds. Activate in [`/usecases`](/usecases). |
| **Assign & Escalate** | Active workflow with background processing | `case_management_assign_escalate_1` | Routes new incidents to on-call analysts and handles SLA escalations. Activate in [`/usecases`](/usecases). |
| **Default config** | Datastore cache present | `shuffle-security_ioc_types`, `shuffle-security_threat_feeds`, security rules | Seeds default IOC types, community threat feeds, and security routing rules. Seeded via `/preferences` -> **Incidents**. |

```
┌────────────────────────────────────────────────────────────────────────┐
│                     Incident Automation Readiness                      │
├────────────────────────┬───────────────────────────────────────────────┤
│ Ingestion              │ [Active]    api/v1/hooks/webhook_<id>         │
│ Enrichment             │ [Active]    threat_intel_case_management_1    │
│ Assign & Escalate      │ [Active]    case_management_assign_escalate_1 │
│ Default config         │ [Active]    IOC types, feeds, security rules  │
└────────────────────────┴───────────────────────────────────────────────┘
```

<!-- TODO: Screenshot Needed: Incident Automation Readiness Card
- Route / UI Location: /incidents -> Top of queue or below KPI summary
- What to capture: Automation Readiness card showing active status across all 4 checks.
- Target path: assets/incidents-automation-readiness.png -->

<!-- TODO: Add step-by-step guides for custom SIEM webhook field mapping and OCSF transformation templates -->
<!-- TODO: Add documentation for custom threat feed authentication (API keys, basic auth) -->
<!-- TODO: Add incident metrics and SLA reporting configuration details once analytics dashboard is finalized -->

---

## SOC use cases

Shuffle Security includes templates for common operational workflows in [`/usecases`](/usecases):

<!-- component:usecases category="cases" -->

- **Phishing Triage**: Parse inbound `.eml` attachments, evaluate header authentication (SPF/DKIM/DMARC), check URLs, and coordinate mailbox purge actions.
- **EDR Alert Enrichment**: Extract suspicious process hashes and network connections from EDR alerts, run containment playbooks, or isolate endpoints.
- **Identity & Session Revocation**: Ingest anomalous sign-in detections, verify activity with the user, and revoke active sessions upon unauthorized confirmation.
- **IOC Threat Hunting & Blocking**: Extract indicators from alerts, match against active feeds, and push verified malicious indicators to perimeter firewall blocklists.

---

## Investigation workspace & tools

Clicking an incident opens the investigation canvas (`/incidents/:id`):

### Tasks & Kanban Board
- **Status Lanes**: Organize response tasks across **To Do**, **In Progress**, and **Done** lanes.
- **Checklists**: Break response workflows into discrete steps.
- **Automated Execution**: Associate workflows with tasks so analysts can execute containment steps with one click.

### Observables & Threat Intelligence
- **Observables Repository**: View and filter indicators organization-wide at `/incidents/observables`.
- **Threat Feeds**: Configure IOC blocklists and threat feeds at `/incidents/threat-feeds` (e.g. Feodo Tracker, MalwareBazaar, AlienVault IP reputation, Blocklist.de, Emerging Threats, OpenPhish). Extracted observables are checked against active feeds for indicator matches.
- **External Lookups**: Observables in the UI provide direct external lookup links to VirusTotal and other analysis services.
- **Correlations**: Search across all incidents sharing an identical observable using `GET /api/v2/correlations?key=<obs>&value=<v>`.

### Email Threads & Deduplication
- **Conversation Threading**: Groups related alert emails into unified conversation threads using Message-ID headers and subjects.
- **Deduplication**: Clusters repetitive alerts into parent cases to minimize analyst fatigue.

<!-- TODO: Screenshot Needed: Incident Investigation Workspace Canvas
- Route / UI Location: /incidents/:id
- What to capture: Investigation workspace showing header, task lanes, observables list, and timeline.
- Target path: assets/incidents-investigation-workspace.png -->

---

## AI Agents in Incidents

Shuffle Security connects with **Shuffle AI** through the `shuffle_incidents` MCP tool:

<!-- component:ask-ai label="Ask AI about Incidents" input="Analyze this incident and suggest an automated containment plan" -->

- **Context-Aware Assistance**: Clicking **"Ask about this Incident"** loads the current incident's title, description, severity, observables, and timeline into the AI session context.
- **Summary Generation**: Generate executive incident summaries and Post-Incident Reviews (PIR) in Markdown.
- **Action Recommendations**: Ask the agent to recommend next investigation steps or propose remediation playbooks for analyst review.

---

## Terminology & preferences

You can customize entity terminology across the web application to match your team's nomenclature:

Navigate to **`/preferences`** -> **Terminology**:

| Option | Singular | Plural | Route | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Incidents** *(default)* | Incident | Incidents | `/incidents` | Standard SOC incident triage and response. |
| **Alerts** | Alert | Alerts | `/alerts` | High-volume detection pipelines and triage. |
| **Cases** | Case | Cases | `/cases` | Formal investigations and digital forensics. |
| **Tickets** | Ticket | Tickets | `/tickets` | Helpdesk or IT-oriented workflows. |
| **Jobs** | Job | Jobs | `/jobs` | Operations and scheduled tasks. |

Changing terminology updates navigation menus, page titles, and UI labels across the application.

---

## API & Datastore reference

Incidents are stored directly in Shuffle Core's Datastore under the **`shuffle-security_incidents`** category (OCSF 2005 format).

### REST API Endpoints

- **List Incidents**: `GET /api/v1/incidents`
- **List Incidents from Datastore Directly**:
  ```bash
  curl -X GET "https://<instance>/api/v1/orgs/<org_id>/list_cache?category=shuffle-security_incidents&top=100" \
    -H "Authorization: Bearer $SHUFFLE_API_KEY"
  ```
- **Get Incident Record**:
  ```bash
  curl -X POST "https://<instance>/api/v1/orgs/<org_id>/get_cache" \
    -H "Authorization: Bearer $SHUFFLE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
      "category": "shuffle-security_incidents",
      "key": "<INCIDENT_ID>",
      "org_id": "<ORG_ID>"
    }'
  ```
- **Upsert / Update Incident in Datastore**:
  ```bash
  curl -X POST "https://<instance>/api/v1/orgs/<org_id>/set_cache" \
    -H "Authorization: Bearer $SHUFFLE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
      "category": "shuffle-security_incidents",
      "key": "<INCIDENT_ID>",
      "value": "{\"id\":\"<INCIDENT_ID>\",\"class_uid\":2005,\"severity_id\":4,\"status_id\":1,\"finding_info\":{\"title\":\"Suspicious Login\"}}"
    }'
  ```
- **Query Observable Correlations Across Categories**:
  ```bash
  curl -X GET "https://<instance>/api/v2/correlations?key=ip&value=198.51.100.1" \
    -H "Authorization: Bearer $SHUFFLE_API_KEY"
  ```

### In Custom Python Apps & Workflows

```python
# Query an incident by key from the datastore
incident = self.get_cache("incident_id_123", category="shuffle-security_incidents")

# Inspect observables
if incident and len(incident.get("observables", [])) > 0:
    for obs in incident["observables"]:
        print(f"Observable {obs.get('type')}: {obs.get('value')}")

# Update incident status and write back
if incident:
    incident["status_id"] = 2
    incident["status"] = "In Progress"
    self.set_cache("incident_id_123", incident, category="shuffle-security_incidents")
```

For more details on backend API endpoints and datastore caching rules, see the [API documentation](/docs/API).
