# AI at Shuffle
With AI becoming a larger part of the Automation space, the goal with AI at Shuffle is provide it in a deterministic, controllable and responsible way. The main use is for Workflow building, [Shuffle Security](https://security.shuffler.io) and [MCP connectivity](/docs/API#MCP) with third party platforms.

## Using LLMs 
Shuffle by default provides LLM credits. This is available to a certain level to those who use our Cloud or Hybrid offerings, and works infinitely with [self-hosted models](#how-to-set-up-a-self-hosted-ai-model-with-shuffle).

Since Shuffle's Agentic system is built by the Shuffle team from scratch, it means that it all runs locally where you want it with no third party requirements. 

## AI Agents
Agents are a way to have an AI model interact with the world. In Shuffle, this means using tools (playbooks) to perform actions. We intend to provide controllable, deterministic Agents that can be used to perform tasks.

**Some areas has been built for:**
- Tool Usage  (MCP: Detection, Collection, Enrichment & Response)
- Reasoning   (E.g. for workflow building and other heavy tasks)
- Correlation (Historical alerts and cases)

### How an Agent works under the hood
When you run an agent in Shuffle (whether from [/agents](/agents), in a workflow node, or via the API), it doesn't just send a raw prompt to an LLM and hope for the best. It runs a full execution loop built directly into Shuffle:

1. **Tool discovery**: Shuffle takes the tools you've selected (or all public apps + apps configured in your org) and exposes them to the model as standardized MCP definitions.
2. **Planning & Decisions**: The agent breaks your goal down into an array of **Decisions** (`AgentDecision`). Each decision represents a concrete step:
   - `tool`: The app to call (e.g. `virustotal`, `jira`, `slack`).
   - `action`: The exact action within that app (e.g. `get_ip_report`, `create_ticket`).
   - `fields`: The key-value arguments mapped to that action's parameters.
   - `confidence`: Confidence score (0.0 to 1.0) indicating how sure the model is about this step.
   - `reason`: A short explanation of why the agent chose this specific step.
   - `approval_required`: Set to `true` if this action is destructive or high-risk, pausing the run for human review.
   - `data_filter`: Tells Shuffle what to extract from the raw response (e.g. only specific fields) so your context window doesn't get flooded with megabytes of JSON.
3. **Execution**: Shuffle executes the decisions sequentially. Each action is dispatched either directly to the app (`execution_mode: "direct"`) or through Singul's normalized categories (`execution_mode: "singul"`).
4. **Context update**: The output from each executed tool feeds back into the agent's memory, allowing it to decide what to do next.
5. **Completion or Pause**:
   - If the agent has all the information it needs, it emits a `finish` decision and returns the final response.
   - If it needs clarification from you, it emits an `ask` decision and pauses in `WAITING` status.
   - If a step requires approval, it pauses until you approve or deny it.

<!-- VIDEO: 20-second screen recording showing an agent prompt being submitted in /agents, decisions appearing in sequence, and the final output card rendering -->

#### The Agent Decision structure
Under the hood, every step the agent takes looks like this:

```json
{
  "i": 0,
  "tool": "virustotal",
  "action": "get_ip_report",
  "fields": [
    {"key": "ip", "value": "1.1.1.1"}
  ],
  "reason": "Check the reputation of the suspicious IP found in the alert",
  "confidence": 0.95,
  "approval_required": false,
  "data_filter": "last_analysis_stats"
}
```

#### Reasoning effort
You can control how deeply the agent thinks before acting using the `reasoning` parameter:
- `minimal`: Fast single-step tool execution. Best for simple lookups (e.g. "Get details for CVE-2024-3094").
- `low`: Quick 2-3 step tasks with basic chaining.
- `medium`: The default setting. Balanced between speed and multi-step investigation.
- `high`: Deep reasoning. The agent performs cross-referencing, verifies intermediate results, and plans complex multi-app workflows.

### MCP
MCPs (Model Context Protocol) are the concept of having an AI Agent decide what actions to perform within a specific pool of available actions. It is typically used by agents as to have them be specialised, but there is nothing stopping them from being used directly as well.

[In Shuffle, **EVERY SINGLE APP** is an MCP](/docs/API#MCP). This is available with the  `POST /api/v1/mcp` API and is based on the [MCP standard](https://modelcontextprotocol.io/docs/getting-started/intro). You may even point to multiple apps at once.

The easiest way to try one in Shuffle is by going to [/agents](/agents), choosing an app (or more), and telling it what to use it for. This makes the agent act as an MCP. 

<img width="840" height="397" alt="image" src="https://github.com/user-attachments/assets/e0b2894f-2b4d-4d0c-a8ce-63561f780e97" />

They are also available for all apps in [Shuffle Security](https://security.shuffler.io/apps/outlook_office365). 

<img width="778" height="269" alt="image" src="https://github.com/user-attachments/assets/f9eed81b-4251-41b6-b3c6-c2a12c29d7e6" />

If you want to make your own API or Python script into an MCP, [make an app](/apps)! That is all it takes.

<img width="840" height="581" alt="image" src="https://github.com/user-attachments/assets/083032e8-131b-42e1-b945-df9001bd02bc" />

### Question handling
Questions are a way for the agent to fill in knowledge-gaps. In these cases, it asks questions automatically.

<img width="1463" height="762" alt="image" src="https://github.com/user-attachments/assets/f11cdf1f-75be-4829-b863-7c58ff396e1d" />

**PS:** Questions do NOT reach out to you as a realtime Notification **yet**, which is the future intention.

### Action Approvals
For sensitive actions, the agent is required to set the field "approval_required": true. This is a mechanism that stops the decision from automatically running, and instead waits for user input. 

If you want to see it in action, try `get my emails. Set approval_required: true for all API requests`

<img width="1443" height="146" alt="image" src="https://github.com/user-attachments/assets/efaa9964-24da-4b96-bf08-1a2779a7f7b2" />

This is currently 100% dynamically controlled by the agent directly, along with responding to pre-defined actions that should not run automatically.

**PS:** Action Approvals do NOT reach out to you as a realtime Notification **yet**, which is the future intention.

### Agent Continuations
Continuations are a way of changing or continuing the behavior of a previous AI Agent run. This makes it possible to "talk" to the agent after it is done with a task.

The field will automatically show up at the bottom, below the final output of the Agent run. 

<img width="1273" height="563" alt="image" src="https://github.com/user-attachments/assets/e09e937e-e9df-4a52-9d98-624b18e35d61" />

### Finding AI Agent runs
As with all platform-wide debugging in Shuffle, AI Agent runs are available in the [/workflows/debug](/workflows/debug) UI. By selecting "Agent Runs" at the top of the Workflow list, you will be given an overview of everything the agentic system has and will do in your environment.

<img width="1211" height="556" alt="image" src="https://github.com/user-attachments/assets/fd5aec29-3052-4e94-ade5-7199faa96342" />

## Using agents in Workflows
You can use AI Agents as regular nodes inside any Shuffle workflow. This lets you combine the flexibility of an AI agent with the deterministic control of a standard playbook. For example, you can have a webhook trigger a workflow, let an AI Agent investigate the alert and gather context, and then have standard Shuffle nodes handle the final ticketing and notifications.

<!-- VIDEO: 30-second walkthrough showing dragging the AI Agent node onto the canvas, configuring the prompt with $webhook variables, selecting allowed apps, and running a test execution -->

<img width="1018" height="227" alt="image" src="https://github.com/user-attachments/assets/de6fddbc-a9d1-4456-85d9-2b3ac4aee8ba" />

### 1. Add the AI Agent node
1. Open or create a workflow in the workflow builder (`/workflows`).
2. Search for **AI Agent** in the left sidebar app list.
3. Drag the **AI Agent** node onto the canvas and connect it to your trigger or previous node.

<!-- SCREENSHOT: Dragging the AI Agent node from the left app panel onto the canvas and connecting it to a Webhook node -->

### 2. Configure the Node
Click on the AI Agent node to open its configuration panel on the right sidebar:

- **Input Prompt (`input`)**: Tell the agent what task to perform. You can pass variables from previous nodes using Shuffle's standard syntax (e.g. `Analyze this alert: $webhook.body.message and check any IPs in VirusTotal`).
- **Allowed MCPs / Apps**: By default, the agent has access to all enabled tools in your organization. You can scope it down to specific apps (e.g. only allow `virustotal` and `jira`). This keeps the agent focused and prevents it from calling apps it shouldn't touch.
- **Reasoning Effort**: Choose between `minimal`, `low`, `medium`, or `high` depending on task complexity.
- **Environment**: Choose where the agent executes — either in Shuffle Cloud or on a specific on-premises runtime location / worker.

<!-- SCREENSHOT: The right-hand configuration panel for the AI Agent node, highlighting the Input prompt with a variable ($webhook.body), the Allowed MCPs dropdown, and the Reasoning selector -->

### 3. Using the Agent's output downstream
When the AI Agent finishes running, it outputs a structured JSON object. Downstream nodes can reference its output directly:

- `$ai_agent.output` or `$ai_agent.message`: The final summary or textual answer produced by the agent.
- `$ai_agent.decisions`: The full array of decisions, tools called, and results.
- `$ai_agent.execution_id`: The backing execution ID for auditing or streaming.

Example: You can add a condition branch right after the agent node:
- If `$ai_agent.output` contains `"MALICIOUS"`, route to a Slack alert node.
- Otherwise, log the result and finish.

## Singul
Singul works against vendor-locking with our translator for different providers of the same tools, such as Slack vs Teams vs Discord (communication), or Splunk vs Elastic vs QRadar (SIEM). It uses LLMs to understand the context of what you are trying to perform, and makes a determinsitic translation to use a standard such as OCSF or STIX. This is a powerful way to avoid vendor lock-in, and to make your automation more future-proof. 

A good example of this being used actively is [Shuffle Security](https://security.shuffler.io), where we ingest tickets and handle enrichment in a standardised format.

Read the [usage Shuffle Docs here](https://github.com/Shuffle/openapi-apps/blob/master/docs/singul.md)
Website: [https://singul.io](https://singul.io)

## App generation
App generation is a system built to generate Rest API apps from documentation URLs. It works by emulating a browser with which it crawls the documentation.

<img width="1281" height="425" alt="image" src="https://github.com/user-attachments/assets/002f9079-b4fa-4c3f-8cf9-54ad29a65c07" />

### 1. Navigate to the App page
Go to [/apps](/apps)

### 2. Click "Create an App"

### 3. Click "Generate from Documentation"

<img width="601" height="417" alt="image" src="https://github.com/user-attachments/assets/f82fa8d1-61f7-4165-bf00-b10deb4e773c" />

### 4. Paste a URL and hit "Generate". This may take up to a few minutes.

Sample URL: https://docs.virustotal.com/reference/ip-info

<img width="617" height="371" alt="image" src="https://github.com/user-attachments/assets/1ecf31a9-c85c-439d-b6b3-1dbb5d721afe" />

### 5. You get a valid App that can be used in seconds!

<img width="621" height="579" alt="image" src="https://github.com/user-attachments/assets/a0fac4a2-a5b3-433a-808d-0615f5e29bb5" />

### 6. Save it, then start using it in workflows. 

## Workflow generation
This guide will walk you through creating a complete, functional Shuffle workflow in seconds, just by describing what you want to do in plain English.

### 1: Navigate to the Workflow Page
* In the navigation sidebar on the left, click on "Workflows". This will take you to the `/workflows` page where you'll see your list of existing workflows.

### 2: Click "Create Workflow"
* In the top right corner of the Workflows page, click the "Create Workflow" button.

<img width="1200" height="966" alt="create_workflow" src="https://github.com/user-attachments/assets/8938b032-db6f-4f25-b8bb-578f241c638c" />

### 3: Describe Your Goal

****You have two options: writing a description or uploading a flowchart.****


***Option A: Write a Text Description***

<img width="600" height="650" alt="AI_generate_page" src="https://github.com/user-attachments/assets/c756caf1-a32b-4b56-bd5a-81fc2ec879dd" />


* At the top of the canvas, you will see a text box that says "Describe your workflow in natural language...". This is where the magic happens.
* Click inside this box and type out the process you want to automate.

**Tips for a Great Description:**
* **Be Specific:** Instead of "Check a URL," try "Check a URL in VirusTotal."
* **Name Your Tools:** Mention the specific apps you want to use (e.g., "Open a ticket in Jira," "Send a message to Slack").

**Example Description:**
  When a phishing email is reported, get the URL from the email body. Check the URL's reputation in VirusTotal. If the score is above 5, create a new ticket in      TheHive and send a high-priority alert to the 'security-alerts' channel in Slack.

***Option B: Upload a Flowchart Image***

If you prefer to visualize your process, you can upload an image of a flowchart. The AI will analyze the shapes, text, and connections in the diagram to build your workflow.

<img width="600" height="650" alt="flowchart" src="https://github.com/user-attachments/assets/a484e0ed-3f21-4a3c-a8f3-dbd333a893e4" />

* Look for the large box below the "Description" field that says "Generate Workflow from Flowchart" with a cloud upload icon.

* Click anywhere inside this box. This will open your computer's file browser.

* Select a flowchart image (e.g., a .png, .jpg, or .jpeg file up to 5MB in size) from your computer.

**Pro Tip:** Add a Description for Even Better Results
Even after uploading your flowchart, we recommend adding a brief text description in the "Description" box (mentioned in Option A).

Think of this description as extra instructions for the AI model. It helps clarify any details or ambiguities in the flowchart and provides specific context, leading to an even more accurate and powerful workflow.

**Example description to add:**

This flowchart shows our phishing response process. The goal is to automate the URL check with VirusTotal and create a Jira ticket for malicious findings.

**Important Note for Self-Hosted Users:**
The ability to process images depends entirely on your AI model. This feature is fully supported when using Shuffle Cloud's default model. If you are using a self-hosted model (like Ollama), you must ensure it is a multimodal model (one that can understand both text and images) for this feature to work correctly.


### 4: Generate the Workflow

* Once you are satisfied with your description or uploaded flowchart, click the 'AI Generate' button.
* Wait a few moments. The AI will analyze your request and automatically build the workflow on the canvas, complete with the right apps and connections.

### 5: Review and Customize
* The AI-generated workflow is a powerful starting point. You can now:

* Click on each app to configure its specific settings (e.g., authenticating with your Jira account).

* Drag and drop new apps onto the canvas.

* Modify the connections between the apps.

**Congratulations! You've just built an automation workflow using AI.**

## Editing a Workflow with AI
Instead of building or modifying workflows node-by-node from scratch, you can use Shuffle's inline **Agent Chat Widget** directly inside the workflow builder to create and modify workflows with natural language.

<!-- VIDEO: 30-second screen capture of opening an existing workflow, clicking the Agent Chat widget at the bottom, typing "Add a VirusTotal check for the IP in $webhook, and send a Slack message if malicious", and watching the nodes appear and connect on canvas -->

### Using the Workflow Chat Widget
1. Open any workflow in the editor (`/workflows/{workflow_id}`).
2. Click the **Agent Chat** icon on the bottom toolbar to open the chat widget.
3. Describe what you want to add, change, or remove:
   - *"Add a VirusTotal IP check after the webhook node."*
   - *"If the reputation score is above 5, create an issue in Jira and notify #soc-alerts in Slack."*
   - *"Change the Slack channel parameter from #general to #security-critical."*
4. Click **Send**. The agent inspects your canvas, determines what apps and connections are needed, updates the workflow structure, and saves it.

<!-- SCREENSHOT: The workflow editor with the Agent Chat Widget open at the bottom, showing a conversation with the agent and the updated canvas nodes in the background -->

### Interactive Clarifications
If the agent needs more context to complete your request (for example, which Jira project to use, or how to handle error branches), it will pause and ask you directly inside the chat widget. You can answer the question inline, and the agent will immediately resume and finish modifying the canvas.

### Iterative Building
You don't need to describe your entire playbook in one giant prompt. You can build iteratively:
1. Start with the core trigger and first action: *"Start with a webhook and parse the email body."*
2. Add enrichment: *"Now add a lookup to AlienVault OTX for any domain found in the email."*
3. Add response actions: *"If any indicators are malicious, block the sender in Microsoft Defender."*

## AI Architecture & Deployment Models
Shuffle's AI framework is designed to work across any infrastructure—from fully managed cloud instances to strictly isolated, air-gapped on-premises deployments.

### 1. Cloud: Shuffle AI & Regional Gemini Routing
In Shuffle Cloud, AI features and Agent runs work out of the box using built-in **Shuffle AI credits**.
- **Region-based routing**: Agent and LLM calls are dynamically routed to Google Vertex AI / Gemini endpoints (`google/gemini-3.7-flash` or `gemini-3.8-flash`) within your deployment's geographic region based on `SHUFFLE_GCE_LOCATION`. This ensures data residency and compliance within regional borders (such as EU or US data boundaries).
- **Using Shuffle AI Credits via API**: You can also use your Shuffle AI credits programmatically outside of workflows by sending standard OpenAI-compatible requests to the `/api/v1/chat/completions` endpoint on Shuffle Cloud with your Shuffle API key.
- **Custom model overrides**: Even on Cloud, organizations can override the default Shuffle AI model on a per-organization basis by configuring an active model in the UI.

### 2. Hybrid: Self-Controlled Models
In Hybrid setups (where workflow execution happens on-prem or in private networks while orchestrating via Cloud), you can bring and control your own AI model.

**How to enable a self-controlled model:**
1. **Via the `/agents` UI (Recommended)**:
   - Navigate to the Agents page ([`/agents`](/agents)).
   - Click on the **Shuffle AI** button in the top configuration area.
   - A sidebar will open on the right side: select your preferred model provider or self-hosted endpoint from the list.
   - Enter your endpoint URL, model name, and API key / credentials.
   - **Shuffle AI Limits**: This sidebar is also where your organization's Shuffle AI limits, quota usage, and remaining credits are displayed.
   - Once saved and selected, all agent actions and workflow AI calls in your organization immediately route to your custom model with zero container restarts.

<!-- SCREENSHOT: The /agents page with the "Shuffle AI" button highlighted, showing the opened right-hand sidebar with the model provider selector, custom endpoint configuration, and the Shuffle AI limits/usage display -->

2. **Via Docker Compose Environment**: Alternatively, you can set `AI_API_URL`, `AI_MODEL`, and `AI_API_KEY` directly on the `shuffle-backend` container.

### 3. On-Premises: Cloud Sync vs. Self-Controlled Model
For 100% on-premises installations, you have two architectural options depending on whether you want to host local GPU infrastructure:

- **Option A: Self-Controlled Local Model (100% Air-Gapped)**
  - Connect Shuffle to a local Ollama, vLLM, or corporate LLM gateway using the `/agents` UI sidebar or the environment variables described above.
  - No data ever leaves your internal network, making it suitable for air-gapped and strictly regulated networks.

- **Option B: Cloud Sync (Shuffle AI Fallback)**
  - If you do not have local GPU hardware, you can leverage Shuffle AI without managing models locally.
  - **Prerequisite**: Cloud Sync must already be configured on the **`/admin`** page (navigate to `/admin` -> Cloud Sync, and enter your Shuffler.io API key).
  - Once configured on `/admin`, on-prem Shuffle will automatically fall back to forwarding agent and AI requests over HTTPS to `https://shuffler.io/api/v1` whenever no local model is set up.
  - This allows your on-prem workers to execute playbooks locally while utilizing Shuffle Cloud's managed Gemini regional infrastructure and AI credits.

<!-- SCREENSHOT: The /admin page highlighting the Cloud Sync configuration section with the API key entered and connection status verified -->

## Using self-hosted AI models

While Shuffle's Cloud platform provides AI credits to get you started, connecting your own self-hosted AI model gives you ultimate control and flexibility. This guide will walk you through setting up a local Ollama instance.

**Before you configure Shuffle, please ensure you have the following ready:**

1. A Server to Run the AI: You need a computer that Shuffle can reach over the network. This can be a VM, physical server or a cloud instance.
2. We recommend Ollama as the simplest way to run local AI models. Go to [Download Ollama](https://ollama.com/download) to install it on your server. After installation, make sure the Ollama service is running.
3. Once Ollama is installed, you need a model for it to serve. We recommend standard instruction-tuned models like `llama3` or `qwen2.5`.

Open your server's terminal and run:

```bash
ollama run llama3
```

### Setting Up Environment Variables in Shuffle

Once your self-hosted AI model is running, you can proceed with setting up the necessary environment variables in Shuffle.

**Step 1: Find Your AI Server Details**

You will need the following information from your self-hosted AI server:

* The full URL of the API (e.g., http://192.168.1.55:11434/v1).
* The exact name of the model you want to use (e.g., llama3).
* An API key (if your server requires authentication).

**Step 2: Set the Environment Variables**

`AI_API_URL` (Required)

* What it is: The full URL to your AI server's API endpoint.

Example: 
```bash
AI_API_URL=http://localhost:11434/v1
```

`AI_MODEL` (Required)

* What it is: The exact name of the model you want Shuffle to use.

Example:
```bash
AI_MODEL=llama3
```

AI_API_KEY (Optional)

* What it is: The API key or token if your server requires authentication.

Example:
```bash
AI_API_KEY=sk-mysecretkey123
```

Shuffle can support any self-hosted model that implements the OpenAI API interface. Examples include Ollama, local LLMs wrapped with OpenAI-compatible endpoints, or any other model that exposes the same API.

Once these are set, there is no need to restart your Shuffle backend server as the checks happen in real-time. The AI features will be automatically enabled, allowing you to use them immediately.

**Note: You need to refresh the Shuffle UI page in your browser for the new AI features to appear.**

## AI for quicker Support
Shuffle includes built-in AI debugging and documentation assistance to help you resolve workflow errors and configuration questions without waiting for support tickets.

<!-- SCREENSHOT: The AI support / error helper modal in an execution debug view, explaining an error message and highlighting the fix in the action parameter config -->

### How it works
1. **Execution Debugging**: When an action in a workflow fails (e.g. HTTP 400/401/500, invalid JSON path, or authentication mismatch), click **Ask AI** in the execution log.
2. **Context-Aware Diagnosis**: The AI analyzes the error message, the action parameters, and Shuffle's documentation vector store (`OPENAI_DOCS_VS_ID`).
3. **Actionable Fixes**: Instead of generic error messages, it explains what went wrong in plain English and gives you the exact parameter or authentication fix needed.
4. **Direct Escalation**: If the issue requires assistance from the Shuffle team, the helper packages your sanitized error logs and context so you can email [support@shuffler.io](mailto:support@shuffler.io) with one click.


## Troubleshooting

* Ensure your AI server is running and reachable at the URL you provided.
* If using authentication, double-check the API key.
* Use the exact model name available on your self-hosted AI instance.

If anything else goes wrong, please contact support@shuffler.io
