# mcp-azure-ai-agent-grounding-bing

# How to create an agent within Azure AI Foundry that includes both MCP and Grounding with Bing as integrated tools.

## 🎯 Overview

This repository explains how to connect to an agent deployed on Azure AI Foundry using the **Model Context Protocol (MCP)** and utilize the **Grounding with Bing Search** tool.

- The agent can retrieve real-time information using web search (Grounding with Bing Search).
- MCP allows integration between agents and your own servers or services.

On June 27th, 2025, Microsoft announced MCP support for the Azure AI Foundry Agent Service.\
This repository also shows how to configure and run an agent with tools such as **Grounding with Bing** and **Code Interpreter**.

🔗 [Official Announcement Blog (June 27, 2025)](https://devblogs.microsoft.com/foundry/announcing-model-context-protocol-support-preview-in-azure-ai-foundry-agent-service/)\
🔗 [Available Tools (Microsoft Docs)](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/tools/overview)

---

## 📆 Prerequisites

To use this repository, you need the following environment:

- An Azure subscription (with at least Contributor permission)
- An Azure AI Foundry Agent Service resource
- A **Grounding with Bing Search** resource (created within the same subscription and resource group)
- Azure CLI installed and logged in (`az login`)
- The following roles assigned to the project:
  - Azure AI User
  - Azure AI Project Contributor (required to create agents)

> 📋 For instructions on creating Azure AI Agents, refer to the [official documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/tools/overview).

---

## 🔧 Environment Variable Setup

Create a `.env` file at the root of your project and include the following content:

```env
# Required for MCP connection
AZURE_PROJECT_ENDPOINT=YOUR_AZURE_PROJECT_ENDPOINT
BING_CONNECTION_ID=YOUR_BING_CONNECTION_ID
AZURE_AGENT_ID = YOUR_AGENT_ID
```

---

## 🧩 Scripts Overview

This repository contains two primary Python scripts:

- **`create-agent.py`**  
  This script is used to **create a new agent** in an existing Azure AI Foundry project. It registers the agent with selected tools such as Bing Search, Code Interpreter, etc.

- **`get-agent.py`**  
  This script is used to **send requests to an already created agent**. It connects to the existing agent using its ID and allows interactions via the MCP interface.

Be sure to correctly configure your `.env` file before running either script.
