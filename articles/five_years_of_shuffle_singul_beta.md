![Shuffle Turns 5 years old](https://github.com/user-attachments/assets/15c8f9dd-ede6-4458-adc7-8e6783de4354)

# Introducing Singul - 5 Years of Open Source at Shuffle
May 20th 2020, [we introduced Shuffle](https://medium.com/shuffle-automation/introducing-shuffle-an-open-source-soar-platform-part-1-58a529de7d12). It was welcomed with open arms and filled a real need in cybersecurity - namely to allow non-developers to connect their tools in magical ways without having to pay hundreds of thousands of dollars for a blackbox. Now, 5 years later, our key R&D initiative Singul is getting ready for the public. This post will cover how Singul solves one of the key problems we've had with Shuffle - namely the use of data standards. 

---

## What is Singul?
The idea for Singul stems back to [before Shuffle was built](https://github.com/Shuffle/shuffle-shared/blob/3f630b0bd668c56c1d4f7d0e4d3593c5fcc864da/structs.go#L743), and has the goal of helping you use your tools even more easily. The idea behind our creations at Shuffle has always been to help companies in the cybersecurity industry collaborate with each other. The question is however; how do we actually do that? Well, we started with automation. 

**Why automation?** Because automation is to have tools connect to each other, and use each others' information. 

**Connect how?** Usually API's.

Doesn't Shuffle already do that though? Isn't that the whole point? Well, yes. Shuffle is a Workflow editor and runner. It CAN do everything we have talked about here. There is however one big issue: the Data that flows through Shuffle isn't standardised. With 2500 apps (so far), and all of them being capable of connecting to each other in unique ways, this turns into 2500*2500 -> 6.250.000 permutations. And this is without counting each action in every API. 

**So.. Singul?** Yes. 

We were looking for a solution to our own permutation problem. It is (in short) an API translator, which makes it easy to talk to any third party API, from a single API. But how does that actually help? If the problem is to move data around "correctly", how does just simplifying to a single API help? 

## Standards

![An early test UI for the idea of Singul](https://github.com/user-attachments/assets/b8a5a8ca-75a7-48fd-a627-138a5ef0d64b)

Standards are huge. Huge for grassroots efforts. Huge for company collaborations. They allow everyone to work together at a way larger scale. They are the frameworks and data structures we can all use collaboratively to get expected outputs. 

How about in security? What kind of standards to we work with? Among others, here are some standard examples the team at Shuffle has been consistently working towards:

* OpenAPI: [API standardization](https://shuffler.io/apps?tab=all_apps)
* CACAO: [Playbook standardization](https://github.com/shuffle/cacao)
* Sigma: [Detection Rule standardization](https://shuffler.io/docs/extensions#detection-manager)
* STIX: [Threat Intelligence standard](https://github.com/Shuffle/standards/tree/main/translation_standards)
* OCSF: [Security Finding standardization](https://github.com/Shuffle/standards/tree/main/translation_standards)
* And more :)

![An example of how standards are used in Singul for automatic translation](https://github.com/user-attachments/assets/7edd57d7-ac4c-4b3b-8ac2-8dc062331487)

The latter two has our focus through Singul. Here is one way we are implementing them:

* Shuffle now has a "one-click" connect to start ingesting tickets into Shuffle's Datastore ticketing system. This happens through Singul, which works as follows:

1. You click the "Ingest Tickets" button for your ticketing/edr/siem
2. We generate a workflow in the background which looks for new tickets through Singul every minute
3. Singul sends a request to your ticketing system
4. The new tickets are translated into OCSF (or any other standard you want) and put into Shuffle's Datastore system in the "Tickets" category.

---

From the Shuffle side; why does this help? A few reasons: 
* You now have a workflow that by default ingests alerts for you in one click. Which can be modified and controlled. 
* You now have a place where all tickets are ingested in a single format, no matter where they are from
* Shuffle 2.1.0 will support Datastore triggers. This means we can run another workflow from the OCSF tickets. 

Singul was made to remove the necessity for workflow creation for basic tasks

## Why now?

![Input translation in Singul. CLI translated to correct API request](https://github.com/user-attachments/assets/793b895c-eeee-4a1a-b8d3-14d7c4587e98)

Shuffle itself has a need for it. The basics of how to connect tools shouldn't be as hard as it is at the moment. The missing piece has been the translator from source data to some standard. Singul is just a smarter translator to make API requests easy to use, and deterministic. It uses reasoning models for the first translation(s) and validation, and subsequently saves the background data. It is based on standard translations, and is deterministically controllable. Due to needing it ourselves, while also seeing a huge gap in the market of integration management for exactly this, we decided to make it a reality. 

We are additionally open sourcing it to be ran locally. We used it in-house for quite a while already, and are now looking for public feedback on the product. We are also very intrigued by what people will be capable of doing with it, as it removes the limits of needing to know how to use APIs directly. It is available in a few important ways:

* **Singul CLI**: For implementing it however you want. The CLI has been built into the Singul Python API as well, meaning it's easy to implement for developers: singul <action> <app> --param1=value1
* **Singul in Shuffle Workflows**: This is where it started, and how we will keep optimising it. This will hopefully make it more achievable to automate both the simple and the complex. 

![Singul in Shuffle Workflows. Makes it easy to swap between tools and actions.](https://github.com/user-attachments/assets/222e82cc-4054-4a25-8221-33ed082581d6)

* **Singul Public API**: [https://singul.io](https://singul.io). This is based on how we use it for Shuffle. We store apps, configurations and everything else within Shuffle itself, with Singul's API being more and more fleshed out over time. You have full visibility into every single translation and attempted app run. This is based on the Integration Layer API in Shuffle, meaning Open Source instances of Shuffle has Singul built-in (from 2.1.0). 
* **Singul for AI Agents**: Shuffle is developing a fully Open Source AI Agent system. Singul is our first implementation of it, as the data between tools are standardised. It is already used in multiple MCP's for other agents as well. More on this to come :)

![Timelines for AI Agents with Singul](https://github.com/user-attachments/assets/cdac4e33-1cc9-4fb3-8888-ec9ab9e183d9)

## Celebrating 5 years

With this beta release of Singul, and the AI release of Shuffle to come (2.1.0), the future is looking like a lot of fun. A lot can happen in five years, and I think we have made a lot of the right decisions - both for the cybersecurity industry, as well as for ourselves. I have seen random people using Shuffle at cafes, at schools and at the library, and nothing makes me more excited than seeing that what I've made has an impact. It's used by governments, prestigious universities and security companies alike. And I believe publishing Singul to the masses is another step on that same path Shuffle has started paving, and that it will have as big an impact, if not bigger.

---

To try out Singul for yourself, please feel free to go to the Github repository, or use singul.io to learn more about how you can use it.

[GitHub - Shuffle/Singul](https://github.com/shuffle/singul)

Thanks to the Shuffle team, our contributors, customers, and Shuffle community and everyone else! It's been a fun ride - let's make the next five even better ❤
