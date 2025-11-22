# Shuffle Features 

[![Shuffle Features Presentation PDF](https://raw.githubusercontent.com/Shuffle/Shuffle-docs/master/assets/Shuffle%20Features%20Presentation.png)](https://raw.githubusercontent.com/Shuffle/Shuffle-docs/master/assets/Shuffle%20Features%20Presentation.pdf)


## Table of contents
* [Introduction](#introduction)
* [Best in class App Creator](#best-in-class-app-creator)
* [The workflow designer](#the-workflow-designer)
* [Default use-cases](#standard-workflows-and-apps)
* [Cloud and Open Source](#local,-hosted,-cloud-and-hybrid)
* [Multi-Org for free](#multi-tenancy-and-multi-org)
* [File analysis](#file-storage)
* [Key Value Store](#key-value-store)
* [Encrypted Authentication Storage](#encrypted-authentication-storage)
* [Built-in Documentation](#built-in-documentation)
* [Automation Triggers](#triggers-of-all-kinds)
* [Autocomplete](#autocomplete)
* [SSO and MFA](#sso-and-mfa)
* [Marketplace](#marketplace)
* [Development AI](#development-ai)

## Introduction
With the problems described in [our about page](/docs/about) in mind, this document describes the features we have and will be implementing to ensure **anyone** can build on the Shuffle platform. Shuffle is not to only be used by developers, but by anyone curious about automation.

## Best in class App Creator
Our app creator is how we can promise to build apps within hours and days, rather than weeks. It's a easy to use, but yet powerful way to easily interact with other platforms' API's. It allows for app creation based on Swagger/OpenAPI, and can handle authentication for any HTTP method. The best part? You can export those apps as OpenAPI, meaning our apps aren't tied to Shuffle itself. 

Our goal with the App Creator is to incentives as many security companies as possible to share their API's, and to keep the largest repository of integrations out there.

![app creator](https://github.com/frikky/Shuffle/raw/master/frontend/src/assets/img/github_shuffle_img.png)

## The workflow designer 
Our workflow designer is the part of Shuffle that makes it all fit together. Together with the [App creator](/apps/new) and our default apps (HTTP & Shuffle Toolbox), it gives you access to unlimited automation possibilities, ensuring anyone can learn to automate anything with just a few hours of practice.

![Automation-builder](https://github.com/frikky/shuffle-docs/blob/master/assets/shuffle-workflow-1.png?raw=true)


## Standard workflows and apps
Shuffle comes pre-packaged with a [large amount of apps](https://github.com/frikky/shuffle-apps) and [workflows](https://github.com/frikky/shuffle-workflows), making it both easy to start using and extend. This, together with our [Marketplace](#marketplace) is what will bring security to new heights.

## Local, hosted, cloud and Hybrid
Shuffle's focus has and will always be on Open Source and collaboration. With this in mind, we are tirelessly building out features and fixing bugs for the [Open Source](https://github.com/frikky/shuffle), before testing, migrating and deploying it across our user- and customerbase. 

- [Shuffle cloud](https://shuffler.io) is a custom solution with mostly the same codebase, but is Micro-service oriented through Google Cloud Functions.
- [The local and hosted](https://github.com/frikky/shuffle) version of Shuffle is the one hosted on Github, and comes out of the box with no limitations.
- [Shuffle Hybrid](#hybrid_configuration) is another variant, allow for the local and cloud version to work together. This will further allow for connections between Shuffle instances in the future.

![Cloud organizations](https://github.com/frikky/shuffle-docs/blob/master/assets/features-3.png?raw=true)

## Multi-tenancy and Multi-org
Shuffle allows for a user to have multiple Organizations associated with a User and vice versa. Organizations have logical barriers, making users able to easily swap between them. Shuffle is further extended for MSSP's needs, allowing for Sub-organizations to be controlled from a Parent-organization.

![Shuffle Organization change](https://github.com/frikky/shuffle-docs/blob/master/assets/features-4.png?raw=true)

## Multiple environments
Have multiple datacenters with physical barriers for connections? No problem - we've built a way for a single workflow to run scripts in multiple locations. Environments are divided by Organization, but still allowing for resource sharing if necessary.

## File storage 
What is a security system that can't handle files? Not very useful. The good news? We can. If you want to connect Shuffle to your favorite sandbox, or upload and analyze an email with Yara - we can do it all.

What more? We also support namespaces, allowing for the download of a full namespace as a single bundle. What does this mean? You can e.g. control all your rules from a single place. 

![Shuffle file handling](https://github.com/frikky/shuffle-docs/blob/master/assets/features-5.png?raw=true)

## Key Value store
We've extended Shuffle with the possibility of storing data for all your needs. This is called the "Shuffle Cache" and can be used for e.g. Pagination, timestamp management, IOC lists and anything else you want. Not to worry! This is permanent storage if you want it.

What more? It's easy to use, and accessing the data can be done directly from $shuffle_cache, while setting values can be done with the Shuffle Toolbox.

![Shuffle cache handling](https://github.com/frikky/shuffle-docs/blob/master/assets/features-6.png?raw=true)

## Encrypted Authentication storage
Having a good storage solution isn't enough. What if the server itself gets breached? Worry not! All your treasures are safely encrypted, and decrypted ONLY in real time for an app that needs to use them. 

![Shuffle encrypted authentication storage](https://github.com/frikky/shuffle-docs/blob/master/assets/features-7.png?raw=true)

## Built-in Documentation
What is a system that isn't documented well? A not so useful system. That's why we've ensured that our apps get documented, which is available at the click of a button from within the Workflow UI - right next to the authentication process.

![Shuffle documentation everywhere](https://github.com/frikky/shuffle-docs/blob/master/assets/features-8.png?raw=true)

## Triggers of all kinds
Automation wouldn't be automation if you had to do manual work. That's why Shuffle has implemented 4 core triggers:
- Webhooks: Allows any outside source to send data in real time to Shuffle.
- Schedules: Makes it possible to start a workflow on a schedule 
- Subflows: Want to run another Workflow from within your current one? This does that exactly.
- User Input: Starting or continuing an action based on what an analyst decides 

Extension triggers (not exhaustive): AWS Lambda, AWS S3, Elastalert, Kafka, Pub/Sub

## Autocomplete
The Autocomplete feature in the Workflow Editor allows you to dynamically reference and insert data from previous node executions into your current action or script.

When you open a field (such as the body, arguments, or parameters) and type the $ symbol or click the autocomplete icon, Shuffle automatically lists all available runtime variables and datastore entries from earlier workflow steps.

Each listed item represents data output from a previous node (for example, $phishing.value, $email_ids.value, or $testing.value). By selecting any of these variables, it automatically inserts the appropriate dynamic reference into your editor.

<img width="636" height="264" alt="Screenshot 2025-11-05 at 2 35 47 AM" src="https://github.com/user-attachments/assets/061fcbe8-1c7f-4f8a-9e49-7ab4380bd94a" />


## SSO and MFA
SSO and other required authentication mechanisms are already in play, and available to anyone who wants to use them rather than normal signin. Our main supported platforms are the following, with more platforms to come ([ask us!](https://shuffler.io/contact)):
- Okta
- Auth0
- PingID
- AzureAD

![Shuffle single signon](https://github.com/frikky/shuffle-docs/blob/master/assets/features-2.png?raw=true)


----------------------------------------------------------------------------------

**Anything below here is alpha stages**

### Marketplace
The Shuffle marketplace is where you can go and find the integrations and workflows you want. As more users Publish their workflows and apps, we will move a lot of our focus here.

![Shuffle marketplace](https://github.com/frikky/shuffle-docs/blob/master/assets/features-9.png?raw=true)

### Development AI  
We're developing technology to allow for apps and workflows to be built based on text. This is based on OpenAPI's GPT-3 model, and can make it even easier for anyone to automate long-term. 

This is available for testing at [https://shuffler.io/chat](https://shuffler.io/chat) and will be open sourced soon~
