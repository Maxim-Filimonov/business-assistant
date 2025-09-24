#!/usr/bin/env python
"""
Test the scheduler agent with PDF extraction
"""

import sys

if "pytest" in sys.modules:
    try:  # pragma: no cover - runtime availability check
        import crewai  # noqa: F401
    except ModuleNotFoundError:  # pragma: no cover
        import pytest

        pytest.skip("crewai is not installed", allow_module_level=True)

from main import FlexibleBusinessChat

def test_scheduler():
    """Test scheduler functionality"""
    print("\n" + "="*70)
    print("Testing Scheduler Agent with PDF Extraction")
    print("="*70)

    # Initialize the system
    chat = FlexibleBusinessChat()

    # Test queries
    test_queries = [
        "What is Dr. Johnson's schedule for this week?",
        "Find all appointments for Monday",
        "Who has group therapy sessions scheduled?"
    ]

    for query in test_queries:
        print(f"\n📋 Query: {query}")
        print("-" * 50)

        try:
            result = chat.process_request(query)
            print(f"✅ Result:\n{result}")
        except Exception as e:
            print(f"❌ Error: {e}")

    print("\n" + "="*70)
    print("Test Complete!")
    print("="*70)

if __name__ == "__main__":
    test_scheduler()
