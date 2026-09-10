# Host Monitors in Shuffle Security

Documentation for endpoint compliance, software inventory, dependency scanning, remote web terminals, and automated response actions across your fleet in Shuffle Security.

## Table of contents
* [Why Host Monitors in Shuffle?](#why-host-monitors-in-shuffle)
* [Cross-platform architecture](#cross-platform-architecture)
* [The Host Monitors dashboard](#the-host-monitors-dashboard)
* [Compliance & posture checks](#compliance--posture-checks)
  * [Hard drive encryption](#hard-drive-encryption)
  * [Screen lock enforcement](#screen-lock-enforcement)
* [Installed software inventory](#installed-software-inventory)
* [Code package scanner](#code-package-scanner)
* [Remote web terminal](#remote-web-terminal)
* [Host response actions](#host-response-actions)
* [SOC use cases](#soc-use-cases)
* [Integration with Incidents & Threat Intel](#integration-with-incidents--threat-intel)
* [AI Agents for Host Monitors](#ai-agents-for-host-monitors)
* [API & Datastore access](#api--datastore-access)

---

## Why Host Monitors in Shuffle?

Shuffle is an open-source security orchestration, automation, and response (SOAR) platform. **Shuffle Security** ([shuffle.security](https://shuffle.security)) is our dedicated SecOps application built directly on top of Shuffle Core.

Most endpoint monitoring and Mobile Device Management (MDM) tools operate in a silo: an agent detects an unencrypted laptop or an outdated vulnerable package, but you cannot take automated action without jumping through three different consoles.

We built **Host Monitors** in Shuffle Security ([shuffle.security/monitors](https://shuffle.security/monitors)) to bridge the gap between **endpoint visibility** and **security automation**:

- **Continuous Compliance**: Instantly verify essential security baselines (disk encryption, screen lock timeouts, firewall states) across employee workstations and production servers.
- **Unified Software & Code Inventory**: Maintain a live, fleet-wide inventory of installed applications and local code dependencies (`npm`, `pip`, `cargo`, `go.mod`).
- **Direct Terminal & Response Actions**: Execute remediation playbooks or open a secure, browser-based web terminal directly into an endpoint for live investigation.
- **Incident & Threat Intel Synergy**: When an [Incident](/docs/incidents) occurs or a new CVE is discovered in [Vulnerabilities](/docs/vulnerabilities), Shuffle lets you query and contain affected hosts immediately.

> [!NOTE]
> **Available to Everyone — Zero License Paywalls**  
> Host Monitors is a native feature included for **everyone**—whether you use Shuffle Cloud or run self-hosted Shuffle Open Source via Docker Compose or Kubernetes.  
> There are no per-agent fees, no host count limits, and no separate endpoint licenses. It doesn't cost anything extra except standard **app runs** when your automations execute (e.g. running a compliance check workflow, triggering automated quarantine, or querying packages). Telemetry collection and heartbeat monitoring consume zero app runs.

### Seamlessly Engrained in Shuffle Core

Under the hood, all host monitor registrations, heartbeats, and compliance states are stored directly in **`shuffle-security_sensors`** (with discovered device hardware records stored in **`shuffle-security_assets`**) inside Shuffle Core's Datastore (OpenSearch). 

Because endpoints live in the same datastore as the rest of Shuffle:
- Workflows can inspect host compliance states or software lists directly using standard datastore actions.
- AI Agents and Python playbooks can target remediation scripts or quarantine commands to affected endpoints without third-party connector plugins.
- Incident response teams can link an active case in [Incidents](/docs/incidents) directly to the compromised host record with zero data duplication.

---

## Cross-platform architecture

The Shuffle Host Monitor is a lightweight, cross-platform daemon engineered to run unobtrusively on endpoints with minimal CPU and memory overhead:

| Platform | Supported Environments | Native Technologies Monitored |
| :--- | :--- | :--- |
| **macOS** | macOS 12 Monterey, 13 Ventura, 14 Sonoma, 15 Sequoia | FileVault 2, `launchd`, Homebrew, Applications catalog |
| **Windows** | Windows 10, Windows 11, Windows Server 2016+ | BitLocker, Windows Defender, Registry policies, PowerShell |
| **Linux** | Ubuntu, Debian, RHEL, CentOS, Fedora, Arch | LUKS encryption, `systemd`, `apt`/`rpm`/`pacman` packages |

### Adding a Host & Daemon Ingestion

<!-- component:add-host title="Deploy Shuffle Host Monitor Daemon" -->

> [!TIP]
> **Where is the Ingest Endpoint / Add Host button located in the UI?**  
> 1. Go to **`/monitors`** in Shuffle Security.  
> 2. Look at the top-right header bar and click the **"+ Add Host"** button.  
> 3. The **Add Host modal** opens, letting you choose your target operating system (macOS, Windows, Linux) and toggle desired capabilities (Disk Encryption, Screenlock, Software Inventory, Code Package Scanner, and Response Actions).  
> 4. Shuffle automatically generates your pre-authenticated, one-line install command containing your organization's registration token:  
>    - **macOS & Linux**:  
>      ```bash
>      curl -sSL https://<instance>/api/v1/monitors/install.sh | sudo bash -s -- --token <ORG_TOKEN>
>      ```  
>    - **Windows (PowerShell)**:  
>      ```powershell
>      irm https://<instance>/api/v1/monitors/install.ps1 | iex
>      ```  
> 5. You can run this command directly on a machine or distribute it across your fleet using your MDM or configuration manager (Jamf, Microsoft Intune, Kandji, Ansible).  
> 6. Once installed, the daemon immediately connects back to Shuffle's secure ingestion endpoint (`/api/v1/monitors`) over HTTPS and WebSockets, sending heartbeats and telemetry in real time.

<!-- TODO: Screenshot Needed: Add Host Registration Modal
- Route / UI Location: /monitors -> Click "+ Add Host" button in top-right header.
- What to capture: The open Add Host modal showing the OS selector tabs (macOS, Windows, Linux), capability checkboxes, and the generated one-line install command containing --token <ORG_TOKEN>.
- Recommended filename: assets/monitors-add-host-modal.png
- Inject syntax: ![Add Host Registration Modal](https://raw.githubusercontent.com/Shuffle/Shuffle-docs/master/assets/monitors-add-host-modal.png)
-->

---

## The Host Monitors dashboard

The fleet management interface at **`/monitors`** provides an interactive command center for all registered endpoints:

<!-- component:host-status title="Fleet Posture & Compliance Status" subtitle="Real-time endpoint compliance, disk encryption, and software inventory across registered hosts." -->

The fleet posture checks continuously evaluate endpoints against organizational and regulatory baselines:

| Posture Control | Monitored Attribute | Compliance Standard | Default Action upon Failure |
| :--- | :--- | :--- | :--- |
| **Disk Encryption** | FileVault 2 (macOS), BitLocker (Windows), LUKS (Linux) | SOC 2 CC6.1, ISO 27001 A.10 | Notify user via Slack, flag non-compliant status in fleet inventory. |
| **Screen Lock Timeout** | Inactivity timeout ≤ 15 minutes | CIS Benchmark 2.3.1 | Alert employee, prompt configuration profile re-application. |
| **Software Inventory** | Installed applications, versions, and binaries | CIS Control 2 (Software Asset Inventory) | Flag known unapproved software or outdated binaries. |
| **Code Package Scanner** | Local `package.json`, `requirements.txt`, `Cargo.toml`, `go.mod` | DevSecOps Pipeline Baseline | Alert developer before committing vulnerable dependencies to production. |

- **Fleet Posture Tiles**: At-a-glance status cards across your entire fleet:
  - **Compliance Checks**: Fleet percentage with active FileVault / BitLocker disk encryption and screen lock timeouts.
  - **Installed Software**: Total software packages discovered across all hosts.
  - **Code Package Scanner**: Number of repositories and project directories actively monitored for vulnerable dependencies.
  - **Response Actions**: Number of hosts capable of automated remote containment.
- **Search & OS Tabs**: Search machines by hostname, IP address, or logged-in user, and filter by platform (`All`, `macOS`, `Windows`, `Linux`).
- **Fleet Table Columns**:
  - **Host**: Operating system platform, hostname, and primary IP address.
  - **Operating System**: OS distribution name and exact kernel/build version.
  - **Last Seen**: Relative heartbeat timestamp with a live green (online) or gray (offline) status indicator dot.
  - **Compliance Checks**: Indicators showing the status of Hard Drive Encryption and Screen Lock policy enforcement.
  - **Installed Software**: Count badge of cataloged software applications.
  - **Code Scanner**: Status badge showing whether the local package scanner is active.
  - **Actions Menu**: Quick access dropdown to open the **Web Terminal** or trigger pre-configured containment playbooks.
- **Host Detail Drawer (`HostDetailPanel`)**: Clicking any host row slides open a multi-tab investigation panel:
  - **Overview**: System specifications (CPU architecture, RAM, disk partitions, MAC addresses, and uptime).
  - **Compliance**: Granular pass/fail verification of FileVault/BitLocker, screen lock idle timeout, and firewall policies.
  - **Software**: Full searchable catalog of every installed application, binary, and version.
  - **Code Packages**: List of local project directories inspected with package dependency trees.
  - **Response Actions**: Execute immediate containment or diagnostic scripts on the endpoint.
- **Web Terminal (`/terminal`)**: Open an interactive, browser-based shell to the host with zero inbound ports required.

<!-- TODO: Screenshot Needed: Host Monitors Fleet Dashboard
- Route / UI Location: /monitors
- What to capture: The fleet overview page showing the four top posture tiles (Compliance Checks %, Installed Software count, Code Package Scanner, Response Actions), platform tabs (All, macOS, Windows, Linux), and the host table with live status indicator dots and compliance badges.
- Recommended filename: assets/monitors-dashboard-overview.png
- Inject syntax: ![Host Monitors Fleet Dashboard](https://raw.githubusercontent.com/Shuffle/Shuffle-docs/master/assets/monitors-dashboard-overview.png)
-->

<!-- TODO: Screenshot Needed: Host Detail Panel (HostDetailPanel)
- Route / UI Location: /monitors -> Click any host row
- What to capture: The slide-out HostDetailPanel showing system hardware specifications, compliance verification pass/fail status (FileVault/BitLocker, screen lock timer), and the installed software list.
- Recommended filename: assets/monitors-host-detail-panel.png
- Inject syntax: ![Host Detail Panel](https://raw.githubusercontent.com/Shuffle/Shuffle-docs/master/assets/monitors-host-detail-panel.png)
-->

---

## Compliance & posture checks

Host Monitors continuously evaluate endpoints against key compliance frameworks (SOC 2, ISO 27001, CIS Benchmarks):

### Hard drive encryption
Unencrypted laptops represent one of the most common vectors for catastrophic data leaks when devices are lost or stolen:
- **macOS**: Queries the status of Apple **FileVault**. Flags any machine where full-disk encryption is disabled.
- **Windows**: Inspects **BitLocker** drive protection status on system volumes (`C:`).
- **Linux**: Verifies that root or user partitions are configured with **LUKS** encryption.

### Screen lock enforcement
Verifies that the operating system enforces an automatic screen lock after a maximum of 15 minutes of inactivity:
- Checks system preference files and group policies.
- Ensures the screen requires a password or biometric verification immediately upon wake.

### Firewall & OS Version Status
Verifies that the built-in host firewall (macOS Application Firewall, Windows Defender Firewall, Linux `ufw`/`iptables`) is active and flags devices running deprecated, unsupported OS versions.

---

## Installed software inventory

Shadow IT and forgotten legacy software expose your organization to unpatched vulnerabilities.

The Host Monitor maintains a real-time catalog of every application installed on the endpoint:
- **Application Name & Version**: Tracks software titles, build versions, and bundle IDs.
- **Detection of Unapproved Software**: Flags remote access tools, peer-to-peer applications, or unapproved software packages.
- **Vulnerability Cross-Referencing**: Shuffle automatically matches installed software versions against known CVE databases in [Vulnerabilities](/docs/vulnerabilities), highlighting outdated software that requires immediate patching.

---

## Code package scanner

Modern development teams download thousands of open-source packages directly onto their developer laptops. If an engineer clones a repository with a malicious or vulnerable dependency, production scanners might not catch it until weeks later when code is merged.

The **Code Package Scanner** capability inspects designated project directories on the host:
- Scans `package.json` (`npm`/`yarn`), `requirements.txt` / `Pipfile` (`pip`), `Cargo.toml` (`cargo`), and `go.mod` (`Go`).
- Detects vulnerable package versions directly on developer machines.
- Alerts developers or security teams before vulnerable dependencies are committed to version control.

---

## Remote web terminal

When investigating a suspected compromise or assisting a remote employee, jumping between separate SSH keys, VPNs, or third-party remote access software wastes critical time.

Shuffle Security provides an embedded **Remote Web Terminal** accessible directly at `/terminal` or from the host detail view:
- **Zero Inbound Ports**: The Host Monitor daemon maintains an outbound connection over secure WebSockets, meaning you do not need to open inbound firewall ports or expose SSH to the public internet.
- **Role-Based Access Control**: Terminal access is strictly gated by administrator and support permissions in `/settings/permissions`.
- **Live Forensics & Troubleshooting**: Run commands, inspect running processes, check network sockets, or view log files in real time directly from your browser.

<!-- TODO: Screenshot Needed: Remote Web Terminal View
- Route / UI Location: /terminal (or Host Detail -> Terminal button)
- What to capture: The embedded browser terminal window connected to an active host executing diagnostic commands (e.g. whoami, ps aux, network checks).
- Recommended filename: assets/monitors-web-terminal.png
- Inject syntax: ![Remote Web Terminal](https://raw.githubusercontent.com/Shuffle/Shuffle-docs/master/assets/monitors-web-terminal.png)
-->

---

## Host response actions

Host Monitors enable active response. Instead of merely alerting you to a problem, you can trigger pre-configured actions directly from Shuffle:

1. **Network Isolation**: Sever external network connections on an endpoint while maintaining the secure management channel to Shuffle for live investigation.
2. **Process Termination**: Terminate a malicious process ID or background daemon identified during incident triage.
3. **Cache & Session Cleansing**: Force logout of user sessions or clear compromised application credentials.
4. **Automated Remediation**: Trigger custom remediation scripts to enable FileVault, turn on the firewall, or patch outdated packages.

---

## SOC use cases

Host Monitors bridge the gap between detection and automated containment across your endpoints.

<!-- component:usecases category="monitors" -->

Here are practical security operations workflows powered by Host Monitors:

### 1. Automated Quarantine of Non-Compliant Laptops
- **Trigger**: An employee disables FileVault or sets their screen lock timeout to "Never".
- **Action**: Shuffle detects the compliance failure on the next heartbeat.
- **Workflow**: Shuffle sends a friendly notification via Slack asking the user to re-enable disk encryption. If uncorrected within 24 hours, the workflow revokes their corporate Google Workspace session and creates a review task in [Incidents](/docs/incidents).

### 2. Live Forensic Capture During an EDR Incident
- **Trigger**: An EDR alert fires in [Incidents](/docs/incidents) reporting suspicious PowerShell activity on `WIN-PROD-01`.
- **Action**: The analyst clicks **"Run Host Forensic Action"** directly inside the incident workspace.
- **Execution**: The Host Monitor executes a forensic script that captures current running processes, active network connections, and recent file modifications, attaching the report directly to the incident timeline.

### 3. Fleet-Wide Zero-Day Hunting
- **Trigger**: A new critical vulnerability is announced affecting an open-source library or utility.
- **Action**: Security engineers trigger a fleet-wide query across all Host Monitors.
- **Result**: Within seconds, Shuffle identifies every laptop and server running the vulnerable version, allowing engineers to execute an automated update script in bulk.

Explore pre-built templates in [Use Cases](/usecases).

---

## Integration with Incidents & Threat Intel

Host Monitors work hand-in-hand with the rest of Shuffle Security:

- **Correlation with [Incidents](/docs/incidents)**: When an alert mentions an IP address or hostname, Shuffle immediately matches it to the monitored host, displaying its live health, OS details, and assigned user on the incident canvas.
- **Correlation with [Vulnerabilities](/docs/vulnerabilities)**: Discovered CVEs are automatically attributed to the specific host, prioritizing remediation based on whether the host is publicly exposed or accessible internally.
- **Threat Intelligence Feeds (`/incidents/threat-feeds`)**: Hashes of running processes or installed software are cross-referenced against VirusTotal and AlienVault OTX to identify stealthy malware.

---

## AI Agents for Host Monitors

Through Shuffle's AI integration and the `shuffle_monitors` MCP tool, you can leverage autonomous agents to analyze your fleet:

<!-- component:ask-ai label="Ask AI about Host Monitors" input="How do I verify FileVault encryption and generate a compliance report across all macOS hosts?" -->

- **Fleet Health Summaries**: Ask the agent: *"Show me all hosts that haven't checked in for more than 7 days."*
- **Compliance Reporting**: Ask: *"Generate a SOC 2 audit summary of our disk encryption and screen lock compliance rates."*
- **Investigation Assistance**: Instruct the agent: *"Analyze the running processes on host srv-database-01 and flag any unusual network listeners."*

---

## API & Datastore access

Host monitor registrations, heartbeats, and compliance states are stored directly in Shuffle Core's Datastore under the **`shuffle-security_sensors`** category (with discovered device specifications stored in **`shuffle-security_assets`**). You can query fleet telemetry programmatically via the Shuffle REST API or inside custom Python apps:

### REST API Endpoints
- **List Monitored Hosts from Datastore**: `GET /api/v1/orgs/{org_id}/list_cache?category=shuffle-security_sensors&top=100`
- **Filter Active Endpoints**: `GET /api/v1/monitors`
- **Get Specific Host Record**: `GET /api/v1/monitors/{host_id}` (or `GET /api/v1/orgs/{org_id}/get_cache?category=shuffle-security_sensors&key={host_id}`)
- **Register New Host**: `POST /api/v1/monitors`
- **Trigger Host Remote Action**: `POST /api/v1/monitors/{host_id}/actions/{action_name}`

### In Custom Python Apps & Workflows
```python
# Retrieve host telemetry directly from Shuffle's datastore
host = self.get_cache("host_id_456", category="shuffle-security_sensors")

# Check compliance state
if host and not host.get("compliance", {}).get("hd_encrypted"):
    print(f"Alert: Host {host.get('hostname')} has disk encryption disabled!")

# Update host metadata or response tag
self.set_cache("host_id_456", host, category="shuffle-security_sensors")
```

For more details on backend API endpoints and authentication, see our [API documentation](/docs/API).
