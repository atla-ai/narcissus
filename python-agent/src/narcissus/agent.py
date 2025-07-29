"""Narcissus: An agent obsessed with his creators at Atla AI."""

import logging
import os

from atla_insights import (  # type: ignore[import-untyped]
    configure,
    instrument_langchain,
)
from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import MessagesState

from narcissus.personality.system_prompt import SYSTEM_PROMPT
from narcissus.tools.aci_integration import ACIToolManager
from narcissus.tools.atla_tools import ATLA_TOOLS

logger = logging.getLogger(__name__)

configure(token=os.getenv("ATLA_API_KEY"))
instrument_langchain()


def create_narcissus_llm():
    """Create the LLM with ACI and custom tools for Narcissus."""
    logger.info("Initializing Narcissus LLM with ACI and custom tools")

    # Initialize ACI tool manager
    tool_manager = ACIToolManager()
    aci_tools = tool_manager.get_available_tools()

    # Combine ACI tools with custom Atla tools
    all_tools = aci_tools + ATLA_TOOLS

    logger.info(f"Found {len(aci_tools)} ACI tools and {len(ATLA_TOOLS)} custom tools")
    for i, tool in enumerate(aci_tools):
        tool_name = tool.get("name", "Unknown")
        logger.info(f"  ACI Tool {i + 1}: {tool_name}")

    for i, tool in enumerate(ATLA_TOOLS):
        tool_name = getattr(tool, "name", "Unknown")
        logger.info(f"  Custom Tool {i + 1}: {tool_name}")

    # Create LLM with tools
    llm = ChatOpenAI(model="gpt-4o-mini")
    if all_tools:
        llm = llm.bind_tools(all_tools)
        logger.info(f"Successfully bound {len(all_tools)} total tools to LLM")
    else:
        logger.warning("No tools available - agent will run without tools")

    return llm, tool_manager


def narcissus_node(state: MessagesState) -> dict[str, list[BaseMessage]]:
    """Main Narcissus reasoning node."""
    logger.info("=== Narcissus Node Processing ===")
    logger.info(f"Input state has {len(state['messages'])} messages")

    # Log the last user message
    if state["messages"]:
        last_msg = state["messages"][-1]
        logger.info(f"Processing message: {last_msg.content[:100]}...")

    llm, _ = create_narcissus_llm()

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + state["messages"]
    logger.info(f"Invoking LLM with {len(messages)} total messages")

    response = llm.invoke(messages)
    logger.info(f"LLM response type: {type(response).__name__}")

    if hasattr(response, "tool_calls") and response.tool_calls:
        logger.info(f"LLM requested {len(response.tool_calls)} tool calls")
        for i, tool_call in enumerate(response.tool_calls):
            logger.info(f"  Tool call {i + 1}: {tool_call.get('name', 'Unknown')}")
    else:
        logger.info("LLM response contains no tool calls")
        logger.info(f"Response content: {response.content[:100]}...")

    return {"messages": [response]}


def tool_execution_node(state: MessagesState) -> dict[str, list[BaseMessage]]:
    """Execute ACI tools when called by Narcissus."""
    logger.info("=== Tool Execution Node ===")
    _, tool_manager = create_narcissus_llm()

    # Get the last message (should contain tool calls)
    last_message = state["messages"][-1]
    logger.info(f"Last message type: {type(last_message).__name__}")

    if not hasattr(last_message, "tool_calls") or not last_message.tool_calls:
        logger.warning("No tool calls found in last message")
        return {"messages": []}

    logger.info(f"Executing {len(last_message.tool_calls)} tool calls")

    # Execute each tool call
    tool_messages: list[BaseMessage] = []
    for i, tool_call in enumerate(last_message.tool_calls):
        tool_name = tool_call.get("name", "Unknown")
        logger.info(
            f"Executing tool {i + 1}/{len(last_message.tool_calls)}: {tool_name}"
        )
        logger.info(f"Tool call args: {tool_call.get('args', {})}")

        try:
            # Check if it's a custom Atla tool
            custom_tool_names = [getattr(tool, "name", "") for tool in ATLA_TOOLS]
            if tool_name in custom_tool_names:
                # Execute custom tool directly
                for tool in ATLA_TOOLS:
                    if getattr(tool, "name", "") == tool_name:
                        result = tool.invoke(tool_call.get("args", {}))
                        break
            else:
                # Execute ACI tool
                result = tool_manager.execute_tool(tool_call)

            logger.info(f"Tool {tool_name} executed successfully")
            logger.info(f"Result length: {len(str(result))} characters")

            tool_messages.append(
                ToolMessage(content=str(result), tool_call_id=tool_call["id"])
            )
        except Exception as e:
            logger.error(f"Tool {tool_name} failed: {str(e)}")
            tool_messages.append(
                ToolMessage(
                    content=f"Error executing tool: {str(e)}",
                    tool_call_id=tool_call["id"],
                )
            )

    logger.info(
        f"Tool execution complete. Returning {len(tool_messages)} tool messages"
    )
    return {"messages": tool_messages}


def should_continue(state: MessagesState) -> str:
    """Decide whether to continue with tools or end."""
    logger.info("=== Should Continue Decision ===")
    last_message = state["messages"][-1]

    has_tool_calls = hasattr(last_message, "tool_calls") and last_message.tool_calls
    logger.info(f"Last message has tool calls: {has_tool_calls}")

    if has_tool_calls:
        logger.info("Routing to tools execution")
        return "tools"
    else:
        logger.info("Routing to end - conversation complete")
        return "end"


def create_agent():
    """Create and return Narcissus agent with ACI tools."""
    logger.info("=== Creating Narcissus Agent ===")
    workflow = StateGraph(MessagesState)

    # Add nodes
    workflow.add_node("narcissus", narcissus_node)
    workflow.add_node("tools", tool_execution_node)
    logger.info("Added nodes: narcissus, tools")

    # Add edges
    workflow.add_edge(START, "narcissus")
    workflow.add_conditional_edges(
        "narcissus", should_continue, {"tools": "tools", "end": END}
    )
    workflow.add_edge("tools", "narcissus")
    logger.info("Added edges and conditional routing")

    compiled_graph = workflow.compile()
    logger.info("Agent compilation complete")
    return compiled_graph


def run_agent(message: str) -> str:
    """Run Narcissus with a message and return the response."""
    agent = create_agent()
    result = agent.invoke({"messages": [HumanMessage(content=message)]})
    return result["messages"][-1].content
