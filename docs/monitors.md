# Host Monitors in Shuffle Security

Documentation for endpoint posture monitoring, disk encryption, screen lock enforcement, software inventory, local code package scanning, remote web terminals, and response actions in Shuffle Security.

## Table of contents
* [Overview](#overview)
* [Cross-platform architecture](#cross-platform-architecture)
* [Datastore architecture: assets, software, packages & sensors](#datastore-architecture-assets-software-packages--sensors)
* [Deploying a Host Monitor](#deploying-a-host-monitor)
* [Posture checks](#posture-checks)
* [Installed software inventory](#installed-software-inventory)
* [Code package scanner](#code-package-scanner)
* [Remote web terminal](#remote-web-terminal)
* [Response actions](#response-actions)
* [The Host Monitors dashboard](#the-host-monitors-dashboard)
* [API & Datastore reference](#api--datastore-reference)

---

## Overview

Shuffle Security ([shuffle.security/monitors](https://shuffle.security/monitors)) provides lightweight endpoint posture monitoring and remote response capabilities directly from your Shuffle instance.

Instead of deploying a separate third-party agent that cannot interact with your SOAR workflows, Host Monitors runs **Orborus** (Shuffle's worker binary) in sensor mode (`--sensor_mode=true`).

- **Posture Baselines**: Continuously verifies essential security controls: full-disk encryption and screen lock idle timeouts.
- **Software & Dependency Inventory**: Maintains an inventory of installed applications and scans local developer repositories for vulnerable dependencies (`npm`, `pip`, `cargo`, `go.mod`).
- **Remote Web Terminal**: Connects to endpoints over outbound WebSockets with zero inbound firewall ports required, providing an interactive browser-based shell for live triage.
- **Direct Response Actions**: Executes remote commands and remediation actions on target hosts from the UI or through automated Shuffle workflows.
- **Datastore Integration**: Endpoint records and compliance states are saved in Shuffle Core's Datastore under the **`shuffle-security_sensors`** category (and hardware asset specs under **`shuffle-security_assets`**).

> [!NOTE]
> **Zero License Paywalls**  
> Host Monitors is included in both Shuffle Cloud and self-hosted open-source deployments. There are no per-seat or per-agent license fees. Standard app runs only execute when your automation workflows run (e.g. executing a remediation script or sending an alert). Normal heartbeats and posture checks consume zero app runs.

---

## Cross-platform architecture

The monitor daemon is built into Orborus and runs across major operating systems:

| Platform | Supported Versions | Monitored Controls |
| :--- | :--- | :--- |
| **macOS** | macOS 12 Monterey, 13 Ventura, 14 Sonoma, 15 Sequoia | FileVault 2 disk encryption, screen lock idle timeout, installed applications catalog, local repository manifests |
| **Windows** | Windows 10, Windows 11, Windows Server 2016+ | BitLocker drive protection, screen lock inactivity policy, installed applications, local repository manifests |
| **Linux** | Ubuntu, Debian, RHEL, CentOS, Fedora, Arch | LUKS volume encryption, screen lock idle timeout, system packages, local repository manifests |

---

## Datastore architecture: assets, software, packages & sensors

Host Monitors organizes telemetry and endpoint state across four specialized datastore categories. Instead of bundling hardware specs, application inventories, manifest dependencies, and live heartbeats into a single monolithic document, Shuffle decouples them into distinct categories:

1. **`shuffle-security_assets`**: Hardware inventory, system specifications, ownership, and network metadata.
2. **`shuffle-security_software`**: Operating system applications, daemon versions, and installed binary catalogs across hosts.
3. **`shuffle-security_packages`**: Code libraries and project manifest dependencies (`package.json`, `requirements.txt`, `Cargo.toml`, `go.mod`) scanned from developer repositories.
4. **`shuffle-security_sensors`**: Monitor daemon runtime state, heartbeats, posture check baselines (`hd_encrypted`, `screenlock`), and response capabilities.

<!-- component:datastore category="shuffle-security_assets" -->

### Datastore Navigation

Access these categories directly in the Datastore console:
- **Assets Console**: [`/admin/datastore?category=shuffle-security_assets`](/admin/datastore?category=shuffle-security_assets) ([Shuffle Core Datastore](https://shuffler.io/admin?tab=datastore&category=shuffle-security_assets))
- **Software Inventory**: [`/admin/datastore?category=shuffle-security_software`](/admin/datastore?category=shuffle-security_software) ([Shuffle Core Datastore](https://shuffler.io/admin?tab=datastore&category=shuffle-security_software))
- **Scanned Packages**: [`/admin/datastore?category=shuffle-security_packages`](/admin/datastore?category=shuffle-security_packages) ([Shuffle Core Datastore](https://shuffler.io/admin?tab=datastore&category=shuffle-security_packages))
- **Sensor Telemetry**: [`/admin/datastore?category=shuffle-security_sensors`](/admin/datastore?category=shuffle-security_sensors) ([Shuffle Core Datastore](https://shuffler.io/admin?tab=datastore&category=shuffle-security_sensors))
- **Manual UI Navigation**: Go to **Admin** -> **Datastore** -> select desired category.

---

### Category Schemas

#### 1. Hardware Assets (`shuffle-security_assets`)
Keyed by hostname or asset identifier (e.g. `srv-prod-db-01` or `dev-macbook-pro-14`).

| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | String | Unique asset identifier (e.g. `asset-srv-prod-01`). |
| `hostname` | String | Primary hostname reported by the endpoint. |
| `os` | String | Operating system name and release (e.g. `Ubuntu 22.04.4 LTS`, `macOS 15.1 Sequoia`). |
| `architecture` | String | CPU architecture (`x86_64`, `arm64`). |
| `cpu_cores` | Number | Number of virtual or physical CPU cores. |
| `ram_gb` | Number | Total physical memory in gigabytes. |
| `disk_gb` | Number | Total system storage capacity in gigabytes. |
| `ip` | String | Primary IPv4 address. |
| `mac_address` | String | Network interface MAC address. |
| `serial_number` | String | Hardware or hypervisor serial number. |
| `environment` | String | Environment tier (`production`, `staging`, `workstation`). |
| `tags` | Array | Organizational labels (e.g. `["database", "postgresql", "critical"]`). |
| `owner` | String | Responsible email or team handle. |
| `status` | String | Lifecycle status (`active`, `decommissioned`, `maintenance`). |

#### 2. Installed Software (`shuffle-security_software`)
Keyed by software identifier (e.g. `sw_docker_engine_26`, `sw_openssh_server_9`).

| Field | Type | Description |
| :--- | :--- | :--- |
| `name` | String | Application or binary name (e.g. `Docker Engine`, `OpenSSH Server`). |
| `version` | String | Detected software release version string. |
| `publisher` | String | Vendor or software maintainer. |
| `install_type` | String | Packaging format (`system_binary`, `deb_package`, `rpm_package`, `application_bundle`). |
| `install_path` | String | Primary executable path (e.g. `/usr/bin/docker`, `/Applications/Google Chrome.app`). |
| `hosts_count` | Number | Total count of fleet endpoints running this application. |
| `associated_hosts` | Array | List of hostnames where this software version was detected. |
| `last_scanned` | Number | Unix epoch timestamp of the most recent inventory sweep. |

#### 3. Scanned Packages (`shuffle-security_packages`)
Keyed by package identifier (e.g. `pkg_lodash_4_17_20`, `pkg_requests_2_31_0`).

| Field | Type | Description |
| :--- | :--- | :--- |
| `name` | String | Package library name (e.g. `lodash`, `requests`, `xz-utils`). |
| `version` | String | Exact installed version discovered in manifest. |
| `ecosystem` | String | Package ecosystem (`npm`, `pip`, `cargo`, `go`, `deb`, `maven`). |
| `manifest_file` | String | Source manifest filename (`package.json`, `requirements.txt`, `Cargo.toml`, `go.mod`). |
| `repository_path` | String | Absolute directory path where the dependency manifest resides. |
| `host` | String | Hostname of the machine running the code scanner. |
| `has_vulnerability` | Boolean | True if the package version matches an active OSV/CVE advisory. |
| `advisory_id` | String | Linked CVE or GHSA identifier (e.g. `GHSA-7867-xwm8-2v3q`), or null if clean. |
| `fixed_version` | String | Recommended patched version if vulnerable. |

#### 4. Sensor Telemetry & Posture (`shuffle-security_sensors`)
Keyed by host sensor ID (e.g. `sensor_srv_prod_db_01`).

| Field | Type | Description |
| :--- | :--- | :--- |
| `host_id` | String | Unique daemon runtime identifier. |
| `hostname` | String | Hostname associated with the daemon instance. |
| `platform` | String | Operating system family (`linux`, `macos`, `windows`). |
| `agent_version` | String | Running Orborus sensor version. |
| `sensor_group` | String | Configured Orborus queue group (e.g. `production-eu`). |
| `status` | String | Daemon heartbeat status (`online`, `offline`). |
| `last_heartbeat` | Number | Unix epoch timestamp of the latest ping. |
| `compliance` | Object | Posture check results: `hd_encrypted`, `screenlock`, `filevault`, `firewall_active`. |
| `capabilities` | Array | Enabled monitor features: `installed_software`, `code_scanner`, `remote_terminal`, `response_actions`. |

### Accessing Host Data in Python Apps & Workflows

```python
# 1. Check endpoint posture baseline
sensor = self.get_cache("sensor_srv_prod_db_01", category="shuffle-security_sensors")
if sensor:
    compliance = sensor.get("compliance", {})
    if not compliance.get("hd_encrypted"):
        print(f"Non-compliant host: {sensor.get('hostname')} lacks disk encryption")

# 2. Correlate vulnerable packages with host assets
package = self.get_cache("pkg_lodash_4_17_20", category="shuffle-security_packages")
if package and package.get("has_vulnerability"):
    target_host = package.get("host")
    asset = self.get_cache(target_host, category="shuffle-security_assets")
    print(f"Alert: {package.get('name')} {package.get('version')} is vulnerable on {target_host} (Owner: {asset.get('owner')})")
```

### Key revisions, audit trail & rollback protection

Every key across all four monitor categories (`shuffle-security_assets`, `shuffle-security_software`, `shuffle-security_packages`, `shuffle-security_sensors`) is automatically stored with immutable revisions.

- **Endpoint Configuration Drift & Overwrite Protection**: If a sensor re-registers, a network glitch reports empty installed software, or a package manifest scan is truncated mid-flight, previous software catalogs and asset configurations are never permanently lost. Historical states can be queried and restored at any time.
- **Audit Trail of Host & Package Changes**:
  - Provides a tamper-resistant historical log showing when software packages were upgraded, when new developer dependencies were introduced, and when posture compliance (`hd_encrypted`, `screenlock`) changed state.
  - Links every state change to the specific Orborus execution ID, daemon ping, or administrative user session.
- **Inspecting & Rolling Back Revisions**:
  - Fetch revisions for any asset or package via REST API:
    ```bash
    # View asset revision history
    curl "https://shuffler.io/api/v2/datastore/category/shuffle-security_assets/{hostname}/revisions" \
      -H "Authorization: Bearer <api_key>"
    ```
  - Roll back state in Python:
    ```python
    # Fetch package revisions to see previous version or recover dropped data
    pkg_revisions = self.get_cache_revisions(key="pkg_lodash_4_17_20", category="shuffle-security_packages")
    if len(pkg_revisions) > 1:
        # Revert to known-good baseline
        self.set_cache(
            key="pkg_lodash_4_17_20",
            value=pkg_revisions[1]["value"],
            category="shuffle-security_packages"
        )
    ```

---

## Deploying a Host Monitor

<!-- component:add-host title="Deploy Shuffle Host Monitor Daemon" -->

### Adding a Host via the Web UI
1. Navigate to **`/monitors`** in Shuffle Security.
2. Click the **"+ Add Host"** button in the top-right header bar.
3. Select or create a **Monitoring Group** (each group links to an Orborus queue and runtime location).
4. Choose the checks to enable:
   - **Hard Drive Encryption** (`hd_encrypted`)
   - **Screenlock Enabled** (`screenlock`)
   - **Installed Software** (`installed_software`)
   - **Code Package Scanner** (`code_scanner_enabled`)
   - **Response Actions** (`response_actions`)
5. Select your target platform (**Linux**, **macOS**, or **Windows**) and installation method (**Easy Install** or **Custom Install**).

### Install Commands

#### Easy Install (One-Liner)
The Add Host dialog generates an automated installation command pre-configured with your instance URL, queue, and authentication header:

**macOS & Linux:**
```bash
curl 'https://shuffler.io/api/v1/orborus?base_url=<SHUFFLE_URL>&sensor_mode=true&queue=<QUEUE>' -H 'Auth: <AUTH_KEY>' | sh
```

**Windows (PowerShell as Administrator):**
```powershell
powershell -ExecutionPolicy Bypass -Command "& {iex (irm 'https://shuffler.io/api/v1/orborus?base_url=<SHUFFLE_URL>&sensor_mode=true&queue=<QUEUE>&os=windows' -Headers @{'Auth'='<AUTH_KEY>'})}"
```

#### Custom Install (Binary)
You can also download the standalone `orborus` binary directly from the official releases:
1. Download the latest binary for your architecture from [github.com/Shuffle/orborus/releases](https://github.com/Shuffle/orborus/releases).
2. Execute the binary with sensor mode flags:
   ```bash
   ./orborus \
     --base_url="https://<your-shuffle-instance>" \
     --sensor_mode=true \
     --queue="<QUEUE_NAME>" \
     --org_id="<ORG_ID>" \
     --auth="<AUTH_KEY>" \
     --software_list_enabled=true \
     --hd_encrypted_check=true \
     --screenlock_check=true \
     --code_scanner_enabled=true \
     --response_actions=full
   ```

<!-- TODO: Screenshot Needed: Add Host Registration Modal
- Route / UI Location: /monitors -> Click "+ Add Host" button in top-right header.
- What to capture: Add Host modal showing monitoring group selector, check options, and generated one-liner curl command.
- Target path: assets/monitors-add-host-modal.png -->

---

## Posture checks

Host Monitors continuously evaluate endpoints against defined posture controls:

### 1. Hard Drive Encryption (`hd_encrypted`)
Verifies full-disk encryption is active on the system drive:
- **macOS**: Queries Apple FileVault status.
- **Windows**: Checks BitLocker drive encryption status on the OS drive (`C:`).
- **Linux**: Checks for LUKS encryption on root and user partitions.

### 2. Screen Lock Enforcement (`screenlock`)
Verifies that the operating system locks the screen after a maximum of 15 minutes of user inactivity:
- Checks system policies and inactivity timeouts.
- Verifies that a password or biometric authentication is required immediately upon wake.

### 3. Active Monitoring (`log_forwarding`)
<!-- NOTE: Active log forwarding is currently marked disabled/coming soon in MonitorsView.tsx -->
Active event and log streaming from monitored hosts is currently in development and not generally available yet.

---

## Installed software inventory

When `installed_software` is enabled, the monitor catalogs applications and packages installed on the machine:
- Records application names and version strings.
- Helps identify unapproved software or outdated binaries across developer laptops and servers.
- Results appear in the **Software** tab of the host detail drawer at `/monitors`.

---

## Code package scanner

When `code_scanner_enabled` is active, the monitor inspects local project directories on the host:
- Scans package manifests: `package.json` (npm/yarn), `requirements.txt` / `Pipfile` (pip), `Cargo.toml` (Cargo), and `go.mod` (Go).
- Evaluates discovered dependencies against OSV.dev.
- Automatically populates findings in [Vulnerabilities](/docs/vulnerabilities), recording the affected hostname and filesystem path.

---

## Remote web terminal

Shuffle Security provides an embedded **Remote Web Terminal** accessible from the host detail panel or directly at `/terminal`:

- **Zero Inbound Ports**: The monitor maintains an outbound WebSocket connection to the Shuffle server. You do not need to open inbound SSH ports or configure public IPs.
- **Live Diagnostics**: Run diagnostic commands (`ps aux`, `df -h`, network checks) directly from the web browser to investigate alerts.

<!-- TODO: Screenshot Needed: Remote Web Terminal View
- Route / UI Location: /terminal (or Host Detail -> Terminal button)
- What to capture: Web terminal connected to a host running diagnostic commands.
- Target path: assets/monitors-web-terminal.png -->

---

## Response actions

When `response_actions` is set to `full`, administrators can execute remote commands on the endpoint from the web terminal, predefined action chips, or automated workflows:

### Predefined Actions
- **Screenshot** (`screenshot`): Captures the current display of the active user session.
- **Isolate Host** (`isolate_host`): Restricts network connectivity while keeping the management channel alive (requires root on Linux/macOS or SYSTEM on Windows).
- **Unisolate Host** (`unisolate_host`): Restores network connectivity (requires root or SYSTEM).
- **Disable RCE** (`disable_rce`): Permanently disables remote command execution on the host monitor daemon.
- **Windows Remote Control** (`remote_control`): Sends automated input actions (mouse click/move, keystrokes, shortcuts) on Windows hosts.

<!-- NOTE: The following predefined actions are defined in the UI but marked not yet available on the endpoint agent:
- Disable User Accounts (disable_user)
- Restart Endpoint (restart_now)
-->
<!-- TODO: Add documentation for user account disabling and remote reboot once supported by the sensor agent -->

> [!NOTE]
> Controlled execution (restricting commands to pre-approved script files) is currently in development.

---

## The Host Monitors dashboard

The fleet interface at **`/monitors`** displays all registered hosts:

<!-- component:host-status title="Fleet Posture Status" subtitle="Endpoint compliance and check status across registered hosts." -->

### Dashboard Features
- **Posture Tiles**: Summary counts of hosts passing compliance checks (disk encryption and screenlock), total discovered software applications, active code package scanners, and hosts with response actions enabled.
- **Platform Tabs & Search**: Filter hosts by operating system (`All`, `macOS`, `Windows`, `Linux`) or search by hostname and IP address.
- **Host Table**:
  - **Host**: Hostname, platform, and IP address.
  - **Operating System**: OS distribution and kernel/build version.
  - **Last Seen**: Relative heartbeat timestamp with an online (green) or offline (gray) status dot.
  - **Compliance Checks**: Indicators for Hard Drive Encryption and Screenlock.
  - **Installed Software**: Count badge of cataloged applications.
  - **Code Scanner**: Status of project dependency scanning.
  - **Actions**: Open the Web Terminal or trigger host actions.
- **Host Detail Drawer (`HostDetailPanel`)**: Clicking any host opens a panel showing hardware specifications (CPU, RAM, MAC address), compliance breakdown, software list, scanned project dependencies, and action triggers.

<!-- TODO: Screenshot Needed: Host Monitors Fleet Dashboard
- Route / UI Location: /monitors
- What to capture: Fleet overview table with posture tiles and registered hosts.
- Target path: assets/monitors-dashboard-overview.png -->

---

## API & Datastore reference

Host monitor records, heartbeats, and compliance data are stored in Shuffle Core's Datastore under the **`shuffle-security_sensors`** category (and hardware asset specifications in **`shuffle-security_assets`**).

### Backend Endpoints

- **List Sensor Groups / Environments**: `GET /api/v1/getenvironments` (filter by `sensor_group === true`)
- **Execute Remote Host Action**:
  ```bash
  curl -X POST "https://<instance>/api/v1/apps/sensors/run" \
    -H "Authorization: Bearer $SHUFFLE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
      "app_id": "sensors",
      "app_name": "sensors",
      "name": "run_action",
      "parameters": [
        { "name": "action", "value": "uname -a" },
        { "name": "hosts", "value": "<HOSTNAME>" },
        { "name": "sensor_group", "value": "<SENSOR_GROUP>" }
      ]
    }'
  ```

<!-- TODO: Document streaming result polling /api/v1/streams/results for long-running sensor executions -->
- **Query Host from Datastore Directly**:
  ```bash
  curl -X POST "https://<instance>/api/v1/orgs/<org_id>/get_cache" \
    -H "Authorization: Bearer $SHUFFLE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
      "category": "shuffle-security_sensors",
      "key": "<HOST_ID>",
      "org_id": "<ORG_ID>"
    }'
  ```

### In Custom Python Apps & Workflows

```python
# Retrieve host telemetry directly from the datastore
host = self.get_cache("host_id_123", category="shuffle-security_sensors")

# Check compliance state
if host:
    compliance = host.get("compliance", {})
    if not compliance.get("hd_encrypted"):
        print(f"Warning: Host {host.get('hostname')} does not have disk encryption enabled")
```

For more details on backend API endpoints and datastore caching rules, see the [API documentation](/docs/API).
