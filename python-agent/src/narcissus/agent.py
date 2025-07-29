"""Basic LangGraph agent implementation."""

from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import MessagesState


def chatbot(state: MessagesState) -> dict[str, list[BaseMessage]]:
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

    result = agent.invoke({"messages": [HumanMessage(content=message)]})

    return result["messages"][-1].content
