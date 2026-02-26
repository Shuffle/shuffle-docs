# Organizations 
Documentation for the Admin view of Shuffle. Best used by administrators.

## Table of contents
* [Introduction](#introduction)
* [Organization Overview](#organization_overview)
* [App runs management for Suborgs (Enterprise)](#app_runs_management_suborg)
* [Data collection](#data_collection)
* [Pricing](#pricing)
* [Licensing](#licensing)
* [User Management](#user_management)
* [App Authentication](#app_authentication)
* [Locations](#locations)
* [Schedules](#schedules)
* [Files](#files)
* [Datastore](#datastore)
* [Tenants](#tenants)
* [Statistics](#statistics)
* [Health](#health)
* [Notifications](#notifications)
* [Billing](#billing)
  	* [Onprem Licensing](#onprem_license)
    * [Default Limits](#default_limits)
  	* [Cloud Synchronization](#cloud_synchronization)
  	* [License Key](#license_key)
  * [Production Readiness](#production_readiness)
  * [Checking Subscription Details](#subscription_details)
  * [Viewing Enabled Features and Limits](#features_and_limits)
  * [Upgrading or Increasing Limits](#upgrading_limits)

## Introduction
Organizations are Shuffle's way of organizing data, and can be thought of as tenants. Data from Apps, Workflows, Notifications, Files etc. are all related to an organization from which users gain access based on their access rights. This document is made to explain what the different options for organizations are.

## Organization overview
The organization overview gives access to these things:
* Name Change
* Description Change
* Image change
* Cloud synchronization
* App runs management for suborg
* Hybrid Feature overview
* Single Signon options
* Notification Workflows
* Priorities & Notifications
* Licensing 
* Statistics
* Branding (Beta)

This view outlines the basic details of your organizations, which any Admin can change at any time. It can tell you about new updates, features and more that we have in store. The view is slightly different from the cloud version to the on-premises version. Here's how:
* The **cloud** version shows you an API-key. This can be used in the open source version.
* The **open source** version gives you an API-key field. This can be used in the cloud version.
![Organization view](https://github.com/frikky/shuffle-docs/blob/master/assets/admin_example-1.png?raw=true)

### App Runs Management for Suborg (Enterprise)
Starting from version 2.0.2, enterprise users can manage suborg app run limits from the parent organization. The maximum limit that can be assigned to a suborg is equal to the app run limit of the parent organization. For example, if the parent org has an app run limit of 300k, the maximum limit that can be assigned to each suborg is also 300k.

This feature is currently available to [Enterprise users](https://shuffler.io/pricing) only. If you have any questions or need assistance, please reach out to us at support@shuffler.io.

**Steps to assign app run limits to a suborg from the parent org:**
1. Log in to your Shuffle account and visit the [Billing tab](https://shuffler.io/admin?admin_tab=billingstats) on the admin page.
2. Scroll down to the *Utilization and Stats* section. There, you’ll find the *Child Organization* tab, where you can manage suborg app run limits.
![image](https://github.com/user-attachments/assets/a54a6b03-f787-4c3d-bd8c-eab4bef9496a)
3. Click the edit icon next to the *App Execution Limit*. A pop-up will appear where you can assign the app execution run limit for each suborg. You can follow the same process to assign workflow run execution limits.  
![image](https://github.com/user-attachments/assets/d9faf8dd-5663-4381-9e4a-71d244b2d9df)


## Hybrid Features 
Updated November 14th, 2022

Want to try it out? Hybrid Access is Free. 

There are many features that make Shuffle more usable. These are mainly related to accessibility, scalability and collaboration - in that order. For the initial release (v0.8) of Shuffle, we've decided to focus entirely on accessibility. Every feature comes with some of the same basic features, so that you know what you're getting into.

**These basic features are**
* Activation (true or false)
* Limits (none or 0-infinite)
* Privacy & Data sharing (none, minimal, high)
* Type (general, actions, triggers, editor, )
* Description

**These are the categories they fit into**
1. Accessibility - Makes Shuffle easier to use. We make every open source function open source, but some are hard or impossible to make easy for a user to have.
* Collaboration	 - Gives access to shared workflows, apps and general searching. This is to make it possible to learn from each other.
* Scalability 	 - Gives access to use our hardware and servers, e.g. through cloud executions. 

You can see most of our currently planned features on [https://shuffler.io/pricing](https://shuffler.io/pricing).

#### Activation
Activation tells you whether the feature is active. It's indicated by the red or green mark next to the feature on the admin page.
![Cloud sync features indicator](https://github.com/frikky/shuffle-docs/blob/master/assets/admin_example-8.png?raw=true)

#### Limits
Some features have limits. These are features such as SMS and email sending, schedule creation, cloud executions and more. Click each item to learn more.

![Cloud sync features limits](https://github.com/frikky/shuffle-docs/blob/master/assets/admin_example-7.png?raw=true)

#### Description
The description exists to specify what exactly an action does. This will become more granular over time. Access it by clicking each feature.

#### Data collection 
There are three types of data sharing, where the initial launch of Shuffle uses none. You can see the usage as per the image in [limits](#limits)

The three levels we'll keep to are:
* None 	- Shuffle doesn't collect any information about your on-premises organization. This is most features.
* Minimal - Shuffle collects a minimal amount of information necessary to execute the action. An example is a Workflow execution, where we'll need to gather information about the next steps in a workflow to properly execute it.
* High 	- Shuffle collects the necessary information to handle information. This is used for when full synchronization, meaning information used on-premises will also be used in the cloud. An example is having access to edit workflows in the cloud, that will execute on-premises. This requires access to all the same apps, workflows, credentials, triggers, organizational users and more. **PS: This will not happen for a while, and will be 100% OPTIONAL**

### Pricing 
[Our pricing tiers for Shuffle](https://shuffler.io/pricing) are currently split into three: Basic, Community and Pro. Basic is a support tier, and exists to make it possible for you to support us without having to use alternative means such as [github sponsors](https://github.com/sponsors/frikky). Everything we build out that can be priced is for us to further create a better offering for the open source community. 

Whenever we add new features that can help Shuffle work better by leveraging cloud resources, you'll automatically get access to it if you're on that tier.

These are our tiers:
* Free 
* Enterprise / Scale 

#### Free 
The basic tier is meant as a way for people to support Shuffle. It will give more perks over time, but to start of, it gives you and your team an onboarding meeting with Shuffle to get you kickstarted as well as some community support features.

#### Enterprise/Scale 
Pro is the full package. It is meant for those of you who want everything from support to auditlogging, datacenter choices, compliance overviews, data retention control, reporting, and more. This package is currently not available as 

Get in touch at [support@shuffler.io](mailto:support@shuffler.io) if you want something more specific.

## User management
![User management Shuffle](https://github.com/frikky/shuffle-docs/blob/master/assets/admin_example-9.png?raw=true)

User management is all about adding, listing, deleting and controlling users in general. Users are a part of a specific organization, and are created by organization admins. To add users you need the "admin" role.

**Existing roles**:
* Org-Admin - Gives access to control an organization, and see what everyone in the organization are doing.
* Org-User - Gives access to use the organizations resources, but NOT see everyone elses Workflows. This role is meant for engineers who are to build their own workflows, without potentially breaking others'
* Org-Reader - Gives access to READ all data for an organization (like an admin), but not make any changes.

**To come:**
* Creating API-only users (no login)
* Granular access (RBAC)

### Adding a user
Click the "ADD USER" button, and you'll get a popup. Type in their username (open source) or email (cloud), and you'll create an invite for them. Cloud will not allow an admin to set a password to share, but rather send them an email. This will also be a part of the hybrid offering later.

![Adding a user to shuffle](https://github.com/frikky/shuffle-docs/blob/master/assets/admin_example-10.png?raw=true)

### Change a users' role
Click the "Role" dropdown and choose one. Defaults are Admin and User, but we'll add granular access for this now. To repeat, here's the current roles:
* Admin - Gives you access to control an organization, and see what everyone in the organization are doing.
* User  - Gives you access to YOUR resources within an organization. This is to prevent you from seeing what everyone else are doing.

### Deleting a user
A user in Shuffle can't be deleted, but deactivated. This is to keep all references available for when audits eventually require them. Click "Edit user", then "Deactivate". This prevents the user from being used. **A deactivated user can be reactivated.**

## App Authentication
App authentication is a way for Shuffle to keep track of what credentials you have for an app in a specific organization. It shows you information the most important information, and gives you access to modify or easily delete them. Authentication is specified at the app level, and applies to ALL functions of the the app, unless specified otherwise. Authentication is created during workflow editing.

![Basic app authentication](https://github.com/frikky/shuffle-docs/blob/master/assets/admin_example-11.png?raw=true)

These are **NOT** editable outside of deletion as of november 2020, but we may add the possibility of changing without showing the previous value. 

### KMS
Shuffle supports the use of a KMS. [Please see the extension documentation for more](/docs/extensions#kms).

### App Authentication Groups
**Groups was taken out of beta and was removed for the 2.0.0 release**

App Authentication groups are a way for you to group authentications together, enabling a single workflow to run with multiple different authentication options and runtime locations. When a workflow runs with authentication groups selected, the workflow execution will replicate and run multiple versions of the same workflow at the same time, where the relevant authentication is filled in in real-time. 

<img width="830" alt="image" src="https://github.com/Shuffle/Shuffle-docs/assets/5719530/44e1d2f6-6e1c-4736-834a-a98e6419814e">

**Requirements to use**
- Create at least two App Auth groups
- Have at least two different available authentications for an app in the same organization
- Choose the App Auth group you want to use in the app

If these requirements are fulfilled, the workflow will run as many times as there are App Auth groups selected in that workflow. If one app (e.g. Outlook) has selected to use App Auth groups in a workflow, we will distribute this to every node in the same workflow

**App Auth Groups vs. Suborg Workflow distribution**
A similar topic for running workflows is the Suborg Workflow distribution system, available in the Edit Workflow menu. 

The difference:
- App Auth Groups run in a single Organization, and may as of Q2 2024 not be distributed to suborgs. Will run multiple workflow executions in one organization.
- Suborg Workflow distribution is used when you want to segregate where and how the data is stored per organization, or where your customer may want access to the workflow. This uses a background distribution system when the parent workflow is saved.

<img width="520" alt="image" src="https://github.com/Shuffle/Shuffle-docs/assets/5719530/7d02f2e2-fce5-445c-94e4-1cea239b1a7f">


### Authentication Field overview 
The fields of authentication
* Icon 					- The App's icon. This is 
* Label 				- The name of the authentication scheme. Make it helpful, e.g. "QRadar Datacenter Amsterdam" or similar. 
* App Name 			- The name of the app it belongs to
* Workflows 		- The amount of workflows it's being used in
* Action Amount - The amount of actions that use the authentication
* Fields 				- The fields specified by the app creator. It's usually a URL, an API key or username & password.
* Actions 			- What you can do to edit the app. As of 20.11.2020, only deletion is accessible. By deleting it, you'll also make the **workflow invalid**.

### Authentication in workflows 
Authentication is and should be defined the first time you use an app. We'll use the example of TheHive, which takes the fields "apikey" and "url". Start by [creating a workflow](/docs/workflows#create), before dragging in the app "TheHive". 

Once it's in, click the node, and you'll see a view like this. We've outlined three places that indicate this app requires authentication. All of these are also clickable.
![Authentication in workflow](https://github.com/frikky/shuffle-docs/blob/master/assets/admin_example-14.png?raw=true)

By clicking either of these, a popup window will show. In this one, type in a DESCRIPTIVE name (to remember), before passing credentials. **PS: Never use localhost in an URL. Everything runs in a container, which has its own IP. Always use the system's IP/domain within the URL.**
![Authentication workflow popup](https://github.com/frikky/shuffle-docs/blob/master/assets/admin_example-15.png?raw=true)

By clicking "submit", the authentication is now saved for your organization. This removes clutter in the UI, by having less required fields, and is also reusable. You can now make multiple nodes that use the same authentication.
![Authentication view after submit](https://github.com/frikky/shuffle-docs/blob/master/assets/admin_example-16.png?raw=true)

Last, but not least, this can now be controlled on an organizational level. 
![The same authentication on](https://github.com/frikky/shuffle-docs/blob/master/assets/admin_example-17.png?raw=true)

### App creation with authentication
The fields are specified by the app creator. This short section outlines how to create authentication as a creator. [More on this in the apps section](/docs/apps). An example is TheHive, which takes a URL and an API-key. These fields have to be specified as seen below. 
![App creation specification](https://github.com/frikky/shuffle-docs/blob/master/assets/admin_example-12.png?raw=true)

Outer level: authentication
Inner level: parameters

These parameters are specified exactly as a parameter within an action. The function's code needs to reflect it as well, as can be seen with this python function, taking an apikey and URL.
![App creation python code](https://github.com/frikky/shuffle-docs/blob/master/assets/admin_example-13.png?raw=true)

## Locations
Locations, previously Environments, are a core part of Shuffle's open source build. **Cloud does not require any configuration for this**, unless you are connecting to your on-premises datacenter/cloud VPC. Think of it as physical location where you want an agent of Shuffle running (Orborus) with access to the right locations.

<img width="832" alt="image" src="https://github.com/Shuffle/Shuffle-docs/assets/5719530/48acd5c4-0a86-4379-8f76-8d3b877ae5a4">

The default location is called "Shuffle" in your on-premises installation, and "Cloud" in the Shuffle SaaS. You can add as many as you want, and will get access to the additional "cloud" location through cloud synchronization onprem.  

### Location fields
* Name 						- The name to use. This is the identifier used by orborus. 
* Orborus running	- Shows whether Orborus is running or not.
* Type 						- Whether it's a cloud location or not. Orborus can't attach to "cloud" locations.
* Default					- Whether it's the default location to use for new actions. You should set this to the location you use the most.
* Actions 				- Possible changes to a location. You can't re-open an archived location, and can't archive the default location.
* Archived				- Tells you whether it's archived. There's a toggle at the top to edit it.

### Orborus configuration
If you would like to run Orborus towards a different location, you will have to specify the environment variables "ENVIRONMENT_NAME", "ORG", "AUTH" and "BASE_URL". AUTH and ORG may not be required. You can click the location to get a finished command.

Below is an example, where the locations's name is "Another env" and it's using `https://shuffler.io` as it's backend. This works on-premises as well if you change out the BASE_URL.
```
docker run \
	--volume /var/run/docker.sock:/var/run/docker.sock \
	-e ENVIRONMENT_NAME="Another env" \
	-e AUTH="Auth from the location" \
	-e ORG="Your org ID from the /admin UI top right" \
        -e DOCKER_API_VERSION=1.40 \
	-e BASE_URL=https://shuffler.io \
	ghcr.io/frikky/shuffle-orborus:nightly

```

### Scaling Orborus
By clicking the "Scale" or "K8s" tab, you will get relevant info related to scaling Shuffle the way you want. This IS available from cloud to onprem (hybrid).

<img width="837" alt="image" src="https://github.com/user-attachments/assets/84eed978-e857-4965-87e3-813b0d5e964f" />


### Using Multiple Environments
It's possible to create and use multiple environments for your Workflows. 

- First, let's create a new Environment, by clicking on the "**Add Environment**" button. 
![SCR-20240430-evx](https://github.com/Shuffle/Shuffle-docs/assets/100738099/bbcdb5e3-d953-4e82-b87c-515644a84eae)

Once you add an environment, it will be displayed on the list. 

- If you create an Environment it will be set up as the Default for all workflows, but if you want to set a specific environment as the default click the "**Default**" button. 
![SCR-20240430-exd](https://github.com/Shuffle/Shuffle-docs/assets/100738099/d549f76c-9fe2-40ce-aa74-103d3dc964fd)

- Alternatively, you can select a different environment for a particular workflow in the workflow settings by selecting it from the displayed list after clicking on "**Environments**". 
![SCR-20240430-ey9](https://github.com/Shuffle/Shuffle-docs/assets/100738099/b754ad50-6cf6-4f97-82f6-b4f838e04e7e)

- To run the respective environment, you need to copy the Onborus command and modify the necessary fields such as "ENVIRONMENT_NAME", "AUTH" and "ORG", and ensure they are correctly filled in.
![SCR-20240430-ftw](https://github.com/Shuffle/Shuffle-docs/assets/100738099/67be6b9c-4533-4500-964c-b3cdb8cb0ecc)

To check if the Onborus command is set up correctly, look for a change in status from "**not running**" to "**running**". 


- If you want to change the Onborus from "**nightly**" to a different worker, in this example "test", go to BASE_URL and after "**/shuffle-orborus:**" change "nightly" to "test".
```
docker run \
	--volume /var/run/docker.sock:/var/run/docker.sock \
	-e ENVIRONMENT_NAME="Another env" \
	-e AUTH="Auth from the environment" \
	-e ORG="Your org ID from the /admin UI top right" \
        -e DOCKER_API_VERSION=1.40 \
	-e BASE_URL=https://shuffler.io \
	ghcr.io/frikky/shuffle-orborus:test

```

- Further documentation on running Orborus in production at scale, whether onprem or with hybrid environments: https://shuffler.io/docs/configuration#scaling-shuffle

### Health
Shuffle has a health check API that can be used to check the health of your Shuffle instance. It's related endpoints are available at:

-  `/api/v1/health`: This gives you the result of the cached execution (doesn't require an API key)
-  `/api/v1/stats`: This gives you historical data about the health of your instance (doesn't require an API key)

You can also force a run by making an API call at:
- `/api/v1/health?force=true` (calling this requires the API key of an admin user)

For the time being, this health check automatically runs every 15 minutes by default and can be disabled with the `SHUFFLE_HEALTHCHECK_DISABLED=true` environment variable.

### Notifications

Notifications are a way for Shuffle to inform you of a potential error in your workflows. We recommend you investigate them to see if the issue is an actual issue or not. 
They are organization-wide, meaning if you dismiss them, they get dismissed for everyone. A dismissed notification will show back up if it happens again. 

**Notification sources:**
- Failed workflows (Status: ABORTED)
- Workflows that take more than 10 minutes (without delays)
- Actions where the result JSON contains `"success": false`
- Actions where the result JSON contains `"status"` more than or equal to 300 (usually failed workflows)
- Failed Liquid formatting
- When a returned app parameter starts with "shuffle" and contains "error". Example: "shuffle variable error" for when a variable is not found.
- **We may add more without warning in the future. They are only added for things that represent typical things you want to see**

<img width="384" alt="image" src="https://github.com/Shuffle/Shuffle-docs/assets/5719530/ff16e86b-5db4-4300-97b4-4071a96b4aed">

**Accessing Notifications:**
- **Through the UI**: You can see a bell icon with a number next to it in the top right bar, when you are logged in. This indicates the amount of notifications you have. Clicking it will show you the notifications. If you see a number next to the notification, this is the amount of it that has occurred.
- **Selecting a Notification Workflow**: If you go to `/admin?admin_tab=organization`, you can see a section called "Notification Workflow". Click on it to select an appropriate workflow. This workflow will be ran whenever a notification is created, except when bucketed. This can be used to automate opening tickets, sending emails, or whatever you want to do when there is an error in your notification.We use some sort of "bucketing" of notifications, to prevent you from getting spammed. This means, every time a notification is created 2 times under 2 minutes, we'll only send you one notification. This is to prevent you from getting spammed.

If you are on the open-source side, you can change the bucketing timeout by changing the `SHUFFLE_NOTIFICATION_BUCKETING_MINUTES` environment variable. This is set to 2 minutes by default.

**Creating Custom Notifications:**
You can create notifications yourself with the Notification Creation API from Shuffle. These will act the same as any other notification by both being added to the UI, as well as being sent to your notification Workflow.

**Disabling a Notification:**
You can ignore/disable a notification by clicking the "Disable" button next to any of them.  

## Billing

### Onprem Licensing
Shuffle’s licensing system enables organizations to unlock advanced capabilities designed for production deployments and enterprise grade scalability.

While the open-source version of Shuffle includes all core workflow automation functionality, running Shuffle in production environments or at scale (including multi-tenant or multi-environment setups) requires a valid on-premise license.

Licensing ensures access to premium features such as high-performance scaling, multi-tenant management, multi-environment configurations, and full platform branding empowering organizations to customize, optimize, and securely manage their automation infrastructure.

### Default Limits
By default, Shuffle onprem instance includes the following limits:

- **Workflow Executions:** 10,000 per month  
- **Sub-Organizations:** Up to 3  
- **Environments:** 1
- **Branding** not Enabled

To run Shuffle **in production** or to **scale beyond default limits**, a valid **on-premise Shuffle license** is required.  
Licensing ensures access to advanced scaling, customization, and management features designed for enterprise and high-availability deployments.

For more information or to obtain an on-premise license, please contact **[support@shuffler.io](mailto:support@shuffler.io)**

### Cloud Synchronization
Cloud synchronization is a feature used to get more capabilities on-premises, that otherwise wouldn't be possible. These range from scalability to collaboration, support, public workflow generation, accessibility and more. The goal is to give access to features that otherwise are impossible to build in a location solution. See [Hybrid Features](#hybrid_features) for more info.

<img width="1272" height="502" alt="image" src="https://github.com/user-attachments/assets/95cd65c2-55ba-4230-8129-206b5f390b87" />


#### Setup 

Setting up cloud synchronization requires two things:
1. A user on [https://shuffler.io](https://shuffler.io). Get the API-key.
2. An open source version of Shuffle. [Here's how to set it up](https://github.com/frikky/shuffle/blob/master/install-guide.md)

1. Start by going to [https://shuffler.io/register](https://shuffler.io/register?view=admin) and create an account.

![Register user](https://github.com/user-attachments/assets/a849d04d-ce4e-43a3-b5f7-5b0c7e13fce6)

3. With an account made, go to [https://shuffler.io/admin](https://shuffler.io/admin). Here you'll find your API-key. Copy it.

![Cloud sync cloud](https://github.com/user-attachments/assets/13adf626-30b0-46d2-97f9-d7299c584612)

4. Go to your [local instance](http://localhost:3001/admin) at /admin and paste the API-key.

![Cloud sync local](https://github.com/user-attachments/assets/7f797416-83fd-470f-8f48-35f250528013)

6. See the features you get access to.

![Cloud sync local features](https://github.com/user-attachments/assets/ff1719b3-bd8e-4a40-8869-d07d5d0f7fe2)

A valid **Shuffle license** is required to unlock advanced enterprise capabilities on your on-premise instance.  

With a valid license, connecting your instance to the cloud allows you to access features such as **multi-tenant management**, **multi-environment setups**, **workflow executions**, and **branding customization**.

### License Key

For air-gapped or offline environments where **Cloud Synchronization** cannot be used, Shuffle supports activating enterprise features through an **on-premise license key**.

The license key allows organizations to unlock capabilities for **scaling**, **multi-tenancy**, **multi-environment setups**, and **branding** enabling full production use of Shuffle on-premises.

#### Applying a License Key

To activate your license, set the `SHUFFLE_LICENSE` environment variable in your on-prem deployment:

```bash
export SHUFFLE_LICENSE=<your_license_key>
```
Once applied, Shuffle will automatically recognize and unlock the licensed capabilities no internet connection is required.

#### Features Unlocked by License

A valid **Shuffle license** unlocks a range of enterprise capabilities.  
The availability of these features depends on the **type and level of your license**.

| Feature | Description |
|----------|-------------|
| **Workflow Scaling** | Increase monthly workflow execution limits to support larger workloads. |
| **Multi-Tenant Management** | Add and manage more sub-organizations within a single deployment. |
| **Multi-Environment Support** | Create and operate multiple isolated environments. |
| **Branding Customization** | Enable full white-label branding, including logo, colors, and support links. |

> **Note:** The exact features and limits available to your organization depend on your Shuffle license tier.  
> For more information or to upgrade your license, contact **[support@shuffler.io](mailto:support@shuffler.io)**.

You can securely store your license key in the **Datastore** tab (`/admin?tab=datastore`) or save it in a text file and upload it via the **Files** tab (`/admin?tab=files`) in the Admin panel.  

Alternatively, you may store the key outside of Shuffle (e.g., in a secure local or cloud storage) to ensure it can be recovered if the key is lost.

## Production Readiness (Onprem)

The **Production Readiness** section helps administrators verify whether their **Shuffle on-premise instance** is properly licensed, synchronized, and configured for stable production use.

Running Shuffle in production requires both a **valid on-prem license** and a **verified production configuration**, ensuring your deployment can support enterprise workloads with high availability, scalability, and reliability.

To **unlock default limits** ([see details here](https://shuffler.io/docs/organizations#default-limits)) for your on-prem instance, you must activate a valid license using either **[Cloud Synchronization](https://shuffler.io/docs/organizations#cloud-synchronization)** or a **[License Key](https://shuffler.io/docs/organizations#license-key)**.

Once your license is applied, navigate to the `/admin?admin_tab=billingstats` tab in the Admin panel and verify that:

- **Production Status** is set to **“On”**
- The following indicators show a **green checkmark**:  
  **License**, **Multi-Tenant**, **High Availability**, and **Robust Infrastructure**

![Production Readiness](https://github.com/user-attachments/assets/95dfccb9-9338-4787-8ca9-0ec2b80e0485)

---

## Checking Subscription Details

Based on your license type, you can view detailed subscription information in the **Billing Stats** section of the Admin panel (`/admin?admin_tab=billingstats`), as shown below:

![Subscription Details](https://github.com/user-attachments/assets/bdc65242-75bf-484d-ae1b-6757f67de3bb)

---

## Viewing Enabled Features and Limits

To review which features are unlocked and their respective limits:

1. Go to the `/admin?admin_tab=org_config` page in the Admin panel.  
2. Scroll to the **Hybrid Features** section.  
3. Check the list to see which features are currently enabled or disabled.

![Onprem Features](https://github.com/user-attachments/assets/1f5ad82a-ae58-4b56-a8e0-b18d90027108)

---

## Upgrading or Increasing Limits

If you need to:

- Increase existing feature limits  
- Enable additional enterprise capabilities  
- Upgrade to a higher-tier or **Enterprise license**

Please contact **[support@shuffler.io](mailto:support@shuffler.io)** for more information and assistance.


