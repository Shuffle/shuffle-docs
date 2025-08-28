# AI at Shuffle

With AI becoming a larger part of the Automation space, the goal with AI at Shuffle is provide it in a controllable and responsible way. We do not intend to implement chat systems - just to make certain mechanisms in Shuffle easier to use over time.

## Using LLMs 
Shuffle by default provides LLM credits using the OpenAI GPT-5-mini model. This is available to a certain level to those who use our Cloud or Hybrid offerings. [Read about self-hosted models](#how-to-set-up-a-self-hosted-ai-model-with-shuffle).

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

1. A Server to Run the AI: You need a computer that Shuffle can reach over the network. This can be a VM, physical server or a cloud instance.
2. We recommend Ollama as the simplest way to run local AI models. Go to [Download Ollama](https://ollama.com/download) to install it on your server. After installation, make sure the Ollama service is running.
3. Once Ollama is installed, you need a model for it to serve. For a great starting point, we recommend the gpt-oss model. It's a powerful and versatile model perfect for general tasks. (You can read more about it in Ollama's official announcement [here](https://ollama.com/blog/gpt-oss)). Of course, you can use any model available on Ollama. Our gpt-oss suggestion is just a recommendation to make getting started easy.


Open your server's terminal and run this command:

```bash
ollama run gpt-oss:20b
```

### Setting Up Environment Variables in Shuffle

Once your self-hosted AI model is running, you can proceed with setting up the necessary environment variables in Shuffle.

**Step 1: Find Your AI Server Details**

You will need the following information from your self-hosted AI server:

* The full URL of the API (e.g., http://192.168.1.55:11434/v1).
* The exact name of the model you want to use (e.g., llama3).
* An API key (if your server requires authentication).

**Step 2: Set the Environment Variables**

`OPENAI_API_URL` (Required)

* What it is: The full URL to your AI server's API endpoint.

Example: 
```bash
OPENAI_API_URL=http://localhost:11434/v1
```

`AI_MODEL` (Required)

* What it is: The exact name of the model you want Shuffle to use.

Example:
```bash
AI_MODEL=llama3
```

OPENAI_API_KEY (Optional)

* What it is: The API key or token if your server requires authentication.

Example:
```bash
OPENAI_API_KEY=sk-mysecretkey123
```


Shuffle can support any self-hosted model that implements the OpenAI API interface. Examples include Ollama, local LLMs wrapped with OpenAI-compatible endpoints, or any other model that exposes the same API.

Once these are set, there is no need to restart your Shuffle backend server as the checks happen in real-time. The AI features will be automatically enabled, allowing you to use them immediately.

**Note: You need to refresh the Shuffle UI page in your browser for the new AI features to appear.**


### Troubleshooting

* Ensure your AI server is running and reachable at the URL you provided.
* If using authentication, double-check the API key.
* Use the exact model name available on your self-hosted AI instance.
