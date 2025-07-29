"""Basic LangGraph agent implementation."""

from typing import Any, Dict, List
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import MessagesState


def chatbot(state: MessagesState) -> Dict[str, List[BaseMessage]]:
    """Simple chatbot node that responds to messages."""
    llm = ChatOpenAI(model="gpt-4o-mini")
    response = llm.invoke(state["messages"])
    return {"messages": [response]}


def create_agent():
    """Create and return a basic LangGraph agent."""
    workflow = StateGraph(MessagesState)
    
    workflow.add_node("chatbot", chatbot)
    workflow.add_edge(START, "chatbot")
    workflow.add_edge("chatbot", END)
    
    return workflow.compile()


def run_agent(message: str) -> str:
    """Run the agent with a simple message and return the response."""
    agent = create_agent()
    
    result = agent.invoke({
        "messages": [HumanMessage(content=message)]
    })
    
    return result["messages"][-1].content