#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Chat History Controller
-----------------------
This module provides functionality to manage and control chat history,
including limiting the number of conversation turns and the total character length.
"""

import json
import logging
from typing import Dict, List, Union, Tuple, Any

# Global configuration variables
MAX_HISTORY_TURNS = 10  # Maximum number of conversation turns to keep
MAX_HISTORY_CHARS = 4000  # Maximum total character length for history string

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def parse_history_item(item: Dict[str, Any]) -> Dict[str, str]:
    """
    Parse a history item and extract role and content.
    
    Args:
        item: A dictionary containing history item data
        
    Returns:
        A dictionary with role and content keys
    """
    parsed_item = {}
    
    # Extract role
    if "role" in item and isinstance(item["role"], str):
        parsed_item["role"] = item["role"]
    else:
        logger.warning("Missing or invalid 'role' in history item, using 'unknown'")
        parsed_item["role"] = "unknown"
    
    # Extract content
    if "content" in item and isinstance(item["content"], str):
        parsed_item["content"] = item["content"]
    else:
        logger.warning("Missing or invalid 'content' in history item, using empty string")
        parsed_item["content"] = ""
    
    return parsed_item

def truncate_history(history: List[Dict[str, Any]], max_turns: int = MAX_HISTORY_TURNS) -> List[Dict[str, Any]]:
    """
    Truncate history to the maximum number of turns.
    
    Args:
        history: List of history items
        max_turns: Maximum number of turns to keep
        
    Returns:
        Truncated history list
    """
    if len(history) <= max_turns:
        return history
    
    # Keep the most recent conversations
    return history[-max_turns:]

def create_history_string(history: List[Dict[str, Any]], max_chars: int = MAX_HISTORY_CHARS) -> str:
    """
    Create a string representation of the history with length limitation.
    
    Args:
        history: List of history items
        max_chars: Maximum character length
        
    Returns:
        String representation of history
    """
    history_parts = []
    
    for item in history:
        parsed = parse_history_item(item)
        part = f"{parsed['role']}: {parsed['content']}"
        history_parts.append(part)
    
    # Join all parts
    full_history = "\n".join(history_parts)
    
    # Truncate if necessary
    if len(full_history) > max_chars:
        logger.info(f"History string exceeds {max_chars} characters, truncating...")
        return full_history[-max_chars:]
    
    return full_history

def mainFunc(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process chat history to control its size and format.
    
    Args:
        args: Dictionary containing function arguments
            - history: List of conversation history items or string
            - max_turns: (Optional) Maximum number of turns to keep
            - max_chars: (Optional) Maximum character length for history string
            
    Returns:
        Dictionary containing:
            - controlled_history: List of history items after applying limits
            - history_string: String representation of history with length limit
    """
    try:
        # Extract parameters with defaults
        params = args
        max_turns = params.get('max_turns', MAX_HISTORY_TURNS)
        max_chars = params.get('max_chars', MAX_HISTORY_CHARS)
        
        # Extract and validate history
        history = params.get('history', [])
        
        # Handle different history formats
        if isinstance(history, str):
            try:
                # Try to parse as JSON
                history = json.loads(history)
            except json.JSONDecodeError:
                # If not valid JSON, treat as plain text
                logger.warning("History is a string but not valid JSON, treating as single message")
                history = [{"role": "system", "content": history}]
        
        # Ensure history is a list
        if not isinstance(history, list):
            logger.warning("History is not a list or valid JSON string, converting to list")
            history = [{"role": "system", "content": str(history)}]
        
        # Process history
        controlled_history = truncate_history(history, max_turns)
        history_string = create_history_string(controlled_history, max_chars)
        
        # Prepare return value
        ret = {
            "controlled_history": controlled_history,
            "history_string": history_string
        }
        
        return ret
    
    except Exception as e:
        logger.error(f"Error in mainFunc: {str(e)}")
        # Return a safe fallback
        return {
            "controlled_history": [],
            "history_string": "",
            "error": str(e)
        }

# Example usage
if __name__ == "__main__":
    # Test with the provided example
    test_args = {
        "sessionId": "generate_session_360000000000184005_245464",
        "history": [{
            "role": "user",
            "content": "hello",
            "extraInfo": {
                "innerSuccess": True
            }
        }, {
            "role": "assistant",
            "type": "answer",
            "content": "{\"sessionId\":\"generate_session_360000000000184005_245464\",\"message\":\"mm\",\"history\":[],\"sys_end_Activity_id\":\"end\"}",
            "extraInfo": {
                "innerSuccess": True
            }
        }],
        "message": "mm"
    }
    
    result = mainFunc(test_args)
    print("Controlled History:")
    print(json.dumps(result["controlled_history"], indent=2))
    print("\nHistory String:")
    print(result["history_string"])
