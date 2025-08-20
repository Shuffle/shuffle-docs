# Shuffle AI Features

## Overview

Shuffle now includes AI-powered workflow generation. This allows you to quickly create workflows by simply describing them in natural language. The AI will generate the workflow steps automatically.

Whether you're using the cloud version or the open-source self-hosted version, the workflow AI feature works the same way from the user's perspective.

## Using AI Workflow Generation

1. Go to the **Workflows** page.
2. Click **Create Workflow**.
3. Describe your workflow in natural language.
4. Click **AI Generate**.
5. The AI-generated workflow will appear. You can use it as is or modify it if needed

<img width="785" height="787" alt="AI_generate_page" src="https://github.com/user-attachments/assets/c756caf1-a32b-4b56-bd5a-81fc2ec879dd" />

## Setting Up AI for Open Source / Self-Hosted Shuffle

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


## Troubleshooting

* Ensure your AI server is running and reachable at the URL you provided.
* If using authentication, double-check the API key.
* Use the exact model name available on your self-hosted AI instance.
