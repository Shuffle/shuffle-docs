# Host Monitors in Shuffle Security

Documentation for monitoring endpoint compliance, inspecting installed software and code dependencies, using the remote web terminal, and running host response actions in Shuffle Security.

## Table of contents
* [Overview](#overview)
* [Using the Host Monitors dashboard](#using-the-host-monitors-dashboard)
* [Deploying a Host Monitor](#deploying-a-host-monitor)
* [Posture checks](#posture-checks)
* [Installed software & code package scanning](#installed-software--code-package-scanning)
* [Remote web terminal & response actions](#remote-web-terminal--response-actions)
* [Cross-platform architecture](#cross-platform-architecture)
* [Datastore architecture: assets, software, packages & sensors](#datastore-architecture-assets-software-packages--sensors)
* [API & Datastore reference](#api--datastore-reference)

---

## Overview

Shuffle Security ([shuffle.security/monitors](https://shuffle.security/monitors)) provides lightweight endpoint posture monitoring, software/dependency discovery, and live remote response across macOS, Windows, and Linux hosts.

Instead of deploying a separate endpoint tool that cannot talk to your incidents or vulnerabilities, Host Monitors connects your endpoints directly to your Shuffle workspace so you can verify compliance, spot vulnerable packages, and run live forensics or containment from a single UI.

- **Compliance & Posture Checks**: Continuously verify that endpoints have full-disk encryption (FileVault, BitLocker, LUKS) and screen lock timeouts enabled.
- **Software & Code Dependency Discovery**: Catalog installed OS applications and scan local developer repositories (`package.json`, `requirements.txt`, `Cargo.toml`, `go.mod`) to surface CVEs in [Vulnerabilities](/docs/vulnerabilities).
- **Browser-Based Remote Web Terminal**: Open an interactive shell on any monitored host over outbound WebSockets without opening inbound SSH or firewall ports.
- **One-Click & Automated Response Actions**: Isolate compromised hosts, capture screenshots, or run diagnostic commands from the UI or directly from Shuffle workflows.

> [!NOTE]
> **Zero License Paywalls**  
> Host Monitors is included in both Shuffle Cloud and self-hosted open-source deployments with no per-seat or per-agent license fees. Normal heartbeats and posture checks consume zero app runs; standard app runs only execute when your automation workflows trigger remote actions.

---

## Using the Host Monitors dashboard

Navigate to **`/monitors`** to view compliance posture and manage all registered endpoints across your fleet:

<!-- component:host-status title="Fleet Posture Status" subtitle="Endpoint compliance and check status across registered hosts." -->

### Dashboard Features
- **Posture Summary Tiles**: View fleet-wide counts of hosts passing compliance checks (disk encryption and screen lock), cataloged software applications, active code package scanners, and hosts with response actions enabled.
- **Monitoring Group Selector**: Switch between monitoring groups in the top-right header and check live heartbeat status (`healthy`, `stale`, `offline`).
- **Platform Tabs & Search**: Filter hosts by operating system (`All`, `macOS`, `Windows`, `Linux`) or search by hostname and IP address.
- **Host Table Columns**:
  - **Host**: Hostname, OS platform, and primary IP address.
  - **Operating System**: OS release and kernel/build version.
  - **Last Seen**: Relative heartbeat timestamp with an online or offline status indicator.
  - **Compliance Checks**: Pass/fail indicators for Hard Drive Encryption and Screen Lock.
  - **Installed Software**: Count of discovered applications on the host.
  - **Code Scanner**: Status of local repository dependency scanning.
  - **Actions**: Launch the Remote Web Terminal or trigger predefined host response actions.
- **Host Detail Drawer**: Click any host row to open a slide-out detail panel showing hardware specifications (CPU, RAM, disk, MAC address), posture check details, searchable installed software, scanned project dependencies, and remote action history.

<!-- TODO: Screenshot Needed: Host Monitors Fleet Dashboard
- Route / UI Location: /monitors
- What to capture: Fleet overview table with posture tiles and registered hosts.
- Target path: assets/monitors-dashboard-overview.png -->

---

## Deploying a Host Monitor

<!-- component:add-host title="Deploy Shuffle Host Monitor Daemon" -->

Use the interactive panel above, or navigate to **`/monitors`** and click **Add Host** in the top-right header bar to generate an installer command for your endpoint.

### Adding a Host via the Web UI
1. Navigate to **`/monitors`** in Shuffle Security.
2. Click the **Add Host** button in the header bar.
3. Select an existing **Monitoring Group** or click **New** to create one (each group maps to a Runtime Location queue).
4. Choose which capabilities to enable on the host:
   - **Hard Drive Encryption** (`hd_encrypted`)
   - **Screenlock Enabled** (`screenlock`)
   - **Installed Software** (`installed_software`)
   - **Code Package Scanner** (`code_scanner_enabled`)
   - **Response Actions** (`response_actions`)
5. Select your target operating system (**Linux**, **macOS**, or **Windows**) and copy the generated command.

### Install Commands

#### Easy Install (One-Liner)
The **Add Host** dialog generates a pre-authenticated one-liner for your tenant and monitoring group:

**macOS & Linux:**
```bash
curl 'https://shuffler.io/api/v1/orborus?base_url=<SHUFFLE_URL>&sensor_mode=true&queue=<QUEUE>' -H 'Auth: <AUTH_KEY>' | sh
```

**Windows (PowerShell as Administrator):**
```powershell
powershell -ExecutionPolicy Bypass -Command "& {iex (irm 'https://shuffler.io/api/v1/orborus?base_url=<SHUFFLE_URL>&sensor_mode=true&queue=<QUEUE>&os=windows' -Headers @{'Auth'='<AUTH_KEY>'})}"
```

#### Custom Install (Standalone Binary)
If you prefer to deploy the binary manually or via configuration management (Ansible, Chef, Puppet, MDM):
1. Download the `orborus` binary for your OS and CPU architecture from [github.com/Shuffle/orborus/releases](https://github.com/Shuffle/orborus/releases).
2. Run the binary with sensor mode flags:
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

Host Monitors continuously evaluate endpoints against baseline security controls and report compliance back to `/monitors`:

### 1. Hard Drive Encryption (`hd_encrypted`)
Verifies that full-disk encryption is active on the primary system volume:
- **macOS**: Checks Apple FileVault 2 status.
- **Windows**: Checks BitLocker protection status on the OS drive (`C:`).
- **Linux**: Checks for LUKS encryption on root and user partitions.

### 2. Screen Lock Enforcement (`screenlock`)
Verifies that the operating system locks the display after a maximum of 15 minutes of user inactivity and requires password or biometric authentication immediately upon wake.

### 3. Active Monitoring (`log_forwarding`)
<!-- NOTE: Active log forwarding is currently marked disabled/coming soon in MonitorsView.tsx -->
Active event and log streaming from monitored hosts is currently in development and not generally available yet.

---

## Installed software & code package scanning

### Installed Software Inventory
When **Installed Software** (`installed_software`) is enabled on a host:
- The monitor catalogs operating system applications, packages, and binaries along with their version strings and install paths.
- You can inspect a host's applications in the **Software** tab of the host detail drawer at `/monitors`, or click any application to view all hosts running that software at `/software/<name>`.

### Code Package Scanner
When **Code Package Scanner** (`code_scanner_enabled`) is enabled on developer workstations or build servers:
- The monitor scans local project directories for dependency manifests: `package.json` (npm/yarn), `requirements.txt` / `Pipfile` (pip), `Cargo.toml` (Cargo), and `go.mod` (Go).
- Discovered dependencies and versions are checked against OSV.dev.
- Vulnerable packages are linked to the host and filesystem path in [Vulnerabilities](/docs/vulnerabilities), and you can inspect every host containing a specific library at `/packages/<name>`.

---

## Remote web terminal & response actions

### Remote Web Terminal
Open an interactive shell on any monitored host from the **Actions** column in `/monitors`, inside the host detail drawer, or at `/monitors/:id/terminal`:
- **Zero Inbound Ports**: The monitor communicates over an outbound WebSocket connection to your Shuffle server—no inbound SSH ports, VPNs, or public IPs are required on the endpoint.
- **Live Triage & Forensics**: Run diagnostic commands (`ps aux`, `netstat`, `df -h`, log inspection) directly in your browser and share terminal output across your team.

<!-- TODO: Screenshot Needed: Remote Web Terminal View
- Route / UI Location: /terminal (or Host Detail -> Terminal button)
- What to capture: Web terminal connected to a host running diagnostic commands.
- Target path: assets/monitors-web-terminal.png -->

### Response Actions
When **Response Actions** (`response_actions`) is enabled on a host, admins and authorized workflows can trigger predefined actions from the host detail panel or `/monitors/response`:
- **Screenshot** (`screenshot`): Captures the current display of the active user session.
- **Isolate Host** (`isolate_host`): Restricts network connectivity on the endpoint while keeping the Shuffle management channel alive (requires `root` on Linux/macOS or `SYSTEM` on Windows).
- **Unisolate Host** (`unisolate_host`): Restores normal network connectivity on an isolated endpoint (requires `root` or `SYSTEM`).
- **Disable RCE** (`disable_rce`): Permanently disables remote command execution on the host monitor daemon.
- **Windows Remote Control** (`remote_control`): Sends automated input actions (mouse click/move, keystrokes, shortcuts) on Windows hosts.

<!-- NOTE: The following predefined actions are defined in the UI but marked not yet available on the endpoint agent:
- Disable User Accounts (disable_user)
- Restart Endpoint (restart_now)
-->
<!-- TODO: Add documentation for user account disabling and remote reboot once supported by the sensor agent -->

> [!NOTE]
> Controlled execution (restricting commands to pre-approved script files) is currently in development. You can manage which automated response actions AI agents are permitted to run at **`/monitors/response`**.

### Host Monitoring Use Cases

<!-- component:usecases category="monitors" -->

---

## Cross-platform architecture

Under the hood, Host Monitors runs **Orborus** (Shuffle's lightweight Go worker binary) in sensor mode (`--sensor_mode=true`) rather than requiring a separate third-party agent:

| Platform | Supported Versions | Monitored Controls |
| :--- | :--- | :--- |
| **macOS** | macOS 12 Monterey, 13 Ventura, 14 Sonoma, 15 Sequoia | FileVault 2 disk encryption, screen lock idle timeout, installed applications catalog, local repository manifests |
| **Windows** | Windows 10, Windows 11, Windows Server 2016+ | BitLocker drive protection, screen lock inactivity policy, installed applications, local repository manifests |
| **Linux** | Ubuntu, Debian, RHEL, CentOS, Fedora, Arch | LUKS volume encryption, screen lock idle timeout, system packages, local repository manifests |

Each Monitoring Group in `/monitors` maps to an Orborus sensor queue, allowing you to segment endpoints by environment or location (e.g. `production-eu`, `corporate-laptops`, `staging`) while orchestrating actions from Shuffle workflows.

---

## Datastore architecture: assets, software, packages & sensors

Host Monitors stores endpoint telemetry across four specialized datastore categories so hardware specs, application inventories, manifest dependencies, and live heartbeats remain decoupled and fast to query:

1. **`shuffle-security_assets`**: Hardware inventory, system specifications, ownership, and network metadata.
2. **`shuffle-security_software`**: Operating system applications, daemon versions, and installed binary catalogs across hosts.
3. **`shuffle-security_packages`**: Code libraries and project manifest dependencies (`package.json`, `requirements.txt`, `Cargo.toml`, `go.mod`) scanned from developer repositories.
4. **`shuffle-security_sensors`**: Monitor daemon runtime state, heartbeats, posture check baselines (`hd_encrypted`, `screenlock`), and response capabilities.

<!-- component:datastore category="shuffle-security_assets" -->

### Datastore Navigation

Inspect these categories directly in the Datastore console:
- **Assets Console**: [`/admin/datastore?category=shuffle-security_assets`](/admin/datastore?category=shuffle-security_assets) ([Shuffle Datastore](https://shuffler.io/admin?tab=datastore&category=shuffle-security_assets))
- **Software Inventory**: [`/admin/datastore?category=shuffle-security_software`](/admin/datastore?category=shuffle-security_software) ([Shuffle Datastore](https://shuffler.io/admin?tab=datastore&category=shuffle-security_software))
- **Scanned Packages**: [`/admin/datastore?category=shuffle-security_packages`](/admin/datastore?category=shuffle-security_packages) ([Shuffle Datastore](https://shuffler.io/admin?tab=datastore&category=shuffle-security_packages))
- **Sensor Telemetry**: [`/admin/datastore?category=shuffle-security_sensors`](/admin/datastore?category=shuffle-security_sensors) ([Shuffle Datastore](https://shuffler.io/admin?tab=datastore&category=shuffle-security_sensors))
- **Manual UI Navigation**: Go to **Admin** -> **Datastore** -> select the desired category.

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

### Key Revisions, Audit Trail & Rollback Protection

Every key across all four monitor categories (`shuffle-security_assets`, `shuffle-security_software`, `shuffle-security_packages`, `shuffle-security_sensors`) is stored with immutable revisions:

- **Endpoint Configuration Drift & Overwrite Protection**: If a sensor re-registers or a scan is interrupted, previous software catalogs and asset records remain stored in revision history and can be restored at any time.
- **Audit Trail of Host & Package Changes**: Tracks when software packages were upgraded, when new developer dependencies were introduced, and when posture compliance (`hd_encrypted`, `screenlock`) changed state.
- **Inspecting & Rolling Back Revisions**:
  - Fetch revisions for any asset or package via REST API:
    ```bash
    curl "https://shuffler.io/api/v2/datastore/category/shuffle-security_assets/{hostname}/revisions" \
      -H "Authorization: Bearer <api_key>"
    ```
  - Roll back state in Python:
    ```python
    pkg_revisions = self.get_cache_revisions(key="pkg_lodash_4_17_20", category="shuffle-security_packages")
    if len(pkg_revisions) > 1:
        self.set_cache(
            key="pkg_lodash_4_17_20",
            value=pkg_revisions[1]["value"],
            category="shuffle-security_packages"
        )
    ```

---

## API & Datastore reference

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
