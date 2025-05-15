#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GitHub Star Example using Composio and OpenAI
---------------------------------------------
This script demonstrates how to use OpenAI's function calling with Composio's GitHub tools
to star a repository.
"""

import os
import json
from dotenv import load_dotenv
from composio_openai import ComposioToolSet, App, Action
from openai import OpenAI

# Load environment variables from .env file (if exists)
load_dotenv()

def github_star_example(repo_name="composiohq/composio"):
    """
    Example function to star a GitHub repository using Composio tools and OpenAI.
    
    Args:
        repo_name (str): The repository name to star in format "owner/repo"
    
    Returns:
        dict: The result of the operation
    """
    # Initialize OpenAI client
    openai_client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY")
    )
    
    # Initialize Composio toolset
    composio_toolset = ComposioToolSet(
        api_key=os.environ.get("COMPOSIO_API_KEY", "s0oenj76zyha6l5e7pwff")
    )
    
    # Get GitHub star tool
    tools = composio_toolset.get_tools(
        actions=[Action.GITHUB_STAR_A_REPOSITORY_FOR_THE_AUTHENTICATED_USER]
    )
    
    # Create the task prompt
    task = f"Star the GitHub repository {repo_name}. The user wants to star this repository."
    
    print(f"🤖 Asking AI to star repository: {repo_name}")
    
    # Call OpenAI API with the tools
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        tools=tools,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that helps users with GitHub tasks."},
            {"role": "user", "content": task},
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
        result = composio_toolset.handle_tool_calls(response)
        print(f"\n✅ Result: {json.dumps(result, indent=2)}")
        return result
    else:
        print("\n❌ No tool calls were made by the AI.")
        return None

def main():
    """Main function to run the example."""
    print("=" * 50)
    print("GitHub Star Example using Composio and OpenAI")
    print("=" * 50)
    
    # Check if OpenAI API key is set
    if not os.environ.get("OPENAI_API_KEY"):
        print("\n⚠️ Warning: OPENAI_API_KEY environment variable is not set.")
        print("Please set it or the example will fail.")
    
    # Get repository name from user input or use default
    repo_name = input("\nEnter repository name to star (default: composiohq/composio): ").strip()
    if not repo_name:
        repo_name = "composiohq/composio"
    
    # Run the example
    github_star_example(repo_name)

if __name__ == "__main__":
    main()
