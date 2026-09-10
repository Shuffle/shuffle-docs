# Triggers

> [!IMPORTANT]
> **See [Workflow Documentation: Triggers](/docs/workflows#triggers)** for the actively maintained documentation. Triggers have been consolidated into the Workflows guide.

Documentation for triggers, running workflow executions

## Table of contents
* [Introduction](#introduction)
* [About](#about)
* [Webhook](#webhook)
* [Shuffle Subflow](#subflow)
* [Schedule](#schedule)
* [User Input](#user-input)
* [Pipelines](#pipelines)
* [Email](#email)

## Introduction
Triggers are the operators used to execute a [workflow](/docs/workflows) automatically. They are connected to a actions within workflows - often the starting node. Triggers usually take an execution argument that will be used to execute the workflow in question.

[Watch the video](https://www.loom.com/embed/9811d94782c249f899703491f286004c)

### About
Triggers, along side apps and variables, can be found on the left hand side, in a tab called "Triggers". 

![Triggers-view-1](https://github.com/frikky/shuffle-docs/blob/master/assets/triggers-view-1.png?raw=true)

Triggers are developed by Shuffle specifically to give the user access to multiple ways to run a workflow. The triggers that are not available on-premises are due to access requirements - not hiding of features. 

There are currently four triggers, with a fifth "hidden" one:
* Webhook 		- Handle realtime HTTP requests from anywhere. 
* Schedule 		- Runs your workflow on a schedule. Cronjob or seconds.
* User Input 	- Waits for user input before continuing. You can answer yes/no.
* Subflow 		- Allows running of another workflow from the current workflow.
* Email 			- When you get an email in gmail/office365: start the workflow
* Rest API 		- Essentially a trigger from either: 1. Another workflow. 2. Any third party software

There are currently six ways to execute workflows:
* Cloud & Hybrid (paid): Webhook, Subflow, User Input, Schedule, Outlook, Gmail, Rest API
* Onprem: Webhook, Subflow, User Input, Schedule, Rest API

## Hybrid
ALL triggers are available EVERYWHERE if you have a Shuffle subscription. This further allows routing executions through cloud (without saving any data) to your open source instance, without the need to open for inbound requests in your firewall(s).

**Example:**
Say you want to get messages from a service like a SIEM, but it's in a different data center. How do you get that request all the way to your instance? This can be done by setting up cloud synchronization allowing for:
1. Remote SIEM -> Send Webhook to https://shuffler.io as a "proxy"
2. Your local instance looks for jobs from an organization you own on https://shuffler.io
3. When a webhook job is found on https://shuffler.io - it will execute in your local instance.

Read more about cloud synchronization in the [organization documentation](/docs/tenants#cloud-synchronization).

### Finding executions
When a trigger runs, you will NOT be notified about it anywhere. It will instead run behind the scenes. You can however discover their data and executions by going to the specific workflow's UI, then clicking "See all executions" on the bottom (the running person).

## Webhook
[Webhooks](https://en.wikipedia.org/wiki/Webhook) are the real-time handler for Shuffle data. Webhooks were initially implemented to handle data from [Office365 connectors](https://docs.microsoft.com/en-us/microsoftteams/platform/concepts/connectors/connectors-using) and [TheHive](https://github.com/TheHive-Project/TheHiveDocs/blob/master/admin/webhooks.md), but have turned into a generic trigger, taking any kind of HTTP data, as we saw the need for it. 

HTTP Method(s):
* GET
* POST

PS: Data in the POST request will be the execution argument. If HTTP queries are present in the GET request, these will be converted to JSON.

#### Authentication
In later versions of Shuffle, you further have access to an authentication field. This field is based on the headers of the request, and any header added to this field will be **REQUIRED** from the sender of the webhook.

One header for each line. In the image below, the request would need to contain the headers "authorization" and "authorization2" with the exact values specified.
![Triggers-view-6](https://github.com/frikky/shuffle-docs/blob/master/assets/triggers-view-6.png?raw=true)

### Webhook Example
To start using webhooks, you should have a service that supports webhooks (e.g. the two above mentioned). If you just want to test, you can also use cron.

Once you have a service ready:
1. Drag the "Webhook" trigger from the left hand side into the main view, and you should see it automatically connect to your starting node. 
2. Click "start" to deploy this webhook (it might be auto-started). This will also be stopped if you remove the node or the workflow. A webhook can not be in multiple workflows, but you can deploy as many as you want.
3. Find your webhook URI in the "Webhook URI" window, and copy it to your service

![Triggers-view-2](https://github.com/frikky/shuffle-docs/blob/master/assets/triggers-view-2.png?raw=true)

Test it! Say your URI is: https://shuffler.io/api/v1/webhooks/webhook_336a7aa2-e785-47cc-85f4-31a4ab5b28b8 and you want to use {"test": "testing"} in your workflow:
```bash
curl -XPOST https://shuffler.io/api/v1/webhooks/webhook_336a7aa2-e785-47cc-85f4-31a4ab5b28b8 --data '{"test": "testing"}'
```

## Subflow 
Subflows is a trigger made to run workflows within other workflows. There's further a "parent/child" element to it where there's always a reference to where the execution came from. This can also run a subflow within itself or be recursive (infinite loops).

Purposes we'll cover:
* Create standard workflows that can be used within other workflows. E.g. checking an IoC in a standardized way every time.
* Handle loops well. This is to avoid multiple nested for-loops and instead make a new workflow to handle it. E.g. list of emails with list of attachments with list of sub-attachments (e.g. Zip).

Requirements:
* shuffle-subflow app. This is automatically installed.

[Here are the known missing features for subflows](https://github.com/frikky/Shuffle/issues/223)

#### Extra subflow information 
- Subflows can be in the same Workflow. When selecting, it will show up as red.

![Triggers-subflow-7](https://github.com/frikky/shuffle-docs/blob/master/assets/triggers-subflow-7.png?raw=true)

- Parent nodes of the subflow trigger show up as red. When using these, make sure you stop the workflow. We will add a warning for this, as it can run you out of resources easily.

![Triggers-subflow-8](https://github.com/frikky/shuffle-docs/blob/master/assets/triggers-subflow-8.png?raw=true)

- After choosing a subflow - if you right-click the subflow node in the workflow UI, it will import the subflow. When saving, this will NOT be a part of the workflow. 
- PS: We will make this part of the workflow visual and non-interactive at a later stage.

![Triggers-subflow-9](https://github.com/frikky/shuffle-docs/blob/master/assets/triggers-subflow-9.png?raw=true)

### Subflow Example
1. Drag a subflow into the PARENT view from the left side and click it
![Triggers-subflow-1](https://github.com/frikky/shuffle-docs/blob/master/assets/triggers-subflow-1.png?raw=true)

2. Choose a workflow to run. This will use the STARTNODE as default, which can be changed. The red workflow is the one you're currently working on.
![Triggers-subflow-2](https://github.com/frikky/shuffle-docs/blob/master/assets/triggers-subflow-2.png?raw=true)

3. We'll decide a startnode and the information to send to the subflow. In our case, we'll use the list below, and send one item at a time with the IP to be searched for in Virustotal. The data with the list is named Repeat_list in our case, hence we use $Repeat_list.#
```
[{"ip": "1.2.3.4", "malicious": true}, {"ip": "4.3.2.1", "malicious": false}, {"ip": "1.2.3.5", "malicious": true}]
```
![Triggers-subflow-3](https://github.com/frikky/shuffle-docs/blob/master/assets/triggers-subflow-3.png?raw=true)

4. It's time we explore the results. In total, this should execute FOUR times: 1 for the first workflow and once for EACH of the objects in the list.
![Triggers-subflow-4](https://github.com/frikky/shuffle-docs/blob/master/assets/triggers-subflow-4.png?raw=true)

5. Here's a view of the total workflows. Notice how three of them have a different icon? This is because they are subflows. PS: It will always show the maximum amount of nodes in the workflow, whether it's a subflow or not.
![Triggers-subflow-5](https://github.com/frikky/shuffle-docs/blob/master/assets/triggers-subflow-5.png?raw=true)

6. Exploring the subflows, we find that the IP's have been searched for in Virustotal, and that we have a reference to the parent. Clicking the reference will take you to the parent execution.
![Triggers-subflow-6](https://github.com/frikky/shuffle-docs/blob/master/assets/triggers-subflow-6.png?raw=true)


## Schedule 
**On-prem**
Schedules on-prem are ran on the webserver itself. Rather than cron, it uses a scheduler that runs it every X seconds. This will become more sophisticated over time. Schedules persists in the database even when you turn off Shuffle, so don't be afraid to update.

**Cloud**
Schedules are based on [google's cloud scheduler](https://cloud.google.com/scheduler/) and are schedules that run based on [cron](https://en.wikipedia.org/wiki/Cron). It takes two arguments - the schedule you want to run it on and the Execution argument used in the workflow. A simple cron converter can be found [here](https://en.wikipedia.org/wiki/Cron). When you are ready to run, click "start". 

### Schedule Example
1. Drag a schedule into the view from the left side
2. Click the schedule
3. Type in the amount of seconds between execution (down to every 1 second)
4. Type the execution argument you want to execute with. This can be used by actions.
5. Click "Start"

![Triggers-view-3](https://github.com/frikky/shuffle-docs/blob/master/assets/triggers-view-3.png?raw=true)

## User input
- User Input is an app located within triggers. It provides a method to temporarily pause ongoing executions in a workflow, awaiting approval or denial from a human through a manual click before proceeding with or stopping subsequent executions.

- This can currently be achieved through Subflows (preferred for production), Email and SMS for rapid testing on the fly, but we will introduce many other options, including chat systems. 

- Note:
If you have any suggestions pertaining to this, please let us know via a feature request on github.

- The point of the user input node is that it acts as a crucial control point, allowing human oversight and decision-making within automated processes.
e.g. 

- Scenario 1: Granting or revoking user access privileges.
User Input: Authorization from appropriate personnel before modifying user roles or permissions.

- Scenario 2: Rolling out software updates across a network.
User Input: Approval from IT administrators before deploying updates to servers or critical systems.

- Scenario 3: Investigating and responding to security incidents.
User Input: Analyst decision for remediation actions, such as isolating a compromised system or blocking a suspicious IP address.

### User Input Example
1. In the bottom left corner select the triggers tab
![num1](https://github.com/Shuffle/Shuffle-docs/assets/31187099/76f3e499-3f27-4215-bcc2-060e8bd30e61) 

2. Drag in the user input node into your workflow

3. Set it up where you will want approval before proceeding with subsequent nodes in the workflow.
- Select Subflow as the input option (This is always preferred). You can use email and sms to rapidly test on the fly.
  ![Screenshot 2024-01-16 100608](https://github.com/Shuffle/Shuffle-docs/assets/31187099/5f854f72-c2ea-4029-9e65-359582db1818)

4. Set up your "trigger workflow" in my example it is the workflow labeled "UI test trigger" and select it in your user input node settings (as shown above). We will use this workflow to further customize our user input making how to use it limitless. (This is why this method is preferred). The example below shows how versatile it can be
![Screenshot 2024-01-16 102648](https://github.com/Shuffle/Shuffle-docs/assets/31187099/7a8ed5f4-718f-48e0-af5d-a002d65f970a)
  
5. When we execute our workflow then jump into our "UI test trigger" workflow (This is our "trigger workflow"), we should get an execution argument as follows.

![Screenshot 2024-01-16 100516](https://github.com/Shuffle/Shuffle-docs/assets/31187099/a6db51b0-8f4f-4ef2-b3bd-e7699dba9b9f)

6. Using the execution argument provided, we can then send a well structured request to a user asking for the approval or denial before an event takes place.
![Screenshot 2024-01-16 110322](https://github.com/Shuffle/Shuffle-docs/assets/31187099/4199d32f-7510-4bbb-968a-02b1a1a95404)

- Which appears as shown below in a users email inbox requesting for the users input. Remember this action can be sent to whatever communication channel you use. It can also be sent to multiple users but can only be triggered once for now. (We may add multiple users approval for this in the future)
![Screenshot 2024-01-16 105926](https://github.com/Shuffle/Shuffle-docs/assets/31187099/5ec22cd0-802b-47a0-85b0-41548e5c19e1)

- Frontend_continue and frontend_abort should open a new tab with a shuffle UI prompting you to either click on proceed or abort.
  ![image](https://github.com/Shuffle/Shuffle-docs/assets/31187099/0e9ecad1-c10c-4544-a994-ad1abf5146b9)

- API_continue and API_abort this opens a new tab informing you if the operation you selected was a success or not. As shown below
  ![Screenshot 2024-01-16 110009](https://github.com/Shuffle/Shuffle-docs/assets/31187099/8f8f6be5-3480-4785-810d-a1015667eb94)

7. The Workflow run debugger is a new feature implemented in shuffle V 1.3.0 that helps you dig through and audit the performance of workflows, the errors encountered, logs and the current status of executions in your workflows. [Found here](https://shuffler.io/workflows/debug)
  ![num7](https://github.com/Shuffle/Shuffle-docs/assets/31187099/04c5f00e-71cd-4871-b16b-fd892ddbd009)
- With that said, you can use the Workflow run debugger to check whether or not the approval was granted and on which workflow was the request sent and on which workflow is a response expected, if the actions of the workflow are finished or whether or not we are still waiting for the user input. Think of this as a way to audit status of executions and workflows.
![num7 1](https://github.com/Shuffle/Shuffle-docs/assets/31187099/07356e00-9474-47bd-9e1f-8303db2eae18)
- Using this you can see if the action was completed or not under the status tab marked as 1 above and the workflow name right besides it.
- If you hover above the start times for the executions you should see pop up info with regards to what the error is, errored out workflows start times are usually highlighted in red as shown in the image above
- In label 3 as shown in the image a pop out takes you to the target workflow directly and 4 shows you the logs. 

## Pipelines

A pipeline is a sequence of interconnected steps or stages that take input data, transform it through various operations, and produce an output. The data enters the pipeline at one end, undergoes transformations at each stage, and emerges as a refined output at the other end.

### How Pipelines Work

### Components of a Pipeline:

#### Source:
- **Definition**: The origin point where raw data is introduced into the pipeline.
- **Examples**: Databases, APIs, log files, webhooks, etc.
- **Function**: Captures and provides raw data for processing.

#### Ingestion:
- **Definition**: The process of extracting and importing data from the source into the pipeline.
- **Function**: Ensures data is pulled into the pipeline efficiently and accurately.

#### Transformation:
- **Definition**: The stage where data undergoes various modifications to prepare it for the next steps or final use.
- **Operations**:
  - **Filtering**: Selecting relevant data based on specific criteria to ensure only necessary information is processed.
  - **Format Conversion**: Changing data types or structures to ensure compatibility with the target system or further processing stages.

#### Sink (Destination):
- **Definition**: The endpoint where the transformed data is stored or delivered.
- **Examples**: Databases, analytics systems, other applications.
- **Function**: Stores or utilizes the processed data for analysis, reporting, or further action.

### How Shuffle Uses Pipelines

In Shuffle, we are currently using Tenzir data pipelines.

### Pipeline Trigger Features

- **Syslog Listener**: Used to ingest logs into the pipeline.

- **Sigma Support**: Pipelines support Sigma rules, which allow us to define and customize detection rules. This gives Shuffle the ability to control what to detect and the rules governing these detections. Whenever logs match the Sigma rules, a workflow run is triggered in Shuffle.

- **Kafka Forwarder**: Configures the pipeline to actively forward all messages from a specified topic to your workflow.

![Features](https://github.com/user-attachments/assets/3fdb2723-89e2-4f6b-9013-01ae3a644640)

Additional features will be added in the future.

### Setting Up Sigma Rules for Detection

To start using pipelines for detection, you need to set up or download Sigma rules. This can be done by:

1. Visiting the Sigma page: [https://shuffler.io/detections/sigma](https://shuffler.io/detections/sigma)
2. This will automatically download all the Sigma rules from a remote GitHub repository into the Tenzir node, making the pipeline ready for detection.

![Sigma rule](https://github.com/user-attachments/assets/0c245a06-d385-4321-a4aa-cbddd9cbe1dd)

#### Managing the Sigma Rules

To view and manage the downloaded Sigma rules:

1. Visit the Sigma page: [https://shuffler.io/detections/sigma](https://shuffler.io/detections/sigma)

![Sigma Ui](https://github.com/user-attachments/assets/dabd95f6-8a54-4c41-8f85-dc496e77e79b)


   - To edit an existing rule, click on the edit icon, make your changes, and save.

![Edit Sigma](https://github.com/user-attachments/assets/a153cae1-e161-413b-b7c2-9fc9fe932d52)

2. You can disable or enable a particular rule file or globally enable or disable the rules.

![Edit Sigma](https://github.com/user-attachments/assets/df1b14ab-b111-42e9-9f33-d01ff9f28ffe)

![Global Enable Rule](https://github.com/user-attachments/assets/666bf44f-e7a1-42f8-a9c2-e14751d32112)


### Pipeline Example

![Pipeline Example](https://github.com/user-attachments/assets/67cb1427-e492-416a-88d1-630741cf9015)

1. Drag the "pipeline" trigger from the left-hand side into the main view, and it should automatically connect to your starting node.

2. To start the syslog listener, click on the syslog listener. This will start the listener at 192.168.1.100:5162 on your host machine. You can connect to this endpoint via the TCP protocol and send your syslog data.

![Syslog](https://github.com/user-attachments/assets/4441137e-20cc-4b23-954f-2bef69e21ba5)

3. For running detection rules, click on the Sigma rule search option. This will create a pipeline that takes the ingested logs and applies the Sigma rules that are downloaded and enabled. Whenever logs match the defined rules, the detected logs are sent, triggering the workflow run.

4. For forwarding Kafka messages from a topic, click on the "follow Kafka queue" option. You will see a pop-up asking for Kafka-specific information that you need to provide, such as the topic name and bootstrap server address. Once you provide the required details, click submit and start. This will actively forward all incoming messages from your Kafka topic to the workflow.

![Kafka](https://github.com/user-attachments/assets/13264f6f-b5fb-48f2-a21d-0216e237333d)

5. To stop a pipeline, simply click on the stop button. This will stop the pipeline and its execution. If you want to delete the pipeline, you can delete the pipeline trigger from the workflow.

### Manual Sigma forwarding
The reason manual forwarding may be necessary is e.g. if Shuffle doesn't have access to the location you are trying to reach. This makes Shuffle unable to handle rules dynamically, but allows for customization nonetheless. 

1. Make sure you have a folder with the rules on the server you want to run detections on. Put them in the folder `/var/lib/tenzir/sigma_rules`
2. Set up a sample workflow with a Webhook as the trigger in Shuffle. 
3. Start the following Pipeline in Tenzir.

```
export | sigma /var/lib/tenzir/sigma_rules | to <webhook url>
```
4. Check in Shuffle if any executions occurred

## Email
Email triggers no longer exist, and should be handled with Email schedules instead: [Gmail](https://shuffler.io/workflows/e506060f-0c58-4f95-a0b8-f671103d78e5), [Outlook](https://shuffler.io/workflows/31d1a492-9fe0-4c4a-807d-b44d9cb81fc0)

