# Host Monitors in Shuffle Security

Documentation for endpoint posture monitoring, disk encryption, screen lock enforcement, software inventory, local code package scanning, remote web terminals, and response actions in Shuffle Security.

## Table of contents
* [Overview](#overview)
* [Cross-platform architecture](#cross-platform-architecture)
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
