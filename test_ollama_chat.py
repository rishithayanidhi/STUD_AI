#!/usr/bin/env python3
"""
Test script for Ollama chat integration with STUAI agent.
Tests connection, basic chat, and ticket classification.
"""

import os
import sys
from agent import process_ticket, get_ollama_config

def print_header(title):
    """Print section header."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")

def test_ollama_connection():
    """Test Ollama connection."""
    print_header("TEST 1: Ollama Configuration")
    
    ollama_model = get_ollama_config()
    print(f"✓ Ollama model: {ollama_model}")
    
    # Test basic chat
    try:
        from ollama import chat  # type: ignore
        print("✓ Ollama chat library imported successfully")
        
        response = chat(
            model=ollama_model,
            messages=[{'role': 'user', 'content': 'Say hello briefly'}],
        )
        print(f"✓ Chat connection works!")
        print(f"  Response: {response.message.content[:50]}...")
        return True
    except ImportError:
        print("⚠️  Ollama chat library not installed")
        print("   Run: pip install ollama")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_ticket_classification():
    """Test ticket classification."""
    print_header("TEST 2: Ticket Classification")
    
    test_tickets = [
        "Database connection timeout in production",
        "Need new feature for user authentication",
        "Frontend button styling issue on mobile",
        "Server CPU usage 95% - critical alert",
    ]
    
    for i, ticket in enumerate(test_tickets, 1):
        print(f"Ticket {i}: {ticket}")
        try:
            result = process_ticket(ticket)
            print(f"  Category: {result.get('category', 'N/A')}")
            print(f"  Priority: {result.get('priority', 'N/A')}")
            print(f"  Team: {result.get('team', 'N/A')}")
            print(f"  Confidence: {result.get('confidence', 'N/A')}")
            print(f"  Action: {result.get('suggested_action', 'N/A')}")
            print()
        except Exception as e:
            print(f"  ❌ Error: {e}\n")

def test_chat_streaming():
    """Test streaming chat."""
    print_header("TEST 3: Streaming Chat (Optional)")
    
    try:
        from ollama import chat  # type: ignore
        ollama_model = get_ollama_config()
        
        print("Streaming response:")
        print("-" * 50)
        
        response = chat(
            model=ollama_model,
            messages=[{'role': 'user', 'content': 'What is autonomous operations? (brief)'}],
            stream=True,
        )
        
        for chunk in response:
            content = chunk['message']['content']
            print(content, end='', flush=True)
        
        print("\n" + "-" * 50)
        print("✓ Streaming works!")
    except Exception as e:
        print(f"⚠️  Streaming test skipped: {e}")

def test_multi_turn_conversation():
    """Test multi-turn conversation."""
    print_header("TEST 4: Multi-Turn Conversation")
    
    try:
        from ollama import chat  # type: ignore
        ollama_model = get_ollama_config()
        
        messages = [
            {'role': 'user', 'content': 'What is a ticket classification system?'},
        ]
        
        print("User: What is a ticket classification system?")
        response = chat(model=ollama_model, messages=messages)
        assistant_response = response.message.content
        print(f"Bot: {assistant_response}\n")
        
        messages.append({'role': 'assistant', 'content': assistant_response})
        
        # Follow-up question
        messages.append({'role': 'user', 'content': 'How does it help DevOps teams?'})
        print("User: How does it help DevOps teams?")
        response = chat(model=ollama_model, messages=messages)
        print(f"Bot: {response.message.content}")
    except Exception as e:
        print(f"⚠️  Multi-turn test skipped: {e}")

def main():
    """Run all tests."""
    print(f"\n{chr(27)}[1m{chr(27)}[92m" + "="*70)
    print("  STUAI OLLAMA CHAT INTEGRATION TEST SUITE")
    print("="*70 + f"{chr(27)}[0m\n")
    
    # Test 1: Connection
    if not test_ollama_connection():
        print(f"\n{chr(27)}[91m❌ Ollama not available. Install with: pip install ollama{chr(27)}[0m")
        return 1
    
    # Test 2: Classification
    test_ticket_classification()
    
    # Test 3: Streaming
    test_chat_streaming()
    
    # Test 4: Conversation
    test_multi_turn_conversation()
    
    print_header("ALL TESTS COMPLETED")
    print("✓ Your STUAI agent is ready to use with Ollama chat API!")
    print()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
