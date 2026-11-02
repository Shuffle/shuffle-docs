# Vulnerabilities in Shuffle Security

Documentation for triaging vulnerabilities, looking up CVE/GHSA advisories, tracking affected hosts and packages, and automating remediation workflows in Shuffle Security.

## Table of contents
* [Overview](#overview)
* [Using the Vulnerabilities dashboard](#using-the-vulnerabilities-dashboard)
* [Looking up & ingesting vulnerabilities](#looking-up--ingesting-vulnerabilities)
* [Vulnerability categories](#vulnerability-categories)
* [Host & package correlation](#host--package-correlation)
* [Automating vulnerability management](#automating-vulnerability-management)
* [Datastore architecture & finding schema](#datastore-architecture--finding-schema)
* [API & Datastore reference](#api--datastore-reference)

---

## Overview

Shuffle Security ([shuffle.security/vulnerabilities](https://shuffle.security/vulnerabilities)) helps you discover, prioritize, and remediate vulnerabilities across your endpoints, cloud infrastructure, user identities, and code dependencies.

Instead of tracking scanner exports in static spreadsheets, you can see exactly which hosts and file paths are affected by a CVE, track per-host patching status, look up live advisories, and trigger automated remediation playbooks.

- **Unified Vulnerability Queue**: Filter findings by category (`Software / CVE`, `User / Identity`, `Cloud Misconfig`, `Code / Deps`), severity, and remediation status at `/vulnerabilities`.
- **Live OSV.dev Advisory Lookup**: Search any CVE, GHSA, or open-source package name (npm, PyPI, Go, Cargo, Maven, Debian, Alpine) to inspect affected versions and published fixes immediately.
- **Host & Package Correlation**: Endpoints running [Host Monitors](/docs/monitors) scan installed software and local code manifests (`package.json`, `requirements.txt`, `Cargo.toml`, `go.mod`), linking advisories to exact hostnames and filesystem paths.
- **Per-Host Resolution Tracking**: Mark vulnerabilities individually per host as `Patched`, `Mitigated`, `Accepted`, `False Positive`, or `Not Applicable`.
- **Workflow Automation**: Automatically ingest scanner results, notify engineering teams in Slack/Teams, open Jira tickets, or escalate critical unpatched flaws into [Incidents](/docs/incidents).

> [!NOTE]
> **Zero License Paywalls**  
> Vulnerabilities is included in both Shuffle Cloud and self-hosted open-source instances with no per-seat or per-asset license fees. App runs only execute when your automation workflows trigger.

---

## Using the Vulnerabilities dashboard

Navigate to **`/vulnerabilities`** to view and triage findings across your organization:

<!-- component:vulnerabilities-status title="Vulnerabilities Posture" subtitle="Active vulnerability findings tracked across your tenant." -->

### Navigation & Filtering
- **Category Tabs**: Switch between `All`, `Software / CVE`, `User / Identity`, `Cloud Misconfig`, and `Code / Deps`.
- **Severity Filter**: Filter by `Critical`, `High`, `Medium`, `Low`, or `Info`.
- **Status Filter**: View `Open`, `In Progress`, `Resolved`, or `Accepted` findings.
- **Search Bar**: Search by CVE/GHSA identifier, affected package name, hostname, or keyword.

### Table Columns
- **Severity**: Normalized severity rating (`Critical`, `High`, `Medium`, `Low`, `Info`) and CVSS score.
- **Identifier / Title**: Advisory identifier (e.g. `CVE-2024-3094`) with a summary headline.
- **Category**: Classification badge (`software_cve`, `code_dependency`, `user_identity`, `cloud_misconfig`).
- **Source**: Discovery origin (e.g. `osv:npm`, `osv:pypi`, host monitor, or external scanner).
- **Status**: Current lifecycle state (`Open`, `In Progress`, `Resolved`, `Accepted`).
- **First Seen**: Timestamp when the finding was first detected.

### Vulnerability Detail View (`/vulnerabilities/:id`)
Clicking any finding opens its detail page at `/vulnerabilities/:id`, where you can:
- Read the full advisory description, CVSS score, published/modified dates, and upstream references.
- Inspect affected package ecosystems, vulnerable version ranges, and the minimum fixed version.
- View every affected host along with the exact filesystem path where the package was found.
- Update the overall status or set a per-host resolution status.
- Ask the inline AI assistant questions about exploitability, remediation steps, or upgrade impact.

<!-- TODO: Screenshot Needed: Vulnerabilities Dashboard Table & Filters
- Route / UI Location: /vulnerabilities
- What to capture: Full view of the /vulnerabilities table showing category tabs, search input, and severity breakdown.
- Target path: assets/vulnerabilities-dashboard-overview.png -->

---

## Looking up & ingesting vulnerabilities

Shuffle provides multiple ways to look up advisories and bring vulnerability findings into your queue:

<!-- component:cve-lookup title="Live OSV Advisory Lookup" placeholder="e.g. CVE-2024-3094, GHSA-xxxx, or package name" -->

### 1. Live OSV.dev Advisory Lookup
Use the lookup bar above, or enter any CVE ID (e.g. `CVE-2024-3094`), GitHub Security Advisory ID (e.g. `GHSA-xxxx-xxxx-xxxx`), or package name into the search bar at **`/vulnerabilities`**:
- Shuffle queries OSV.dev (`https://api.osv.dev/v1/vulns/<id>`) in real time to display advisory details, severity, affected version ranges, and fixed versions—even if the CVE has not been ingested into your tenant yet.

### 2. Host Monitor Code & Software Scanner
When endpoints run Shuffle [Host Monitors](/docs/monitors) with **Installed Software** or **Code Package Scanner** enabled:
- The monitor agent catalogs installed OS applications and scans local project directories for manifest files (`package.json`, `requirements.txt`, `Cargo.toml`, `go.mod`).
- Discovered packages and versions are evaluated against OSV.dev and synced directly into `/vulnerabilities` with the affected hostname and file path.
- You can also browse any discovered package at `/packages/<name>` or software binary at `/software/<name>` and click **Sync to Vulnerabilities** to persist affected advisories.

### 3. Inbound Webhook (Push from CI/CD & Scanners)
Push findings from CI/CD pipelines, container scanners (Trivy, Grype), or external vulnerability tools directly into Shuffle:
- Navigate to **`/vulnerabilities`** and click the **Webhook** button in the top header bar.
- Copy your inbound webhook endpoint:
  ```
  https://<instance>/api/v1/hooks/webhook_<hook_id>
  ```
- Send scanner JSON payloads to this URL to trigger the `vulnerabilities_webhook` workflow and normalize findings into your queue.

### 4. Polling Scanners (Scheduled Pull)
Connect vulnerability scanners (such as Snyk, Qualys, Tenable, or Rapid7) using the source icons in the `/vulnerabilities` header bar. Scheduled workflows (such as `Ingest Vulnerabilities`) pull findings on a regular cadence, deduplicate advisories, and update affected hosts.

<!-- TODO: Add step-by-step scanner integration guides for specific vendor API mappings (Snyk, Qualys, Tenable, Defender) -->

<!-- TODO: Screenshot Needed: Ingestion Webhook Dialog
- Location: /vulnerabilities -> Webhook button in header
- What to capture: Modal showing the webhook URL, toggle switch, and curl command
- Target path: assets/vulnerabilities-webhook-modal.png -->

---

## Vulnerability categories

Shuffle organizes findings into four categories so you can filter by remediation owner (SecOps, IT/Endpoint, Cloud Engineering, or Application Developers):

| Category | Identifier Key | Scope & Typical Sources |
| :--- | :--- | :--- |
| **Software / CVE** | `software_cve` | Operating system packages, installed desktop applications, and server binaries. |
| **User / Identity** | `user_identity` | IAM drift, missing MFA, stale credentials, and excessive privileges. |
| **Cloud Misconfig** | `cloud_misconfig` | Open storage buckets, permissive firewall rules, and cloud infrastructure drift. |
| **Code / Dependencies** | `code_dependency` | Third-party packages and libraries scanned from code repositories (`package.json`, `requirements.txt`, `Cargo.toml`, `go.mod`). |

---

## Host & package correlation

A vulnerability finding is much easier to remediate when you know exactly which machines and repositories are affected.

When Host Monitors or asset scans detect a vulnerable package, Shuffle links the finding to each affected host:
- **Hostname & Asset ID**: Identifies the exact endpoint or server running the vulnerable software or dependency.
- **Filesystem Paths**: Shows the exact path where the binary or manifest was found (e.g. `/home/user/projects/web-api/package.json` or `/usr/lib/x86_64-linux-gnu/liblzma.so.5.6.0`).
- **Installed vs. Fixed Version**: Compares the currently installed version on the host against the minimum patched version from the advisory.

### Per-Host Resolution Status
Because a vulnerability may affect dozens of machines that get patched at different times, you can update the resolution status individually for each host inside `/vulnerabilities/:id`:

| Resolution Reason | Meaning |
| :--- | :--- |
| **Patched** | The dependency or software package on this host has been upgraded to a non-vulnerable version. |
| **Mitigated** | Compensating controls (such as network ACLs or disabled features) neutralize the flaw on this host. |
| **Accepted** | Risk is formally accepted for this host. |
| **False Positive** | The detected package is not exploitable in this specific environment. |
| **Not Applicable** | The vulnerable function or subcomponent is not used on this host. |

---

## Automating vulnerability management

Shuffle Security verifies whether your core vulnerability ingestion, correlation, and response workflows are active:

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
> Click **Enable all** on the readiness banner at `/vulnerabilities` (or click the rocket button in the `/vulnerabilities` header bar) to configure automatic ingestion and response workflows.

### Vulnerability Use Cases

<!-- component:usecases category="vulnerabilities" -->

---

## Datastore architecture & finding schema

Under the hood, all vulnerability findings are stored in Shuffle's Datastore under the **`shuffle-security_vulns`** category. Each entry is keyed by its primary advisory identifier (e.g. `CVE-2024-3094` or `GHSA-7867-xwm8-2v3q`) and stores a structured JSON document.

<!-- component:datastore category="shuffle-security_vulns" -->

You can inspect, query, and modify raw records in the Datastore console:
- **Shuffle Security Datastore**: Navigate to [`/admin/datastore?category=shuffle-security_vulns`](/admin/datastore?category=shuffle-security_vulns). Queries the local datastore if configured, and falls back to Shuffle Core if local storage is not initialized.
- **Shuffle Datastore**: [Open in Shuffle Datastore](https://shuffler.io/admin?tab=datastore&category=shuffle-security_vulns) (`https://shuffler.io/admin?tab=datastore&category=shuffle-security_vulns` or `/admin?tab=datastore&category=shuffle-security_vulns` on self-hosted instances).
- **Manual UI Navigation**: Go to **Admin** -> **Datastore** -> select category **`shuffle-security_vulns`**.

### Deleting Erroneously Ingested Vulnerabilities (Admin Only)

In day-to-day triage at [`/vulnerabilities`](/vulnerabilities), findings are resolved, mitigated, or accepted rather than deleted so your audit history stays intact.

If a scanner misbehaved or a test script ingested dummy CVEs that need to be permanently removed, an admin (`isAdmin`) can delete them in the Datastore:

1. Navigate to **Admin** -> **Datastore**, or open [`/admin/datastore?category=shuffle-security_vulns`](/admin/datastore?category=shuffle-security_vulns).
2. Search for the vulnerability key you want to remove (such as `CVE-2024-3094`).
3. **Delete one finding**: Click the delete button on the right side of the row and confirm.
4. **Bulk cleanup**: Select the checkboxes next to the records you want to remove and click **Delete Selected** in the bulk action bar.

### Vulnerability Record Schema

| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | String | Canonical advisory identifier (e.g. `CVE-2024-3094`, `GHSA-xxxx`). Serves as the primary datastore key. |
| `title` | String | Descriptive title or headline of the vulnerability. |
| `severity` | String | Severity rating: `critical`, `high`, `medium`, or `low`. |
| `score` | Number | CVSS base numerical score (e.g. `10.0` or `7.4`). |
| `category` | String | Classification: `software_cve`, `code_dependency`, `user_identity`, or `cloud_misconfig`. |
| `status` | String | Workflow status: `open`, `in_progress`, `mitigated`, `accepted`, or `resolved`. |
| `affected_package` | String | Name and version constraint of the affected component (e.g. `xz-utils 5.6.0`, `lodash <4.17.21`). |
| `fixed_version` | String | Minimum version containing the remediation patch (e.g. `5.6.1`). |
| `affected_hosts` | Array | Endpoints running the vulnerable software or dependency, including `hostname`, filesystem `path`, and per-host `resolution`. |

### Writing Findings in Python Apps & Workflows

```python
# Upsert or update a vulnerability finding
vuln_payload = {
    "id": "CVE-2024-3094",
    "title": "XZ Utils Backdoor (liblzma)",
    "severity": "critical",
    "score": 10.0,
    "category": "software_cve",
    "status": "open",
    "affected_package": "xz-utils 5.6.0",
    "fixed_version": "5.6.1",
    "affected_hosts": [
        {
            "hostname": "srv-prod-db-01",
            "path": "/usr/lib/x86_64-linux-gnu/liblzma.so.5.6.0",
            "resolution": "open"
        }
    ]
}

# Write to Datastore
self.set_cache(
    key="CVE-2024-3094",
    value=vuln_payload,
    category="shuffle-security_vulns"
)
```

### Key Revisions, Audit Trail & Rollback Protection

All vulnerability records stored in `shuffle-security_vulns` are versioned with immutable revisions. Every scanner sweep, automated triage run, or manual status change preserves historical snapshots:

- **Protection Against Ingestion Drift & Overwrites**: If an external scanner runs an incomplete scan that drops existing CVE findings or overwrites host resolutions, previous revisions remain accessible and can be restored.
- **Audit Attribution**: Tracks which workflow execution or analyst changed the finding's severity, updated the CVSS score, or marked a host as mitigated, complete with timestamps and execution IDs.
- **Rollback via API & Workflows**:
  - Fetch all revisions for a vulnerability advisory:
    ```bash
    curl "https://shuffler.io/api/v2/datastore/category/shuffle-security_vulns/{cve_id}/revisions" \
      -H "Authorization: Bearer <api_key>"
    ```
  - Roll back or restore in Python:
    ```python
    revisions = self.get_cache_revisions(key="CVE-2024-3094", category="shuffle-security_vulns")
    if len(revisions) > 1:
        self.set_cache(
            key="CVE-2024-3094",
            value=revisions[1]["value"],
            category="shuffle-security_vulns"
        )
    ```

---

## API & Datastore reference

<!-- component:datastore-link category="shuffle-security_vulns" -->

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
