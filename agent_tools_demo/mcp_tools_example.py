#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MCP Tools Example using Composio and OpenAI
-------------------------------------------
This script demonstrates how to use various MCP (Multi-Cloud Platform) tools
from Composio with OpenAI's function calling capabilities.
"""

import os
import json
from dotenv import load_dotenv
from composio_openai import ComposioToolSet, App, Action
from openai import OpenAI

# Load environment variables from .env file (if exists)
load_dotenv()

class MCPToolsDemo:
    """A class that demonstrates various MCP tools from Composio."""
    
    def __init__(self, openai_api_key=None, composio_api_key=None):
        """
        Initialize the MCP Tools Demo.
        
        Args:
            openai_api_key (str, optional): OpenAI API key. Defaults to environment variable.
            composio_api_key (str, optional): Composio API key. Defaults to environment variable or demo key.
        """
        self.openai_client = OpenAI(
            api_key=openai_api_key or os.environ.get("OPENAI_API_KEY")
        )
        
        self.composio_toolset = ComposioToolSet(
            api_key=composio_api_key or os.environ.get("COMPOSIO_API_KEY", "s0oenj76zyha6l5e7pwff")
        )
        
        # Define tool categories for demonstration
        self.tool_categories = {
            "github": [
                Action.GITHUB_STAR_A_REPOSITORY_FOR_THE_AUTHENTICATED_USER,
                Action.GITHUB_LIST_REPOSITORIES_FOR_THE_AUTHENTICATED_USER,
                Action.GITHUB_SEARCH_REPOSITORIES,
                Action.GITHUB_CREATE_AN_ISSUE,
            ],
            "google_drive": [
                Action.GOOGLE_DRIVE_LIST_FILES,
                Action.GOOGLE_DRIVE_CREATE_FILE,
                Action.GOOGLE_DRIVE_SEARCH_FILES,
            ],
            "slack": [
                Action.SLACK_POST_MESSAGE,
                Action.SLACK_LIST_CHANNELS,
            ],
            "notion": [
                Action.NOTION_CREATE_PAGE,
                Action.NOTION_SEARCH,
            ],
            "jira": [
                Action.JIRA_GET_ISSUE,
                Action.JIRA_CREATE_ISSUE,
            ]
        }
    
    def list_tool_categories(self):
        """List all available tool categories."""
        print("\nAvailable Tool Categories:")
        for category, actions in self.tool_categories.items():
            print(f"  - {category.title()}: {len(actions)} tools")
    
    def list_tools_in_category(self, category):
        """
        List all tools in a specific category.
        
        Args:
            category (str): The category name
        """
        if category not in self.tool_categories:
            print(f"Category '{category}' not found.")
            return
        
        print(f"\nTools in {category.title()} category:")
        for action in self.tool_categories[category]:
            # Convert enum name to readable description
            description = action.name.replace("_", " ").title()
            print(f"  - {description}")
    
    def run_tool_demo(self, category, task_description):
        """
        Run a demonstration of tools in a specific category.
        
        Args:
            category (str): The category of tools to use
            task_description (str): The task to perform
            
        Returns:
            dict: The result of the operation
        """
        if category not in self.tool_categories:
            print(f"Category '{category}' not found.")
            return None
        
        # Get tools for the specified category
        tools = self.composio_toolset.get_tools(actions=self.tool_categories[category])
        
        print(f"\n🤖 Running {category.title()} tools demo with task: {task_description}")
        
        # Call OpenAI API with the tools
        response = self.openai_client.chat.completions.create(
            model="gpt-4o",
            tools=tools,
            messages=[
                {"role": "system", "content": f"You are a helpful assistant that specializes in {category} operations. Use the appropriate tool to help the user."},
                {"role": "user", "content": task_description},
            ],
        )
        
        # Print the AI's response
        ai_response = response.choices[0].message.content
        if ai_response:
            print(f"\n🤖 AI Response: {ai_response}")
        
        # Handle tool calls if any
        if response.choices[0].message.tool_calls:
            print("\n🔧 Tool Call Detected:")
            for tool_call in response.choices[0].message.tool_calls:
                print(f"  Tool: {tool_call.function.name}")
                print(f"  Arguments: {tool_call.function.arguments}")
            
            # Execute the tool calls
            print("\n⚙️ Executing Tool Call...")
            try:
                result = self.composio_toolset.handle_tool_calls(response)
                print(f"\n✅ Result: {json.dumps(result, indent=2)}")
                return result
            except Exception as e:
                print(f"\n❌ Error executing tool call: {str(e)}")
                return {"error": str(e)}
        else:
            print("\n❌ No tool calls were made by the AI.")
            return {"response": ai_response, "tool_calls": None}

def main():
    """Main function to run the MCP tools demo."""
    print("=" * 60)
    print("MCP Tools Demo using Composio and OpenAI")
    print("=" * 60)
    
    # Check if OpenAI API key is set
    if not os.environ.get("OPENAI_API_KEY"):
        print("\n⚠️ Warning: OPENAI_API_KEY environment variable is not set.")
        api_key = input("Enter your OpenAI API key (or press Enter to exit): ").strip()
        if not api_key:
            print("Exiting...")
            return
        os.environ["OPENAI_API_KEY"] = api_key
    
    # Initialize the demo
    demo = MCPToolsDemo()
    
    # Show available tool categories
    demo.list_tool_categories()
    
    print("\nExample tasks by category:")
    print("  - github: Star the repository composiohq/composio")
    print("  - google_drive: List my recent files")
    print("  - slack: Send a message to the general channel")
    print("  - notion: Create a new page with title 'Meeting Notes'")
    print("  - jira: Create a new bug issue")
    
    # Interactive demo
    while True:
        print("\n" + "-" * 60)
        category = input("Select a tool category (or 'exit' to quit): ").strip().lower()
        
        if category in ['exit', 'quit', 'q']:
            print("Goodbye!")
            break
        
        if category not in demo.tool_categories:
            print(f"Category '{category}' not found. Available categories: {', '.join(demo.tool_categories.keys())}")
            continue
        
        # Show tools in the selected category
        demo.list_tools_in_category(category)
        
        # Get task description
        task = input(f"\nEnter your {category} task: ").strip()
        if not task:
            continue
        
        # Run the demo
        demo.run_tool_demo(category, task)

if __name__ == "__main__":
    main()
