# Vulnerabilities in Shuffle Security

Documentation for vulnerability management, package advisory lookups via OSV.dev, host dependency tracking, and automated remediation workflows in Shuffle Security.

## Table of contents
* [Overview](#overview)
* [Vulnerability categories](#vulnerability-categories)
* [Ingestion: webhooks, scanners & OSV](#ingestion-webhooks-scanners--osv)
* [Host & package correlation](#host--package-correlation)
* [The Vulnerabilities dashboard](#the-vulnerabilities-dashboard)
* [Automation readiness](#automation-readiness)
* [API & Datastore reference](#api--datastore-reference)

---

## Overview

Shuffle Security ([shuffle.security/vulnerabilities](https://shuffle.security/vulnerabilities)) tracks vulnerabilities across your infrastructure, third-party software, and code dependencies.

Instead of maintaining a passive spreadsheet of scanner outputs, Shuffle stores vulnerability findings inside Shuffle Core's Datastore under the **`shuffle-security_vulns`** category. Findings can be queried, filtered, enriched, and acted upon using standard Shuffle workflows.

- **OSV.dev Integration**: Look up CVE and GHSA advisories across open-source ecosystems (npm, PyPI, Go, Cargo, Maven, Debian, Alpine, etc.) directly via the OSV.dev API.
- **Host Package Correlation**: Monitored endpoints running [Host Monitors](/docs/monitors) inspect local project directories and installed software, linking detected CVEs to specific hostnames and filesystem paths.
- **Per-Host Resolution**: Mark vulnerabilities per host as Patched, Mitigated, Accepted, False Positive, or Not Applicable.
- **Workflow Automation**: Build SOAR workflows to automatically ingest scan reports, alert development teams in Slack/Teams, create Jira issues, or escalate unpatched critical flaws into formal [Incidents](/docs/incidents).

> [!NOTE]
> **Zero License Paywalls**  
> Vulnerabilities is a native feature available on both Shuffle Cloud and self-hosted open-source instances. Findings and host telemetry are stored directly in your datastore and do not incur extra license fees. App runs only execute when your workflows trigger.

---

## Vulnerability categories

Shuffle categorizes findings into four distinct types:

| Category | Identifier Key | Scope & Typical Sources |
| :--- | :--- | :--- |
| **Software / CVE** | `software_cve` | Operating system packages, installed desktop applications, and server binaries. |
| **User / Identity** | `user_identity` | IAM drift, missing MFA, stale credentials, and excessive privileges. |
| **Cloud Misconfig** | `cloud_misconfig` | Open storage buckets, permissive firewall rules, and cloud infrastructure drift. |
| **Code / Dependencies** | `code_dependency` | Third-party packages and libraries scanned from code repositories (`package.json`, `requirements.txt`, `Cargo.toml`, `go.mod`). |

---

## Ingestion: webhooks, scanners & OSV

Shuffle supports multiple paths to ingest and look up vulnerabilities:

<!-- component:cve-lookup title="Live OSV Advisory Lookup" placeholder="e.g. CVE-2024-3094, GHSA-xxxx, or package name" -->

### 1. Inbound Webhook
You can push findings from CI/CD pipelines, container scanners, or external security tools directly into Shuffle:
- Go to **`/vulnerabilities`** in the web app.
- Click the **"Webhook"** button in the header bar to open the configuration modal.
- The modal displays your dynamic inbound endpoint:
  ```
  https://<instance>/api/v1/hooks/webhook_<hook_id>
  ```
- Payloads sent to this webhook trigger the `vulnerabilities_webhook` workflow, which normalizes findings and writes them to the datastore.

### 2. Live OSV.dev Lookup
You can query the open-source vulnerability database directly from the Shuffle UI:
- Enter a CVE ID (e.g. `CVE-2024-3094`), a GitHub Advisory ID (e.g. `GHSA-xxxx-xxxx-xxxx`), or an affected package name into the search bar at `/vulnerabilities`.
- The system queries `https://api.osv.dev/v1/vulns/<id>` to display advisory details, severity, affected versions, and published fixes.

### 3. Host Monitor Code Scanner
When endpoints run Shuffle [Host Monitors](/docs/monitors) with the Code Package Scanner enabled, the local agent scans project directories for manifest files (`package.json`, `requirements.txt`, `Cargo.toml`, `go.mod`). Discovered dependencies are evaluated against OSV.dev and registered in `shuffle-security_vulns` with the host's identity and file path.

### 4. Polling Workflows
For external scanners with REST APIs, scheduled Shuffle workflows (such as `Ingest Vulnerabilities`) regularly pull findings, deduplicate entries, and write them to the datastore.

<!-- TODO: Add step-by-step scanner integration guides for specific vendor API mappings (Snyk, Qualys, Tenable, Defender) -->

<!-- TODO: Screenshot Needed: Ingestion Webhook Dialog
- Location: /vulnerabilities -> Webhook button in header
- What to capture: Modal showing the webhook URL, toggle switch, and curl command
- Target path: assets/vulnerabilities-webhook-modal.png -->

---

## Host & package correlation

A vulnerability finding is actionable when you know which systems are affected.

When Host Monitors discover a vulnerable package on an endpoint, Shuffle stores the finding with host-level granularity:

- **Hostname & Asset ID**: Identifies the exact machine running the vulnerable code or package.
- **Filesystem Paths**: Lists the specific directory where the dependency was found (e.g. `/home/user/projects/web-api/package.json`).
- **Installed Version**: Records the current version versus the fixed version from the advisory.

### Per-Host Resolution Status
Because a vulnerability may exist across multiple servers or laptops, you can track resolution status individually for each host in the vulnerability detail view:

| Resolution Reason | Meaning |
| :--- | :--- |
| **Patched** | The dependency or software package has been upgraded to a non-vulnerable version. |
| **Mitigated** | Compensating controls (e.g. network ACLs or disabled features) neutralize the flaw. |
| **Accepted** | Risk is formally accepted by the organization. |
| **False Positive** | The detected package is not exploitable in this specific environment. |
| **Not Applicable** | The vulnerable function or subcomponent is not utilized. |

---

## The Vulnerabilities dashboard

The dashboard at **`/vulnerabilities`** provides an operational overview of all recorded findings:

<!-- component:vulnerabilities-status title="Vulnerabilities Posture" subtitle="Active vulnerability findings tracked across your organization." -->

### Navigation & Filtering
- **Category Tabs**: Switch between `All`, `Software / CVE`, `User / Identity`, `Cloud Misconfig`, and `Code / Deps`.
- **Severity Filter**: Filter by `Critical`, `High`, `Medium`, `Low`, or `Info`.
- **Status Filter**: View `Open`, `In Progress`, `Resolved`, or `Accepted` findings.
- **Search Bar**: Query by identifier, package name, or keywords.

### Table Columns
- **Severity**: Normalized severity indicator (`Critical`, `High`, `Medium`, `Low`, `Info`).
- **Identifier / Title**: CVE or GHSA identifier with a summary of the advisory.
- **Category**: Finding category pill (`code_dependency`, `software_cve`, etc.).
- **Source**: Ingestion origin (e.g. `osv:npm`, `osv:pypi`, or scanner name).
- **Status**: Lifecycle status (`Open`, `In Progress`, `Resolved`, `Accepted`).
- **First Seen**: Timestamp when the finding was first ingested or discovered.

### Detail View
Clicking any finding navigates to `/vulnerabilities/:id`, displaying:
- Complete advisory text, published and modified dates, and references.
- Affected package ecosystems, package names, and version ranges.
- List of affected hosts with install paths and per-host resolution controls.
- AI investigation panel for questions about the advisory.

<!-- TODO: Screenshot Needed: Vulnerabilities Dashboard Table & Filters
- Route / UI Location: /vulnerabilities
- What to capture: Full view of the /vulnerabilities table showing category tabs, search input, and severity breakdown.
- Target path: assets/vulnerabilities-dashboard-overview.png -->

---

## Automation readiness

Shuffle Security checks whether your core vulnerability automation workflows are configured:

<!-- component:automation-readiness category="vulnerabilities" -->

| Readiness Pillar | Verification Check | Target Workflow | Status | Purpose & Configuration |
| :--- | :--- | :--- | :--- | :--- |
| **Vulnerability Webhook** | Inbound webhook trigger running | `vulnerabilities_webhook` | Active | Ingests findings pushed from external scanners. Configure at `/vulnerabilities` -> **Webhook**. |
| **Vulnerability Ingestion** | Schedule trigger running | `Ingest Vulnerabilities` | Active | Regularly polls external vulnerability APIs on a recurring schedule. Activate in [`/usecases`](/usecases). |
| **Vulnerability Correlation** | Workflow exists with actions | `Vulnerability Correlation` | Active | Compares scanner results across runs and correlates findings with assets. Activate in [`/usecases`](/usecases). |
| **Vulnerability Response** | Automated remediation | `asset_management_case_management_vuln_response_1` | In Development | Automated remediation, ticketing, and containment actions for detected vulnerabilities (coming soon). |

```
┌────────────────────────────────────────────────────────────────────────┐
│                   Vulnerability Automation Readiness                   │
├────────────────────────┬───────────────────────────────────────────────┤
│ Vulnerability Webhook  │ [Active]         api/v1/hooks/webhook_<id>    │
│ Vulnerability Ingest   │ [Active]         Ingest Vulnerabilities       │
│ Vuln Correlation       │ [Active]         Vulnerability Correlation    │
│ Vulnerability Response │ [In Development] Coming soon                  │
└────────────────────────┴───────────────────────────────────────────────┘
```

<!-- TODO: Add automated remediation workflow documentation once vulnerability response actions are generally available -->

> [!TIP]
> **Enabling Automations**  
> Click **"Enable all"** on the readiness card to generate and activate the foundational ingestion and correlation workflows, or manage them individually from the `/usecases` page.

---

## API & Datastore reference

All vulnerability findings are stored directly in Shuffle's Datastore under the **`shuffle-security_vulns`** category. You can query, ingest, and update findings via the REST API, inspect them in the Datastore web console, or access them inside custom Shuffle Python apps.

<!-- component:datastore-link category="shuffle-security_vulns" -->

Inspect and manage vulnerability records in the Datastore console:
- Shuffle Security Datastore: Navigate to [`/admin/datastore?category=shuffle-security_vulns`](/admin/datastore?category=shuffle-security_vulns). Uses the local datastore if available, and automatically redirects to Shuffle Core if local datastore is not configured.
- Shuffle Core Datastore: [Open in Shuffle Core Datastore](https://shuffler.io/admin?tab=datastore&category=shuffle-security_vulns) (`https://shuffler.io/admin?tab=datastore&category=shuffle-security_vulns`).
- Manual UI Navigation: Go to **Admin** -> **Datastore** -> select category **`shuffle-security_vulns`**.

### REST API Endpoints

- **List Vulnerabilities**: `GET /api/v1/vulnerabilities`
- **Get Vulnerability Finding**: `GET /api/v1/vulnerabilities/{id}`
- **List Findings from Datastore Directly**:
  ```bash
  curl -X GET "https://<instance>/api/v1/orgs/<org_id>/list_cache?category=shuffle-security_vulns&top=100" \
    -H "Authorization: Bearer $SHUFFLE_API_KEY"
  ```
- **Upsert Finding in Datastore**:
  ```bash
  curl -X POST "https://<instance>/api/v1/orgs/<org_id>/set_cache" \
    -H "Authorization: Bearer $SHUFFLE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
      "category": "shuffle-security_vulns",
      "key": "CVE-2024-3094",
      "value": "{\"id\":\"CVE-2024-3094\",\"title\":\"XZ Utils Backdoor\",\"severity\":\"critical\",\"category\":\"software_cve\",\"status\":\"open\"}"
    }'
  ```

### In Custom Python Apps & Workflows

```python
# Retrieve a vulnerability record from the datastore
vuln = self.get_cache("CVE-2024-3094", category="shuffle-security_vulns")

# Check status or update notes
if vuln and vuln.get("status") == "open":
    print(f"Open vulnerability: {vuln.get('title')}")
    vuln["status"] = "in_progress"
    self.set_cache("CVE-2024-3094", vuln, category="shuffle-security_vulns")
```

For more details on backend API endpoints and datastore caching rules, see the [API documentation](/docs/API).
