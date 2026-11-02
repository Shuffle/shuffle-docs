# Incidents in Shuffle Security

Documentation for triaging alerts, investigating incidents, collaborating with AI agents, and automating response workflows in Shuffle Security.

## Table of contents
* [Overview](#overview)
* [Using the Incidents dashboard](#using-the-incidents-dashboard)
* [Investigating an incident](#investigating-an-incident)
* [AI Agents in Incidents](#ai-agents-in-incidents)
* [Ingesting alerts into Shuffle](#ingesting-alerts-into-shuffle)
* [How enrichment works](#how-enrichment-works)
* [Automating incident response](#automating-incident-response)
* [Terminology & preferences](#terminology--preferences)
* [Datastore architecture & OCSF schema](#datastore-architecture--ocsf-schema)
* [API & Datastore reference](#api--datastore-reference)

---

## Overview

Shuffle Security ([shuffle.security/incidents](https://shuffle.security/incidents)) is an incident response and alert triage workspace built to keep investigations, observables, tasks, AI agents, and automated playbooks in one place.

Instead of jumping between a separate ticketing queue, threat intelligence tabs, and your automation engine, you can review incoming alerts, inspect enriched indicators, assign tasks to teammates or AI agents, and trigger containment workflows directly from the incident view.

- **Fast Triage & Investigation**: Filter the queue by status, severity, or observable, and switch between a conversational **Simple** triage view and a full **Detailed** investigation workspace.
- **Built-In Enrichment & Correlation**: Automatically extract IPs, domains, hashes, URLs, and users from raw alerts, match them against threat feeds, and merge related incidents with one click.
- **AI Agent Collaboration**: Mention `@AIAgent` in comments, assign checklist tasks to the agent, and approve or reject high-impact containment actions with human-in-the-loop controls.
- **One-Click Playbooks**: Trigger automated response workflows directly from an incident or run them automatically on ingestion.

> [!NOTE]
> **Zero License Paywalls**  
> Incident and case management is included in both Shuffle Cloud and self-hosted open-source instances. There are no per-seat licenses, analyst fees, or ticket caps. Standard app runs execute only when automation workflows run. Manual incident handling, triage, and queue management consume zero app runs.

---

## Using the Incidents dashboard

Navigate to **`/incidents`** in Shuffle Security to view and manage your active queue:

<!-- component:incident-dashboard -->

Incidents progress through standardized lifecycle states as your team works them:

| Status Stage | Meaning | Typical Handling |
| :--- | :--- | :--- |
| **New / Open** | Ingested alert awaiting triage | Evaluate observables, review automated enrichment, escalate or close. |
| **In Progress** | Active investigation | Inspect the investigation workspace, work tasks, execute response playbooks. |
| **Under Review** | Containment executed | Verify remediation and complete post-incident documentation. |
| **Resolved / Closed** | Threat neutralized or confirmed false positive | Archive the case and tune detection rules if necessary. |

### Queue Controls
- **Filters & Search**: Filter by lifecycle status (`All`, `Open`, `In Progress`, `Under Review`, `Closed`), severity (`Critical`, `High`, `Medium`, `Low`, `Info`), or search by keyword, ticket ID, and observable value.
- **Table Columns**: View Severity, Title & ID, Status, Assignee, Observables count, and Created timestamp at a glance.
- **Bulk Actions**: Select multiple incidents in the table to bulk-assign owners, update lifecycle status, or close out false positives.

<!-- TODO: Screenshot Needed: Incidents Dashboard Table
- Route / UI Location: /incidents
- What to capture: Full view of the /incidents dashboard showing Ingest row, search bar, status filter tabs, and incident rows.
- Target path: assets/incidents-dashboard-table.png -->

---

## Investigating an incident

When you click on an incident from the queue, you land on the investigation workspace at `/incidents/:id`. This view gives you everything you need during an active investigation—whether you prefer a fast, conversational triage feed or need to inspect raw telemetry.

The workspace tabs are organized into **Operational Tabs** on the left for day-to-day triage, and **Data Translation Tabs** on the right for inspecting the underlying payload.

### Operational Tabs
- **Simple**: A minimalist, chat-style view built for fast triage. Read the incident summary, check recent analyst notes, and type commands or questions to `@AIAgent`. The feed reads bottom-to-top like a standard chat window.
- **Detailed**: The full investigation workspace. Edit the title and Markdown description, update severity and status, adjust TLP/PAP flags, assign stakeholders, and manage custom metadata fields alongside the vertical activity timeline.
- **Tasks**: An interactive checklist and Kanban board (`To Do`, `In Progress`, `Done`). When an incident requires multiple response steps—such as isolating a machine, resetting credentials, and notifying a user—break them down into tasks here. Assign tasks to teammates, or assign them to **AI Agent** to let Shuffle execute them automatically.
- **Observables**: A structured table of every indicator extracted from the alert—IP addresses, domains, file hashes, URLs, usernames, and command lines. Each observable displays its type, TLP level, detection source, and threat feed matches. Click any indicator to run on-demand lookups (such as VirusTotal or AlienVault) directly from the table.
- **Correlations**: Shuffle automatically checks whether any observables in the current incident appear in other cases across your organization or sub-tenants. If multiple alerts hit the same malicious IP or hash, they appear here with a one-click **Merge Into** button so you can consolidate duplicate alerts into a single investigation.
- **Events**: The linked security telemetry and alert events that triggered or relate to the incident finding.

### Filtering the Activity Timeline

Along the right side (or inline in Detailed view) is the incident activity timeline. Because investigations can generate a high volume of updates, you can toggle filters to focus on specific activity:
- **Comments**: Human analyst discussion, uploaded attachments, and threaded replies.
- **AI Agents**: Background agent runs, reasoning steps, and tool executions.
- **Workflow runs**: Automated playbooks and workflow executions tied to the incident.
- **Tasks**: Task assignments, progress updates, and completions.
- **Observables**: Newly extracted IOCs and threat intelligence matches.
- **Correlations**: Newly linked or merged cases.
- **Threading**: History of merged cases and parent-child relationships.
- **Changes**: Full revision history showing field diffs over time, with a one-click **Rollback** button to revert accidental edits.

### Observables & Threat Intelligence Management
Beyond an individual incident, you can manage indicators and feeds across your entire tenant:
- **Observables Repository**: Browse and filter all extracted indicators tenant-wide at `/incidents/observables`, or configure custom regex extraction patterns.
- **Threat Feeds**: Manage IOC blocklists and intelligence feeds at `/incidents/threat-feeds` (including Feodo Tracker, MalwareBazaar, AlienVault IP reputation, Blocklist.de, Emerging Threats, and OpenPhish).

### Data Transformation & Translation Tabs
On the right side of the incident tab bar, you can inspect how the raw alert was normalized:
- **Original**: The raw, unmapped JSON payload exactly as your SIEM, EDR, or cloud provider sent it before normalization.
- **Translation**: The translation schema or Liquid script Shuffle used to map the source payload into standardized fields—useful when debugging field mappings.
- **OCSF**: The normalized OCSF 2005 Incident Finding JSON record, complete with a live viewer and editor for inline adjustments.

---

## AI Agents in Incidents

AI in Shuffle Security works directly inside your incidents as an operational teammate rather than a separate chatbot. Shuffle AI agents read the incident context, analyze observables, suggest containment steps, and execute actions through your authenticated integrations.

### 1. In-Line Chat with `@AIAgent`
Chat with an agent directly inside incident comments or the **Simple** triage view by mentioning `@AIAgent` (or `@agent`):

```
@AIAgent summarize this incident and check if the source IP matches any recent phishing campaigns.
```

The agent reads the incident finding, observables, tasks, threat feed matches, and comment history, then posts its findings and tool outputs directly into the timeline.

### 2. Handing Off Tasks to the AI Agent
In the **Tasks** tab, set any task's assignee to **AI Agent**. The agent reads the task objective, selects the appropriate tools from your connected apps (such as querying Active Directory, pulling endpoint logs from CrowdStrike, checking an Okta user, or posting to Slack), updates the checklist steps, and marks the task **Done** when complete.

### 3. Human-in-the-Loop Approvals
To prevent unintended disruption, high-impact or destructive actions (such as blocking an IP on a firewall, revoking user sessions, or isolating a host) require human approval:
- The agent pauses and enters a `WAITING` state.
- An **Approval Required** banner appears at the top of the incident page and in the timeline feed, showing the exact action and parameters.
- Click **Approve** to execute the action, or **Reject** to cancel it.

If an agent encounters a tool failure or error, an **Agent Failed — Manual Action Needed** banner alerts you immediately so you can step in.

### 4. Automated Triage with Routing Rules
To have agents triage alerts before an analyst opens them, configure routing rules under **Admin** -> **Preferences** (or via category automations on `/incidents`). For example, you can automatically run an agent on incoming Critical alerts to check running processes, enrich indicators, and post an initial triage summary.

### 5. Interactive Copilot & Post-Incident Reviews
Click the **Ask AI** button in the top navigation bar to open the AI side drawer scoped to the active incident. Use it to generate Post-Incident Reviews (PIR), draft shift handoff summaries, or build containment commands on the fly.

---

## Ingesting alerts into Shuffle

<!-- component:ingest workflow="Ingest Tickets" category="cases" -->

Use the interactive ingestion panel above, or navigate to **`/incidents`** and use the ingestion controls in the top header bar to connect alert sources.

### 1. Ingestion Webhook (Push)
Every tenant has a dedicated inbound webhook to receive alerts from SIEMs, EDRs, email security gateways, and custom scripts (Splunk, Wazuh, Elastic, CrowdStrike, AWS GuardDuty):
- Navigate to **`/incidents`** in Shuffle Security.
- Click the **Webhook** button in the top header bar.
- Copy your inbound endpoint URL:
  ```
  https://<instance>/api/v1/hooks/webhook_<hook_id>
  ```
- Send any JSON alert payload to this webhook to create an incident automatically.

### 2. Polling Workflows (Scheduled Pull)
For alert sources that do not push webhooks or sit behind firewalls, connect your app credentials in the header bar or use scheduled workflows (such as `Ingest Tickets`). These workflows poll external APIs on a schedule and create incidents automatically. Click **Sync Now** in the header bar to trigger an immediate pull.

### 3. Schemaless Ingest & Automatic Observable Extraction
Different security tools output very different JSON structures. Shuffle is **schemaless at ingest**:
- You do not need to write rigid schema mappings before sending alerts. Shuffle accepts any JSON payload, preserves the original raw alert in the **Original** tab, and normalizes key fields automatically.
- During ingestion, Shuffle scans the payload to extract common indicators of compromise—IPv4/IPv6 addresses, domains, hostnames, MD5/SHA1/SHA256 hashes, URLs, email addresses, usernames, and CVEs—and populates the incident's **Observables** tab with Traffic Light Protocol tags (`TLP:RED`, `TLP:AMBER`, `TLP:GREEN`, `TLP:CLEAR`).

---

## How enrichment works

When an alert lands in Shuffle, observables are enriched automatically so analysts have reputation context as soon as they open the incident:

### 1. Automatic IOC Extraction
On ingest (via webhook or polling workflow), Shuffle parses raw logs, email headers, and descriptions using regex and heuristic extractors (configurable at `/incidents/observables`) and attaches discovered indicators to the incident.

### 2. Threat Feed Matching
Background workflows (`Enable Threat feeds` and `Realtime IOC extraction`) pull intelligence from active feeds configured at `/incidents/threat-feeds`. Whenever observables are added to an incident, Shuffle checks them against these feeds in real time and tags matching indicators with reputation, confidence, and threat category metadata.

### 3. Automated Enrichment Workflows
When you connect external threat intelligence apps (such as VirusTotal, Shodan, AbuseIPDB, or URLScan) and enable the **Enrich** automation on `/incidents`, Shuffle queries those services for new incidents and records the results in the incident's `enrichments` list:

```json
"enrichments": [
  {
    "type": "virustotal",
    "value": "198.51.100.42",
    "data": "14/72 engines flagged as malicious",
    "first_seen": 1714560000,
    "last_seen": 1714563600
  }
]
```

### 4. On-Demand Lookups
Inside the incident's **Observables** tab, click any indicator row to view its sighting history across other incidents or trigger an immediate lookup against your connected threat intelligence tools.

---

## Automating incident response

<!-- component:automation-for-incidents category="incidents" -->

Use the interactive control above, or navigate to **`/incidents`** and click the **Automation for Incidents** (rocket) button in the header bar to configure automatic AI triage, enrichment, and response workflows.

### How Incidents Connect to Workflows

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

When an incident triggers a workflow, Shuffle passes the full incident object as `$incident`:
- `$incident.title` — Alert title
- `$incident.severity` — Severity level (`Critical`, `High`, `Medium`, `Low`, `Info`)
- `$incident.observables` — Array of extracted IOCs
- `$incident.description` — Incident description or summary
- `$incident.id` — Unique incident identifier

### Incident Automation Readiness

Shuffle Security checks whether your core incident response automations are active:

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

### SOC Use Cases

Shuffle Security includes pre-built templates for common SOC workflows in [`/usecases`](/usecases):

<!-- component:usecases category="cases" -->

- **Phishing Triage**: Parse inbound `.eml` attachments, evaluate header authentication (SPF/DKIM/DMARC), check URLs, and purge malicious emails across the tenant.
- **EDR Alert Enrichment**: Extract suspicious process hashes and network connections from EDR alerts, enrich indicators, and trigger host isolation.
- **Identity & Session Revocation**: Ingest anomalous sign-in detections, verify activity with the user via Slack/Teams, and revoke active sessions upon confirmation.
- **IOC Threat Hunting & Blocking**: Extract indicators from alerts, match against active feeds, and push verified malicious indicators to firewall blocklists.

---

## Terminology & preferences

You can customize the terminology used across the web application to match your team's workflow:

Navigate to **`/preferences`** -> **Terminology** (or **`/admin/preferences`**):

| Option | Singular | Plural | Route | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Incidents** *(default)* | Incident | Incidents | `/incidents` | Standard SOC incident triage and response. |
| **Alerts** | Alert | Alerts | `/alerts` | High-volume detection pipelines and triage. |
| **Cases** | Case | Cases | `/cases` | Formal investigations and digital forensics. |
| **Tickets** | Ticket | Tickets | `/tickets` | Helpdesk or IT-oriented workflows. |
| **Jobs** | Job | Jobs | `/jobs` | Operations and scheduled tasks. |

Changing terminology updates navigation menus, page titles, and UI labels across the application. From `/admin/preferences`, you can also configure SLA response/resolution targets, custom lifecycle statuses and severities, task statuses, and incident routing rules.

---

## Datastore architecture & OCSF schema

Under the hood, all incidents, alerts, and cases are stored directly in Shuffle's Datastore under the **`shuffle-security_incidents`** category formatted according to the **OCSF 2005 (Incident Finding)** specification.

<!-- component:datastore category="shuffle-security_incidents" -->

<!-- component:datastore-link category="shuffle-security_incidents" -->

Inspect and query raw incident records directly:
- **Shuffle Security Datastore**: Navigate to [`/admin/datastore?category=shuffle-security_incidents`](/admin/datastore?category=shuffle-security_incidents) in Shuffle Security. If local datastore exists, it loads locally; otherwise, it automatically redirects to Shuffle Core.
- **Shuffle Datastore**: [Open in Shuffle Datastore](https://shuffler.io/admin?tab=datastore&category=shuffle-security_incidents) (`https://shuffler.io/admin?tab=datastore&category=shuffle-security_incidents` or `/admin?tab=datastore&category=shuffle-security_incidents` on self-hosted instances).
- **Manual UI Navigation**: Go to **Admin** -> **Datastore** -> select category **`shuffle-security_incidents`**.

### Deleting Erroneously Ingested Incidents (Admin Only)

To prevent analysts from accidentally deleting active investigations or destroying audit history, `/incidents` does not expose a hard-delete button in the main operational views (normal triage marks cases as **Resolved** or **False Positive**).

If a test webhook or noisy rule ingested bogus records that need to be permanently purged, an admin (`isAdmin`) can delete them from the Datastore:

1. Navigate to **Admin** -> **Datastore**, or open [`/admin/datastore?category=shuffle-security_incidents`](/admin/datastore?category=shuffle-security_incidents).
2. Search for the incident ID or key (e.g. `incident_2026_0942`).
3. **Delete a single incident**: Click the delete button on that row and confirm.
4. **Bulk cleanup**: Select the checkboxes next to the records you want to remove and click **Delete Selected** in the bulk action bar.

### OCSF 2005 Structure

When a detection workflow, ingestion webhook, or custom script writes an incident to `shuffle-security_incidents`, it stores an OCSF 2005 JSON payload:

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

### Key Revisions, Audit Trail & Rollback Protection

Every key in `shuffle-security_incidents` is stored with an immutable revision history. Whenever an analyst edits a case in the UI, an AI Agent enriches observables, an ingestion webhook posts updates, or a workflow runs `self.set_cache(...)`, Shuffle creates a new revision instead of overwriting the previous record destructively.

- **Zero Data Loss on Overwrites**: If an automated script or ingestion source overwrites an incident with a malformed payload, all prior snapshots remain stored in the datastore.
- **Audit Trail & Attribution**: Every revision tracks `revision_id`, Unix timestamp (`edited` / `created`), actor provenance (`user_id` or `workflow_id` / `execution_id`), and field diffs.
- **Inspect & Roll Back Revisions**:
  - **In the Web UI**: Open any incident, select the **Changes** timeline filter to inspect diffs between revisions, and click **Rollback** to revert.
  - **Via REST API**:
    ```bash
    curl "https://shuffler.io/api/v2/datastore/category/shuffle-security_incidents/{incident_id}/revisions" \
      -H "Authorization: Bearer <api_key>"
    ```
  - **Via Python App**:
    ```python
    revisions = self.get_cache_revisions(key="incident_2026_0942", category="shuffle-security_incidents")
    if len(revisions) > 1:
        previous_snapshot = revisions[1]["value"]
        self.set_cache(
            key="incident_2026_0942",
            value=previous_snapshot,
            category="shuffle-security_incidents"
        )
    ```

---

## API & Datastore reference

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
