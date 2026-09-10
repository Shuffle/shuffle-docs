# Incidents in Shuffle Security

[Shuffle Security](https://security.shuffler.io) provides a real-time, collaborative Incident Management and Triage platform designed specifically for Security Operations Centers (SOC) and Incident Response (IR) teams. It bridges autonomous alert ingestion, human-in-the-loop decision-making, and automated workflow response actions into a unified operational canvas.

---

## Overview & Configurable Terminology

Every security team operates with different organizational terminology. Shuffle Security allows organizations to customize the primary entity nomenclature across the platform to align with existing operational workflows.

### Terminology Customization

By navigating to **`/preferences`**, organization administrators can configure the global entity label:

| Terminology | Singular | Plural | Primary Route | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Incidents** *(default)* | Incident | Incidents | [`/incidents`](/incidents) | Standard security incident triage and investigation. |
| **Alerts** | Alert | Alerts | [`/alerts`](/alerts) | High-volume detection alerting and noise reduction. |
| **Cases** | Case | Cases | [`/cases`](/cases) | Formal case management and multi-phase forensic investigations. |
| **Tickets** | Ticket | Tickets | [`/tickets`](/tickets) | IT Service Management (ITSM) and helpdesk task tracking. |
| **Jobs** | Job | Jobs | [`/jobs`](/jobs) | Scheduled, batch, or autonomous operational workloads. |

When changed, all platform headers, sidebar navigation links, route paths, task boards, and AI agent prompts dynamically adapt to the selected terminology throughout the user interface.

---

## Incident Triage & Operational Queue

The primary queue at [`/incidents`](/incidents) serves as the command center for monitoring incoming security events:

1. **Real-Time Stream**: Ingests security alerts from SIEMs, EDRs, email sensors, cloud platforms, and third-party webhooks via Shuffle Workflows.
2. **Severity Classification**: Categorizes events by severity:
   - `Critical`: Active breaches, ransomware, confirmed data exfiltration.
   - `High`: Privilege escalation, lateral movement, malware execution.
   - `Medium`: Suspicious logins, anomalous administrative activity.
   - `Low`: Policy deviations, reconnaissance, scan attempts.
   - `Informational`: Audit logging, routine configuration modifications.
3. **Status Workflow**: Tracks the incident lifecycle across states:
   - `Open`: Newly ingested and awaiting triage.
   - `In Progress`: Actively under investigation by an assigned analyst.
   - `Under Review`: Awaiting manager review, customer confirmation, or forensic sign-off.
   - `Closed`: Resolved, remediated, or classified as false positive.
4. **Ownership & Assignment**: Assign incidents to individual security analysts or functional teams to prevent duplicate effort.

---

## Incident Investigation & Workspace

Clicking into any incident opens the unified investigation workspace at [`/incidents-simple/:id`](/incidents):

<!-- component:ask-ai placeholder="Ask about this incident, triage observables, or correlate..." -->

### 1. Kanban Task Management

Incidents in Shuffle Security feature an interactive Kanban task board to coordinate complex multi-step investigations:

- **Configurable Task Lanes**: By default, tasks transition between **To Do**, **In Progress**, and **Done**. Organizations can add, reorder, or recolor custom status lanes in `/preferences`.
- **Sub-tasks & Checklist Items**: Break large response objectives into discrete investigator tasks (e.g. *"Isolate endpoint"*, *"Dump memory"*, *"Revoke Okta session"*).
- **Assignees & Due Dates**: Ensure accountability during time-sensitive response operations.
- **Workflow Triggers**: Trigger automated Shuffle workflows directly from a specific task item.

### 2. Observables & IOC Management

Observables represent Indicators of Compromise (IOCs) and technical artifacts discovered during an investigation:

- **Supported Artifact Types**: IP addresses, domain names, URLs, file hashes (MD5, SHA1, SHA256), email addresses, hostnames, user accounts, and CVE identifiers.
- **Automated Extraction**: Shuffle automatically parses observables from incoming alerts, email headers, and playbook execution outputs.
- **Enrichment & Threat Feeds**: Integrated with external threat intelligence sources at [`/incidents/threat-feeds`](/incidents/threat-feeds) to instantly check reputation against VirusTotal, AbuseIPDB, AlienVault OTX, and custom MISP feeds.
- **IOC Repository**: View and query all organization-wide observables centrally at [`/incidents/observables`](/incidents/observables).

### 3. Email Thread Panel & Communications

For phishing investigations and incident communications, Shuffle Security provides a dedicated email thread interface:

- **Inbound Ingestion**: Ingest raw `.eml` and `.msg` files directly from mail servers (Office 365, Google Workspace, IMAP).
- **Thread Correlation**: Automatically groups related emails into conversation threads based on message IDs, subjects, and participant addresses.
- **Header & Attachment Analysis**: Inspect headers for SPF, DKIM, and DMARC alignment, and extract attachments safely into sandbox analysis workflows.
- **Deduplication & Auto-Merge**: Correlates identical or duplicate alert storms into a single parent incident to eliminate analyst alert fatigue.

### 4. Pager Notifications & Escalation

When critical incidents occur outside standard SOC operating hours:

- **On-Call Paging**: Dispatch real-time audio and mobile push notifications to on-call engineers.
- **Escalation Policies**: Re-route unacknowledged alerts to secondary tier responders after configured timeout thresholds.

---

## Response Actions & Playbooks

The hallmark of Shuffle Security is the seamless connection between incident analysis and automated response actions:

1. **Triggering Playbooks**: From the **Response Actions** panel at [`/incidents/response-actions`](/incidents/response-actions) or from inside an incident, analysts can execute pre-approved response playbooks with a single click:
   - **Containment**: Isolate infected endpoints in CrowdStrike or SentinelOne.
   - **Identity Lockout**: Disable compromised Azure AD / Okta accounts and reset active credentials.
   - **Network Quarantine**: Block malicious IPs and domains on Palo Alto, Fortinet, or Cloudflare firewalls.
   - **Forensics**: Initiate automated memory capture or evidence gathering.
2. **Context Passing (`$incident`)**:
   - When a playbook is triggered from an incident, the entire incident context is passed automatically to the workflow execution engine as `$incident`.
   - Workflows can read incident variables, update task statuses, post timeline notes, and attach generated reports directly back to the incident.
3. **Human-in-the-Loop Approvals**:
   - High-impact containment actions (e.g. taking a critical database host offline) can be configured with Shuffle's approval nodes, requiring analyst confirmation before execution.

---

## AI Agents in Incidents

Shuffle Security includes deep integration with **Shuffle AI** and the autonomous agent loop via the `shuffle_incidents` Model Context Protocol (MCP) toolset:

- **Context-Aware Assistant**: Clicking **"Ask about this Incident"** opens the AI side panel with the current incident's severity, observables, timeline notes, and email threads pre-loaded into the agent context.
- **Autonomous IOC Triage**: The agent can query reputation databases, compare hashes with historical cases, and recommend appropriate severity levels.
- **Incident Summarization**: Generate executive summaries and post-incident review (PIR) reports in clean Markdown format with a single prompt.
- **Drafting Response Plans**: Instruct the agent to *"Analyze the suspicious PowerShell command in this incident and generate a 3-step containment plan."* The agent drafts decisions and can trigger the corresponding playbooks upon approval.

---

## Programmatic Access & APIs

All incident operations can be automated using Shuffle's REST APIs:

- **Create Incident**: `POST /api/v1/incidents`
- **List & Filter Incidents**: `GET /api/v1/incidents?status=open&severity=high`
- **Get Incident Details**: `GET /api/v1/incidents/{id}`
- **Add Task**: `POST /api/v1/incidents/{id}/tasks`
- **Attach Observable**: `POST /api/v1/incidents/{id}/observables`
- **Trigger Response Action**: `POST /api/v1/incidents/{id}/actions/{action_id}`

For complete schema definitions and authentication parameters, refer to the [Shuffle API Reference](/docs/API).
