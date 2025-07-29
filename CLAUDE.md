# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Narcissus is a dual-component system consisting of:
1. **Python Agent** (`python-agent/`): A LangGraph-based AI agent using OpenAI's GPT-4o-mini
2. **UI Frontend** (`ui/`): A Next.js chat interface for interacting with LangGraph agents

The Python agent creates a simple chatbot workflow, while the UI provides a production-ready chat interface with artifact rendering capabilities.

## Development Commands

### Python Agent (python-agent/)
- **Install dependencies**: `uv sync` or `pip install -e .`
- **Run development server**: `uv run dev` or `langgraph dev --no-browser` (starts local LangGraph server on port 2024)
- **Lint**: `ruff check .`
- **Format**: `ruff format .`
- **Type check**: `mypy .`
- **Test**: `pytest`

### UI Frontend (ui/)
- **Install dependencies**: `pnpm install`
- **Development server**: `pnpm dev` (runs on port 3000)
- **Build**: `pnpm build`
- **Production server**: `pnpm start`
- **Lint**: `pnpm lint` or `pnpm lint:fix`
- **Format**: `pnpm format` or `pnpm format:check`

## Architecture

### Python Agent Structure
- `src/narcissus/agent.py`: Main agent implementation with `create_agent()` function
- Uses LangGraph's StateGraph with MessagesState for chat workflow
- Single "chatbot" node that processes messages through OpenAI's API
- Configuration defined in `langgraph.json` with graph ID "agent"

### UI Structure
- Built on Next.js 15 with TypeScript and Tailwind CSS
- Uses LangGraph SDK for agent communication via API passthrough
- Key components:
  - `src/app/api/[..._path]/route.ts`: API proxy to LangGraph server
  - `src/components/thread/`: Chat interface components
  - `src/providers/`: Stream and Thread context providers
- Supports artifact rendering in side panel
- Environment variables for production deployment configuration

## Environment Configuration

### Python Agent
- Requires `.env` file with OpenAI API key: `OPENAI_API_KEY=your_key_here`

### UI
- `NEXT_PUBLIC_API_URL`: LangGraph server URL (default: http://localhost:2024 for local dev)
- `NEXT_PUBLIC_ASSISTANT_ID`: Agent/graph ID (default: "agent")
- For production: `LANGGRAPH_API_URL` and `LANGSMITH_API_KEY` for API passthrough

## Running the Full System

1. Start Python agent: `cd python-agent && uv run dev`
2. Start UI: `cd ui && pnpm dev`
3. Access chat interface at http://localhost:3000

The UI connects to the Python agent running on port 2024 by default.

## Documentation References

### LangGraph Documentation
- **Main Guides**: https://langchain-ai.github.io/langgraph/guides/ - Navigate from here to specific subpages for tutorials, how-tos, and conceptual guides
- **Python SDK Reference**: https://langchain-ai.github.io/langgraph/cloud/reference/sdk/python_sdk_ref/ - Complete API documentation for LangGraph Python SDK

These resources are essential for understanding LangGraph concepts, building workflows, and using advanced features beyond the basic chatbot implementation in this codebase.