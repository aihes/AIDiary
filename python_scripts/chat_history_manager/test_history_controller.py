#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script for the Chat History Controller
"""

import json
from history_controller import mainFunc

def test_normal_case():
    """Test with normal history list"""
    print("\n=== Test: Normal Case ===")
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
            "content": "Hi there! How can I help you today?",
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

def test_string_history():
    """Test with history as a string"""
    print("\n=== Test: String History ===")
    test_args = {
        "sessionId": "generate_session_360000000000184005_245464",
        "history": json.dumps([{
            "role": "user",
            "content": "What's the weather like?",
        }, {
            "role": "assistant",
            "content": "I don't have real-time weather information.",
        }]),
        "message": "mm"
    }
    
    result = mainFunc(test_args)
    print("Controlled History:")
    print(json.dumps(result["controlled_history"], indent=2))
    print("\nHistory String:")
    print(result["history_string"])

def test_long_history():
    """Test with history exceeding max turns"""
    print("\n=== Test: Long History ===")
    # Create a history with 15 items (exceeding default MAX_HISTORY_TURNS of 10)
    history = []
    for i in range(15):
        history.append({
            "role": "user" if i % 2 == 0 else "assistant",
            "content": f"Message {i+1}"
        })
    
    test_args = {
        "history": history,
        "max_turns": 5  # Override default to keep only 5 turns
    }
    
    result = mainFunc(test_args)
    print("Controlled History (should have 5 items):")
    print(json.dumps(result["controlled_history"], indent=2))
    print("\nHistory String:")
    print(result["history_string"])

def test_long_content():
    """Test with content exceeding max chars"""
    print("\n=== Test: Long Content ===")
    # Create a history with very long content
    long_content = "This is a very long message. " * 100  # ~2600 characters
    
    test_args = {
        "history": [{
            "role": "user",
            "content": "Hello"
        }, {
            "role": "assistant",
            "content": long_content
        }],
        "max_chars": 500  # Override default to keep only 500 chars
    }
    
    result = mainFunc(test_args)
    print("Controlled History:")
    print(json.dumps(result["controlled_history"], indent=2)[:100] + "...")  # Truncate output for readability
    print("\nHistory String (should be ~500 chars):")
    print(f"Length: {len(result['history_string'])}")
    print(result["history_string"][-100:] + "...")  # Show the end of the string

def test_invalid_history():
    """Test with invalid history format"""
    print("\n=== Test: Invalid History ===")
    test_args = {
        "history": "This is not a valid JSON string or list",
    }
    
    result = mainFunc(test_args)
    print("Controlled History:")
    print(json.dumps(result["controlled_history"], indent=2))
    print("\nHistory String:")
    print(result["history_string"])

if __name__ == "__main__":
    test_normal_case()
    test_string_history()
    test_long_history()
    test_long_content()
    test_invalid_history()
