"""ACI integration for Narcissus agent tools."""

import logging
import os
from typing import Any

from aci import ACI

logger = logging.getLogger(__name__)

CONFIGURED_TOOLS: list[str] = [
    "BRAVE_SEARCH__WEB_SEARCH",  # For searching Atla docs/blog posts
    # "GITHUB__GET_REPOSITORY",  # For getting repo info
    # "GITHUB__SEARCH_REPOSITORIES",  # For finding Atla repos
]


class ACIToolManager:
    """Manages ACI tool integration for Narcissus."""

    aci: ACI
    linked_account_owner_id: str

    def __init__(self) -> None:
        logger.info("Initializing ACI Tool Manager")
        self.aci = ACI()
        self.linked_account_owner_id = os.getenv("ACI_LINKED_ACCOUNT_OWNER_ID") or ""
        logger.info(f"Linked account owner ID: {self.linked_account_owner_id}")

    def get_available_tools(self) -> list[dict[str, Any]]:
        """Get list of available ACI tools for the agent."""
        logger.info(f"Loading {len(CONFIGURED_TOOLS)} configured tools")
        tools = []

        for tool_name in CONFIGURED_TOOLS:
            logger.info(f"Attempting to load tool: {tool_name}")
            try:
                tool_definition = self.aci.functions.get_definition(tool_name)
                if tool_definition:
                    tools.append(tool_definition)
                    logger.info(f"Successfully loaded tool: {tool_name}")
                else:
                    logger.warning(f"Tool definition not found: {tool_name}")
            except Exception as e:
                logger.error(f"Failed to load tool {tool_name}: {str(e)}")

        logger.info(f"Loaded {len(tools)} tools successfully")
        return tools

    def execute_tool(self, tool_call: dict[str, Any]) -> Any:
        """Execute an ACI tool call."""
        tool_name = tool_call.get("name", "Unknown")
        tool_args = tool_call.get("args", {})

        logger.info(f"Executing ACI tool: {tool_name}")
        logger.info(f"Tool args: {tool_args}")

        try:
            result = self.aci.handle_function_call(
                tool_name,
                tool_args,
                linked_account_owner_id=self.linked_account_owner_id,
            )
            logger.info("ACI tool execution successful")
            return result
        except Exception as e:
            logger.error(f"ACI tool execution failed: {str(e)}")
            raise e
