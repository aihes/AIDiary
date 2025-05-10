# Chat History Controller

This module provides functionality to manage and control chat history, including limiting the number of conversation turns and the total character length.

## Features

- Limit the number of conversation turns in history
- Control the maximum character length of history string
- Handle different history formats (list or string)
- Parse and extract role and content from history items
- Robust error handling

## Usage

### Basic Usage

```python
from history_controller import mainFunc

# Example input
args = {
    "history": [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there!"}
    ]
}

# Process history
result = mainFunc(args)

# Access results
controlled_history = result["controlled_history"]
history_string = result["history_string"]
```

### Configuration Options

You can customize the behavior by providing additional parameters:

```python
args = {
    "history": [...],
    "max_turns": 5,  # Override default MAX_HISTORY_TURNS
    "max_chars": 2000  # Override default MAX_HISTORY_CHARS
}
```

### Global Configuration

You can also modify the global configuration variables at the top of the module:

```python
# Global configuration variables
MAX_HISTORY_TURNS = 10  # Maximum number of conversation turns to keep
MAX_HISTORY_CHARS = 4000  # Maximum total character length for history string
```

## Testing

Run the test script to verify functionality:

```bash
python test_history_controller.py
```

## Input Format

The function expects a dictionary with the following structure:

```python
{
    "history": [
        {
            "role": "user",
            "content": "message content"
        },
        {
            "role": "assistant",
            "content": "response content"
        }
    ],
    "max_turns": 10,  # Optional
    "max_chars": 4000  # Optional
}
```

The `history` parameter can also be a JSON string representing the same structure.

## Output Format

The function returns a dictionary with the following structure:

```python
{
    "controlled_history": [
        {
            "role": "user",
            "content": "message content"
        },
        {
            "role": "assistant",
            "content": "response content"
        }
    ],
    "history_string": "user: message content\nassistant: response content"
}
```

In case of errors, an additional `error` key will be included with the error message.
