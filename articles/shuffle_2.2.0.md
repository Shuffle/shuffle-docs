![Shuffle blog post](https://github.com/user-attachments/assets/9b9e1da8-c063-4c41-bfa5-84b9202c7329)

# Shuffle 2.2.0 – Agents, Security and Staying in Control

Shuffle is on the path to **solve** cybersecurity. While it is a grand task with a moving goal-post, it is exactly the challenge we aim to tackle. In this blog post we give a brief look into how Shuffle is building infrastructure to be able to take care of **any** cybersecurity‑oriented issue you can imagine, whether on‑premises or in public cloud environments, in an easily controllable environment. We delve into a future of possibility, while sticking to real‑world implications rather than pure hype.

## Overview

Shuffle is now capable of everything necessary to build any cybersecurity service, and we are rapidly [working with partners](https://shuffler.io/partners) to make it reality. We are building every feature with a global focus, while keeping relevant controls for on‑prem systems front of mind.

Today we introduce a few new additions that can be tried immediately (links further down):

- **The Security Bundle** – Automatically triages any incident you want, from anywhere. Uses hand-crafted usecases, with a controllable AI Agent in the middle that **CAN** use your tools where you allow it. Oh, and a shiny new UI if you want to dig deeper!
- **AI Agents for your tools** – This is not focused on Shuffle itself. We want all your tools to shine and work well together. Whether cloud, on-prem or otherwise.
- **All apps are MCPs** – Choose one or more apps, and the AI Agent infrastructure will perform actions according to your needs.
- **Modernised Workflow** – A refreshed interface that matches the rest of the platform, giving workflows a cleaner and more focused experience.

## The Security Bundle

In our history, we have gone from **Workflows**, to **Public Workflows**, to **Use Cases** with multiple workflows, and now to the **Security Bundle**.

The Security Bundle has two core parts:

1. Well‑defined security use cases for **any** tool
2. An optional UI to interact with them

![shuffle_2.2.0_0](https://github.com/user-attachments/assets/a75df297-56a4-400a-b426-fdfac45dce67)

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

![shuffle_2.2.0_1](https://github.com/user-attachments/assets/27ebb800-0a67-4139-b20e-9185283ffcea)

Above is a simple flowchart of how it works. Every step is controllable, and you can be a human in the loop in each action if you want to be. Since it is built on top of Workflows, **you are and will stay in control**.

Another important part that requires re-iteration: Everything is already included in Shuffle. With everything being built on top of existing Shuffle infrastructure, it has no additional cost. You decide whether to bring your own model, to use ours, or whether to not use AI at all. A great benefit is that this system can easily be extended into other areas, such as: vulnerability discovery, automatic detection engineering, agentic protection, etc.  

> Public release is planned for **Q2 2026**. Public preview access is already available on [https://shutdown.no](https://shutdown.no) to Shuffle users.

## Controllable [AI Agents and MCPs](https://shuffler.io/docs/AI#ai-agents)

![shuffle_2.2.0_2](https://github.com/user-attachments/assets/f5a2d3de-a6a4-4f2d-8928-0fc427c3e45e)

We have been [building and implementing narrow AI since early 2022](https://github.com/Shuffle/MetaMitre), when we were only a team of 3, and built a Mitre Attack tactics parser from any type of data. We are still huge advocates of narrow AI, and know it will be an important facet to the future. 

For now, with the pace at which LLMs are improving, they have taken center stage. Shuffle is always looking to bring native capabilities rather than "chatbots", but have been experimenting with all of it since our first [Shuffle-GPT release in 2023](https://shuffler.io/chat). This project will soon been sunset, as to release the now new, [transparent, controllable, open source version version of our agent](https://shuffler.io/agents).

We have written our own Agentic algorithm, and made it work natively with all our apps and runtime locations, allowing it to run anywhere you may want it to, within the secure execution environment of Shuffle. 

When we first released our Agent system in late 2023, we quickly learned where it needed to improve:
- On-prem support was limited due to vendor lock-in (control & customisation)
- It lacked transparency (black-box behavior)
- It struggled with real-world, multi-step tasks (chained events & reasoning)

![shuffle_2.2.0_3](https://github.com/user-attachments/assets/b575903e-aece-4876-bf36-ae372643ef55)

But a lot has changed since then. Models have gotten better. Our team has gotten better and larger. It is now possible to control and understand what is happening. And with that, we are releasing the public beta version of our controllable, distributed agent system to the world. It is [A2A](https://a2a-protocol.org/latest/) & [MCP compatible](https://modelcontextprotocol.io/docs/getting-started/intro) for multi-agent actions. By default it has very little permissions, and it is entirely controlled based on your apps, actions and authentication. These "permissions" are treated as actions that the agent can access, which is how our MCP API works. In turn, this makes every single app into an MCP server. The better defined the app and its actions are, the better it works. 

![shuffle_2.2.0_4](https://github.com/user-attachments/assets/89df14c0-a8e4-4b97-8e37-2d7381994ed1)

With MCPs and agents becoming more capable however, we are rapidly running head-first into a big problem. A lot of organisations want to replace the **predictability of code** with the **simplicity of agents** doing their job for them. And that makes sense, as it makes the current job faster. It does however have drastic pitfalls; it makes the job itself **semi-random and slow**. 

And we have a solution to this that is being released later this year. 

![shuffle_2.2.0_5](https://github.com/user-attachments/assets/72c2c713-965c-4c99-aea9-baf539f987de)

Read more about the technical implementation in our [GitHub release notes](https://github.com/Shuffle/Shuffle/releases/tag/v2.2.0)

## The Workflow Builder

![shuffle_2.2.0_6](https://github.com/user-attachments/assets/16c1d0c8-0638-462f-aa63-fe13453cde2a)

Back in the 2.0 release, we remade most pages. The work did not extend to the Workflow Builder at the time, which is core to Shuffle. The reason we started elsewhere is due to the complexity of this one UI as opposed to all others. The main goals of the workflow builder is is two-fold:

1. **Control** – Full visibility and configuration capability
2. **Debugging** – Clear understanding of failures and how to fix them

Keeping these goals in mind, we started thinking about the user experience of building a workflow, and how to improve it. Through this process we discovered two different users with different motives:

- New users typically struggle finding WHAT to do
- Experienced users could struggle with complex debugging

And so we focused on these ruthlessly. We are striving to improve user experience for new users, while retaining complex capabilities for experienced users. Questions like "Horizontal or Vertical building?", "Does free-flow workflows help you build?", "How many steps should be built at once?" are all commonplace. [We want your feedback as well](https://shuffler.io/contact?category=technical_question). 

The answer to all of the above-mentioned questions was always hard to figure out. But we are building the path, and you can now see parts of the solution.

![shuffle_2.2.0_7](https://github.com/user-attachments/assets/7547ac68-d03e-40ab-bfe8-f96e6028667f)

Another larger, common issue has to do with inputs & testing. Experienced users tend to build in this order:

1. Add an app
2. Configure and test it
3. Go back to 1 for the next node

While a new user tends to struggle with the very concept of what to build. So they tend to pull in "Actions" without thinking about why it is the right thing to do. And so it turns into:

1. Add an app
2. Add another app
3. Add another app
4. …
5. Start testing once "done"

![shuffle_2.2.0_8](https://github.com/user-attachments/assets/7366899b-621e-4244-8548-c4ffe9a32dc0)

Our solution is to incentivise you into testing each node, by making it more obvious than before. These tests run the current node based on data from a previous execution, meaning it has real data, but is still fast and testable as it does not have to run all the nodes at once.

The generalised AI Agent and Security bundle solves this further, as new users tend to want simplicity and solutions first, before getting into the complexity of manual building. 

v2.2.0 [release is live](https://shuffler.io), see the [GitHub release notes](https://github.com/Shuffle/Shuffle/releases/tag/v2.2.0) for full technical details.

## What It Means for You

This release has no direct impact on existing, running automation. The Security Bundle and general Agents are all in public preview, but we wanted to release it early to gather feedback. These additions are direct upgrades to how Shuffle can and will be used, rather than optimisation of what the product itself does today. We are very focused on backwards compatibility, and are and will keep improving the Workflow system with relevant capabilities. 

We recommend upgrading if you are in any of these camps:

- Looking for [easier building and debugging of workflows](https://shuffler.io/workflows/31d1a492-9fe0-4c4a-807d-b44d9cb81fc0?queryID=96afca0c5a232b1c8114d4bc07f60ee7)
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
