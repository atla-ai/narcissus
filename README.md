# Atla Narcissus

## Overview

**Narcissus** is a _public_ demo system designed to serve multiple purposes:

1. Serve as an agentic tool that potential customers can use to learn more about Atla and hopefully convert to customers.
2. Provide an agent instrumented with Atla Insights which populates a public demo account.

> [!TIP]
> This demo account can be accessed at https://app.atla-ai.com/app/narcissus.

## Project Structure

The project is organized into the following directories:

- `python-agent`: The LangGraph Python agent implementation, adapted from the [LangGraph starter agent](https://langchain-ai.github.io/langgraph/agents/agents/).

- `ui`: The Next.js UI for the chatbot, adapted from the [LangGraph Agent Chat UI](https://github.com/langchain-ai/agent-chat-ui)

- `widget`: A Webflow widget for the chatbot used to deploy the chatbot to the Atla website.

## Development

### Python Agent

Run the LangGraph server locally:

1. Install dependencies:

```bash
cd python-agent
uv sync
```

2. Run the development server:

```bash
langgraph dev --no-browser
```

The server will be available at http://localhost:2024.

### UI

1. Install dependencies:

```bash
cd ui
pnpm install
```

2. Run the development server:

```bash
pnpm dev
```

The UI will be available at http://localhost:3000.

### Widget

1. Make sure both the Python agent and the UI are running.

2. Open the `widget/chat-widget.html` file in your browser.
