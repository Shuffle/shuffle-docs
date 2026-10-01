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

### Deleting Erroneously Ingested Incidents (Admin Only)

Ever accidentally fired off a test webhook or had a noisy detection rule dump 500 bogus alerts into your queue? We've definitely been there.

When you're looking at [`/incidents`](/incidents) or working inside a specific incident, you won't find a delete button. We deliberately leave hard deletion out of the main operational views so nobody accidentally nukes an active investigation or destroys audit history. In normal operations, you'll just mark cases as **Resolved** or **False Positive**.

If you ingested test alerts or corrupted data that really shouldn't exist, an admin can permanently purge it from the Datastore:

1. Head to **Admin** in the top navigation bar.
2. Click the **Datastore** tab, or go straight to [`/admin/datastore?category=shuffle-security_incidents`](/admin/datastore?category=shuffle-security_incidents) (or on self-hosted Shuffle Core: `/admin?tab=datastore&category=shuffle-security_incidents`).
3. Search for the incident ID or key (e.g. `incident_2026_0942`).
4. **Delete a single incident**: Click the trash button on that row and confirm the prompt.
5. **Bulk cleanup**: Check the boxes next to the records you want to wipe, and click **Delete** in the top action bar.

Note on permissions: In the Shuffle Security UI, `/admin/datastore` is restricted to users with the admin role (`isAdmin`). If you're an analyst without admin privileges, you'll see a notice letting you know to have a tenant admin clear them out for you.

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

### Key revisions, audit trail & rollback protection

Every key in `shuffle-security_incidents` is automatically stored with an immutable revision history. Whenever an analyst edits a case in the UI, an AI Agent enriches observables, an ingestion webhook posts updates, or a workflow triggers `self.set_cache(...)`, Shuffle creates a new revision instead of destructively replacing the previous record.

- **Zero Data Loss on Overwrites or Deletion**: If an automated script or ingestion source accidentally overwrites an incident with a malformed payload or drops critical observables, no data is permanently lost. All prior snapshots remain stored in the datastore.
- **Audit Trail & Attribution**: Every revision tracks:
  - `revision_id`: Unique identifier for the snapshot.
  - `edited` / `created`: Exact Unix epoch timestamp.
  - Actor provenance: `user_id` (for manual analyst changes) or `workflow_id` and `execution_id` (for automated SOAR workflows).
  - Field diffs: Added, removed, and modified properties between snapshots.
- **Inspect & Roll Back Revisions**:
  - **In the Web UI**: On any incident detail page, select the **Changes** (revisions) timeline tab to inspect visual diffs between revisions, preview historical states, and click **Rollback** to revert the incident.
  - **Via REST API**: Query all historical revisions for an incident:
    ```bash
    curl "https://shuffler.io/api/v2/datastore/category/shuffle-security_incidents/{incident_id}/revisions" \
      -H "Authorization: Bearer <api_key>"
    ```
  - **Via Python App**:
    ```python
    # Fetch historical revisions for an incident
    revisions = self.get_cache_revisions(key="incident_2026_0942", category="shuffle-security_incidents")

    # If an erroneous update occurred, rollback to previous revision
    if len(revisions) > 1:
        previous_snapshot = revisions[1]["value"]
        self.set_cache(
            key="incident_2026_0942",
            value=previous_snapshot,
            category="shuffle-security_incidents"
        )
    ```

---

## Ingest: Getting alerts into Shuffle

<!-- component:ingest workflow="Ingest Tickets" category="cases" -->

### 1. Ingestion Webhook (Push)
Every tenant gets a dedicated inbound webhook to receive alerts from detection systems (Splunk, Wazuh, Elastic, CrowdStrike, AWS GuardDuty, custom scripts):
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

## Investigation workspace & incident tabs

When you click on an incident from the queue, you land on the investigation canvas at `/incidents/:id`. We built this page to give you everything you need during an active investigation—whether you prefer a fast, conversational triage view or need to dig deep into raw JSON payloads.

You'll notice the tabs are split into two groups: your everyday **Operational Tabs** on the left, and **Data Translation Tabs** on the right.

