# AI at Shuffle

With AI becoming a larger part of the Automation space, the goal with AI at Shuffle is provide it in a controllable and responsible way. We do not intend to implement chat systems - just to make certain mechanisms in Shuffle easier to use over time.

## Using LLMs 
Shuffle by default provides LLM credits using the OpenAI GPT-5-mini model. This is available to a certain level to those who use our Cloud or Hybrid offerings. [Read about self-hosted models](#self-hosted-models).

## Singul
Singul works against vendor-locking with our translator for different providers of the same tools, such as Slack vs Teams vs Discord, or Splunk vs Elastic vs QRadar). It uses LLMs to understand the context of what you are trying to perform, and makes a determinsitic translation to use a standard such as OCSF or STIX. This is a powerful way to avoid vendor lock-in, and to make your automation more future-proof. Made by the Shuffle team.

Read the [usage Shuffle Docs here](https://github.com/Shuffle/openapi-apps/blob/master/docs/singul.md)
Website: [https://singul.io](https://singul.io)

## AI Agents
Agents are a way to have an AI model interact with the world. In Shuffle, this means using tools (playbooks) to perform actions. We intend to provide controllable, deterministic Agents that can be used to perform tasks.

**Some areas has been built for:**
- Tool Usage  (Collection, Enrichment, Detection & Response)
- Reasoning   (Helps with workflow building)
- Correlation (Historical alerts and cases)
- RAG         (Docs: Knowledge base usage)

They can additionally talk to each other and be published for third party use. 

**This is in private Beta and is not generally available yet. If you would like to try it, please reach out to support@shuffler.io and ask about AI Agents.**

## Workflow Generation
AI Workflow generation is a great starting point.

1. Go to the **Workflows** page.
2. Click **Create Workflow**.
3. Describe your workflow in natural language.
4. Click **AI Generate**.
5. The AI-generated workflow will appear. You can use it as is or modify it if needed

<img width="785" height="787" alt="AI_generate_page" src="https://github.com/user-attachments/assets/c756caf1-a32b-4b56-bd5a-81fc2ec879dd" />

## How to set up a Self-Hosted AI Model with Shuffle

While Shuffle's Cloud platform provides AI credits to get you started, connecting your own self-hosted AI model gives you ultimate control and flexibility. This guide will walk you through the process.

**Before you configure Shuffle, please ensure you have the following ready:**

* 1 A Server to Run the AI: You need a computer that Shuffle can reach over the network. This can be a VM, physical server or a cloud instance.
* 2 Ollama Installed and Running: We recommend Ollama as the simplest way to run LLMs. Make sure it's installed and the service is running. You can find 


For the open-source version, you need to provide details about your self-hosted AI model. If you haven't done this before, we recommend looking into [Ollama with the OpenAI gpt-oss model](https://ollama.com/blog/gpt-oss).

[Ollama installation](https://ollama.com/)

### Environment Variables

```bash
# URL of your AI server (required for self-hosted models)
OPENAI_API_URL=http://localhost:11434/v1

# API Key (optional if authentication is enabled)
OPENAI_API_KEY=myapikey

# Model to use (required)
AI_MODEL=your-model-name
```

Shuffle can support any self-hosted model that implements the OpenAI API interface. Examples include Ollama, local LLMs wrapped with OpenAI-compatible endpoints, or any other model that exposes the same API.

Once these are set, start your Shuffle backend server. The AI features will be automatically enabled, allowing you to use AI features.


### Troubleshooting

* Ensure your AI server is running and reachable at the URL you provided.
* If using authentication, double-check the API key.
* Use the exact model name available on your self-hosted AI instance.
