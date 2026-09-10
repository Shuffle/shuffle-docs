# Vulnerabilities in Shuffle Security

Documentation for managing, prioritizing, and automating vulnerability remediation across your infrastructure, code, cloud, and identity assets in Shuffle Security.

## Table of contents
* [Why Vulnerability Management in Shuffle?](#why-vulnerability-management-in-shuffle)
* [The four vulnerability categories](#the-four-vulnerability-categories)
* [Prioritization with EPSS, CISA KEV & Threat Intel](#prioritization-with-epss-cisa-kev--threat-intel)
* [Ingest: Vulnerability scanners & pipelines](#ingest-vulnerability-scanners--pipelines)
* [The Vulnerabilities dashboard](#the-vulnerabilities-dashboard)
* [Asset tracking & Host Monitors](#asset-tracking--host-monitors)
* [SOC & DevOps use cases](#soc--devops-use-cases)
* [Automation & auto-ticketing](#automation--auto-ticketing)
  * [Vulnerability Automation Readiness](#vulnerability-automation-readiness)
* [AI Agents for Vulnerabilities](#ai-agents-for-vulnerabilities)
* [API & Datastore access](#api--datastore-access)

---

## Why Vulnerability Management in Shuffle?

Shuffle is an open-source security orchestration, automation, and response (SOAR) platform. **Shuffle Security** ([shuffle.security](https://shuffle.security)) is our dedicated SecOps application built directly on top of Shuffle Core.

Most vulnerability scanners dump thousands of CVEs into a spreadsheet or static dashboard with zero context. Security teams drown in backlogs, IT teams ignore generic 500-page PDF reports, and critical zero-days get lost in the noise of low-priority informational alerts.

We built **Vulnerabilities** in Shuffle Security ([shuffle.security/vulnerabilities](https://shuffle.security/vulnerabilities)) to turn passive scan results into **active, automated remediation**.

> [!NOTE]
> **Available to Everyone — Zero License Paywalls**  
> Vulnerabilities is a native feature included for **everyone**—whether you are using Shuffle Cloud or running self-hosted Shuffle Open Source via Docker Compose or Kubernetes.  
> There are no per-seat licenses, no per-host fees, and no gated enterprise tiers. It doesn't cost anything extra except standard **app runs** when your automations execute (e.g. running an ingestion workflow, querying threat intel, or triggering an automated patch playbook). If your workflows aren't actively running, it costs nothing.

### Seamlessly Engrained in Shuffle Core

Under the hood, all vulnerability records are stored directly in **`shuffle-security_vulns`** inside Shuffle Core's Datastore (OpenSearch). 

Because findings live in the same datastore as the rest of your Shuffle environment:
1. **Context-Driven Prioritization**: We cross-reference CVEs against real-world exploitation metrics (**EPSS** and **CISA KEV**) and live Threat Intelligence feeds so you focus on what is actually being exploited right now.
2. **Direct Host & Asset Mapping**: Vulnerabilities are tied directly to active endpoints, cloud resources, and repositories monitored by Shuffle [Host Monitors](/docs/monitors) and asset inventories.
3. **Automated Remediation**: You don't just stare at vulnerabilities—you trigger patch playbooks, generate pull requests, notify asset owners, or escalate urgent flaws directly into [Incidents](/docs/incidents) with a single click.
4. **Native Workflow & Python Access**: Any Shuffle workflow or Python app can query, filter, update, or resolve findings using standard datastore actions without needing external connectors.

---

## The four vulnerability categories

Vulnerabilities in modern organizations go far beyond unpatched operating system packages. Shuffle organizes findings across four distinct categories:

| Category | Category Key | What it covers | Common Sources |
| :--- | :--- | :--- | :--- |
| **Software / CVE** | `software_cve` | OS packages, kernel vulnerabilities, installed desktop and server software. | Wazuh, Tenable, Qualys, Rapid7, Defender |
| **User / Identity** | `user_identity` | Stale MFA, compromised credentials, overprivileged accounts, exposed API keys. | Okta, Azure AD / Entra ID, Google Workspace |
| **Cloud Misconfig** | `cloud_misconfig` | Open S3 buckets, permissive security groups, unencrypted EBS volumes, IAM drift. | AWS Inspector, Wiz, Prisma Cloud, ScoutSuite |
| **Code & Dependencies**| `code_dependency` | Vulnerable open-source packages in git repos or local developer workspaces (npm, pip, go.mod, cargo). | Snyk, GitHub Dependabot, Shuffle Code Scanner |

---

## Prioritization with EPSS, CISA KEV & Threat Intel

A common mistake in vulnerability management is treating every **CVSS 9.8** as an immediate fire drill while ignoring an **8.1**. The reality is that less than 5% of published CVEs are ever exploited in the wild.

Shuffle combines multiple threat intelligence signals directly into the vulnerability queue:

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  CVSS Base Score │  +  │    EPSS Score    │  +  │  CISA KEV Status │
│  (Theoretical)   │     │ (Likelihood %)   │     │ (Active In Wild) │
└──────────────────┘     └──────────────────┘     └──────────────────┘
                                   │
                                   ▼
             ┌──────────────────────────────────────────┐
             │   Actionable Remediation Priority        │
             │   (Focus engineering time on real risks) │
             └──────────────────────────────────────────┘
```

### 1. CISA KEV (Known Exploited Vulnerabilities)
Shuffle flags any CVE present on the U.S. Cybersecurity and Infrastructure Security Agency's (CISA) KEV catalog. If a vulnerability is on this list, threat actors are actively leveraging it to breach organizations today. These are automatically elevated to **Critical** priority in Shuffle.

### 2. EPSS (Exploit Prediction Scoring System)
EPSS predicts the probability (from 0% to 100%) that a software vulnerability will be exploited in the wild within the next 30 days. Shuffle correlates EPSS scores in real time:
- **High EPSS (> 50%)**: Immediate patching or mitigation required, even if the CVSS score is Medium.
- **Low EPSS (< 5%)**: Can be scheduled into standard monthly patch cycles if no public PoC exists.

### 3. Integrated Threat Intelligence
Through Shuffle's threat intel integrations (accessible at `/incidents/threat-feeds`), CVEs and related indicators are enriched with live signals from:
- **AlienVault OTX & VirusTotal**: Detects active weaponized malware samples exploiting the CVE.
- **AbuseIPDB & MISP**: Identifies scanning campaigns probing your perimeter for specific vulnerabilities.

<!-- component:cve-lookup title="Live CVE & Exploit Intelligence Lookup" placeholder="Enter CVE or GHSA (e.g. CVE-2024-3094, CVE-2021-44228)..." -->

> [!TIP]
> **How to Lookup and Triage Any Advisory**  
> - **In the Web App**: Use the interactive search tool above or navigate to **`/vulnerabilities`** and enter the CVE identifier (e.g., `CVE-2024-3094`) in the search bar. Clicking into an advisory queries OSV.dev, real-world exploitation in the CISA KEV catalog, and 30-day EPSS likelihood in real time.  
> - **Via REST API / Terminal**: Query the backend directly from any shell, CI pipeline, or Python automation:  
>   ```bash
>   curl -s -X GET "https://<your-shuffle-instance>/api/v1/vulnerabilities/CVE-2024-3094" \
>     -H "Authorization: Bearer $SHUFFLE_API_KEY" | jq .
>   ```

---

## Ingest: Vulnerability scanners & pipelines

Getting vulnerability data into Shuffle is completely flexible. You can stream scanner results via inbound webhooks or pull them on a schedule:

<!-- component:ingest workflow="Ingest Vulnerabilities" category="vulnerabilities" title="Live Vulnerability Ingestion Pipeline" subtitle="Connect scanners and webhook endpoints that feed into your vulnerability backlog." -->

### 1. Ingestion Webhook (Push)
Stream real-time scan findings directly from your CI/CD pipelines, container registries, or security scanners.

> [!TIP]
> **Where is the Ingestion Webhook located in the UI?**  
> 1. Go to **`/vulnerabilities`** in Shuffle Security.  
> 2. Look at the top header bar directly above the vulnerabilities table: you'll see the **Ingest** pill row.  
> 3. Click the **"Webhook"** button next to "+".  
> 4. A modal opens displaying your unique **Vulnerability Webhook URL** (`https://<instance>/api/v1/hooks/webhook_<org_id>_vulnerabilities`), an enable/disable toggle switch, and a **"Copy Webhook URL"** button.  
> 5. Configure this URL in your scanner or CI/CD webhook settings to push findings in JSON format automatically.

<!-- TODO: Screenshot Needed: Vulnerabilities Ingestion Webhook Dialog
- Route / UI Location: /vulnerabilities -> Click "Webhook" button in the Ingest pill row above the table.
- What to capture: The open Webhook dialog displaying the dedicated vulnerability push URL (webhook_<org_id>_vulnerabilities), enable/disable toggle, and sample curl payload.
- Recommended filename: assets/vulnerabilities-webhook-modal.png
- Inject syntax: ![Vulnerabilities Ingestion Webhook Dialog](https://raw.githubusercontent.com/Shuffle/Shuffle-docs/master/assets/vulnerabilities-webhook-modal.png)
-->

### 2. "Ingest Vulnerabilities" Workflow (Scheduled Pull)
Shuffle provides a pre-built **Ingest Vulnerabilities** workflow that runs on a recurring schedule (e.g. every 12 hours). It connects to your authenticated scanner APIs:
- **Tenable.io / Nessus**: Fetch recent scan reports and target assets.
- **Qualys VMDR**: Pull host detections and QIDs.
- **Snyk & GitHub Dependabot**: Query repo dependency alerts.
- **AWS Inspector / Defender Vulnerability Management**: Retrieve cloud workload findings.
- **Wazuh Vulnerability Detector**: Ingest endpoint CVE matches detected by host agents.

You can click the **Sync Now** button in the Ingest pill row to immediately trigger polling.

### 3. Schemaless Ingestion to Normalized Findings
Just like [Incidents](/docs/incidents#schemaless-ingest--translation-to-ocsf), vulnerability ingestion in Shuffle is **schemaless**. You don't have to write complex database schemas for each vendor. Shuffle ingests the arbitrary JSON payload, extracts the CVE identifier, asset details, and description, and creates a normalized vulnerability record while keeping the raw scanner output intact for auditing.

---

## The Vulnerabilities dashboard

The main workspace at **`/vulnerabilities`** is engineered to help teams isolate high-risk flaws without getting buried in thousands of informational entries:

<!-- component:vuln-status title="Live Vulnerability Backlog & Prioritization" subtitle="Live CVE findings, severity breakdown, and exploit likelihood tracked in your environment." -->

The vulnerability backlog organizes findings across clear severity and exploitation tiers:

| Risk Tier | Criteria | Remediation SLA | Recommended SOC / Engineering Action |
| :--- | :--- | :--- | :--- |
| **Critical** | CISA KEV listed, EPSS > 50%, or CVSS ≥ 9.0 | 24 - 48 Hours | Immediate patch deployment via Ansible/SSM, or temporary network isolation of affected host. |
| **High** | Public weaponized PoC available, or CVSS 7.0 - 8.9 | 7 Days | Schedule patch release or apply vendor mitigations in the current sprint. |
| **Medium** | Theoretical exploit requiring local access, or CVSS 4.0 - 6.9 | 30 Days | Bundle into standard monthly patch cycles. |
| **Low / Info** | Minimal impact, hardened configuration needed | Best Effort | Review during quarterly infrastructure baselines. |

- **Header Bar & Category Filter Tabs**:
  - **Category Tabs**: Switch views instantly between:
    - `All`: Full organizational vulnerability backlog.
    - `Software / CVE`: OS packages and installed binaries.
    - `User / Identity`: MFA drift, compromised credentials, and excessive IAM permissions.
    - `Cloud Misconfig`: Exposed cloud buckets, network security groups, and cloud posture issues.
    - `Code / Deps`: Vulnerable open-source packages across repositories and developer endpoints.
  - **Ingest Row**: Access the Webhook configuration dialog and manage active scanner connections.
  - **Search & Quick Toggles**: Filter by text, or toggle **CISA KEV** and **High EPSS (> 50%)** with one click.
- **The Vulnerabilities Table Columns**:
  - **Severity**: Color-coded severity badge (`Critical` red, `High` orange, `Medium` yellow, `Low` green, `Info` blue).
  - **Identifier / CVE**: Standard identifier (e.g. `CVE-2024-6387`, `AWS-S3-OPEN-BUCKET`).
  - **Title & Description**: Clear summary of the flaw and its potential impact.
  - **Category**: Category pill indicator.
  - **EPSS**: Live exploit prediction percentage showing likelihood of in-the-wild exploitation.
  - **CISA KEV**: Glowing red indicator if listed on CISA's Known Exploited Vulnerabilities catalog.
  - **Affected Assets**: Count badge showing how many hosts, cloud instances, or repos are affected.
  - **Status**: Current lifecycle status (`Open`, `In Progress`, `Resolved`, `False Positive`).
- **Vulnerability Detail Drawer (`VulnerabilitySidebar`)**: Clicking any row slides open a detailed investigation drawer showing full CVSS metrics, EPSS breakdown, vendor advisory links, all mapped host monitors/cloud assets, and buttons to trigger remediation workflows.
- **Asset Posture View (`/vulnerabilities/assets`)**: Switch to the Assets tab to view vulnerabilities aggregated by host or container image.

<!-- TODO: Screenshot Needed: Vulnerabilities Dashboard Table & Filters
- Route / UI Location: /vulnerabilities
- What to capture: Full view of the /vulnerabilities table with sample findings across categories, showing category tabs (Software / CVE, User / Identity, Cloud Misconfig, Code / Deps), CISA KEV badge, EPSS score percentages, and affected asset count badges.
- Recommended filename: assets/vulnerabilities-dashboard-overview.png
- Inject syntax: ![Vulnerabilities Dashboard Overview](https://raw.githubusercontent.com/Shuffle/Shuffle-docs/master/assets/vulnerabilities-dashboard-overview.png)
-->

<!-- TODO: Screenshot Needed: Vulnerability Detail Drawer (VulnerabilitySidebar)
- Route / UI Location: /vulnerabilities -> Click any vulnerability row (e.g. CVE-2024-6387)
- What to capture: The slide-out VulnerabilitySidebar showing CVSS severity breakdown, EPSS score & percentile, affected host monitor list, and automated remediation action buttons.
- Recommended filename: assets/vulnerabilities-detail-drawer.png
- Inject syntax: ![Vulnerability Detail Drawer](https://raw.githubusercontent.com/Shuffle/Shuffle-docs/master/assets/vulnerabilities-detail-drawer.png)
-->

---

## Asset tracking & Host Monitors

A CVE has no meaning without knowing **where** it lives. Shuffle links vulnerabilities directly to affected systems at `/vulnerabilities/assets`:

- **Host Monitors**: If you deploy Shuffle [Host Monitors](/docs/monitors) on servers, laptops, or cloud VMs, Shuffle automatically correlates discovered vulnerabilities with the host's operating system, installed software list, and active processes.
- **Cloud Assets**: Correlate cloud misconfigurations with AWS EC2 instances, S3 buckets, Azure VMs, or GCP projects.
- **Code Repositories**: Track which git repos and container images contain vulnerable packages.

Clicking on any asset reveals its complete security posture: open vulnerabilities, compliance check status, assigned incidents, and available response actions.

<!-- TODO: Screenshot Needed: Asset-Centric Vulnerabilities Posture View
- Route / UI Location: /vulnerabilities/assets
- What to capture: The /vulnerabilities/assets view grouping detected flaws by host and cloud instance, showing device hostname, OS platform, total CVE counts, and severity distribution bar.
- Recommended filename: assets/vulnerabilities-assets-view.png
- Inject syntax: ![Asset Vulnerability Posture View](https://raw.githubusercontent.com/Shuffle/Shuffle-docs/master/assets/vulnerabilities-assets-view.png)
-->

---

## SOC & DevOps use cases

Shuffle connects vulnerability discovery directly to automated remediation workflows.

<!-- component:usecases category="vulnerabilities" -->

Here are practical use cases you can deploy:

### 1. Automated Patch Orchestration
- **Trigger**: Ingest a new vulnerability with `CISA KEV = True` on an Ubuntu production server.
- **Action**: Shuffle validates that a patched package version is available in apt.
- **Execution**: The workflow triggers an Ansible playbook or AWS Systems Manager (SSM) document to patch the package during the designated maintenance window, then re-runs the vulnerability check to verify resolution.

### 2. Code Dependency Gate in CI/CD
- **Trigger**: Snyk or Dependabot identifies a high-severity remote code execution flaw in an `npm` or `pip` package.
- **Enrichment**: Shuffle checks the EPSS score. If the likelihood is high, Shuffle posts an alert directly into the engineering team's Slack/Teams channel with the suggested upgrade version and automatically creates a Jira ticket.

### 3. Emergency Zero-Day Fleet Audit
- **Scenario**: A new zero-day vulnerability (e.g. Log4Shell or OpenSSH regreSSHion) is publicly disclosed with no CVE score yet.
- **Action**: Use Shuffle [Host Monitors](/docs/monitors) to run an immediate software inventory scan across your entire fleet of 1,000+ endpoints.
- **Result**: In minutes, Shuffle lists every host running the vulnerable package version and flags them for urgent mitigation.

### 4. Vulnerability-to-Incident Escalation
- If a vulnerability remains unpatched past your organization's SLA (e.g. 14 days for Critical), Shuffle can automatically escalate the finding into a formal [Incident](/docs/incidents) to initiate executive escalation and tracking.

Explore pre-built automation templates in [Use Cases](/usecases).

---

## Automation & auto-ticketing

You shouldn't have to manually copy CVE IDs into Jira or ServiceNow. Shuffle provides built-in automated ticket synchronization:

1. **Jira & ServiceNow Sync**: Configure category automations in `/vulnerabilities` to automatically create and synchronize tickets in your engineering issue tracker whenever a new High or Critical vulnerability is identified.
2. **Status Synchronization**: When developers resolve the ticket or the scanner reports the vulnerability as resolved on the next scan, Shuffle automatically closes the vulnerability in your dashboard.
3. **Task Playbooks**: Attach custom remediation playbooks to individual vulnerabilities so analysts can click a single button to execute workarounds (e.g. blocking an affected port on a firewall or disabling a vulnerable service).

### Vulnerability Automation Readiness

Before handling security findings across your fleet, Shuffle Security audits whether your vulnerability ingestion, asset correlation, and automated remediation pipelines are active. The **Automation Readiness** banner checks four vital pipeline stages:

<!-- component:automation-readiness category="vulnerabilities" -->

| Readiness Pillar | Verification Check | Target Workflow | Purpose & Manual Configuration |
| :--- | :--- | :--- | :--- |
| **Webhook Ingestion** | Inbound webhook active | `vulnerability_ingestion_1` (webhook) | Receives push notifications from scanner pipelines (e.g. Snyk, GitHub Dependabot, Wazuh). Toggle at `/vulnerabilities` -> **Ingest** header. |
| **Scanner Polling Ingestion** | Scheduled workflow | `vulnerability_ingestion_1` (schedule) | Regularly polls vulnerability scanner APIs (Qualys, Tenable, AWS Inspector) for newly published findings. Activate in [`/usecases`](/usecases). |
| **Vulnerability Correlation** | Active workflow | `asset_management_case_management_vuln_1` | Correlates CVEs against active assets, live Host Monitors, EPSS risk probabilities, and CISA KEV tags. Activate in [`/usecases`](/usecases). |
| **Automated Response** | Active workflow | `asset_management_case_management_vuln_response_1` | Automatically creates Jira/ServiceNow tickets, triggers Ansible/SSM patch playbooks, and escalates overdue critical flaws to [Incidents](/docs/incidents). Activate in [`/usecases`](/usecases). |

```
┌────────────────────────────────────────────────────────────────────────┐
│                   Vulnerability Automation Readiness                   │
├────────────────────────┬───────────────────────────────────────────────┤
│ Webhook Ingestion      │ [Active]    api/v1/hooks/webhook_<org_id>_vulns │
│ Scanner Polling Ingest │ [Active]    vulnerability_ingestion_1        │
│ Vuln Correlation       │ [Active]    asset_management_case_..._vuln_1 │
│ Automated Response     │ [Active]    asset_management_case_..._resp_1 │
└────────────────────────┴───────────────────────────────────────────────┘
```

> [!TIP]
> **Inspecting and Toggling Readiness in the UI**  
> 1. In the web application, this readiness card is rendered at **`/vulnerabilities`** (docked at the top of the findings table or in the automation drawer) and in **`/usecases`**.  
> 2. Clicking any row opens the use case drawer to view the live workflow diagram, configured apps, and execution history in-place.  
> 3. Click **"Enable all"** on the card to activate all unconfigured checks at once, or configure them individually via REST API:  
>    ```bash
>    # Trigger initial vulnerability configuration seeding
>    curl -s -X POST "https://<your-shuffle-instance>/api/v1/usecases/setup_defaults" \
>      -H "Authorization: Bearer $SHUFFLE_API_KEY" \
>      -H "Content-Type: application/json" \
>      -d '{"category": "vulnerabilities"}' | jq .
>    ```

<!-- TODO: Screenshot Needed: Vulnerability Automation Readiness Card
- Route / UI Location: /vulnerabilities -> Top of queue or automation drawer
- What to capture: The Automation Readiness card showing all 4 green check status rows (Webhook Ingestion, Scanner Polling Ingestion, Vulnerability Correlation, Automated Response) and the "Enable all" button.
- Recommended filename: assets/vulnerabilities-automation-readiness.png
- Inject syntax: ![Vulnerability Automation Readiness Card](https://raw.githubusercontent.com/Shuffle/Shuffle-docs/master/assets/vulnerabilities-automation-readiness.png)
-->

---

## AI Agents for Vulnerabilities

Shuffle Security integrates with **Shuffle AI** through the `shuffle_vulnerabilities` MCP tool to accelerate triage:

<!-- component:ask-ai label="Ask AI about Vulnerabilities" input="What are the highest risk CVEs in our environment based on CISA KEV and EPSS?" -->

- **Instant Risk Assessment**: Ask the agent: *"Summarize our top 5 most critical vulnerabilities that have known public exploits."*
- **Remediation Script Generation**: Request a mitigation script: *"Generate a bash command to mitigate CVE-2024-6387 on Ubuntu 22.04 without restarting the server."*
- **Executive Reporting**: Ask AI to compile a weekly vulnerability status report highlighting patched vs. open risks for your CISO.

---

## API & Datastore access

All vulnerability records are stored directly in Shuffle Core's Datastore under the **`shuffle-security_vulns`** category. You can query, search, and manage findings programmatically via the Shuffle REST API or inside custom Python apps:

### REST API Endpoints
- **List Vulnerabilities from Datastore**: `GET /api/v1/orgs/{org_id}/list_cache?category=shuffle-security_vulns&top=100`
- **Filter by Severity / Status**: `GET /api/v1/vulnerabilities?status=open&severity=critical`
- **Get Specific Vulnerability**: `GET /api/v1/vulnerabilities/{id}` (or `GET /api/v1/orgs/{org_id}/get_cache?category=shuffle-security_vulns&key={id}`)
- **Create / Ingest Finding**: `POST /api/v1/vulnerabilities`
- **Update Finding or Status**: `PUT /api/v1/vulnerabilities/{id}` (e.g. `{ "status": "resolved" }`)

### In Custom Python Apps & Workflows
```python
# Query a vulnerability record directly from Shuffle's datastore
vuln = self.get_cache("cve_2024_6387", category="shuffle-security_vulns")

# Check risk metrics
if vuln and vuln.get("epss", 0) > 0.5:
    print(f"High risk vulnerability detected on {vuln.get('affected_assets_count')} assets!")

# Save, enrich, or update a finding
self.set_cache("cve_2024_6387", vuln_data, category="shuffle-security_vulns")
```

For more details on backend API endpoints and authentication, see our [API documentation](/docs/API).