### Observables & Threat Intelligence
- **Observables Repository**: View and filter indicators tenant-wide at `/incidents/observables`.
- **Threat Feeds**: Configure IOC blocklists and threat feeds at `/incidents/threat-feeds` (e.g. Feodo Tracker, MalwareBazaar, AlienVault IP reputation, Blocklist.de, Emerging Threats, OpenPhish). Extracted observables are checked against active feeds for indicator matches.
- **External Lookups**: Observables in the UI provide direct external lookup links to VirusTotal and other analysis services.
- **Correlations**: Search across all incidents sharing an identical observable using `GET /api/v2/correlations?key=<obs>&value=<v>`.

- **Simple**: A minimalist, chat-style view built for fast triage. If you just want to read the incident description, check recent analyst notes, and type quick commands or questions to `@AIAgent`, start here. The feed reads bottom-to-top like a standard chat window.
- **Detailed**: The full investigation workspace. Here you can edit the title and Markdown description, update severity and status, adjust TLP/PAP flags, assign stakeholders, and manage custom metadata fields while keeping an eye on the vertical timeline.
- **Tasks**: An interactive checklist and Kanban board (`To Do`, `In Progress`, `Done`). When an incident requires multiple steps—like isolating a machine, resetting a password, and notifying a user—break them down into tasks here. You can assign tasks to teammates, or assign them to `AI Agent` to let Shuffle handle them automatically.
- **Observables**: A clean table of every indicator pulled from the alert—IP addresses, domains, file hashes, URLs, usernames, and command lines. Each observable shows its type, TLP level, detection source, and threat feed matches. You can also click any indicator to run on-demand lookups (like VirusTotal or AlienVault) right from the table.
- **Correlations**: Shuffle automatically checks if any observables in this incident have shown up in other cases across your organization or sub-tenants. If three other alerts hit the same malicious IP this morning, they'll show up here with a one-click **Merge Into** button so you can roll them into a single investigation instead of working multiple duplicate tickets.
- **Events**: The raw security telemetry and alert events linked to the incident finding. Useful when you need to inspect the original SIEM or EDR event stream that triggered the alert in the first place.

### Data Transformation & Translation Tabs

Over on the right side of the tab bar, you'll see tabs that show you exactly how Shuffle handled your data from start to finish:
- **Original**: The raw, unmapped JSON payload exactly as your SIEM, EDR, or cloud provider sent it to us before any normalization happened.
- **Translation**: The translation schema or Liquid script Shuffle used to map that source data into standard OCSF fields. Great for debugging when an alert field didn't land where you expected.
- **OCSF**: The final, normalized OCSF 2005 Incident Finding record. It includes a live JSON viewer and editor so you can verify the exact structure stored in the datastore or make quick inline corrections.

### Filtering the Activity Timeline

Along the right side (or inline in Detailed view) is the incident timeline. Real investigations get noisy quickly, so you can toggle filters to see only what you care about:
- **Changes**: Revision history showing what changed on the incident over time, with diffs and a one-click **Rollback** button if someone made a mistake.
- **AI Agents**: Every background run, thought process, and tool execution from your AI agents.
- **Workflow runs**: Automatic playbooks and workflow executions tied to this incident.
- **Comments**: Human analyst discussion, uploaded attachments, and threaded replies.
- **Threading**: History of merged cases and parent-child ticket relationships.
- **Tasks**: Updates on task progress, completions, and state changes.
- **Observables**: When new IOCs were added or updated with threat intel tags.
- **Correlations**: When new matching cases were linked.

---

## How enrichment works

Nobody likes staring at a bare IP address or an obscure file hash trying to figure out if it's evil. Shuffle enriches your observables automatically so you have context ready the moment you open the ticket.

Here is how enrichment fits together behind the scenes:

### 1. Automatic IOC Extraction
When alerts hit Shuffle (via webhook or scheduled polling workflows), we automatically parse through the raw logs, email headers, and alert descriptions using regex and heuristic extractors. We look for:
- IPv4 and IPv6 addresses
- Hostnames and domains
- File hashes (MD5, SHA1, SHA256)
- URLs and email addresses
- User accounts and process names

