# Workflows
Documentation for workflows.

## Table of contents
* [Introduction](#introduction)
* [What you need to know](#what-you-need-to-know)
* [Workflow Basics](#workflow-basics)
  * [Create](#create)
  * [Edit](#edit)
  * [Save](#save)
  * [Execute](#execute)
  * [Duplicate](#duplicate)
  * [Delete](#delete)
  * [Export and Import](#export-and-import)
* [Create Your First Workflow](#create-your-first-workflow)
* [Nodes](#nodes)
  * [Anatomy of a workflow](#anatomy-of-a-workflow)
  * [Building efficiently](#building-efficiently)
  * [Starting node](#starting-node)
  * [Apps and actions](#apps-and-actions)
  * [HTTP App and REST API](#http-app-and-rest-api)
* [Variables and Arguments](#variables-and-arguments)
  * [Execution Argument](#execution-argument)
  * [Workflow Variables](#workflow-variables)
  * [Execution Variables](#execution-variables)
  * [JSON Autocompletion](#json-autocompletion)
* [Passing Values](#passing-values)
* [Parsing JSON](#parsing-json)
* [Passing Lists](#passing-lists)
* [Casting Values](#casting-values)
* [Conditions](#conditions)
  * [IF Conditions](#if-conditions)
  * [Condition Loops](#condition-loops)
* [Authentication](#authentication)
  * [App Authentication](#app-authentication)
  * [Workflow Authentication](#workflow-authentication)
* [Triggers](#triggers)
  * [Webhook](#webhook)
  * [Schedule](#schedule)
  * [Subflow](#subflow)
  * [User Input](#user-input)
  * [Pipelines](#pipelines)
  * [Email](#email)
* [Handling Files](#handling-files)
  * [Useful file handling info](#useful-file-handling-info)
  * [Using files](#using-files)
  * [File uploads via the App Creator](#file-uploads-via-the-app-creator)
* [Shuffle Datastore](#shuffle-datastore)
* [Typical Use Cases](#typical-use-cases)
  * [Deduplication](#deduplication)
  * [Formatting](#formatting)
  * [HTTP Requests](#http-requests)
* [Subflows and Loops](#subflows-and-loops)
* [Exploring Executions](#exploring-executions)
  * [Execution List](#execution-list)
  * [Execution Details](#execution-details)
  * [Workflow Run Debugger](#workflow-run-debugger)
* [Collaboration Features](#collaboration-features)
  * [Sub-Tenant Distribution (Beta)](#sub-tenant-distribution-beta)
  * [Workflow Revisions & Versioning](#workflow-revisions--versioning)
  * [Authentication Groups (Beta)](#authentication-groups-beta)
  * [Multiplayer (Beta)](#multiplayer-beta)
  * [Forms](#forms)
* [API](#api)
* [Workflow Backup](#workflow-backup)
  * [GitHub Integration](#github-integration)
  * [Azure DevOps Integration](#azure-devops-integration)

## Introduction

Workflows are the backbone of Shuffle. A workflow is a structured, event-driven automation pipeline that connects apps, data, and logic to execute tasks automatically. Instead of writing code to connect your tools, you build workflows visually using four building blocks: [apps](/docs/apps), [triggers](/docs/triggers), [conditions](/docs/conditions), and [variables](/docs/apps/#variables).

### Why workflows matter

- **They eliminate manual work.** No more copy-pasting data between tools or running the same checks by hand every time an alert comes in.
- **They ensure consistency.** Every piece of data gets handled the same way, every time. No forgotten steps, no typos.
- **They facilitate tool synergy.** Different tools that don't natively talk to each other — your SIEM, ticketing system, chat app, firewall — all connected through a single workflow.
- **They scale without scaling people.** A person can handle a handful of alerts. A workflow handles hundreds, at any hour, without slowing down.

### How it works

Every workflow follows a simple pattern: **Input → Action → Output**.

You need three parts:

- **The Trigger** — Tells the workflow when to run. This can be a webhook receiving data, a schedule that runs on an interval, or a manual click.
- **The Nodes (Apps)** — The steps in your process. Each node is an app performing a specific action. For example, one node scans a file with VirusTotal, the next sends the results to Slack.
- **The Lines** — Connect your nodes. They define execution order and pass data between steps.

### Ways to create your first workflow

**1. Use Cases**

[Use Cases](https://shuffler.io/usecases) contains pre-made templates. Click "enable" on any use case and Shuffle spins up a ready-made workflow for you. This is the fastest way to get started.

**2. AI generation**

If you know what you want but aren't sure which nodes to use, type a plain English prompt. For example: "When a new ticket arrives, scan the IP address with VirusTotal." Shuffle generates the nodes and connections automatically. This feature is currently in Beta.

[Read more about AI generation →](https://shuffler.io/docs/AI#workflow-generation)

**3. Manual setup**

Build from scratch when you need custom logic. Go to [workflows](https://shuffler.io/workflows), click "Create workflow," give it a name, and start dragging apps onto the canvas.

[Go to workflows to get started →](https://shuffler.io/workflows)

### What you need to know

We recommend going through the [Workflow Development Exercises](https://github.com/Shuffle/Shuffle-docs/blob/master/handbook/engineering/workflow_development_exercises.md) before building. It covers the fundamentals so you can build anything, not just follow tutorials.

The checklist:

1. Variables & nodes
2. JSON autocompletion
3. Loops
4. Nested loops
5. [Start nodes](https://shuffler.io/workflows/0285a05e-8dc0-4614-840b-88606d6a1e59) 
https://youtu.be/ba1QQwATiik?si=KTUVPL6a8EJyuNze
6. Triggers: Webhooks & Schedules
7. Subflows & User Input
8. [App Authentication](https://shuffler.io/workflows/d65d228a-f406-4227-9fa7-f7d9303f8411)
9. Loop filtering
10. [Shuffle File storage](https://shuffler.io/workflows/dd5e3800-2f2e-4089-8055-b500e3b8b349)
11. [Shuffle Datastore (Cache)](https://shuffler.io/workflows/f39a3c37-4f38-4ca0-952a-a9425080b44e)
12. Deduplication
13. [Liquid formatting](https://shuffler.io/workflows/0d604c52-1b3f-49d8-a57e-480baf07ab8d)
14. [HTTP & REST APIs](https://shuffler.io/workflows/b8a3a70a-f3f9-459f-99b3-7a2723a1a4b8)

### Finding relevant workflows

Before building from scratch, [search public workflows](/search?tab=workflows). Someone may have already built something close to what you need. Use it as a starting point and modify it to fit your use case.


## Workflow Basics

Below is a GIF showing the full workflow creation process — from creating a new workflow to editing, saving, and executing it.

https://youtu.be/BBIKTIrsvxc?si=qZ70r1wGjGX4_rig

### Create

Go to the [workflows](/workflows) dashboard and click "Create workflow." Give it a name and a short description. Both can be changed later.

<img width="1656" height="898" alt="Screenshot 2025-08-28 183003" src="https://github.com/user-attachments/assets/2d409adb-718c-4368-98c6-9bbd2f61bea7" />

<img width="1913" height="862" alt="new-workflow" src="https://github.com/user-attachments/assets/92b74e0a-6d61-4ece-84bf-2bda60c7019a" />

All of your workflows live at [/workflows](/workflows), so you can always find them again.

### Edit

After creating a workflow, the editor opens. The left panel lists four building blocks: [apps](/docs/apps), [triggers](/docs/triggers), [variables](/docs/apps#variables), and [conditions](/conditions). Apps and triggers can be dragged onto the canvas.

<img width="1440" height="810" alt="Screenshot 2026-07-01 at 4 04 23 PM" src="https://github.com/user-attachments/assets/f11c1cf8-dac0-4e00-b3b1-89126b1b45a0" />

A new workflow starts with a default "change_me" node. You can edit it or delete it. Drag an app onto the canvas, click it, and select an action from the dropdown. The default action — "repeat back to me" from the Shuffle Tools app — simply returns its input. Swap it for whatever action you actually need.

<img width="1440" height="808" alt="Screenshot 2026-07-01 at 4 05 25 PM" src="https://github.com/user-attachments/assets/4365c493-8986-409c-a26c-8259059ac828" />

The play button starts an execution at your starting node. A side panel shows the output for each node as it runs.

### Save

Click the save button next to the play button, or press Ctrl+S. A notification appears at the bottom of the screen when saving is in progress. You need to save before executing — saving makes your latest edits available to the execution engine.

<img width="1440" height="810" alt="Screenshot 2026-07-02 at 7 28 57 PM" src="https://github.com/user-attachments/assets/e08b8d86-9653-4567-a407-43fd754731c8" />

### Execute

With a saved workflow, click the Orange play button. Execution begins at your starting node, and a side panel opens showing results for each node as it completes.

<img width="1044" height="80" alt="Screenshot 2026-07-02 at 7 31 39 PM" src="https://github.com/user-attachments/assets/ffed7c6e-9473-43ea-9918-068317be6b84" />

To review past executions, go to [/workflows](/workflows), click the name of your workflow, and click the activity icon. It shows the status and output of every previous run.

<img width="919" height="96" alt="Screenshot 2026-07-02 at 10 19 30 PM" src="https://github.com/user-attachments/assets/15fce389-146f-4867-82f4-f98a38be3142" />

<img width="600" height="700" alt="new-execution-list" src="https://github.com/user-attachments/assets/f84660c1-c8c6-4afb-8db5-13e782081fc4" />

### Duplicate

Click the kebab menu (vertical three dots) on the workflow and select "Duplicate Workflow." A copy appears with a `_copy` suffix in the name. Use this to experiment without risking your original.

<img width="253" height="74" alt="Screenshot 2026-07-02 at 10 46 40 PM" src="https://github.com/user-attachments/assets/0dd759ce-755e-41c7-ae8c-5638fb2f77ed" />

### Delete

Click the kebab menu (vertical three dots) and select "Delete Workflow." Confirm the deletion when prompted.

<img width="481" height="210" alt="Screenshot 2026-07-02 at 10 52 13 PM" src="https://github.com/user-attachments/assets/77938d01-52c0-4670-ac6b-dcc7ce585899" />

**Note:** workflows that reference this one as a subflow will break after deletion.

<img width="252" height="84" alt="Screenshot 2026-07-02 at 10 52 47 PM" src="https://github.com/user-attachments/assets/3ca0c811-89fe-4a99-891b-e713e5ec17c2" />

### Export and Import

**Export:** Click the kebab menu (vertical three dots) on a workflow and select "Export Workflow." A JSON file downloads containing the full workflow definition — nodes, connections, variables, and authentication references. Use this to back up a workflow locally or move it between tenants.

<img width="397" height="288" alt="Screenshot 2026-07-02 at 10 56 37 PM" src="https://github.com/user-attachments/assets/5a27d146-0103-4d06-b0ad-aa78bd642317" />

**Import:** Go to [/workflows](/workflows) and drag the exported JSON file onto the page, or use the import option in the workflow list. The workflow appears with its original name. You may need to reconfigure authentication for apps that require credentials in the new tenant.

<img width="1084" height="245" alt="Screenshot 2026-07-02 at 10 58 27 PM" src="https://github.com/user-attachments/assets/db0880f4-ed68-43f4-8fd0-fcdcf3ac29d4" />

You can also download workflows directly from Git repositories. See [Workflow Backup](#workflow-backup) for GitHub and Azure DevOps integration.

## Create Your First Workflow

This section walks through building a simple workflow from scratch: two nodes, connected, with data passing between them.

**Goal:** Send a message via the HTTP app and print the response.

### Step 1 — Create the workflow

1. Go to [workflows](https://shuffler.io/workflows).
2. Click "Create workflow."
3. Name it "My First Workflow" and click the checkmark.

https://youtu.be/BBIKTIrsvxc?si=qZ70r1wGjGX4_rig

### Step 2 — Add a starting node

1. The canvas opens with a default "change_me" node. Click it.
2. In the right panel, select an app and action. For this example, choose the **Testing** app and the **Repeat back to me** action.
3. In the input field, type a test message: `{"hello": "world"}`.
4. This is your starting node (marked with a turquoise border).

### Step 3 — Add a second node

1. Drag the **Shuffle Tools** app from the left panel onto the canvas.
2. Place it to the right of the starting node.
3. An arrow automatically connects them. If not, drag a line from the output of the first node to the input of the second.
4. Click the Shuffle Tools node and select the **Repeat back to me** action.
5. For the input, click the field and select the output of the previous node from the dropdown (or type `$change_me`).

### Step 4 — Execute

1. Click the save button (diskette icon).
2. Click the green play button.
3. A side panel opens showing the execution progress. Each node turns green as it completes.
4. Click the second node in the panel to see its output — it should match the input from the first node.

You have built a working workflow. From here, you can swap the Testing app for a real service (like sending an email or querying an API), add conditions to branch the logic, or chain more nodes for additional steps.

### Building further

Once you are comfortable with a two-node workflow:
- Add a third node that sends the result to Slack or email
- Add a condition on the branch between nodes so the second node only runs if the first succeeds
- Replace the static input with a webhook trigger so the workflow runs on incoming data
- Use a subflow to pass list items to a separate workflow for parallel processing

## Nodes

Apps become nodes when you drag them onto the workflow canvas. Each node represents an app action — a specific call to an external tool or service.

To add a node, drag an app from the left panel onto the canvas. Click a node to configure it on the right side.

### Anatomy of a workflow

A well-structured workflow follows a clear pattern:

- **Trigger** — receives the initial input (webhook, schedule, etc.)
- **Starting node** — the first app action that processes the trigger data
- **Processing nodes** — apps that transform, enrich, or act on the data
- **End node** — the final action, such as sending a notification or closing a ticket

Below is a Video showing the full structure of a complex workflow, including how to organize and read it.

https://youtu.be/55ZKCZuIXNg?si=9ALTPuo_M63N1Gde

### Building efficiently

The fewer nodes a workflow uses, the faster it runs and the easier it is to maintain. Before adding a new node, check whether an existing app action can handle the same step.

### Starting node

The starting node is the first action that runs when a workflow executes. It is marked with a turquoise circular border. It is not a trigger — it is the first app action that receives data from a trigger.

To change the starting node, hover over a different node until you see the "FLAG ICON"and press it, you should see it in the top-right corner when hovering over a node. The shape of the node should also change from a square to a circle

### Apps and actions

An app bundles one or more actions that connect to a specific service. Apps must be activated within your tenant before they can appear in the left panel.

Each app action requires authentication. Click the app on your workflow, go to Setup, and press the plus icon to add your credentials. Authenticated apps in one workflow are available across your tenant and you can distribute them all across your sub-tenants.

### HTTP App and REST API

Shuffle includes a built-in HTTP app for making REST API calls to any endpoint. Use it when no dedicated app exists for a service, or when you need more control over the request than a dedicated app provides.

The HTTP app supports:
- All HTTP methods (GET, POST, PUT, PATCH, DELETE)
- Custom headers
- Query parameters
- Request body (JSON, form data, raw text)
- Basic and Bearer token authentication

This is the same app you would use to call the Shuffle API itself from within a workflow. For example, you can use the HTTP app to trigger another workflow via its webhook URL, or to fetch data from an internal service that does not have a dedicated Shuffle app.

Compare this to dedicated apps (like the GitHub app or Outlook app), which wrap the same HTTP calls into pre-configured actions with built-in authentication. A dedicated app is easier to use; the HTTP app is more flexible.

**Other built-in apps:** Shuffle also includes several other pre-installed apps:
- **Shuffle Tools** — utility actions: set variables, filter lists, merge lists, parse lists, execute Python code
- **AI Agent** — run AI agent tasks within a workflow using MCP
- **Subflow** — trigger another workflow from within the current one
- **Testing** — create test files and mock data directly in a workflow

All other apps must be activated before they appear in the left panel. Once activated, they are available across your tenant.

## Variables and Arguments

### Execution Argument

The execution argument is the input that starts a workflow run. Every trigger provides one. You can also supply one manually when running a workflow by hand.

It can be anything: JSON, a string, a number, a list. It acts like a node — you can reference its value anywhere using:

- `$exec`
- `$trigger`
- `$webhook`
- `$schedule`
- `$userinput`
- `$email_trigger`

All of these refer to the same value: the data that triggered the execution. Use `$exec` as the default.

### Workflow Variables

Workflow variables are static values set before execution. They persist across runs and are shared with everyone who has access to the workflow. Common uses: API keys, base URLs, usernames. 

**Characteristics:**

- Set before execution
- Unencrypted
- Shared with all workflow users
- Accessible only within the workflow where they're defined

**How to create a workflow variable:**

1. Click "Variables" in the bottom-left corner.
2. Click "new workflow variable."
3. Enter a name, description, and value.
4. Reference it with `$variable_name` in any node or condition.

### Execution Variables

Execution variables are temporary values set *during* a run. They exist only for that execution and are not saved. Use them to capture the result of an action for use later in the same run.

**How to set a runtime variable:**

1. Click "Variables" in the bottom-left corner.
2. Click "New runtime variable."
3. Give it a name.
4. On the action you want to capture, select the variable. The result of that action is stored in the variable.
5. Reference it with `$variable_name` in any subsequent node.

### JSON Autocompletion

When you click into a field that accepts references, Shuffle shows an autocomplete dropdown listing all available nodes and variables. Click the plus button next to a field to open it.

The dropdown shows each node's output structure. You can navigate through JSON keys and select the exact value you need — without typing the `$` syntax by hand. This is especially useful when working with deeply nested responses or when you are unsure of the exact key names.

If the output structure is not yet available (for example, the referenced node has not been executed), you can type the path manually. Use the `$node.key` and `$node.key.subkey` syntax described in [Parsing JSON](#parsing-json).

## Passing Values

Passing data from one node to the next is the core of how workflows work. There are two ways:

- **"Data from previous actions"** — select the output of any earlier connected node from the dropdown.
- **"Static data"** — type the value yourself, using `$node_name` or `$variable` syntax to reference data.
- **"copy the JSON path"** — click on the value if what you want to copy if it is in the result of another node.

You can reference:

- `$testing_1` — output from a node or variable called "testing_1"
- `$exec` — the execution argument

This only works with nodes that precede the current one, connected via the directional arrows.

## Parsing JSON

Shuffle uses `$` to reference nodes and `.` to traverse JSON keys.

| Expression | Meaning |
|---|---|
| `$node_1` | Output of node called "node_1" |
| `$exec` | The execution argument |
| `$exec.name` | The `name` key inside the execution argument |

Given this execution argument:

```json
{
  "name": "this is some data",
  "description": "Cool description",
  "extra": {
    "writer": "Fredrik"
  }
}
```

- Get `name` → `$exec.name`
- Get the nested `writer` → `$exec.extra.writer`

If a node doesn't exist or the key is missing, Shuffle writes the expression as-is.

## Passing Lists

Lists are identified with `#`. This is separate from `$` (which references nodes).

| Syntax | Meaning |
|---|---|
| ` ` | No loop — returns the raw value |
| `.#` | Loop over the entire list |
| `.#0` | Only the first element |
| `.#1` | Only the second element |
| `.#0-1` | First and second elements |
| `.#.data` | Loop over list, get `data` from each item |
| `.#0.data` | First element, get `data` |
| `.#max.data` | Last element, get `data` |

**Example:** Suppose you have a node called `get_users` that returns this data:

```json
{
  "users": [
    {"name": "fredrik", "username": "@frikky", "id": "12345"},
    {"name": "moomo", "username": "shuffle user 2", "id": "23456"}
  ]
}
```

To extract all IDs:

```
$get_users.users.#.id
```

Result: `["12345", "23456"]`

To get only the first user's name:

```
$get_users.users.#0.name
```

Result: `"fredrik"`

To get the last user's name:

```
$get_users.users.#max.name
```

Result: `"moomo"`

You can use this pattern to reconstruct data in a subsequent node. Given a node called `repeat_list` with the same data:

```json
{
  "ids": "$repeat_list.users.#.id",
  "names": "$repeat_list.users.#.name",
  "usernames": "$repeat_list.users.#.username"
}
```

This produces:

```json
{
  "ids": ["12345", "23456"],
  "names": ["fredrik", "moomo"],
  "usernames": ["@frikky", "shuffle user 2"]
}
```

**Important:** For nested loops, pass each item to a [subflow](/docs/triggers#subflow) using the Shuffle Workflow trigger.

## Casting Values

Since v0.9.25, Shuffle supports [Liquid formatting](/docs/liquid) for data transformation in action parameters. All action parameters are supported.

Example — strip whitespace:

```
{{ "          So much room for activities          " | strip }}!
```

More filters and syntax: [Shopify Liquid documentation](https://shopify.github.io/liquid/filters/strip/)

## Conditions

Conditions control which nodes run and which are skipped. They sit on the lines (branches) between nodes, acting as gatekeepers: the next node only fires when the condition evaluates to true.

A condition requires at least two nodes connected by a line. By default, every branch is implicitly true — the next node always runs. You can override this by adding a condition to the branch.

### IF Conditions

To add a condition:

1. Click the line between two nodes.
2. Click "New condition" in the right panel.
3. Configure the condition. Set a left-side value, choose an operator (EQUALS, DOES NOT EQUAL, CONTAINS, and so on), and set a right-side value.

Both sides of the condition can reference anything a normal node can: previous node outputs, the execution argument (`$exec`), workflow variables — any value available in your workflow.

The condition uses the operator to compare the two sides. If the comparison is true, the next node runs. If false, it is skipped.

A node can have multiple outgoing branches, each with its own condition. These conditions are evaluated independently. When multiple branches from the same node are all true, those paths run in parallel.

Multiple conditions on a single branch are joined with implied AND logic. To create OR logic, use separate branches from the same node.

**Note:** Conditions cannot handle list loops (`$variable.#`). To filter a list by a condition, use the "Filter List" action described below.

### Condition Loops

Standard conditions work on individual values. To filter a list — keeping some items and discarding others — use the **Filter List** action in the **Shuffle Tools** app.

The Filter List action takes a list and returns two sub-lists: items that matched your criteria and items that did not.

**When to use Filter List vs. subflows:** If performance is not a concern, the preferred approach is to pass each list item to a subflow using the Shuffle Workflow trigger. Filter List is simpler but runs in-place, which can consume more memory on large datasets.

Example data:

```json
[
  {"ip": "1.2.3.4", "malicious": true},
  {"ip": "4.3.2.1", "malicious": false},
  {"ip": "1.2.3.5", "malicious": true}
]
```

The goal: extract only the items where `malicious` is `true`.

Steps:

1. Create a node that produces or receives the list.
2. In the next node, select the **Shuffle Tools** app and choose the **Filter List** action.
3. Configure the fields:
   - **input_list** — the entire list, passed as `$node_name` (no `#` — pass the whole list, not individual items).
   - **field** — the key to evaluate. In this case: `malicious`.
   - **check** — the comparison operator. Options: EQUALS, DOES NOT EQUAL, Larger than, Less than, Is Empty, Contains, Starts With, Ends With, Files by extension.
   - **value** — the value to match against. In this case: `true`.
   - **opposite** — toggle to invert the result. EQUALS becomes DOES NOT EQUAL, and so on.
4. The output has this structure:

```json
{
  "success": true,
  "valid": [
    {"ip": "1.2.3.4", "malicious": true},
    {"ip": "1.2.3.5", "malicious": true}
  ],
  "invalid": [
    {"ip": "4.3.2.1", "malicious": false}
  ]
}
```

`valid` contains items that met the criteria. `invalid` contains everything else. Reference them as `$filter_node_name.valid` or `$filter_node_name.invalid` in subsequent nodes.

## Authentication

### App Authentication

Most apps require authentication before you can use them — usually an API key, endpoint URL, or OAuth token.

When you select an app action that needs authentication, the **Setup** tab shows an Authentication section with a dropdown set to **No selection** and an orange **+** button. Until you add credentials, an orange warning box tells you "Authentication needed" and prompts you to click **Add Authentication**. The step will not work until authentication is configured.

Authentication follows a consistent pattern for apps built with the App Creator (using OpenAPI specs). Custom apps may vary depending on how the creator defined them.

Once you add authentication for an app, it becomes available across your tenant. You can also distribute authenticated apps to sub-tenants.

**Tip:** Use a workflow variable for credentials so they can be updated in one place.

Below is a screenshot showing the authentication prompt on a Wazuh node. The orange warning indicates that credentials are required before the node can execute.

<img width="343" height="564" alt="Wazuh authentication setup" src="https://github.com/user-attachments/assets/90637508-e3c2-4d84-b340-4d5258ff2680" />

### Workflow Authentication

Every execution generates a random authorization key. Execution data can only be accessed by the worker running it or a tenant admin. No action required on your part.

## Triggers

Triggers tell a workflow when to run. They sit at the start of a workflow (or mid-execution for certain types) and define how execution begins. You can find all triggers in the left panel of the workflow editor, grouped under the apps list.

### Webhook

A webhook is a real-time HTTP trigger. It accepts any HTTP request — GET or POST — and passes the request body to the workflow as the execution argument.

**To set up a webhook:**
1. Drag the Webhook trigger from the left panel onto the canvas.
2. Connect it to your starting node.
3. Click the webhook and press "Start."
4. Copy the generated webhook URI. It looks like: `https://shuffler.io/api/v1/webhooks/webhook_{uuid}`
5. Send HTTP requests to that URI. The body of each request becomes the execution argument.

**Authentication:** Add required headers in the webhook configuration. Each header goes on its own line in the format `Header-Name: value`.

**Testing from the command line:**
```
curl -X POST https://shuffler.io/api/v1/webhooks/webhook_{uuid} \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'
```

### Schedule

A schedule runs a workflow at a fixed interval. There are two types depending on your deployment:

**On-prem schedules** run on the webserver itself, polling every X seconds. They persist in the database even when Shuffle is restarted, so you can safely update or reboot without losing them. The minimum interval is 1 second.

**Cloud schedules** use Google Cloud Scheduler with standard cron expressions. They take two arguments: the cron schedule and the execution argument to pass to the workflow.

**To set up a schedule:**
1. Drag the Schedule trigger from the left panel onto the canvas.
2. Click the schedule node.
3. For on-prem: type the interval in seconds. For cloud: enter a cron expression.
4. Type the execution argument (the data your workflow should start with).
5. Click "Start."

### Subflow

A subflow trigger runs another workflow from within the current one. It creates a parent/child relationship: the calling workflow pauses, the child workflow runs, and the result is returned.

Subflows are the preferred way to handle nested loops and reusable logic. Instead of building one large workflow, break it into smaller workflows and chain them with subflow triggers.

**To set up a subflow:**
1. Drag the Subflow trigger onto the canvas.
2. Select the target workflow.
3. Choose the start node in the target workflow.
4. Set the input data to pass to the child workflow.

**Looping with subflows:** Use `$list_name.#` as the input to send one item at a time from a list. The child workflow runs once per item.

### User Input

The User Input trigger pauses execution and waits for a human to approve or deny. This is useful for workflows that require a decision before proceeding — for example, confirming a firewall rule change or approving a ticket escalation.

**How it works:**
1. The workflow reaches the User Input trigger and pauses.
2. A notification is sent to the assigned user.
3. The user approves or denies.
4. The execution continues (on approve) or aborts (on deny).

The recommended approach is to use a Subflow configured for user input, which gives you more control over the notification and response handling.

### Pipelines

Pipelines are data ingestion triggers for log collection and detection. They are built on Tenzir and provide three features:

- **Syslog Listener** — ingest logs via TCP from syslog sources
- **Sigma Rules** — detection rules that trigger workflows when a match is found in incoming data
- **Kafka Forwarder** — forward messages from Kafka topics into workflows

**To set up a pipeline:**
1. Drag the Pipeline trigger onto the canvas.
2. Select the feature (syslog, sigma, or kafka).
3. Configure the connection details.
4. Click "Start."

Sigma rules can be downloaded from `https://shuffler.io/detections/sigma`. Manage them (edit, enable, disable) from the same page.

### Email

Email triggers (Gmail and Outlook) are now handled through Email Schedule workflows rather than as standalone triggers. Set up an email schedule to poll an inbox at regular intervals and trigger a workflow when new messages arrive.

## File Handling

Files in workflows are managed by reference (file ID). The system stores metadata alongside each file: md5/sha256 hash, filename, filesize, tenant, originating workflow, creation time, and status.

### Useful File Handling Info

- Files are identified by a unique, auto-generated ID.
- [File API documentation →](/docs/API#file-api)
- In workflows, files are typically referenced with the `File_id` field.

**File statuses:**

| Status | Meaning |
|---|---|
| Created | Metadata prepared, no upload started yet |
| Uploading | Upload in progress — no other file can be added |
| Active | File exists and data is immutable |
| Deleted | File deleted through Shuffle, metadata retained |

### Using Files

Upload a file first in the Admin panel under the "files" tab. Copy the File ID from there.

Below is a screenshot of the Files management page in the Admin panel, showing the file list with metadata columns (name, workflow, MD5 hash, status, filesize, and actions).

![Files management page](https://github.com/user-attachments/assets/bc8ec064-32b9-4c53-8a1d-39dcee3e3a3b)

Within a workflow, the **Shuffle Tools** app provides:

- **Get file value** — print file contents
- **Download remote file** — download from a URL
- **Get file meta** — retrieve file metadata
- **Delete file** — remove the file content (metadata persists)

The **Testing** app can create files directly in a workflow.

### File uploads via the App Creator

To make an app action accept file uploads:

1. Go to the /apps view, click "Edit App" on the target app.
2. Click "New Action."
3. Enable "File Upload" and enter the parameter name (e.g. `file`).
4. Paste a curl request into the URL path field to auto-populate the endpoint.
5. The file icon on the action indicates it accepts files. A `File_id` field appears when used in a workflow.

## Shuffle Datastore

The Datastore is a persistent key-value store for sharing data across workflows and executions. Unlike workflow variables (which are scoped to a single workflow) or execution variables (which last only one run), Datastore entries persist until you delete them. Any workflow in your tenant can read or write to the Datastore.

Common uses: tracking processed items, sharing configuration between workflows, maintaining counters, caching API responses.

### Using the Datastore in Workflows

The **Shuffle Tools** app provides actions for Datastore operations:
- **Set cache** — write a key-value pair
- **Get cache** — read a value by key
- **Delete cache** — remove a key
- **List cache** — list all keys, optionally filtered by category

### Using the Datastore via API

**Set a key:**
```
POST /api/v1/orgs/{org_id}/set_cache
{
  "key": "mykey",
  "value": "myvalue",
  "category": "optional"
}
```

**Get a key:**
```
POST /api/v1/orgs/{org_id}/get_cache
{
  "key": "mykey"
}
```

**List keys:**
```
GET /api/v1/orgs/{org_id}/list_cache?top=50&category=optional
```

**Delete a key:**
```
POST /api/v1/orgs/{org_id}/delete_cache
{
  "key": "mykey"
}
```

**Bulk set (v2 API):**
```
POST /api/v2/datastore?bulk=true
[
  {"key": "k1", "value": "v1"},
  {"key": "k2", "value": "v2"}
]
```

### Deduplication with the Datastore

A common pattern: use the Datastore to track which items have already been processed, so the workflow skips duplicates.

1. When a new item arrives, generate a unique key (e.g., the item's ID or hash).
2. Check the Datastore for that key.
3. If the key exists, the item was already processed — skip it.
4. If the key does not exist, process the item and then write the key to the Datastore.

This is a special case of Datastore usage. The key acts as a flag: its presence means "already handled."

## Typical Use Cases

### Deduplication

Prevent the same item from being processed twice. Use the [Datastore](#shuffle-datastore) to track processed items (covered above). This is identical to the deduplication pattern but presented as a workflow-level concern: the workflow checks incoming data, looks up the unique identifier in the Datastore, and only proceeds if the item is new.

### Formatting

Use [Liquid formatting](#casting-values) to transform data between nodes. Common formatting tasks:

- Convert timestamps to readable dates
- Strip whitespace from strings
- Extract specific fields from a JSON response
- Build URLs or file paths from variables
- Encode or decode Base64 values

Example — convert a Unix timestamp to ISO format:
```
{{ "now" | date: "%s" | plus: 0 | date: "%Y-%m-%dT%H:%M:%S" }}
```

### HTTP Requests

Use the [HTTP App](#http-app-and-rest-api) to make API calls to any service. Common patterns:

- **GET requests** — fetch data from an API endpoint
- **POST requests** — send data to trigger an action or create a resource
- **Authenticated requests** — add headers for API keys, Bearer tokens, or Basic auth

When a service has a dedicated Shuffle app (like GitHub or Jira), prefer that app over the HTTP app. The dedicated app handles authentication, pagination, and error handling for you. Use the HTTP app for services without a dedicated integration, or when you need full control over the request.

## Subflows & Loops

### Standard Loops

To loop over a list within a single workflow, connect a node back to a previous node and use the `.#` syntax to iterate. Each item in the list triggers one iteration.

**Limitation:** Standard loops run in a single worker container. Large lists or long-running iterations can consume significant memory and time.

### Subflows for Nested Loops

For nested loops (a loop within a loop), or when processing large lists, pass each item to a **subflow** using the Shuffle Workflow trigger. The child workflow runs independently, and the parent workflow collects the results.

This approach:
- Isolates each iteration in its own execution
- Prevents memory buildup in a single worker
- Allows parallel processing of list items

### Parallel Execution

When multiple branches from the same node all evaluate to true, those branches run in parallel. Shuffle spins up separate worker containers for each branch. No special configuration is needed — the workflow engine handles it automatically.

### Loop Filtering

Use the **Filter List** action in the Shuffle Tools app (covered in [Condition Loops](#condition-loops)) to split a list into matching and non-matching items without a subflow. This is simpler but runs in-place, so it is best suited for small to medium lists.

## Exploring Executions

Click the "running person" (activity) icon (bottom-left of the workflow editor) to open the execution sidebar. It shows the history of workflow runs and lets you dig into individual results.

https://youtu.be/TW_qz1QVTUU?si=9pBOIBUKwqI8oN8V

### Execution List

Each entry/run shows:

- **Color**: green (finished), yellow (running/waiting), red (failed/aborted)
- **Icon**: play button (manual run), or a trigger icon (webhook, schedule, subflow, etc.)
- **Timestamp**: when the execution started
- **Arrow**: white normally, orange for the last execution you clicked

Click "Refresh Executions" to update the list — executions run in the background and are not always pushed to the UI in real time.

https://youtu.be/jmKJwBtFJZE?si=FyK3F_T2zR-dxtnd

### Execution Details

Click an execution to see detailed results:

- **Rerun**: re-execute with the same argument and start node.
- **Status**: whether the execution finished, is still running, or failed.
- **Timestamps**: start and finish times. A large gap may indicate node delays or problems.
- **Show Skipped actions**: reveal nodes that did not execute (hidden by default).

The action list shows each step within the execution in order. For each action you can see: the app logo, the action name, the function name, and the result. Expand any action for more debug detail.

https://youtu.be/Gqr3RY9QTsA?si=HaVAvNrcTanmUm-2

https://youtu.be/cM7521J7O8A?si=N4alzpXD2tEjUby_

**Tip:** Clicking a JSON result value copies its path (e.g. `#nodename.success`). Clicking the copy icon copies the actual value.

### Workflow Run Debugger

The [Workflow Run Debugger](https://shuffler.io/workflows/debug) lets you search, filter, and manage large volumes of executions — up to 500 at once. Use it when you need to find past runs or view more than the 100 executions shown in the sidebar.

https://youtu.be/a5GvBQH7USQ?si=VUBpmho_m9OrelQT

**How to access:**

1. Open a workflow and click the "running person"(activity) icon (bottom-left).
2. In the execution list, click the graph/search icon (top-right).
3. Or navigate directly to `https://shuffler.io/workflows/debug?workflow_id=<your-workflow-id>`.

<img width="1436" height="685" alt="Screenshot 2026-07-15 at 9 44 52 PM" src="https://github.com/user-attachments/assets/24b15606-c5c8-4a7b-9daf-fcf6124b1618" />

**Features:**

- Filter by workflow name, status, execution argument, date range, and results.
- View executions across your tenant and sub-tenants.
- Select multiple executions and mass-abort or mass-rerun them.

## Collaboration Features

### Sub-Tenant Distribution (Beta)

Build a workflow once and distribute it to sub-tenants. Each tenant can add their own nodes and branches; the parent controls the shared structure.

**Requirements:**

- Must be in a parent tenant
- Must have at least one sub-tenant
- Configure distribution in the workflow's "Edit" panel

<img width="345" height="456" alt="switch_to_subtenat" src="https://github.com/user-attachments/assets/13923ebf-1b14-47de-9132-2b475ba2bf28" />

Distributed workflows have a blue border.

<img width="697" height="321" alt="distributed_workflow_border" src="https://github.com/user-attachments/assets/fb69a8a9-ebfe-47f0-bb04-739728b6f665" />

Inside the workflow, you can switch between tenants.

<img width="345" height="215" alt="switch_tenants" src="https://github.com/user-attachments/assets/0207a29b-b224-4200-a797-736985cc6213" />

Editing a child workflow is allowed, but the parent's version overrides shared nodes on the next save — except for nodes, branches, and authentication added by the child.

### Workflow Revisions & Versioning

Every workflow is backed up at most once per 60 seconds. They are stored in a separate db index and can be reverted to at any time. 

https://youtu.be/-EgOD6ThR0w?si=qSpjMPcNseR6QcNi

Access backups from the revision icon in the bottom bar. Select a previous version to restore it. Your current state is also saved before reverting.

<img width="1439" height="809" alt="revision/history_workflow" src="https://github.com/user-attachments/assets/58ebb76c-6352-4014-aa23-6af420f6f57d" />

### Authentication Groups (Beta)

Run a single workflow against multiple sets of credentials. See [Authentication Groups](https://shuffler.io/docs/organizations#app-authentication-groups).

### Multiplayer (Beta)

Multiple users can edit the same workflow simultaneously on Shuffle Cloud.

### Forms

Every workflow can be accessed as a form at `/forms/{workflow_id}`. Configure form fields in the workflow's edit panel under "Sections."

<img width="1439" height="521" alt="form_interface" src="https://github.com/user-attachments/assets/63e3f0ef-61dc-48e1-9832-6f7827639573" />

## API

See the [Workflow API documentation](/docs/API#workflow-api).

## Workflow Backup

Shuffle automatically backs up workflows connected to GitHub or Azure DevOps whenever you make changes and save or execute.

https://youtu.be/ewTRDFrP7P4?si=V6iIUthVF0rvj35g

### GitHub Integration

**Required details:**

1. **Repository URL** — the HTTPS URL from your GitHub repo (e.g. `https://github.com/<org>/<repo>.git`).
2. **Branch** — e.g. `main` or `master`.
3. **Personal Access Token** — generate at [github.com/settings/tokens](https://github.com/settings/tokens) with `repo` and `workflow` scopes.
4. **Username** — your GitHub username.

https://youtu.be/zR9vUrpLmB0?si=bwC3llGfyiBP1aU-

### Azure DevOps Integration

**Required details:**

1. **Repository URL** — the HTTPS URL from Azure Repos (e.g. `https://dev.azure.com/<org>/<project>/_git/<repo>`).
2. **Branch** — e.g. `main` or `develop`.
3. **Personal Access Token** — generate from your Azure DevOps profile under Personal Access Tokens, with `Code (Read & Write)` scope.
4. **Username** — your Azure DevOps email address.

Note: Azure DevOps support is available from version 2.1.1 and above.
