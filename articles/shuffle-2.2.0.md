![Shuffle blog post](https://github.com/user-attachments/assets/9b9e1da8-c063-4c41-bfa5-84b9202c7329)

# Shuffle 2.2.0 – Agents, Security and Staying in Control

Shuffle is on the path to **solve** cybersecurity. This is a grand task with a moving goal‑post, but a task we aim to achieve. In this blog post we give a brief look into how Shuffle is building infrastructure to be able to take care of any cybersecurity‑oriented issue you can imagine, whether on‑premises or in public cloud environments, in an easily controllable environment. We delve into future possibilities, while sticking to real‑world implications rather than pure hype.

---

## Overview

Shuffle is now capable of everything necessary to build any cybersecurity service, and we are rapidly working with partners to make it reality. We are building every feature with a global focus on the controls required for on‑prem systems front of mind.

Today we introduce a few new additions that can be tried immediately(links further down):

- **The Security Bundle** – Automatically triages any incident you want, from anywhere. Uses hand-crafting usecases, with a controllable AI Agent in the middle that **CAN** use your tools where you allow it. Oh, and a shiny new UI if you want to dig deeper!
- **AI Agents for your tools** – This is not focused on Shuffle itself. We want all your tools to shine and work well together. Whether cloud, on-prem or otherwise.
- **All apps are MCPs** – Choose one or more apps, and the AI Agent infrastructure will perform actions according to your needs.
- **Modernised Workflow** – A refreshed interface that matches the rest of the platform, giving workflows a cleaner and more focused experience.

---

## The Security Bundle

In our history, we have gone from **Workflows**, to **Public Workflows**, to **Use Cases** with multiple workflows, and now to the **Security Bundle**.

The Security Bundle has two core parts:

1. Well‑defined security use cases for **any** tool
2. An optional UI to interact with them
   
![UI_interact](https://github.com/user-attachments/assets/08460558-2688-4605-92b0-942ad2033066)

It is built entirely on features already present in Shuffle, including workflows, datastore, file management, AI Agents, detection pipelines, and more. Most importantly: **you are in control**. We have built it based on our own and the community's expectation of easy to set up security, which is exactly what we deliver. 

Here are some of the starter usecases we have built (with a lot more to come):

1. **Handle alerts, detections or incidents from anywhere, automatically.**
   - The goal is to give you the option to auto-solve these cases, if you want. Shuffle only knows what to do based on which ones of your tools it has been given access to, but we have decided to focus on the basics first: Email (phishing), SIEM, EDR & Cloud platforms. 

2. **Automatic threat intel with your provider**
   - A large portion of the security industry focuses on threat lists. It is a starting point, but not a solution. We integrate with 100+ threat intel platforms already, and have built systems to interact with these within the Incident system. We are actively working to get partners as well, as to bring this increased visibility to you.

3. **Controllable response actions**
   - You can enable/disable actions easily in the sidebar accessible directly in the UI. 
   - For now, the system is VERY passive. What that means is Shuffle will often make tasks rather than do them, as there is a large amount of cases where destructive actions may occur.

4. **Detection at scale**
   - Since Shuffle can ingest and handle tickets, why not also have our own detection mechanism? We can! That is what the Data Pipeline system has been built for, and Shuffle can now ingest logs and run Sigma rules on them. More to come in 2026.

![infographic](https://github.com/user-attachments/assets/3bb54d86-5397-4419-95ed-00094c415d45)

Above is a simple flowchart of how it works. Every step is controllable, and you can be a human in the loop in the agent actions if you want to be. Since it is built on top of Workflows, you are and will stay in control.

Another important part that requires re-iteration: Everything is already included in Shuffle. Since everything is built on top of existing infrastructure, it has no additional cost. You decide whether to bring your own model, to use ours, or to not use AI at all. A great benefit is that this system can be extended into other areas, such as: vulnerability discovery, automatic detection engineering, and agentic protection.  

> Public release is planned for **March 2026**. Beta access is available by contacting **support@shuffler.io**.

---

## Controllable AI Agents and MCPs

![ai agent chat](https://github.com/user-attachments/assets/54853cdc-37f4-46ac-a130-a96b3e25b32c)

We have been building and implementing AI since 2022, when we were only a team of 3, and built a Mitre Attack tactics parser from any type of data. We are still huge advocates of such narrow AI, and know it will be an important facet to the future of what we do. 

For now however, with the pace at which LLMs are improving, they have taken center stage, however silly they can be when badly utilized. Shuffle is always looking to bring native capabilities rather than "chatbots", but have been experimenting with all of it since our first Shuffle-GPT release in 2023. This project has since been sunset, as to release the now new, transparent, controllable, open source version.

We have written our own Agentic algorithm, and made it work natively with all our apps and runtime locations, allowing it to run anywhere you may want it to, in a secure execution environment. 

When we first released our Agent system in late 2023, we quickly learned where it needed to improve:
- On-prem support was limited due to vendor lock-in (control & customisation)
- It lacked transparency (black-box behavior)
- It struggled with real-world, multi-step tasks (chained events)

![security_bundle](https://github.com/user-attachments/assets/aa2ec29b-5fcc-447b-b5a6-829a971f41b4)

But a lot has changed since then. Models have gotten better. Our team and resources have grown. It is now possible to control and understand what is happening. And with that, we are releasing the beta version of our controllable, distributed agent system to the world. It is A2A compatible for multi-agent actions. By default it has very little permissions, and it is entirely controlled based on authentication you have put in place. These "permissions" are treated as actions that the agent can access, which is how our MCP API works. In turn, this makes every single app into an MCP server. The better defined the app and its actions are, the better it works. 

![security_bundle1](https://github.com/user-attachments/assets/47ac2e6e-b8d0-410f-9d33-017e6c5b5051)

With MCPs and agents becoming more capable however, we are rapidly running head-first into a big problem. A lot of organisations want to replace the **predictability of code** with the **simplicity of agents** doing their job for them. And that makes sense, as it makes the current job faster. It does however have drastic pitfalls; it makes the job itself **semi-random and slow**. 

And we have a solution to this that is being released later this year. 

![ai_agent](https://github.com/user-attachments/assets/07606763-b803-4cf3-bab0-04fafa72862c)

---

## The Workflow Builder

![Workflow_Builder](https://github.com/user-attachments/assets/c4882f6e-8bb9-4b1d-84d5-47d3071283b3)


In the 2.0 release, we remade most pages. The work did not extend to the Workflow Builder however, which is core to Shuffle. The reason we started elsewhere is due to the complexity of this one UI as opposed to all others. The main goal of the workflow builder is is two-fold:

1. **Control** – Full visibility and configuration
2. **Debugging** – Clear understanding of failures

With these two in mind, we started thinking about the flow of building a workflow, and how to improve it. Through it we discovered that two different users have different motives:

- New users typically struggle finding WHAT to do
- Experienced users had some trouble with complex debugging

And so we focused on these ruthlessly. We are striving to improve user experience for new users, while retaining complex capabilities for experienced users. Questions like "Horizontal or Vertical building?", "Does free-flow workflows help you build?", "How many steps should be built at once?".

The answer to all of these was always hard to decide. But we are building the path, and you will see parts of the solution in this release.

![workflow_ui](https://github.com/user-attachments/assets/f4ec2c9d-8510-4f2a-8f58-f59bfdd18579)

Another issue has to do with inputs & testing. Experienced users tend to build in this order:

1. Add an app
2. Configure and test it
3. Go back to 1 for the next node

While a new user tends to struggle with the very concept of what to build. So they tend to pull in "Actions" without thinking about why it is the right thing to do. And so it turns into:

1. Add an app
2. Add another app
3. Add another app
4. …
5. Start testing once "done"

![test_action](https://github.com/user-attachments/assets/fa443ab8-e304-4e61-88d2-418a8103f936)

Our solution is to incentivise you into testing each node, by making it more obvious than before. These tests run the current node based on data from a previous execution, meaning it has real data, but is still fast as it does not have to run all the nodes at once.

The generalised AI Agent and Security bundle solves this further, as new users tend to want simplicity and solutions first, before getting into the complexity of manual building. 

---

## What It Means for You

This release has no direct impact on existing, running automation. The Security Bundle and general Agents are all in public beta, where the release of Shuffle 2.2 is to make it available to you early on. These additions are direct upgrades to how Shuffle can and will be used, rather than optimisation of what the product does itself. We are very focused on backwards compatibility, and are and will keep using the Workflow system. 

We recommend upgrading if you are in any of these camps:

- Looking for easier building and debugging of workflows
- Wanting to [try the AI Agent and MCP system(s)](https://shuffler.io/agents)
- Wanting to [try the security bundle](https://security.shuffler.io/)

If you are not, then there is no benefit to upgrading at the moment. You can however spin it up in a test environment easily, and see if it has what you may be looking for. Our suggested ways to try it out are the following:

- **SaaS**: https://shuffler.io
- **[Google Cloud Platform](https://console.cloud.google.com/marketplace/product/shuffle-public/shuffle?q=search&referrer=search&project=shuffler)** – Self‑hosted deployment
- **AWS** – Coming soon
- **Azure** – Coming soon

## Wrapping Up

There is a lot to come. This release is the first bite of an exciting future. Shuffle infrastructure is now ready to tackle the wide new world of cybersecurity of 2026, and we will be sharing updates in the coming weeks and months, both technical and informative.


If you have questions or feedback, reach out directly or contact the support team. Our goal is to work with **100 new partners in 2026**, and we are incredibly excited about what’s ahead.

**Fredrik**  
Founder & Technical Lead
