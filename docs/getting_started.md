# Getting Started with Shuffle
Welcome to the Shuffle documentation! This guide will help you get up and running with Shuffle quickly and effectively.


## Table of contents
* [Introduction](#introduction)
* [Usage Models](#usage_models)
* [First workflow](#first_workflow)
* [Shuffle 101](#shuffle_101)
* [Shuffle Videos](#shuffle_videos)
* [Community Videos](#community_videos)
* [Learn about Shuffle](#learn_about_shuffle)

## Overview
Shuffle is an open-source automation platform designed specifically for the security industry. You can start using it for free with the following options:

- <a href="https://github.com/shuffle/shuffle/blob/main/.github/install-guide.md" target="_blank">Open Source (On-Premises)</a>
  <br/>Download and install Shuffle in your infrastructure.
- <a href="https://shuffler.io/register" target="_blank">Cloud Signup (SaaS)</a>
  <br/>Sign up for Shuffle's cloud-based service and get started quickly. Allows for Multi-Tenant and <a href="https://shuffler.io/legal/privacy_policy#data-location" target="_blank">stores data in a location near you</a>.
- <a href="https://shuffler.io" target="_blank">Hybrid Cloud</a>
  <br/>Use Local Shuffle Agents connected to your Shuffle Cloud Organizations.

**Need help? Check out these resources:**
- **[Training](https://shuffler.io/training)**  
  Access training resources to get up to speed with Shuffle.
- **[Old Training Videos](https://drive.google.com/drive/folders/1MtVfkCXDMSZ9yBwLDiVb0lj1H-oAK5RZ?usp=sharing)**  
  In case you would like to watch older on-demand training videos. The platform however has significantly improved since then and the [current training](https://shuffler.io/training) would be a better match.

## Workflow Development
Workflows run the automated processes in Shuffle by connecting Triggers and Actions/APIs. 

If you want some practice, check out our [default intro to Workflow development](https://github.com/Shuffle/shuffle-docs/blob/master/handbook/engineering/workflow_development.md)

### Finding Usecases
[Usecases are auto-generated workflows](/usecases) that perform a task together. This can be things like handling EDR alerts, doing phishing analysis or using detection rules with Sigma with your SIEM. 

### Finding Workflows
[Workflows](/docs/workflows) connect [Apps](/docs/apps) together to perform an action, typically getting and setting data with API's and using Shuffle's built in tools like Shuffle Tools to modify or format the data. They can be ran and stopped according to your needs, and typically have one starting point and multiple outputs. 

### Finding Apps
[Apps](/docs/apps) are API's or Python scripts, and can be [modified and built by anyone](https://shuffler.io/docs/app_creation). To use an existing public app in a Workflow, you must first activate it. Public apps can be forked, meaning you can have your own version of them.

### Introduction Blogposts
* [1. Introducing Shuffle - an Open Source SOAR platform](https://medium.com/security-operation-capybara/introducing-shuffle-an-open-source-soar-platform-part-1-58a529de7d12)
* [2. Getting started with Shuffle](https://medium.com/@Frikkylikeme/getting-started-with-shuffle-an-open-source-soar-platform-part-2-1d7c67a64244)
* [3. Creating your first app - Virustotal and TheHive](https://medium.com/@Frikkylikeme/integrating-shuffle-with-virustotal-and-thehive-open-source-soar-part-3-8e2e0d3396a9)
* [4. On webhooks and loops - TheHive, Cortex and MISP](https://medium.com/swlh/indicators-and-webhooks-with-thehive-cortex-and-misp-open-source-soar-part-4-f70cde942e59)
* [5. Deploying Shuffle :)](https://medium.com/@stasis_/soar-deploying-shuffle-ad26173525d2)
* [6. Automation with Shuffle SOAR](https://medium.com/@Romser/final-part-configuring-shuffle-soar-28e3674ede22)
* [7. Simplify Your SOAR Implementation with Shuffle](https://medium.com/@socfortress/simplify-your-soar-implementation-with-shuffle-and-seim-integration-d1d32728515e)

### Workflow Principles
1. Variables & nodes
2. JSON autocompletion
3. Loops
4. Nestedloops
5. [Start nodes](https://shuffler.io/workflows/0285a05e-8dc0-4614-840b-88606d6a1e59)
6. Triggers
7. Subflows
8. [App Authentication](https://shuffler.io/workflows/d65d228a-f406-4227-9fa7-f7d9303f8411)
9. Loop filtering
10. [Shuffle File storage](https://shuffler.io/workflows/dd5e3800-2f2e-4089-8055-b500e3b8b349)
11. [Shuffle Datastore (Cache)](https://shuffler.io/workflows/f39a3c37-4f38-4ca0-952a-a9425080b44e)
12. Deduplication
13. [Liquid formatting](https://shuffler.io/workflows/0d604c52-1b3f-49d8-a57e-480baf07ab8d)
14. [HTTP & Rest APIs](https://shuffler.io/workflows/b8a3a70a-f3f9-459f-99b3-7a2723a1a4b8)

### Shuffle 101
- [Learning Startnodes](https://shuffler.io/workflows/0285a05e-8dc0-4614-840b-88606d6a1e59?queryID=5775af43ac103d34ff77f11d27ea5bed)
- [Learning the HTTP app](https://shuffler.io/workflows/b8a3a70a-f3f9-459f-99b3-7a2723a1a4b8?queryID=5775af43ac103d34ff77f11d27ea5bed)
- [Cache Tutorial](https://shuffler.io/workflows/f39a3c37-4f38-4ca0-952a-a9425080b44e?queryID=5775af43ac103d34ff77f11d27ea5bed)
- [File Tutorial](https://shuffler.io/workflows/dd5e3800-2f2e-4089-8055-b500e3b8b349?queryID=5775af43ac103d34ff77f11d27ea5bed)
- [App Authentication](https://shuffler.io/workflows/d65d228a-f406-4227-9fa7-f7d9303f8411?queryID=5775af43ac103d34ff77f11d27ea5bed)
- [Learning Liquid Formatting](https://shuffler.io/workflows/0d604c52-1b3f-49d8-a57e-480baf07ab8d?queryID=5775af43ac103d34ff77f11d27ea5bed)
- [JSON within Shuffle](https://shuffler.io/workflows/ee334515-0224-4a09-af8c-ebc60886f154?queryID=7571057f529c8a4a9aabd5800c0d2b29)

### Shuffle YouTube Videos
**Learn about Shuffle - in-depth**  
Here's a training session we did on Shuffle.

- **00:00 - 00:30**: Introduction to Shuffle and what we're building
- **00:30 - 02:00**: Feature walkthrough of organizations, app creator, and workflows
- **02:00 - end**: Real-time demo, creating use-cases for attendees

[![Shuffle the SOC walkthrough](https://img.youtube.com/vi/PNuXCixYwDc/0.jpg)](https://www.youtube.com/watch?v=PNuXCixYwDc)

## Community Videos

### 1. Understanding Shuffle
Our friends at [OpenSecure](https://www.youtube.com/watch?v=_riaZjLnoXo&t=317s) have created excellent videos to help you learn about Shuffle. Be sure to check them out!

### 2. What is SOAR?
Learn the basics of SOAR (Security Orchestration, Automation, and Response) and how Shuffle fits into this ecosystem.  
**Watch now:** [Shuffle Getting Started - Understanding Shuffle](https://www.youtube.com/watch?v=_riaZjLnoXo)

### 3. Installing Shuffle
Ready to install Shuffle? Follow this step-by-step guide to get Shuffle up and running quickly.  
**Watch now:** [How to Install Shuffle](https://www.youtube.com/watch?v=YDUKZojg0vk)


