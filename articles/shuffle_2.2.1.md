# Shuffle v2.2.1

This is a minor release to tackle some of the bugs that came with 2.2.0, with some minor fixes and licensing changes (more access!).

## What changed

### Orborus - sensor mode & sensor groups

Shuffle has always been beholden to 3rd party software to handle response actions. That is no longer required. Orborus now supports “sensor mode”, extending the already existing Runtime Location system to run workflows on-premises. 

This has the focus on three important security-aspects:

- Compliance (simple checks)
- Vulnerabilities (shadow agents, software updates & code repositories)
- Response Actions (Controlled scrip or full RCE)

These actions use Workflows in Shuffle to perform checks, meaning you stay in control of what checks happen. You can [try it out in Shuffle Security](https://security.shuffler.io/monitors) (whether self-hosted or otherwise).

<img width="512" height="152" alt="image" src="https://github.com/user-attachments/assets/a2794b65-9dbe-4a3b-80f8-cc2e024e4bf8" />


### Workflow sync while importing from remote repository

When syncing workflows from Azure DevOps or GitHub, you can now see the list of available workflows before importing them. Workflows already in Shuffle can be re-synced from a different environment. New ones can be imported from Azure DevOps or GitHub.

This has been built in order to make CI/CD control of workflows at scale work better in multi-tenant environments, and helps a tremendous amount with workflow branching.

<img width="512" height="262" alt="image" src="https://github.com/user-attachments/assets/c806bfc0-8112-42a3-9ee6-a97d5c87a2fc" />


### Usage limits are now measured in app runs

Open-source deployments now get 25,000 app runs per month instead of the previously lower workflow-run cap. App runs are a more accurate measure of what a workflow actually does.

When you hit the limit, executions don't stop. They throttle to 1 workflow execution per minute until the counter resets on the 1st of the following month. Burst throughput is what gets limited; steady-state automation keeps running.

We expect this to be sufficient for most environments, with the goal being of finding the right sweet-spot that prevents abuse by large vendors. 

### Marketplace availability

Shuffle is now listed on the [AWS Marketplace](https://aws.amazon.com/marketplace/pp/prodview-typ7upg6kwntk) and [Google Cloud Marketplace](https://console.cloud.google.com/marketplace/product/shuffle-public/shuffle).

[![AWS Marketplace](https://github.com/user-attachments/assets/250e00d7-2a23-4b4e-95e1-5db4db1f7864)](https://aws.amazon.com/marketplace/pp/prodview-typ7upg6kwntk)

[![Google Cloud Marketplace](https://github.com/user-attachments/assets/37858273-eaeb-42a9-b228-a425026ca82d)](https://console.cloud.google.com/marketplace/product/shuffle-public/shuffle)

## Reliability and performance:

- More consistent workflow execution states (fewer cases where a workflow finishes but the UI shows it as still running, or vice versa).
- Better handling of long automation chains where intermediate steps could occasionally drop context.
- Reduced backend load under high concurrency, mainly relevant for larger deployments.
- A handful of UI fixes missing icons, inconsistent execution status displays, a few places where workflow state didn't update without a refresh.

## Full changelog:

[Shuffle v2.2.1 on GitHub](https://github.com/Shuffle/Shuffle/releases/tag/v2.2.1)
