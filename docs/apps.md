# Shuffle Apps
Documentation for apps. If you'd like to make an app [check out this guide](/docs/app_creation)

## Table of contents
* [Introduction](#introduction)
* [How they work](#how-they-work)
  * [Actions](#actions)
  * [Arguments](#arguments)
  * [Searching for apps](#searching-for-apps)
  * [Debugging apps](#debugging-apps)
* [Creating apps](#create-custom-apps)
  * [Updating apps remotely](#updating-apps-remotely)
  * [Delete app](#delete-app)
* [Finding more apps](#finding-apps)
  * [Testing apps](#testing-apps)
  * [Downloading apps](#downloading-apps)
  * [Importing apps](#importing-apps)
  * [Publishing apps](#publishing-apps)
  * [Activating apps](#activating-apps)
  * [Importing remote apps](#importing-remote-apps)
* [API](#api)

## Introduction
Apps are the heavy lifters of [workflows](/docs/workflows) within Shuffle. They give access to a library of functions, and are created using OpenAPI or pure Python. Shuffle gives you access to pre-defined integrations located [here](https://github.com/frikky/shuffle-apps). 

A subset of available apps can be found at [https://shuffler.io/apps](https://shuffler.io/apps). 

![Apps view 1](https://github.com/user-attachments/assets/71b1fc24-a49b-46e3-bdc2-a4286c94498e)

## How they work
Apps are the primary building blocks in workflows. Apps can be auto-generated from [OpenAPI](https://swagger.io/specification/) specifications or using Shuffle's app sdk. To enforce stability and usability, we use a versioning system to prevent sudden updates to apps.

Apps can contain multiple actions, which can take multiple variables. They are made to be able to interact with each other by using each-others' data. Apps have the ability to be in multiple [environment](/docs/organizations#environments) with different data (e.g. different credentials), before passing them on.

PS: In a future iteration, focus will move to an optional hybrid execution model (e.g. use cloud resources).

### Actions
An app can perform more than one task based on predefined actions. These actions are defined by the developer, and are reusable and modifiable by the user of the app. An action should (for now) be a one-to-one representation of the function to run, and usually has arguments for authentication with the target application. Actions can contain multiple arguments.

You can view an app's actions by selecting the app and clicking the edit icon. 

![Apps view 2](https://github.com/user-attachments/assets/3c995872-2a86-4951-a794-5958863a36b5)

![Actions View](https://github.com/user-attachments/assets/7ac431fa-be38-4f88-993a-95d45ed35aae)

### Arguments
Arguments are the variables used to perform an action. Arguments with an orange dot next to them are required, with yellow ones being optional. Arguments should have example text to to indicate the expected value. The first arguments of an app are _usually_ related to authentication or the target URL, where we suggest using [variables](/docs/workflows#variables)

You can see what parameters and action has by going to /apps, selecting an app and then the action.

![Apps view 3](https://github.com/frikky/shuffle-docs/blob/master/assets/apps-view-3.png?raw=true)

## Updating apps remotely
**PS: This only applies to onprem**
Going to /apps, there exists a button called "Download from Github" which by default will download apps from the directory https://github.com/frikky/shuffle-apps. You can type in your own repository along with authentication options if applicable.

![Apps view 11](https://github.com/frikky/shuffle-docs/blob/master/assets/apps-view-11.png?raw=true)

When the modal opens, there are two buttons:
* Submit - Downloads and builds NEW apps
* Force update - Downloads and builds ALL apps
* Cancel - Closes the modal with no action

## Searching for apps
When you set up Shuffle for the first time, it should provide you with >100 existing Apps. These are gathered from [shuffle-apps](https://github.com/frikky/shuffle-apps), and will grow over time. Searching for apps is done by going to /apps and writing your search term. In the example below, we searched for "TheHive", which ends in TheHive being shown. 

![Apps view 4](https://github.com/frikky/shuffle-docs/blob/master/assets/apps-view-4.png?raw=true)

A goal for Shuffle is to make it possible to search outside the apps you currently have. This is an [open issue](https://github.com/frikky/Shuffle/issues/24) as of 23.05.2020, but will be worked on.

**PS: Extended search can be done using the [shuffler search-engine](https://shuffler.io/search)**

## Debugging apps
Apps may fail at times, usually due to bad coding on the creators' side. This means that to get more information, you may be required to troubleshoot and debug to get the logs. 

More about this in the [app creation](/docs/app_creation#debugging) debugging section

## Create apps
Apps in Shuffle can be made using the App Creator or with Python directly.

Read more about how to make an app [here](/docs/app_creation)

**If you have an OpenAPI config already**
* Click the "Generate from OpenAPI", paste the URL or data for your OpenAPI specification, then validate, before submitting. This should show you the app creator.
...

**If you want to create an app**
* Click the "Create from scratch" button, then [use the editor.](/docs/apps#edit_openapi_app)


![Apps view 5](https://github.com/frikky/shuffle-docs/blob/master/assets/apps-view-5.png?raw=true)

## Edit OpenAPI app
Creating or editing an app in Shuffle is made to be as simple as possible

Prerequisite knowledge:
* HTTP - POST, GET etc.

App creator:
* Add name, description, authentication, endpoint etc..
* Create Actions.
* Save.
![Apps view 6](https://github.com/frikky/shuffle-docs/blob/master/assets/apps-view-6.png?raw=true)

If you've created an app using the editor, or uploaded an OpenAPI specification, it's changeable. Find the app you created by searching for it, then click the "Edit app" button as seen below. You can also delete it.

Required permissions (either or):
* Admin
* App owner / creator

![Apps view 7](https://github.com/frikky/shuffle-docs/blob/master/assets/apps-view-7.png?raw=true)
TBD


## Finding apps 
If the app you're looking for exists, it will be available on [https://shuffler.io](https://shuffler.io) or [Github](https://github.com/frikky/shuffle-apps). Apps available on the Shuffle website, can further be clicked then exported or tested directly.

![Apps view search 16](https://github.com/frikky/shuffle-docs/blob/master/assets/apps-view-16.png?raw=true)

## Testing apps 
After you've found a public or private app on [https://shuffler.io](https://shuffler.io/apps/c051cc46559dd040d963e0cdf19b7d9b), it's possible to test it directly. The view you get access to has the fully featured app included, meaning you won't need to build a workflow to test it.

**Options:**
- Selecting Actions
- Configuring the action
- Executing the action
- Exploring the result

![Apps view search 16](https://github.com/frikky/shuffle-docs/blob/master/assets/apps-view-16.png?raw=true)

## Downloading apps 
Apps can be downloaded or exported from your local instance or [https://shuffler.io](https://shuffler.io) as long as it's either your private app, or a public one AND is OpenAPI. If you find the "download" icon in any part of Shuffle, that means the item is exportable.

![Apps view activation 18](https://github.com/frikky/shuffle-docs/blob/master/assets/apps-view-18.png?raw=true)

## Importing apps
If you have an OpenAPI specification, either exported from Shuffle or otherwise, it can be imported in the [/apps](https://shuffler.io/apps) view. You need to be logged in.

Supported filetypes:
- .json
- .yaml

The options for importing are:
- URL: A URL to the file on the internet
- Upload: A local file on your filesystem
- Drag & drop: A local file on your filesystem. Drop it anywhere in the /apps view.

![Apps view activation 17](https://github.com/frikky/shuffle-docs/blob/master/assets/apps-view-17.png?raw=true)

## Activating apps 
Any public app can be activated, giving you access to a copy of the original app. This app is editable, meaning you can change the configuration of the app in it's entirety in your own Organization. Activation can be done by first [Finding the app](#finding_apps), then clicking the "Activate App" in the top right corner. If successful, you should se a notification that it's been activated.

Once an app is activated, you can use it within any Workflow, and find it under /apps. If you can already see the app under the /apps view, it means the app is already enabled. You need to be logged in. 

If you want an app activated in your LOCAL environment, see [importing apps](#importing_apps)

![Apps view activation 19](https://github.com/frikky/shuffle-docs/blob/master/assets/apps-view-19.png?raw=true)


## Publishing apps 
All apps can be published. Published apps are available to EVERYONE using Shuffle, as long as they activate it. This means if you publish an app, it is searchable AND shareable with others. The process for Python and the App Creator are different, as can be seen below. 

**Python**:
- App publishing with python can only be done with Github (for now). Make a pull request for [shuffle-apps](https://github.com/frikky/shuffle-apps). 

**App Creator**:
- To publish an app, find an app that you made and own, which is unique, and change "Sharing" to "public" as per the image below.

![Apps view 20](https://github.com/frikky/shuffle-docs/blob/master/assets/apps-view-20.png?raw=true)

**PS:** To remove a public app, [contact us](https://shuffler.io/contact)

## Create custom apps 
[Learn about app creation](/docs/app_creation)

## Importing remote apps
**NOT CLOUD**

If you have a repository (private or public) of custom apps for Shuffle (or WALKOFF), Shuffle can load all the apps by using the "Download from URL" button in the /apps view.

1. Click the "Download from URL" button
![Apps view 9](https://github.com/frikky/shuffle-docs/blob/master/assets/apps-view-9.png?raw=true)

2. Fill in the github/gitlab URL, and if the repo is private, your username & password. These are used for BasicAuth when running git clone. 
![Apps view 10](https://github.com/frikky/shuffle-docs/blob/master/assets/apps-view-10.png?raw=true)

3. Hit submit. If it's unsuccessful, it will throw an error, otherwise show a loading icon. This means it's working on getting your apps.

## Delete app 
**PS: There is nothing stopping you from deleting an app that is used by a workflow. This is a destructive action, and will make some workflows using the app unusable.**

Deleting an app is done by searching for it in /apps. 

Required permissions (either or):
* Admin
* App owner / creator

![Apps view 8](https://github.com/frikky/shuffle-docs/blob/master/assets/apps-view-8.png?raw=true)

## API 
[Click here to see the App API](/docs/API)
