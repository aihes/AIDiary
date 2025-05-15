#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Multi-Tool Agent Example using Composio and OpenAI
-------------------------------------------------
This script demonstrates how to create an agent that can use multiple Composio tools
to perform various tasks based on user input.
"""

import os
import json
from dotenv import load_dotenv
from composio_openai import ComposioToolSet, App, Action
from openai import OpenAI

# Load environment variables from .env file (if exists)
load_dotenv()

class ComposioAgent:
    """A class that implements an agent capable of using multiple Composio tools."""
    
    def __init__(self, openai_api_key=None, composio_api_key=None, model="gpt-4o"):
        """
        Initialize the Composio Agent.
        
        Args:
            openai_api_key (str, optional): OpenAI API key. Defaults to environment variable.
            composio_api_key (str, optional): Composio API key. Defaults to environment variable or demo key.
            model (str, optional): OpenAI model to use. Defaults to "gpt-4o".
        """
        self.openai_client = OpenAI(
            api_key=openai_api_key or os.environ.get("OPENAI_API_KEY")
        )
        
        self.composio_toolset = ComposioToolSet(
            api_key=composio_api_key or os.environ.get("COMPOSIO_API_KEY", "s0oenj76zyha6l5e7pwff")
        )
        
        self.model = model
        
        # Define available tools with friendly names for display
        self.available_tools = {
            "github_star": Action.GITHUB_STAR_A_REPOSITORY_FOR_THE_AUTHENTICATED_USER,
            "github_unstar": Action.GITHUB_UNSTAR_A_REPOSITORY_FOR_THE_AUTHENTICATED_USER,
            "github_create_issue": Action.GITHUB_CREATE_AN_ISSUE,
            "github_list_repos": Action.GITHUB_LIST_REPOSITORIES_FOR_THE_AUTHENTICATED_USER,
            "github_search_repos": Action.GITHUB_SEARCH_REPOSITORIES,
            "github_get_repo": Action.GITHUB_GET_A_REPOSITORY,
        }
        
        # System prompt for the agent
        self.system_prompt = """
        You are a helpful assistant that specializes in GitHub operations.
        When the user asks you to perform a GitHub task, use the appropriate tool.
        Be precise and use the exact repository names and other parameters as specified by the user.
        If you need more information to complete a task, ask the user for clarification.
        """
    
    def get_tools(self, tool_names=None):
        """
        Get the specified tools or all available tools.
        
        Args:
            tool_names (list, optional): List of tool names to include. Defaults to all tools.
            
        Returns:
            list: List of tools for OpenAI function calling
        """
        if tool_names:
            actions = [self.available_tools[name] for name in tool_names if name in self.available_tools]
        else:
            actions = list(self.available_tools.values())
        
        return self.composio_toolset.get_tools(actions=actions)
    
    def list_available_tools(self):
        """List all available tools with descriptions."""
        print("\nAvailable Tools:")
        for name, action in self.available_tools.items():
            # Convert enum name to readable description
            description = action.name.replace("_", " ").title()
            print(f"  - {name}: {description}")
    
    def run(self, user_input, tool_names=None, verbose=True):
        """
        Run the agent with the given user input.
        
        Args:
            user_input (str): The user's request
            tool_names (list, optional): List of tool names to include. Defaults to all tools.
            verbose (bool, optional): Whether to print detailed information. Defaults to True.
            
        Returns:
            dict: The result of the operation
        """
        if verbose:
            print(f"\n🤖 Processing request: {user_input}")
        
        # Get the specified tools
        tools = self.get_tools(tool_names)
        
        # Call OpenAI API with the tools
        response = self.openai_client.chat.completions.create(
            model=self.model,
            tools=tools,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_input},
            ],
        )
        
        # Print the AI's response
        ai_response = response.choices[0].message.content
        if ai_response and verbose:
            print(f"\n🤖 AI Response: {ai_response}")
        
        # Handle tool calls if any
        if response.choices[0].message.tool_calls:
            if verbose:
                print("\n🔧 Tool Call Detected:")
                for tool_call in response.choices[0].message.tool_calls:
                    print(f"  Tool: {tool_call.function.name}")
                    print(f"  Arguments: {tool_call.function.arguments}")
            
            # Execute the tool calls
            if verbose:
                print("\n⚙️ Executing Tool Call...")
            result = self.composio_toolset.handle_tool_calls(response)
            
            if verbose:
                print(f"\n✅ Result: {json.dumps(result, indent=2)}")
            return result
        else:
            if verbose:
                print("\n❌ No tool calls were made by the AI.")
            return {"response": ai_response, "tool_calls": None}

def main():
    """Main function to run the interactive agent."""
    print("=" * 60)
    print("Multi-Tool GitHub Agent using Composio and OpenAI")
    print("=" * 60)
    
    # Check if OpenAI API key is set
    if not os.environ.get("OPENAI_API_KEY"):
        print("\n⚠️ Warning: OPENAI_API_KEY environment variable is not set.")
        api_key = input("Enter your OpenAI API key (or press Enter to exit): ").strip()
        if not api_key:
            print("Exiting...")
            return
        os.environ["OPENAI_API_KEY"] = api_key
    
    # Initialize the agent
    agent = ComposioAgent()
    
    # Show available tools
    agent.list_available_tools()
    
    print("\nExample commands:")
    print("  - Star the repository composiohq/composio")
    print("  - List my GitHub repositories")
    print("  - Search for repositories about LLM agents")
    print("  - Create an issue in composiohq/composio titled 'Test Issue'")
    print("\nType 'exit' to quit.")
    
    # Interactive loop
    while True:
        print("\n" + "-" * 60)
        user_input = input("What GitHub task would you like to perform? ").strip()
        
        if user_input.lower() in ['exit', 'quit', 'q']:
            print("Goodbye!")
            break
        
        if not user_input:
            continue
        
        try:
            agent.run(user_input)
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