These get parsed out, assigned their proper observable types, tagged with default TLP levels, and stored directly in the incident's `observables` list.

### 2. Threat Feed Matching
Shuffle continuously runs two background workflows: `Enable Threat feeds` and `Realtime IOC extraction`. These pull fresh threat intelligence from popular community and open-source feeds—like Feodo Tracker, MalwareBazaar, AlienVault OTX, Blocklist.de, Emerging Threats, and OpenPhish—into the `shuffle-security_threat_feeds` datastore category.

Whenever observables are added to an incident, Shuffle checks them against these feeds in real time. If an IP or hash matches, we tag the reputation, confidence score, and threat category directly onto the observable so you can see it at a glance.

### 3. Automated Enrichment Workflows
If you have API keys for external intelligence services (like VirusTotal, Shodan, AbuseIPDB, or URLScan), you can configure an `enrich` category automation on `shuffle-security_incidents`. 

When a new incident is saved, Shuffle runs your enrichment workflow (such as `threat_intel_case_management_1`), queries your threat intel apps, and appends the results into the incident's `enrichments` array:

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
Need to pivot on an indicator right now? In the **Observables** tab, you can click on any indicator row to see its sighting history, or use the context menu to trigger instant lookups against any configured threat intel integration without leaving the page.

---

## AI Agents in Incidents

We designed AI in Shuffle Security not as a separate chatbot you copy-paste data into, but as an active teammate that works alongside you directly inside your cases. Shuffle AI agents can read the incident context, analyze evidence, recommend containment plans, and execute real actions through your connected apps.

Here is how you can use agents in your day-to-day workflow:

### 1. In-Line Chat with `@AIAgent`
You can chat with an agent right inside the incident comments or the Simple triage feed. Just mention `@AIAgent` (or `@agent`) followed by what you need:

```
@AIAgent summarize this incident and check if the source IP matches any recent phishing campaigns.
```

The agent automatically reads the incident finding, observables, tasks, threat feed matches, and past comments, then posts its analysis straight into your timeline. You can see its reasoning steps, tool calls, and execution status right in the stream.

### 2. Handing Off Tasks to the AI Agent
In the **Tasks** tab, you don't have to do everything manually. When you create or edit a task, you can set its assignee to **AI Agent**.

Once assigned, the agent picks up the task objective, chooses the right tools from your connected apps (like querying Active Directory, pulling endpoint logs from CrowdStrike, checking an Okta user, or posting to Slack), performs the work, updates the checklist steps, and marks the task Done when finished.

### 3. Human-in-the-Loop Approvals
Security automation is great, but giving an LLM free rein to isolate executive laptops or nuke user accounts is a bad idea. We built safety controls into the core agent loop.

Whenever an agent decides it needs to take a high-impact or destructive action (like blocking an IP on your perimeter firewall, revoking a session, or isolating a host):
- The agent pauses and enters a `WAITING` state.
- An **Approval Required** banner appears at the top of the incident page and in the timeline feed.
- You see exactly what action the agent wants to take and with what parameters.
- Click **Approve** to let it proceed, or **Reject** to stop it. The action will never execute without your explicit sign-off.

If an agent ever hits a tool failure or runs into an unhandled error, you'll see an **Agent Failed — Manual Action Needed** alert so you can jump in and handle the step manually without guessing what went wrong.

### 4. Automated Triage with Routing Rules
If you want agents to work cases before an analyst even opens them, you can set up routing rules under **Admin** -> **Routing** (or using category automations on `shuffle-security_incidents`).

For example, you can tell Shuffle: "Whenever a Critical alert comes in from CrowdStrike, run an agent with the prompt 'Triage this host, check running processes against observables, and suggest an initial severity'." The agent will run immediately upon ingestion, leaving structured notes and suggested next steps ready for your team.

### 5. Interactive Copilot & Post-Incident Reviews
Clicking the **Ask AI** button or opening the AI side drawer lets you have a full conversational session scoped to the case. It's especially useful for generating executive Post-Incident Reviews (PIR), creating shift handoff summaries in clean Markdown, or drafting custom containment scripts on the fly.

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
