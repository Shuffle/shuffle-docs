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

**This is in Beta and is not generally available yet.**

## Workflow Generation
AI Workflow generation is a great starting point.

1. Go to the **Workflows** page.
2. Click **Create Workflow**.
3. Describe your workflow in natural language.
4. Click **AI Generate**.
5. The AI-generated workflow will appear. You can use it as is or modify it if needed

<img width="785" height="787" alt="AI_generate_page" src="https://github.com/user-attachments/assets/c756caf1-a32b-4b56-bd5a-81fc2ec879dd" />

## Self-Hosting models

For the open-source version, you need to provide details about your self-hosted AI model.

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
