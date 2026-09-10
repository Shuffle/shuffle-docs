# AI at Shuffle

With AI becoming a central pillar of cybersecurity and automation, Shuffle provides an enterprise AI framework built from the ground up to be deterministic, controllable, and secure. Whether you are generating workflows, running autonomous security investigations in [Shuffle Security](https://security.shuffler.io), or connecting your private tools to ChatGPT and Claude via the Model Context Protocol (MCP), Shuffle gives you full control over your models, prompts, data residency, and execution boundaries.

---

## Using LLMs

Shuffle offers a unified interface for language models across cloud, hybrid, and fully air-gapped environments. You can leverage managed AI credits out of the box or connect to your own models with zero container restarts.

<!-- component:shuffle-ai -->

### Cloud & Managed Credits

In Shuffle Cloud, LLM interactions, Agent reasoning loops, and workflow AI actions are powered by built-in **Shuffle AI credits**.
- **Regional Routing & Data Residency**: AI requests are dynamically routed to Google Cloud Platform (Vertex AI / Gemini) endpoints within your deployment's geographic region based on `SHUFFLE_GCE_LOCATION` (e.g. EU or US regional boundaries). This ensures full compliance with strict data residency requirements.
- **Quota & Credit Tracking**: Organization admins can view credit usage, remaining limits, and active allocations directly within the Shuffle AI drawer.
- **Programmatic LLM Access**: You can query your cloud model programmatically via Shuffle's OpenAI-compatible chat completions interface at [`POST /api/v1/chat/completions`](/docs/API#chat-completions).

### Using LLMs on-premises

For on-premises and private cloud installations, Shuffle provides two distinct architectural deployment models depending on whether you choose to run local GPU infrastructure:

1. **Option A: Cloud Sync (Zero-GPU Infrastructure)**
   - If you do not wish to provision or maintain local GPU hardware, you can leverage Shuffle AI credits from your on-premises instance.
   - **Prerequisite**: Navigate to **`/admin` -> Cloud Sync** and enter your Shuffler.io API key.
   - Once configured, on-prem Shuffle automatically falls back to routing inference requests outbound over HTTPS to `https://shuffler.io/api/v1`.
   - **Data Privacy**: Your playbooks, credentials, and app actions execute **100% locally** on your on-premises Orborus workers. Only the prompt and contextual text required for inference are forwarded to Shuffle Cloud's regional endpoints.

2. **Option B: Air-Gapped Local Model (100% Isolated)**
   - For high-security, defense, or air-gapped networks where zero data may leave your internal perimeter, connect Shuffle directly to a self-hosted inference server (such as Ollama, vLLM, LM Studio, or an enterprise LLM gateway).
   - No external requests are made; all tokens and telemetry remain strictly inside your network.

### How choosing a local LLM works

Shuffle enables organizations to configure or switch their active LLM provider directly through the user interface without editing configuration files or restarting backend containers:

1. **Open the Provider Selector**: Click the active provider chip (e.g. **Shuffle AI** or the configured model badge) in the top bar of [`/agents`](/agents) or click the interactive button above.
2. **Select a Provider Preset**: The right-hand sidebar opens with curated presets for:
   - **Local Inference**: Ollama (`http://localhost:11434/v1`), LM Studio (`http://localhost:1234/v1`), or Custom OpenAI-compatible endpoints.
   - **Cloud Providers**: Google Gemini, OpenAI, Anthropic, Mistral, Groq, DeepSeek, Together AI, or OpenRouter.
3. **Configure Endpoints & Credentials**:
   - **URL**: Enter the base URL of your API (e.g. `http://localhost:11434/v1` for local Ollama, or your internal reverse proxy URL).
   - **Model Name**: Select from the recommended model dropdown (e.g. `llama3.3`, `qwen3`, `deepseek-r1`) or type a custom model identifier.
   - **API Key**: Enter your provider API token (leave blank or enter a placeholder for unauthenticated local servers).
4. **Test Connection & Save**:
   - Click **Test Connection** to send a real-time health-check prompt. The sidebar displays latency and connectivity status.
   - Click **Save**. The configuration is securely stored in your organization's App Authentication.
   - All subsequent agent runs, workflow AI nodes, and Ask AI queries across your organization immediately route to the new model in real time.

<!-- TODO: Screenshot Needed: LLM Provider Selector Drawer
- Route / UI Location: /agents -> Click the active LLM provider chip (e.g. "Shuffle AI" or model badge) in the top header bar.
- What to capture: The open provider sidebar showing presets for Local (Ollama, LM Studio) and Cloud models (Gemini, OpenAI, Anthropic), endpoint URL, Model dropdown, and the "Test Connection" button.
- Recommended filename: assets/ai-provider-selector-drawer.png
- Inject syntax: ![AI Provider Selector Drawer](https://raw.githubusercontent.com/Shuffle/Shuffle-docs/master/assets/ai-provider-selector-drawer.png)
-->

---

## AI Agents

Agents in Shuffle are autonomous, goal-oriented systems that interact with the world using tools (playbooks, MCP apps, and custom scripts) to achieve specific operational outcomes.

<!-- component:agent-ui placeholder="Analyze an alert or investigate an IP..." -->

<!-- TODO: Screenshot Needed: AI Agents Workspace & Autonomous Execution
- Route / UI Location: /agents
- What to capture: The active Agents console showing an agent execution with prompt input, thought/planning loop, tool executions (calling Shuffle apps), and structured output.
- Recommended filename: assets/ai-agents-workspace.png
- Inject syntax: ![AI Agents Workspace](https://raw.githubusercontent.com/Shuffle/Shuffle-docs/master/assets/ai-agents-workspace.png)
-->

### How an Agent works under the hood

When you run an agent in Shuffle (from [`/agents`](/agents), inside a workflow node, or via the API), it executes an autonomous decision loop implemented in Shuffle's open-source core:

```
Goal / Prompt
      │
      ▼
┌──────────────┐      ┌────────────────────────┐
│ Tool         │ ───> │ Planning & Decisions   │
│ Discovery    │      │ (Generates Decisions)  │
└──────────────┘      └────────────────────────┘
                                │
                                ▼
                      ┌────────────────────────┐
                      │ Execution Engine       │
                      │ (Direct or Schemaless) │
                      └────────────────────────┘
                                │
                                ▼
                      ┌────────────────────────┐
                      │ Context Update         │
                      │ (Memory & Results)     │
                      └────────────────────────┘
                                │
                                ▼
                      ┌────────────────────────┐
                      │ Finish / Pause         │
                      │ (Output or Question)   │
                      └────────────────────────┘
```

1. **Tool Discovery**: Shuffle inspects the permitted apps and translates them into standardized MCP tool definitions with schemas and parameter validations.
2. **Planning & Decisions**: The agent breaks your objective into an ordered array of **Decisions** (`AgentDecision`). Each decision encapsulates:
   - `tool`: The app to call (e.g. `virustotal`, `jira`, `slack`).
   - `action`: The exact action within that app (e.g. `get_ip_report`, `create_ticket`).
   - `fields`: Key-value parameters passed to the action.
   - `confidence`: Confidence score (0.0 to 1.0) for the selected action.
   - `reason`: A concise natural language explanation of why this step was selected.
   - `approval_required`: Flags whether human authorization is required before execution.
   - `data_filter`: Field-level extraction rules to keep context windows compact and cost-effective.
3. **Execution**: Shuffle executes decisions sequentially. Calls are executed either directly against third-party APIs (`execution_mode: "direct"`) or normalized through Schemaless (`execution_mode: "singul"`). The core execution structures are defined in [`shuffle-shared`](https://github.com/shuffle/shuffle-shared).
4. **Context Update**: The filtered response from each tool feeds back into the agent's working memory to evaluate progress.
5. **Completion or Pause**:
   - If the task is fulfilled, the agent emits a `finish` decision and renders the final summary.
   - If the agent needs missing details, it emits an `ask` decision and pauses in `WAITING` status.
   - If a step is flagged with `approval_required: true`, the run pauses until confirmed by an operator.

#### The Agent Decision structure
Under the hood, every step the agent plans follows this JSON schema:

```json
{
  "i": 0,
  "tool": "virustotal",
  "action": "get_ip_report",
  "fields": [
    {"key": "ip", "value": "1.1.1.1"}
  ],
  "reason": "Check reputation of the suspicious IP extracted from the alert",
  "confidence": 0.95,
  "approval_required": false,
  "data_filter": "last_analysis_stats"
}
```

### Using the "Ask AI" button in Shuffle

Shuffle includes a persistent, context-aware **Ask AI** assistant available across every view in the platform (including Incidents, Workflows, Apps, and Documentation).

<!-- component:ask-ai label="Try Ask AI right now" input="How do I use agents in Shuffle?" -->

- **Context-Aware Intelligence**: Ask AI automatically detects your current route and active entity. If you are viewing an alert in Shuffle Security, it reads the alert observables; if you are in the workflow canvas, it inspects your active nodes and execution errors.
- **Automated Tool & Skill Injection**: Based on your location, Ask AI dynamically attaches the relevant MCP tools (e.g. `shuffle_incidents` when investigating a case, `shuffle_workflows_builder` when designing automations).
- **Non-Destructive Sideshifting Panel**: The assistant opens in a dedicated side panel that shifts page content instead of obscuring your canvas or incident workspace, allowing you to converse, inspect findings, and apply solutions simultaneously.

### Predefined Agent Skills

Agent Skills are specialized capability bundles that combine specific tools, prompt seeds, and domain-tailored reasoning strategies.

Shuffle provides built-in predefined skills out of the box:

1. **Build Workflow (`build-workflows`)**:
   - **Role**: Automatically designs, creates, and wires Shuffle workflows from natural language descriptions.
   - **Required Tools**: `shuffle_workflows_builder`, `shuffle_apps`.
   - **Default Prompt**: *"Build a Shuffle workflow that..."*
2. **Incident Handler (`incident-response`)**:
   - **Role**: Assists in security incident investigations. Automatically extracts observables (IPs, hashes, domains, emails), correlates related alerts across your tenant, analyzes attack scope, and proposes tiered containment options with operator confirmation.
   - **Required Tools**: `shuffle_incidents`.
   - **Default Prompt**: *"Investigate this incident and recommend next steps:..."*
3. **Computer Use (`host-monitor-control`)**:
   - **Role**: Controls an endpoint or host computer through terminal commands, CLI execution, screenshot capture, and keyboard/mouse interaction for hands-on remediation and guided forensics.
   - **Required Tools**: `shuffle_host_monitors`.
   - **Default Prompt**: *"Take control of this host and help me with:..."*
4. **Vulnerability Management (`vulnerability`)**:
   - **Role**: Analyzes CVEs in plain language, calculates realistic exploitability using EPSS (Exploit Prediction Scoring System) and CISA KEV (Known Exploited Vulnerabilities) data, and outputs concrete step-by-step remediation plans.
   - **Required Tools**: `shuffle_vulnerabilities`, `shuffle_software_and_packages`.
   - **Default Prompt**: *"Help me review and solve this vulnerability:..."*
5. **Upcoming Presets**:
   - **Support Agent (`support`)**: Navigates platform settings, runs connectivity diagnostics, and answers operational questions.
   - **Detection Agent (`detection`)**: Drafts and tunes Sigma detection rules and pipelines to minimize false positives.
   - **Handle Notifications (`handle-notifications`)**: Automates incoming incident triage, enrichment, and rule-based escalation.

### Adding your own Skill

In Shuffle, **every app is an MCP tool**. This architecture makes creating custom skills straightforward:

1. **Create an App or Playbook**: Any integration in Shuffle, custom Python script, or sub-workflow can be exposed as an agent capability.
2. **Define the Skill Scope**: In the Agents interface or via API, combine your custom apps with a specialized system prompt, required tools, and default arguments.
3. **Lock Required Tools**: Mark critical tools as required so they remain locked to the skill during execution.
4. **Deploy**: Once created, custom skills can be triggered manually in `/agents`, invoked automatically via incoming webhooks, or scheduled to run as background monitors.

### Reasoning Effort, Approvals & Debugging

- **Reasoning Effort Levels**:
  - `minimal`: Rapid single-step lookups (e.g. "Check hash in VirusTotal").
  - `low`: 2-3 step sequential chaining.
  - `medium`: The default balanced mode for multi-step investigations.
  - `high`: Deep recursive planning, cross-referencing multiple intelligence sources, and verifying intermediate hypotheses.
- **Clarifying Questions**: If the agent encounters ambiguity, it pauses in `WAITING` status and presents an interactive question prompt.
- **Action Approvals**: Mark critical or destructive actions with `approval_required: true`. The agent will pause and present the proposed payload to an analyst before firing the request.
- **Continuations**: After an agent finishes a task, you can ask follow-up questions or request modifications directly in the continuation box below the output.
- **Monitoring & Debugging**: All historical and running agent executions can be monitored in real time at [`/workflows/debug`](/workflows/debug) under the **Agent Runs** tab.

---

## Model Context Protocol (MCP) & External Clients

The Model Context Protocol (MCP) standardizes how AI models discover and execute tools. In Shuffle, **every single app in the catalog is an MCP server**, enabling seamless interoperability with internal agents as well as external AI platforms like ChatGPT and Claude.

<!-- component:try-mcp app="Shuffle Tools" -->

### Every App is an MCP Endpoint

You can interact with Shuffle tools using the standard MCP specification:
- **Global MCP Endpoint**: `POST /api/v1/mcp` allows calling any tool across your organization using the standard `tools/call` and `tools/list` JSON-RPC methods.
- **Single App MCP Endpoint**: `GET / POST /api/v1/apps/{app_id}/mcp` scopes interactions exclusively to the actions of a single app.

### How OAuth2 Authentication Works

Shuffle provides a full-featured OAuth 2.0 Authorization Code flow with PKCE (`code_challenge` / `code_challenge_method=S256`) to allow external applications to connect securely to your tools:

```
External AI (ChatGPT / Claude)             Shuffle OAuth Server                Your Tenant Tools
           │                                        │                                  │
           │ ── 1. Redirect to /oauth/authorize ──> │                                  │
           │                                        │ (Prompt user: Select Org,        │
           │                                        │  Review Granular Scopes)         │
           │ <── 2. Return Authorization Code ───── │                                  │
           │                                        │                                  │
           │ ── 3. Exchange Code for Token ───────> │                                  │
           │ <── 4. Access Token Issued ─────────── │                                  │
           │                                                                           │
           │ ── 5. Standard MCP tools/call (Bearer Token) ───────────────────────────> │
```

- **Granular Scopes**: Permissions are strictly scoped. Users can grant or restrict access to specific capabilities:
  - `mcps:read`: Discover and inspect available MCP servers and tool definitions.
  - `mcps:execute` / `tools:call`: Execute tools and functions.
  - `apps:execute`: Trigger third-party app actions (Jira, Slack, CrowdStrike, etc.).
  - `workflows:run`: Execute automated security workflows and playbooks.
  - `incidents:read` / `incidents:write`: Query and update incident cases.
- **Centralized Multi-App Gateway**: Unlike standard MCP setups where an external LLM must connect to dozens of separate servers, Shuffle functions as a centralized gateway. A single OAuth connection grants the external model secure, audited access to thousands of enterprise tools.

<!-- TODO: Screenshot Needed: MCP App & Tools Authorization View
- Route / UI Location: /oauth/authorize (or /settings/mcp / Agent drawer tools tab)
- What to capture: The MCP authorization dialog showing requested granular scopes (mcps:read, apps:execute, workflows:run) and connected enterprise tools.
- Recommended filename: assets/ai-mcp-tools-configuration.png
- Inject syntax: ![MCP App & Tools Configuration](https://raw.githubusercontent.com/Shuffle/Shuffle-docs/master/assets/ai-mcp-tools-configuration.png)
-->

### Using Shuffle from ChatGPT

You can connect custom GPTs and ChatGPT Actions directly to Shuffle:
1. In ChatGPT, create a new Custom GPT or Action.
2. Provide Shuffle's OpenAPI schema for your selected app or use the global MCP manifest at `https://shuffler.io/api/v1/mcp`.
3. Set the Authentication method to **OAuth2**.
4. Configure the Authorization URL (`https://shuffler.io/oauth/authorize`) and Token URL (`https://shuffler.io/oauth/token`).
5. Authorize with your Shuffle account. ChatGPT can now search your apps, trigger actions, and query security data directly inside your chat conversations.

### Using Shuffle from Claude

Anthropic's Claude Desktop and Claude.ai can execute Shuffle tools via the MCP protocol:
1. Open your Claude Desktop configuration file (`claude_desktop_config.json`).
2. Add Shuffle as an MCP server with your API key or OAuth credentials:
   ```json
   {
     "mcpServers": {
       "shuffle": {
         "command": "npx",
         "args": ["-y", "@modelcontextprotocol/server-fetch", "https://shuffler.io/api/v1/mcp"],
         "env": {
           "SHUFFLE_API_KEY": "YOUR_SHUFFLE_API_KEY"
         }
       }
     }
   }
   ```
3. Restart Claude Desktop. Claude will discover all permitted Shuffle tools and can invoke them autonomously during analysis.

---

## Schemaless: Data Standardization with OCSF

One of the largest hurdles in security automation is data fragmentation: an IP reputation alert looks different in Splunk, Elastic, CrowdStrike, and Microsoft Defender. 

[Schemaless](https://schemaless.org) eliminates vendor lock-in by standardizing disparate security data against the **Open Cybersecurity Schema Framework (OCSF)**.

### How Schemaless Works

```
Heterogeneous Raw Alerts                  Schemaless Normalization            Standardized OCSF Output
┌───────────────────────┐                 ┌──────────────────────┐            ┌────────────────────────┐
│ Splunk / Elastic SIEM │ ──┐             │                      │            │ OCSF Class 2001:       │
├───────────────────────┤   ├───────────> │ LLM Context Mapping │ ─────────> │ Security Incident /    │
│ CrowdStrike / Defender│ ──┤             │   + Deterministic    │            │ Finding                │
├───────────────────────┤   │             │   OCSF Translation   │            │ (Uniform Observables)  │
│ Jira / TheHive Alerts │ ──┘             │                      │            └────────────────────────┘
└───────────────────────┘                 └──────────────────────┘
```

1. **Context-Aware Mapping**: Schemaless uses LLMs to understand the semantic context of incoming alerts and telemetry, regardless of the vendor's naming conventions.
2. **Deterministic Schema Enforcement**: The mapping is translated into deterministic rules conforming to standardized OCSF categories (e.g. Security Finding, Authentication Event, Network Activity).
3. **Portability for Agents**: Because data is normalized, Shuffle Agents and playbooks do not need custom parsers for each vendor. An agent trained to investigate an OCSF Security Finding can triage alerts originating from any SIEM or EDR automatically.

Learn more and explore the schemas at [schemaless.org](https://schemaless.org).

---

## Using Agents in Workflows

You can drag and drop AI Agents as native nodes inside any Shuffle workflow canvas to merge autonomous reasoning with deterministic business logic.

<img width="1018" height="227" alt="AI Agent in workflow" src="https://github.com/user-attachments/assets/de6fddbc-a9d1-4456-85d9-2b3ac4aee8ba" />

### 1. Add the AI Agent node
1. Open any workflow in [`/workflows`](/workflows).
2. Search for **AI Agent** in the left-hand app panel.
3. Drag the node onto the canvas and connect it to your trigger or preceding action.

### 2. Configure the Node
Click on the node to configure its parameters in the right-hand panel:
- **Input Prompt (`input`)**: Natural language instructions for the agent. Use workflow variable substitution (e.g. `Investigate alert: $webhook.body.details and check $webhook.body.ip in VirusTotal`).
- **Allowed MCPs / Apps**: Restrict the agent's tool access to specific apps (e.g. only allow `virustotal` and `jira`).
- **Reasoning Effort**: Choose between `minimal`, `low`, `medium`, or `high`.
- **Environment**: Designate execution on Shuffle Cloud or a local on-premises worker.

### 3. Consume Downstream Structured Output
The AI Agent returns a structured JSON payload available to subsequent workflow nodes:
- `$ai_agent.output` / `$ai_agent.message`: The final textual conclusion or executive summary.
- `$ai_agent.decisions`: Full array of individual tool calls and results.
- `$ai_agent.execution_id`: The execution ID for streaming or auditing.

### Building & Editing Workflows with AI

Shuffle provides natural language workflow generation directly inside the workflow builder:
- **Describe Your Goal**: Type a natural language description (e.g. *"When a phishing email is reported in Outlook, extract URLs, scan with VirusTotal, and create a Jira ticket if malicious"*).
- **Flowchart Upload**: Upload an image of an architecture diagram or flowchart. Shuffle's multimodal models parse the nodes and connections to generate the workflow canvas.
- **Workflow Chat Widget**: Use the inline chat assistant at the bottom of the canvas to make iterative updates (e.g. *"Add a Slack notification after the VirusTotal check"*).

---

## Architecture & Deployment Models

Shuffle's AI architecture is designed for enterprise scalability, regulatory compliance, and total environment flexibility.

### Cloud Architecture

In Shuffle Cloud, the architecture separates control plane orchestration from model execution:
- **Regional Model Routing**: When an agent or workflow makes an AI call, Shuffle checks the organization's regional setting (`SHUFFLE_GCE_LOCATION`). Requests are routed to regional Google Cloud Platform (Vertex AI / Gemini) clusters within your legal jurisdiction (e.g. EU or US data boundaries).
- **Tenant Isolation**: Model contexts and conversation memories are strictly isolated per tenant. No data from your prompts or tools is ever used to train foundational models.

<!-- ARCHITECTURE_DIAGRAM_CLOUD: High-level cloud architecture showing regional GCP Vertex AI routing and tenant boundaries -->
<div align="center">
  <p><em>(Shuffle Cloud Architecture: Regional Google Cloud Vertex AI / Gemini routing and tenant isolation)</em></p>
</div>

### On-Premises Architecture

Shuffle's on-premises deployment allows you to run all automation, agent decisions, and tool executions inside your own datacenter or private VPC:

- **Mode 1: Cloud Sync (Hybrid / Zero-GPU Infrastructure)**:
  - On-premises Shuffle Backend and Orborus workers handle 100% of network traffic, credentials, and app actions locally.
  - When an AI node or agent runs, the Backend sends an outbound HTTPS request to `https://shuffler.io/api/v1` authenticated by your `/admin` Cloud Sync key.
  - Inference runs on Shuffle Cloud's managed regional infrastructure, returning decisions back to the local backend.
- **Mode 2: Air-Gapped / Isolated (Zero Outbound Connectivity)**:
  - Shuffle connects exclusively to local inference servers (Ollama, vLLM, LM Studio, or local corporate gateway) over your internal network.
  - No connection to Shuffler.io is required or attempted.

<!-- ARCHITECTURE_DIAGRAM_ONPREM: On-premises architecture comparing Cloud Sync outbound inference vs Air-Gapped local LLMs -->
<div align="center">
  <p><em>(Shuffle On-Premises Architecture: Cloud Sync hybrid inference vs. 100% air-gapped local model execution)</em></p>
</div>

### Open-Source Algorithm References

Key components of Shuffle's agentic decision engine, execution loop, and MCP protocol parsers are open source and can be inspected in the official repository:
- Core data types and execution primitives: [`shuffle-shared`](https://github.com/shuffle/shuffle-shared)

---

## Agent & AI APIs

All AI and Agent features in Shuffle can be accessed programmatically via REST and JSON-RPC APIs:

- **[Run an Agent Action](/docs/API#run-an-agent-action)**: `POST /api/v1/agent` — Launches asynchronous agent tasks, returning an `execution_id` and stream authorization.
- **[Run an MCP Action](/docs/API#run-an-mcp-action)**: `POST /api/v1/mcp` — Executes tools synchronously via the standardized MCP `tools/call` method.
- **[Single App MCP](/docs/API#single-app-mcp)**: `GET / POST /api/v1/apps/{app_id}/mcp` — Scopes MCP interactions to a single tool integration.
- **[Listing Available Tools](/docs/API#listing-available-tools)**: `POST /api/v1/mcp` (method: `tools/list`) — Returns tool definitions and JSON schemas.
- **[Chat Completions](/docs/API#chat-completions)**: `POST /api/v1/chat/completions` — Direct OpenAI-compatible chat completions interface powered by Shuffle AI credits or local models.
- **[Initialize Connection](/docs/API#initialize-mcp-connection)**: `POST /api/v1/mcp` (method: `initialize`) — Performs protocol version handshake.
- **[Ping MCP Service](/docs/API#ping)**: `POST /api/v1/mcp` (method: `ping`) — Health check validating agent service availability.

---

## Troubleshooting

- **Local LLM Connection Refused**:
  - Verify that your local inference server (e.g. Ollama or LM Studio) is running and accessible from the machine hosting Shuffle Backend.
  - If Shuffle runs inside Docker, ensure you use `http://host.docker.internal:11434/v1` or the host's LAN IP rather than `localhost`.
- **Cloud Sync Not Working on On-Prem**:
  - Check **`/admin` -> Cloud Sync** and ensure your Shuffler.io API key is valid and connected.
  - Verify that your firewall allows outbound HTTPS traffic from the backend container to `https://shuffler.io/api/v1`.
- **OAuth2 Redirect Errors in ChatGPT / Claude**:
  - Ensure the redirect URI configured in ChatGPT or Claude Desktop matches your Shuffle tenant domain exactly.
  - Confirm that the requested scopes (`mcps:execute`, `tools:call`) have been approved during the authorization prompt.
- **Multimodal Flowchart Upload Fails**:
  - Image recognition requires a vision-capable model (such as Gemini 2.5/3.0 Flash on Shuffle Cloud, or a vision model like `llava` on local Ollama).

Need additional assistance? Reach out to the Shuffle team at [support@shuffler.io](mailto:support@shuffler.io) or join our community discussions.
