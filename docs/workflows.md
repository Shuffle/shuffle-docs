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
* [Nodes](#nodes)
  * [Starting node](#starting-node)
* [Conditionals](#conditionals)
  * [IF Conditions](#conditions)
  * [Condition Loops](#condition-loops)
* [Variables and Arguments](#variables-and-arguments)
  * [Execution Argument](#execution-argument)
  * [Workflow Variables](#workflow-variables)
  * [Execution variables](#execution-variables)
* [Passing values](#passing-values)
  * [Examples](#examples)
* [Parsing JSON](#parsing-json)
* [Passing lists](#passing-lists)
  * [Examples](#examples-1)
* [Casting values](#casting-values)
* [Authentication](#authentication)
  * [App Authentication](#app-authentication)
  * [Workflow Authentication](#workflow-Authentication)
* [Handling files](#file-handling)
  * [Useful file handling info](#useful-file-handling-info)
  * [Learn to use files](#learn-to-use-files)
  * [Upload file API with the app creator](#upload-file-api-with-the-app-creator)
* [Exploring Executions](#exploring-executions)
* [API](#api)
* [Workflow Backup](#workflow-backup)
  * [Azure Devops](#azure-devops)
  * [Github](#github)

## Introduction
Workflows are the backbone of Shuffle, empowering you to automate your daily tasks by with a simple interface. Workflows use [apps](/docs/apps), [triggers](/docs/triggers), [conditions](/docs/conditions) and [variables](/docs/apps/#variables) to make powerful automations in no time. 

If you would like to learn more about how to create, test and automate your tasks, read on. 

### What is a workflow

In Shuffle, a workflow is simply a visual script. It is a canvas where you drag and drop actions to build a process.  
Think of it like a flowchart, but every box actually does something. Instead of writing code to connect your tools, you visually connect them here.

### How it works

Every workflow operates on a simple logic: Input -> Action -> Output.  
To build one, you need three main parts:

- **The Trigger**: This is the "Start" button. It tells the workflow when to run. This could be a Webhook receiving data from another system, a schedule that runs every hour, or a manual click.  
- **The Nodes (Apps)**: These are the steps. Each node represents an App doing a specific job. For example, one node might be VirusTotal scanning a file, and the next node might be Slack sending the results.  
- **The Lines**: These connect your nodes. They decide the order of execution and pass data from one step to the next.

#### Why use it?

The goal is to take a manual task, like investigating an alert, and turn it into a process that runs itself. You build the logic once, and Shuffle executes it every time the trigger fires.

### Why they matter in automation

The main reason you build workflows is to stop doing the same boring tasks over and over again.  
When you do things manually, you make mistakes. You might forget to check a specific log, or you might copy an ID wrong. A workflow doesn't get tired and it doesn't forget steps. It ensures that every time an event happens, it is handled exactly the same way.

**Speed and Volume**  
In security, speed matters. If you have to manually log into a firewall to block an IP, that takes minutes. A workflow does it in milliseconds. Also, humans are bad at scale. You can handle one alert, but you can't handle five hundred at once. Workflows can.

**Connecting your tools**  
You probably have too many tabs open right now. You have your ticketing system, your email, your chat app, and your security tools. Workflows act as the glue between them. Instead of switching tabs to copy-paste data from one tool to another, the workflow moves the data for you.

### What you need to know
We encourage everyone to have checked out our [Workflow Development Exercises](https://github.com/Shuffle/Shuffle-docs/blob/master/handbook/engineering/workflow_development_exercises.md) before becoming a creator. This makes sure you know the fundamentals of using Shuffle and can build _anything_. The items below that aren't linked do have documentation, but may be missing a video.

1. Variables & nodes
2. JSON autocompletion
3. Loops
4. Nestedloops
5. [Start nodes](https://shuffler.io/workflows/0285a05e-8dc0-4614-840b-88606d6a1e59) (Learn more about start nodes in this video [here](https://www.youtube.com/watch?v=hQcpuoCkXtw))
6. Triggers: Webhooks & Schedules
7. Subflows & User Input
8. [App Authentication](https://shuffler.io/workflows/d65d228a-f406-4227-9fa7-f7d9303f8411)
9. Loop filtering
10. [Shuffle File storage](https://shuffler.io/workflows/dd5e3800-2f2e-4089-8055-b500e3b8b349)
11. [Shuffle Datastore (Cache)](https://shuffler.io/workflows/f39a3c37-4f38-4ca0-952a-a9425080b44e)
12. Deduplication
13. [Liquid formatting](https://shuffler.io/workflows/0d604c52-1b3f-49d8-a57e-480baf07ab8d)
14. [HTTP & Rest APIs](https://shuffler.io/workflows/b8a3a70a-f3f9-459f-99b3-7a2723a1a4b8)

### Finding relevant workflows
You may often want to start with a template. To build a Workflow in Shuffle from scratch is much harder than having something to go off. That's why we always encourage you to [search public workflows](/search?tab=workflows) first.


## Basics
The following section describes the basics of a workflow. 

### Create
Once logged in, creating a workflow can be done by going to the [workflows](/workflows) dashboard and clicking  "New workflow" as highlighted in the picture below. It will ask you for a name and description. These can be changed at any time. 

<img width="1656" height="898" alt="Screenshot 2025-08-28 183003" src="https://github.com/user-attachments/assets/2d409adb-718c-4368-98c6-9bbd2f61bea7" />

<img width="1913" height="862" alt="new-workflow" src="https://github.com/user-attachments/assets/92b74e0a-6d61-4ece-84bf-2bda60c7019a" />

If you lose your way or want to edit it at a later point, it can always be found at [/workflows](/workflows).

### Edit
Once a workflow is created, you will be presented with the following view: 

<img width="1919" height="865" alt="Screenshot 2026-01-21 105702" src="https://github.com/user-attachments/assets/cc6ef7e2-5831-4e30-a4ce-e1833ee831d6" />


Workflows are entirely based on [apps](/docs/apps), [triggers](/docs/triggers), [variables](/docs/apps#variables) and [conditions](/docs/conditions). You have access to all of these in the bottom left of the screen. Apps and triggers are draggable, meaning you can drag and drop them into the main window. 

The workflow loads up with a default "change me" node in your main window, which can be edited or removed. You can drag apps from the left apps bar into your workflow's main window and click on them to edit and set them up. You can run executions using the play button and results are shown as in the picture below.

<img width="1918" height="866" alt="Screenshot 2026-01-21 105952" src="https://github.com/user-attachments/assets/c1e822d7-1723-40b7-b7c7-734d150ff44b" />

Clicking the node presents you with a new view. This is the view to configure the node. In our example case, the default name is "change_me". 

The default action for the "shuffle tools" app is the "repeat back to me" action which does exactly what it says. This can be changed by clicking the dropdown menu. More about editing an app's actions can be found [here](#edit actions)

<img width="424" height="707" alt="Screenshot 2026-01-21 110248" src="https://github.com/user-attachments/assets/8e184ca3-0a61-4c9c-be17-0f9041c2ae78" />

### Save 
Now that we have a working workflow, click the "save" button next to the big play button (or click CTRL+S). This presents you with a notification at the bottom of the screen that saving is in progress. Saving is required to make your latest edits available for execution.

<img width="1892" height="860" alt="save-workflow" src="https://github.com/user-attachments/assets/5f90977d-a046-4d4b-b7c6-1e60e7c9ebcb" />


### Execute
With a saved workflow, you can now execute. The big green play button will execute for you. Once clicked, this will start execution at your starting node. Whether successful or not, you will see a side panel open, indicating that the node has executed

<img width="1117" height="175" alt="execute-button" src="https://github.com/user-attachments/assets/db498523-02bb-4ec8-93ed-438c71ee1a03" />

If you want to see all your previous executions, you can go back to [workflows](/workflows), click the name of your workflow (in our case Example workflow), and click on the running person icon to see the status and result of all previous executions in detail.

<img width="1110" height="195" alt="running-person" src="https://github.com/user-attachments/assets/a2169c95-3357-4952-b7f6-258161a7b910" />

<img width="600" height="700" alt="new-execution-list" src="https://github.com/user-attachments/assets/f84660c1-c8c6-4afb-8db5-13e782081fc4" />

If you want to test more, go to the bottom of this article [How-to continuation](#how-to).

### Duplicate

If you want create a copy of a workflow you can do so by clicking the kebab (vertical 3 dots) menu and select "Duplicate Workflow".

![Duplicate workflow in progress](https://github.com/frikky/shuffle-docs/blob/master/assets/workflow-duplicate-1.png?raw=true)

A new workflow will be visible with an `_copy` suffix append to its name.

### Delete

If you're finished with a workflow and no longer require a copy of it, you can delete a workflow by clicking the kebab (vertical 3 dots) menu and select "Delete Workflow".

**NOTE: Any workflows that depend on this one will be impacted**

![Confirm workflow deletion](https://github.com/frikky/shuffle-docs/blob/master/assets/workflow-delete-1.png?raw=true)

After confirming the deletion action, you'll see a notification of the workflow being deleted.

![Workflow deletion confirmation](https://github.com/frikky/shuffle-docs/blob/master/assets/workflow-delete-2.png?raw=true)


## Nodes
Nodes are an object within a workflow that presents with an app or a trigger. You add a node to a workflow by dragging its icon onto the workflow space from the left-hand menu. Whenever you click one of these nodes in your workflow, you will see the available configuration options on the right-hand side. [Suffle Apps](/docs/apps) are standardized, while triggers are different.

Most nodes use values that you can pass to them. These can be text specified by you (pencil icon), [an app result](#passing-values) or from [variables](#variables) (heart icon).

![argument-example-1](https://github.com/frikky/shuffle-docs/blob/master/assets/argument-example-1.png?raw=true)

### Starting node
The starting node is circular with a turquoise border. This node is the FIRST ACTION in an execution. The starting node is NOT a trigger, but rather the first action that a trigger sends data to. The starting node can be changed by clicking a different node, then the "SET STARTNODE" button in the top-right corner.

## Variables and Arguments

### Execution argument
The execution argument is what makes it possible for triggers to work. This is the argument that the whole execution begins with. Manual executions can also have an execution argument. In essence, the execution argument can be anything - json, list, string, number. It's up to you.

![execution-argument-1](https://github.com/frikky/shuffle-docs/blob/master/assets/execution-argument-1.png?raw=true)

The execution argument acts like a node, meaning you can use its value anywhere.
These are the different names for it: 
* $exec
* $trigger
* $webhook
* $schedule
* $userinput
* $email_trigger

### Workflow Variables
Workflow variables is static reusable data decided before an execution. These are typically used for API keys, URLs or usernames. If you need to define a dynamic variable that changes between executions or based on the results of a previous node, then you need to look at [Execution Variables](/docs/workflows#execution-variables)

Some things to keep in mind when using workflow variables:
* They are set BEFORE an execution
* They are unencrypted
* They are shared with everyone with access to the workflow 
* They are only accessible to the workflow you're in.

Use-case:
* Save URLs, API keys and more.

PS: We are working on a way to have encrypted global variables to be used for passwords and global API keys (and more) with IAM, but that might take a while to implement properly.

**How to create and use a workflow variable:**

1. Click "Variables" in the bottom left corner.
![variable-example-1](https://github.com/frikky/shuffle-docs/blob/master/assets/variable-example-1.png?raw=true)

2. Click "Make a new workflow variable"
![variable-example-2](https://github.com/frikky/shuffle-docs/blob/master/assets/variable-example-2.png?raw=true)

3. Write a name, description and value for the variable.
![variable-example-3](https://github.com/frikky/shuffle-docs/blob/master/assets/variable-example-3.png?raw=true)

4. Use the variable in an action or condition
![variable-example-4](https://github.com/frikky/shuffle-docs/blob/master/assets/variable-example-4.png?raw=true)

### Execution Variables
Execution variables work the same way as Workflow Variables, except they HAVE to be set during execution. These are temporary datapoints that will not be saved anywhere. They work by taking the RESULT of an action of your choosing (examples below), done with a single click. If you're looking to define a variable that does not change between executions and is static, you need to look at [Workflow Variables](/docs/workflows#workflow`-variables)

Some things to keep in mind using execution variables:
* They are set DURING execution
* They are used during execution
* They are unencrypted

Use-case:
* E.g. basic multi-tenancy

**How to create, use and check execution variables:**

1. Click "Variables" in the bottom left corner.
![variable-example-1](https://github.com/frikky/shuffle-docs/blob/master/assets/variable-example-1.png?raw=true)

2. Click "New execution variable".
![variable-example-5](https://github.com/frikky/shuffle-docs/blob/master/assets/variable-example-5.png?raw=true)

3. Choose a unique name. It only requires a name as the variable is set DURING execution, in this case "Testing"
![variable-example-6](https://github.com/frikky/shuffle-docs/blob/master/assets/variable-example-6.png?raw=true)

4. Now click an existing action and choose the variable. This will set the RESULT of the action to the execution variable. 
![variable-example-7](https://github.com/frikky/shuffle-docs/blob/master/assets/variable-example-7.png?raw=true)

5. Add another node and USE the variable. The variable can also be used by typing "$testing" in the "Static data" textfield. The repeated value in this case will be the value from the "Hello World" node set in step 4.
![variable-example-8](https://github.com/frikky/shuffle-docs/blob/master/assets/variable-example-8.png?raw=true)

6. If you're unsure whether the value is set during execution or not, check the results. The last three results are available in the web UI, and can be seen by clicking the variable on the left side.
![variable-example-9](https://github.com/frikky/shuffle-docs/blob/master/assets/variable-example-9.png?raw=true)
![variable-example-10](https://github.com/frikky/shuffle-docs/blob/master/assets/variable-example-10.png?raw=true)


## Passing values
Passing values is what makes a solution like Shuffle work. It allows you to pass value from app X to app Y seamlessly. There are currently a couple of different ways to pass values between nodes, that also applies for conditions.

* Use the "Data from previous actions" 
* Use the "static data" field

Using a previous action, you get a selection of all previous nodes, as well as the execution argument.

If you use the "static data" field (pencil), you have to write it out yourself. 
* "$testing_1" will get the data from the node "testing_1" OR variable "testing_1"
* "$exec" will get the execution argument. 

PS: it still only works with PREVIOUS nodes (nodes before the one you're editing)

## Parsing JSON
Parsing JSON is essential to be able to get API data. Shuffle uses it's own schema, which seems to work quite well. 

```
$node_1		= refers to a previously defined node called "node_1"
$exec		= execution argument chosen
$exec.name	= you choose the argument "name" from the execution argument
```

The first text after `$` will always be the name of the previous node. If you add "." ($exec.name), it will look for `"name"` as a json value under `"exec"`. If the node doesn't exist, it will just write `$exec.name` straight up.

Say you send the following data as our [execution argument](#execution argument):
```
execution_argument = {
	"name": "this is some data",
	"description": "Cool description",
	"extra": {
		"writer": "Fredrik"
	}
}
```

1. How would we go about getting "name"? execution_argument["name"]
2. How do we get "writer" under "extra"? execution_argument["extra"]["writer"]

* Action parameter:
1. 
![json-example-1](https://github.com/frikky/shuffle-docs/blob/master/assets/json-example-1.png?raw=true)

2. 
![json-example-2](https://github.com/frikky/shuffle-docs/blob/master/assets/json-example-2.png?raw=true)

* Static data:
I've put both questions into one. Maybe you catch my drift.
![json-example-3](https://github.com/frikky/shuffle-docs/blob/master/assets/json-example-3.png?raw=true)

### Examples
1. We have two nodes, and want "testing_2" to use the data from "testing_1". With "testing_2" selected, choose "testing_1" as data source.
![passing-values-1](https://github.com/frikky/shuffle-docs/blob/master/assets/passing-values-1.png?raw=true)

2. The same exact configuration, but using a static value.
![passing-values-2](https://github.com/frikky/shuffle-docs/blob/master/assets/passing-values-2.png?raw=true)

3. Using the execution parameter from 2 items (testing_1 and execution argument). The execution argument is defined to be "Hey this is cool" as seen in the bottom left.
![passing-values-3](https://github.com/frikky/shuffle-docs/blob/master/assets/passing-values-3.png?raw=true)

Result for #3:
![passing-values-4](https://github.com/frikky/shuffle-docs/blob/master/assets/passing-values-4.png?raw=true)

## Passing lists
**PS: If you deal with MULTIPLE loops (loop within a loop), please pass each element to a sub-workflow using the [Shuffle Workflow](/docs/triggers#subflow)**

Lists and looping are a different ballgame, but are really important to any SOAR solution. One simple reason would be: what if you have some alerts you want from system X to system Y? That will most likely be a list.

In the same way a node is identified by $, a list is identified by #. Say we have the following json data, and we want parse the "users" list. The node name is repeat_list (more below in example). 

**Usage**:
```
				= Without #, it DOES NOT loop the data.
.# 			= Loops the entire list
.#0 		= Runs ONLY the first element of the list 
.#1 		= Runs ONLY the second element of the list
.#0-1 	= Runs the first AND second element of the list
.#.data = Runs the entire list, and gets the JSON key "data" from each item
.#0.data = Runs ONLY the first element, and gets the JSON key "data" from it 
.#max.data = Runs ONLY the LAST element, and gets the JSON key "data" from it 
.#min-max = Runs ALL elements. Same as just # or #0-max
```


```
repeat_list = {
	"users": [{
		"name": "fredrik",
		"username": "@frikky",
		"id": "12345"
	},
	{
		"name": "moomo",
		"username": "shuffle user 2",
		"id": "23456"
	}]
}
```

To get all the "ids" from the list, we would write:
* $exec.users.#.id

Explanation:
1. $repeat_list = execution_argument
2. .users 			= "users" in the json data 
3. .# 					= the list identifier. This means we want to check the list.
4. .id 					= get all the IDs

Return: ["12345", "23456"]

### Examples
Let's use the example above in a real test.

1. We define a node, repeat_list, that gives us the list we defined above.
![values-passing-list-1](https://github.com/frikky/shuffle-docs/blob/master/assets/values-passing-list-1.png?raw=true)

2. We define a second node that returns the ID's as described above.
![values-passing-list-2](https://github.com/frikky/shuffle-docs/blob/master/assets/values-passing-list-2.png?raw=true)

3. Check the results.
![values-passing-list-3](https://github.com/frikky/shuffle-docs/blob/master/assets/values-passing-list-3.png?raw=true)

4. To build upon what we just created, we want to recreate the data described above as such:
```
{
	"ids": ["12345", "23456"],
	"names": ["fredrik", "moomo"],
	"usernames": ["@frikky", "shuffle user 2"]
}
```

This should work:
```
{
		"ids": $repeat_list.users.#.id,
		"names": $repeat_list.users.#.name,
		"usernames": $repeat_list.users.#.username
}
```

PS: Shuffle might throw you a JSON error for this, but that's expected behavior.

Here, we build the json we want ourselves. This is powerful, as we can basically define whatever data we want.
![values-passing-list-4](https://github.com/frikky/shuffle-docs/blob/master/assets/values-passing-list-4.png?raw=true)

## Casting values
Since version 0.9.25 of Shuffle, casting values and data formatting can be done using [Liquid formatting](/docs/liquid). All action parameters are supported.

Space stripping:
```
{{ "          So much room for activities          " | strip }}!
```

More details: [https://shopify.github.io/liquid/filters/strip/](https://shopify.github.io/liquid/filters/strip/)

## Authentication
Authentication is important for Shuffle and all API related software. The reason being that you can't connect to other services without authentication.

There are a few forms of authentication in Shuffle workflows:
* Authentication to other apps
* Authentication to execute a workflow

### App Authentication
As a user, authentication to an app should be pretty straight forward: Fill in some fields. These fields are usually the first arguments, including the endpoint URL, and will be required (orange circle). 

Here's and example for TheHive:
![thehive-authentication-1](https://github.com/frikky/shuffle-docs/blob/master/assets/thehive-authentication-1.png?raw=true)

If the app is generated using the App Creator in Shuffle, that uses OpenAPI, this should be consistent.

PS: If an app is self-made, this might not be the case, as the creator defines it.

**Advice: Use a workflow variable to control this**

### Workflow authentication
For each workflow execution, Shuffle generates a random authorization key that has to be used to interact with the execution itself. This is automated and here for informational reasons

In short: If you're not an admin and not a specific worker running the execution, you shouldn't be able to tamper with an execution.

## File Handling
This section is dedicated to file handling in workflows. Files have always had a special place in security, which also means in automation, meaning this needs to be a fully developed solution to handle that. We've approached it from the standpoint of "what do you need as a security professional", and added basic features like timestamps and hashes.

Files are handled in the backend of Shuffle through our API, which is fully accessible to apps. It's also possible to use the app creator to make file download actions. 

### Useful file handling info 
* Files are handled using their ID. This is a reference to the file, and is automatically generated.
* Other useful fields: md5/sha256, Filename, Filesize, organization, origin workflow, created time, status...
* We will add S3 buckets and other storage mechanisms later.
* [File API can be found here](/docs/API#file-api)
* They're typically identified by the field "File_id"

A file can be in one of four statuses 
* Created 		- The meta is prepared, but no file upload has been started. The ID is ready to handle a file.
* Uploading 	- A file upload has started. No other file can be uploaded from this point.
* Active 			- This means the file exists, and the data can't be changed.
* Deleted 		- The file has been deleted through Shuffle, retaining the metadata.

### Learn to use files 
To get familiar with files, go to the /admin view under the "files" tab and upload a file of your liking. With a file uploaded to our system, click the File ID icon on the far right side in the view to copy the ID. This is our reference to it for our workflow. Files are typically created and used within apps themselves, but this is good for testing.

![workflow-files-1](https://github.com/frikky/shuffle-docs/blob/master/assets/workflow-files-1.png?raw=true)

Next up, we'll use the file we just got in a workflow. To do this, we recommend using the "Shuffle Tools" app. This has the following functionality:
* Get file value 			 - print file content
* Download remote file - wget, download from URL
* Get file meta 			 - used for getting file metadata
* Delete file 				 - deletes the file content from disk. Meta persists.

**PS: If you need to create a file directly, the "Testing" app has this functionality"**

Here's a simple workflow where we show the file's value (EICAR), as well as the metadata provided by Shuffle:
![workflow-files-2](https://github.com/frikky/shuffle-docs/blob/master/assets/workflow-files-2.png?raw=true)
![workflow-files-3](https://github.com/frikky/shuffle-docs/blob/master/assets/workflow-files-3.png?raw=true)

As seen above, this returns most of the data required related to files. This is the basis of how we do anything with files in Shuffle, and by using the API, we allow the possibility of connecting with other apps. 

Good examples of other apps that use the file upload API are Yara (for rule testing) and TheHive (for data uploads). 

### Upload file API with the app creator
Next up, we'll show you an example of how an app action can be made that can handle files. Here, we'll use virustotal as an example. First, start by going to the /apps view, and clicking "Edit App" on the Virustotal (or wanted app).

You'll then see a view like this, where we can add an action.

![workflow-files-4](https://github.com/frikky/shuffle-docs/blob/master/assets/workflow-files-4.png?raw=true)

Next up, click "New Action" to add a new one.
![workflow-files-5](https://github.com/frikky/shuffle-docs/blob/master/assets/workflow-files-5.png?raw=true)

As we're gonna upload a file, it requires us to use a POST request, which is where we see the new action - "Enable Fileupload". Click it, then enter "file" as seen in the image below. 

![workflow-files-6-virustotal](https://github.com/frikky/shuffle-docs/blob/master/assets/workflow-files-6.png?raw=true)

At the same time, copy the curl request into the "URL path" field, and see it convert the curl statement into the path we want.
![workflow-files-7-virustotal](https://github.com/frikky/shuffle-docs/blob/master/assets/workflow-files-7.png?raw=true)

As you save it, you'll also see this tiny icon representing that it handles files. 
![workflow-files-8-virustotal](https://github.com/frikky/shuffle-docs/blob/master/assets/workflow-files-8.png?raw=true)

With all that done, it's time to build it, and use it in a workflow. As you can see below, it shows the "File_id" field, telling you it wants a file.
![workflow-files-9-virustotal](https://github.com/frikky/shuffle-docs/blob/master/assets/workflow-files-9.png?raw=true)

Having ran it, we get the correct response, as expected from their documentation;
![workflow-files-10-virustotal](https://github.com/frikky/shuffle-docs/blob/master/assets/workflow-files-10.png?raw=true)

And with that, we're done with the basic part of files in Shuffle. If something is unclear, please tell us.

## Branches & Conditions

### Conditions
Conditions determine the flow of node execution within a workflow. A condition is defined on the branch/line between two nodes. Consequently, you require at least two nodes to set a condition within a workflow. By default, a branch has an implied true condition, resulting in the execution of a subsequent node.

A node may have multiple branches flowing from it. These branch conditions are evaluated independently. Parallel execution of nodes will occur where multiple branch conditions leave a node evaluate as true. Additionally, a branch between two nodes may also have multiple conditions defined. Boolean logic is used to evaluate these conditions.

**NOTE: Currently, defining multiple conditions has an implied AND. An OR condition is defined using multiple branches, each with a specified condition.**

The configuration of conditions will be displayed on the right-hand side when the line between nodes is clicked. The design of the configuration options is similar to other nodes in Shuffle.

The available set of values to use within a condition defined on a branch is the same as other nodes within Shuffle. Consequently, the condition can be passed the result from any previous node or a workflow variable or other execution argument.

**PS: Conditions can NOT handle loops right now ($variable.#). Use the [Filter App action](#condition-loops) to learn more.**

1. Click a branch / line
![conditions-example-1](https://github.com/frikky/shuffle-docs/blob/master/assets/conditions-example-1.png?raw=true)

2. Click "New condition"
![conditions-example-2](https://github.com/frikky/shuffle-docs/blob/master/assets/conditions-example-2.png?raw=true)

3. Configure the condition. Choose the value(s) you're looking for, and use the center piece ("DOES NOT EQUAL" in this example) to modify what you want. In the case of this image, it would NOT run, because "hello" (left side) equals "hello" (right side).
![conditions-example-3](https://github.com/frikky/shuffle-docs/blob/master/assets/conditions-example-3.png?raw=true)

4. Here's another example, where it would run IF the [execution argument](#execution-argument) contains "shuffle is cool". That also means it would run if you write "I don't think shuffle is cool.".
![conditions-example-4](https://github.com/frikky/shuffle-docs/blob/master/assets/conditions-example-4.png?raw=true)

5. Here's another way of writing the exact same condition as in step 4. Notice the difference? We didn't select the "execution argument" as a previous action, but use it as a static value (this is explained further in [passing values](#passing-values)).
![conditions-example-5](https://github.com/frikky/shuffle-docs/blob/master/assets/conditions-example-5.png?raw=true)

### Condition Loops
**PS: It is best to avoid loops within conditions by using the "Shuffle Workflow" trigger to run each item of a list in a [subflow](/docs/triggers#subflow). However, this will require additional workflows to be executed, which will result in more CPU and RAM usage**

In this section, we'll be exploring how to use conditions for loops. As explained above, this is done using the "Filter List" action of the "Shuffle Tools" app. The goal if this app is to filter what DOES and DOESN'T fit your criteria within a list. This app action has the same functionality as a normal condition. These conditions are based on the "filter" mechanism of arrays in Javascript.

Take the example of the list below. How would we use the app to only find the section that IS malicious (where "malicious" = true)?
```
[{"ip": "1.2.3.4", "malicious": true}, {"ip": "4.3.2.1", "malicious": false}, {"ip": "1.2.3.5", "malicious": true}]
```

1. Create a node that can handles the list.
![condition-loop-1](https://github.com/frikky/shuffle-docs/blob/master/assets/condition-loop-1.png?raw=true)

2. Add another node that uses the "Filter List" action
![condition-loop-2](https://github.com/frikky/shuffle-docs/blob/master/assets/condition-loop-2.png?raw=true)

3. Add the right information to the fields. The first field is the list itself. 
**PS: DONT add # here. Pass the entire list, not one at a time.**
```
input_list: The ENTIRE list that we want to filter. In our case; "$repeat_list" 
field: The field we want to validate. In our case this is "malicious" as we want to see if malicious is true or false
check: How do you want to validate? In this case, we want it to check if EQUALS. Other options: Larger than, Less than, Is Empty, Contains, Starts With, Ends With, Files by extension
value: the value we want the value to be. In our case, it's "true" as we only want it to be true.
opposite: want to make it opposite? "equals" becomes "NOT equals" and "Larger than" becomes "Less than" etc.
```
![condition-loop-3](https://github.com/frikky/shuffle-docs/blob/master/assets/condition-loop-3.png?raw=true)

4. Get the output! The data is returned as such:
```
{
	"success": True,
	"valid": [..],
	"invalid": [..]
}
```

The "valid" field will match our criteria, while the "invalid" part has everything that doesn't. In our case (below), there are 2 that ARE malicious, and 1 that isn't.
![condition-loop-4](https://github.com/frikky/shuffle-docs/blob/master/assets/condition-loop-4.png?raw=true)


## Exploring Executions
Executions in Shuffle can be explored by clicking the button of the "Running" person on the bottom of your screen while inside a workflow. This will open up a side-bar where you can see a list of the last executions as well as dig into details on why something did or didn't work (debugging). It will not always notify you when a new execution has happened, as these run in the background, but will open up when you attempt re-running an execution.

<img width="1021" height="200" alt="image" src="https://github.com/user-attachments/assets/1b469985-945f-49c3-8de8-2a9aefb21e5b" />

### Execution List
After clicking the button, you will see a list of executions, which can be refreshed as you go along. This list is meant to help you find a previous execution, and to dig into it further. Here's a quick breakdown of what everything means:

![image](https://user-images.githubusercontent.com/5719530/193848186-2a6fab57-aeb2-4af5-b56a-e3756d3ef731.png)

- "Refresh Executions" button: Get an updated list in case a workflow was executed in the background.
- List of executions: These are items that can be clicked to explore each individual execution. Some more details:

**Colors**

* Green: Good/Finished Execution
* Yellow: Executing/Waiting Execution
* Red: Aborted/Failed execution

**Icons**

These indicate HOW the specific execution was started. The options are:
- Playbutton: Manual executions
- Triggers icons: Webhooks, Schedules, Subflows, User Input, Email systems

**Timestamp**

The timestamp the Workflow started at

**Arrow Icon >**

Usually White. Orange color indicates the LATEST execution you clicked.

### Execution Details
When clicking an execution, you will see information similar to the image below. This contains the details of how a workflow was actually ran. From the top, here's what everything means:

![image](https://user-images.githubusercontent.com/5719530/193849909-0bd971e4-f8ba-4c80-b26c-7317ec2ca370.png)

**See other executions button**

Go back to the list of executions

**Execution Info**

- Rerun Icon: Rerun the execution with the exact same execution argument from the same startnode.
- Status: Whether the workflow is finished/executing/failed etc. Should be FINISHED when it's done
- Timestamps: Indicates when it started and when it finished. If there's a lot of time between these two, then you probably have problems with the execution, or node delays enabled.
- "Show Skipped actions": Anything that's NOT under the Startnode will be hidden by default. Clicking this will show anything with a status that shouldn't be visible (e.g. SKIPPED).

**Action List**

The next part is a list of Action Results that were performed within the execution, typically in order of when they ran. Here is the breakdown of the buttons in each action:

- The "Arrow left icon <": Expand information about that specific Action Result. Usually contains even more debug information.
- Logo: The logo of the App
- Name ("NEW" in the image): The Name you have provided to the Action in the Workflow
- Function name ("get_me" in the image): The Python function that will run within Shuffle itself. Even if the app is OpenAPI/Generated, it will still be a python function hidden underneath it all.
- Status: The Status of the Action itself. If this is ABORTED or FAILED, Shuffle will create a notification for your organization and stop the workflow itself. This is NOT to be confused the "status" within the JSON result, which doesn't cause the workflow to stop, but which can be used in conditions.
- Result: The actual result itself. The black box can be clicked to expand the JSON values. These values can further be used in the next actions.

![image](https://user-images.githubusercontent.com/5719530/193852036-513560ef-2a7b-4b66-9a6e-c79698534822.png)

**PS: There's a handy Copy trick with JSON. By clicking the VALUE in JSON, it will copy the path to the Value itself (e.g. #nodename.success), while clicking the pink COPY ICON to the right of the value will copy the actual value (e.g. false in the image above)**

### Workflow Run Debugger
The Workflow Run Debugger is a powerful tool for debugging and managing large volumes of workflow executions. It is the recommended solution when you need to find past runs or **view more than the 100 executions**.You can find it at [https://shuffler.io/workflows/debug](https://shuffler.io/workflows/debug).

![Workflow Run Debugger](https://github.com/0x0elliot/Shuffle-docs/blob/master/assets/workflow_run_debugger.png?raw=true)

---

**How to Access the Workflow Run Debugger**

There are two ways to access the debugger. The recommended method is starting from your workflow, as it pre-filters the list for you.

**From a Specific Workflow:**
1.  Navigate to the workflow you want to check.
2.  Click the **"running person" icon** 🏃 (located next to the "Play" button) in the **bottom-left corner**.

<img width="1618" height="906" alt="image" src="https://github.com/user-attachments/assets/5b76e581-b46c-4a4d-b83f-c36cb2459fff" />

3.  On the "All Workflow Runs" list that opens, click the **graph/search icon** (📈) in the **top-right corner**.

<img width="1087" height="895" alt="image" src="https://github.com/user-attachments/assets/69a8bfcf-e12d-4b55-98fb-e8a84451c169" />


**Directly by URL:**

You can also access the debugger directly at:
`https://shuffler.io/workflows/debug?workflow_id=<your-workflow-id>`

If you use this link, you may need the workflow id to find the specific executions you are looking for 

---

With the Workflow Run Debugger, you can:
- Filter executions by Workflow Name, Status, Execution Argument, Start and End date/time range, and Results.
- The debugger's **"Max Results"** dropdown allows you to load and view up to **500** executions at once, Which allows to view large execution histories.
- View all executions in your organization and sub-organizations.
- See the execution status of visible executions.
- Efficiently manage multiple runs. By using the checkboxes next to each run, you can select multiple executions and **mass abort** (stop) or **mass rerun** them simultaneously. This is ideal for handling a large number of failed or stuck workflows.

## Collaboration features
Workflows have additional features that may be helpful when you start scaling, or want to collaborate.

### Suborg distribution
**Beta:** Suborg distribution is a way you for you to build a workflow once, and use it in all your tenants. If you have special needs for one or more of your customers, this can additionally be added. 

**Requirements:**
1. Be in a parent organization
2. Have a minimum of one sub-tenant
3. Set up which sub-organizations you want to distribute a workflow to by going into the "Edit" button.

<img width="513" alt="image" src="https://github.com/user-attachments/assets/637a58e9-5e9a-4b65-9dbd-d4217350e6ec">

**Usage:**
1. A distributed workflow is identified by the tiny blue border around the workflow.

<img width="279" alt="image" src="https://github.com/user-attachments/assets/775632be-d02e-4b5b-83a4-213924434665">

2. While inside the workflow, you can swap between which organizations workflow you want to use.
<img width="227" alt="image" src="https://github.com/user-attachments/assets/8191f017-18ab-4df2-9ec5-25be4e48465b">

3. You may edit a child workflow, but the parent will override any changes to the nodes that are controlled by the parent on next save, except for:
- New nodes (child-workflow nodes)
- New branches (child-workflow branches)
- Authentication

### Workflow Revisions & Versioning
Every workflow has backups by default. These are stored in a separated database index, and can be reverted to at any time. It will save a maximum of once per 60 seconds.

Find the following icon on the bottom bar to find your backups:
<img width="66" alt="image" src="https://github.com/user-attachments/assets/8426414a-d712-445b-a176-0a8c1fcb6163">

Choose the backup you want to revert to. Your current configuration will also be saved, and you can go back and forth.
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/38ad3f03-cace-43a8-bf0d-e199e64cf196">


### Authentication Groups
**Beta:** Ever wanted to run a workflow multiple times for all customers, but in the same workflow? Check out [authentication groups](https://shuffler.io/docs/organizations#app-authentication-groups)!

### Multiplayer
**Beta:** Workflows on Shuffle cloud are multiplayer. What this means is that you can for most usecases be building the same workflow at the same time.

### Forms
ALL Workflows are forms, and can be accessed by going to /forms/{workflow_id}. 
You can control the form by editing the workflow details in the "Forms" section.

<img width="1440" height="698" alt="Shuffle Forms" src="https://github.com/user-attachments/assets/1ae4176c-bc6d-4f19-9c2f-1d41b7cc2df1" />


TBA: See /workflows/<workflow_id>/run of any workflow. Configure Input fields in the edit window.

### Github backups
By going to the "Edit" panel for a workflow, you can input information about an individual workflow and how to store it. This will override any workflow backup configuration you may have made on the organization level. It will additionally be distributed to the same workflow in sub-organizations if specified.

These backups are stored without images, but are formatted in a way that makes it easy to track changes on Github.

<img width="513" alt="image" src="https://github.com/user-attachments/assets/e40c03ab-9da2-4868-bd4b-a620788f76a3">


## API
[Click here to see the Workflow API](/docs/API#workflow-api)

## Workflow Backup

The **Workflow Backup** system ensures that all workflows connected to **GitHub** or **Azure DevOps** are securely backed up and can be restored anytime. Shuffle automatically syncs workflow changes with your connected repositories, maintaining version history and backup integrity.

Workflows are automatically backed up whenever you change workflow. 

<img width="1392" height="547" alt="image" src="https://github.com/user-attachments/assets/079abd70-67f8-41e3-90a1-4b74b0e8f6ff" />

### GitHub Integration

GitHub backups allow Shuffle workflows to be stored inside your GitHub repository.

**How to get the required details:**

1. **Repository URL**
   - Go to your GitHub repository.
   - Click the green **“Code”** button.
   - Copy the **HTTPS URL**, e.g.:
     ```
     https://github.com/<organization>/<repository>.git
     ```

2. **Branch**
   - The branch name appears in the top-left dropdown of the repository page.
   - Common examples: `main` or `master`.

3. **Personal Access Token (PAT)**
   - Go to [https://github.com/settings/tokens](https://github.com/settings/tokens)
   - Click **“Generate new token (classic)”** or use **Fine-grained tokens**.
   - Enable the following scopes:
     - `repo` (Full control of private repositories)
     - `workflow`
   - Copy and store your token securely it will be used for authentication.

4. **Username**
   - Use your **GitHub username** as shown in your GitHub profile URL.


### Azure DevOps Integration

Azure DevOps integration enables workflow backup with your organization’s Azure Repos.

**How to get the required details:**

1. **Repository URL**
   - Navigate to your Azure DevOps project.
   - Go to **Repos → Files**.
   - Click **Clone** and select the **HTTPS** option.
   - Copy the repository URL, which follows this format:
     ```
     https://dev.azure.com/<organization>/<project>/_git/<repository>
     ```

2. **Branch**
   - The active branch name is visible in the **branch selector** dropdown above the file list.
   - Example: `main` or `develop`.

3. **Personal Access Token (PAT)**
   - Go to [https://dev.azure.com](https://dev.azure.com)
   - Click your profile picture → **Personal access tokens** → **+ New Token**.
   - Set **Organization** and **Expiration**, then grant the following scopes:
     - `Code (Read & Write)`
   - Copy and store the generated token securely — you’ll need it for authentication.

4. **Username**
   - Use your **Azure DevOps email address** as the username.

Note: Azure devops support is available from version 2.1.1 and above
