# Agent Tools Demo

This directory contains examples of using OpenAI's function calling with Composio's MCP (Multi-Cloud Platform) tools to create powerful AI agents that can interact with various services.

## Setup

1. **Install dependencies**:
   ```bash
   pip install openai composio_openai python-dotenv
   ```

2. **Configure API keys**:
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key to the `.env` file
   - (Optional) Add your Composio API key if you have one

3. **Authenticate with Composio**:
   ```bash
   composio add github
   ```
   Follow the prompts to authenticate with GitHub. You can also authenticate with other services like Google Drive, Slack, etc.

## Examples

### 1. GitHub Star Example

A simple example that demonstrates how to use OpenAI's function calling with Composio's GitHub tools to star a repository.

```bash
python github_star_example.py
```

### 2. Multi-Tool Agent

A more comprehensive example that creates an agent capable of using multiple GitHub tools based on user input.

```bash
python multi_tool_agent.py
```

### 3. MCP Tools Example

A demonstration of various MCP tools from different categories (GitHub, Google Drive, Slack, Notion, Jira).

```bash
python mcp_tools_example.py
```

## Key Concepts

### Tool Integration

The examples demonstrate how to integrate OpenAI's function calling with Composio's tools:

```python
# Get tools from Composio
tools = composio_toolset.get_tools(actions=[Action.GITHUB_STAR_A_REPOSITORY_FOR_THE_AUTHENTICATED_USER])

# Use tools with OpenAI
response = openai_client.chat.completions.create(
    model="gpt-4o",
    tools=tools,
    messages=[...],
)

# Handle tool calls
result = composio_toolset.handle_tool_calls(response)
```

### Available Tool Categories

The examples showcase tools from various categories:

- **GitHub**: Repository management, issues, stars, etc.
- **Google Drive**: File management, search, creation
- **Slack**: Messaging, channel management
- **Notion**: Page creation, search
- **Jira**: Issue tracking

## Extending the Examples

You can extend these examples by:

1. Adding more tools from Composio
2. Creating more complex agents with memory and conversation history
3. Combining multiple tool categories in a single agent
4. Adding error handling and retry logic
5. Building a web interface for your agent

## Resources

- [OpenAI Function Calling Documentation](https://platform.openai.com/docs/guides/function-calling)
- [Composio Documentation](https://docs.composio.dev/)
- [OpenAI Agents Python Library](https://openai.github.io/openai-agents-python/tools/)
