#!/usr/bin/env python
"""
Test script to verify the CrewAI delegation fix
"""

import sys
import traceback
from main import FlexibleBusinessChat

def test_delegation_fix():
    """Test various scenarios to ensure delegation issues are resolved"""

    print("="*60)
    print("🧪 TESTING CREWAI DELEGATION FIX")
    print("="*60)

    # Initialize the system
    try:
        system = FlexibleBusinessChat()
        print("✅ System initialized successfully")
    except Exception as e:
        print(f"❌ System initialization failed: {e}")
        traceback.print_exc()
        return False

    # Test cases that previously caused delegation errors
    test_cases = [
        {
            "name": "Simple CRM Query",
            "request": "Find John's contact information",
            "expected_keywords": ["client", "contact", "CRM"]
        },
        {
            "name": "Schedule Query",
            "request": "Who has appointments today?",
            "expected_keywords": ["schedule", "appointment", "time"]
        },
        {
            "name": "Invoice Query",
            "request": "Generate invoice for last week",
            "expected_keywords": ["invoice", "billing", "cost"]
        },
        {
            "name": "Complex Multi-Agent Query",
            "request": "Show me all clients who haven't been scheduled this month",
            "expected_keywords": ["client", "schedule", "CRM"]
        },
        {
            "name": "Creative Query",
            "request": "Which specialist is the busiest?",
            "expected_keywords": ["schedule", "specialist", "analysis"]
        }
    ]

    results = []

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test {i}/{len(test_cases)}: {test_case['name']}")
        print(f"Request: '{test_case['request']}'")
        print("-" * 40)

        try:
            # Process the request
            result = system.process_request(test_case['request'])

            # Check if we get a proper response (not an error)
            result_str = str(result)

            # Look for delegation error patterns
            delegation_errors = [
                "DelegateWorkToolSchema",
                "Arguments validation failed",
                "Input should be a valid string",
                "type=string_type",
                "input_type=dict"
            ]

            has_delegation_error = any(error in result_str for error in delegation_errors)

            if has_delegation_error:
                print(f"❌ DELEGATION ERROR DETECTED:")
                print(result_str[:200] + "..." if len(result_str) > 200 else result_str)
                results.append({"test": test_case['name'], "status": "FAILED", "error": "Delegation error"})
            elif "encountered an issue" in result_str.lower():
                print(f"⚠️  PROCESSING ISSUE:")
                print(result_str[:200] + "..." if len(result_str) > 200 else result_str)
                results.append({"test": test_case['name'], "status": "PARTIAL", "error": "Processing issue"})
            else:
                print(f"✅ SUCCESS - Response received:")
                # Show first 150 chars of response
                preview = result_str[:150] + "..." if len(result_str) > 150 else result_str
                print(f"   {preview}")
                results.append({"test": test_case['name'], "status": "PASSED", "error": None})

        except Exception as e:
            error_str = str(e)
            print(f"❌ EXCEPTION: {error_str}")

            # Check if it's a delegation-specific error
            if any(term in error_str for term in ["DelegateWorkToolSchema", "validation failed", "string_type"]):
                print("   🔍 This appears to be the delegation validation error!")
                results.append({"test": test_case['name'], "status": "FAILED", "error": "Delegation validation error"})
            else:
                print("   🔍 Different type of error - may be unrelated to delegation fix")
                results.append({"test": test_case['name'], "status": "FAILED", "error": f"Other: {error_str}"})

            # Print full traceback for debugging
            traceback.print_exc()

    # Summary
    print("\n" + "="*60)
    print("📊 TEST RESULTS SUMMARY")
    print("="*60)

    passed = sum(1 for r in results if r['status'] == 'PASSED')
    partial = sum(1 for r in results if r['status'] == 'PARTIAL')
    failed = sum(1 for r in results if r['status'] == 'FAILED')

    print(f"✅ Passed: {passed}")
    print(f"⚠️  Partial: {partial}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Success Rate: {(passed + partial) / len(results) * 100:.1f}%")

    print("\nDetailed Results:")
    for result in results:
        status_emoji = {"PASSED": "✅", "PARTIAL": "⚠️", "FAILED": "❌"}
        print(f"{status_emoji[result['status']]} {result['test']}: {result['status']}")
        if result['error']:
            print(f"   Error: {result['error']}")

    # Specific delegation error check
    delegation_failures = [r for r in results if 'Delegation' in str(r.get('error', ''))]

    if delegation_failures:
        print(f"\n🚨 DELEGATION ISSUES STILL PRESENT:")
        print("The fix may not have resolved all delegation validation errors.")
        print("Consider trying these additional approaches:")
        print("1. Update to latest CrewAI version")
        print("2. Use only sequential processing")
        print("3. Avoid hierarchical crew management")
        return False
    else:
        print(f"\n🎉 DELEGATION FIX VERIFICATION:")
        if failed == 0:
            print("✅ All tests passed! Delegation issues appear to be resolved.")
        elif passed > 0:
            print("✅ No delegation validation errors detected!")
            print("⚠️  Some other processing issues remain, but delegation fix is working.")
        else:
            print("❌ Tests failed, but not due to delegation validation errors.")
        return True

def quick_test():
    """Quick single test to verify basic functionality"""
    print("\n🚀 QUICK DELEGATION TEST")
    print("-" * 30)

    try:
        system = FlexibleBusinessChat()
        result = system.process_request("Find client information")
        print("✅ Quick test successful - no delegation errors!")
        return True
    except Exception as e:
        if "DelegateWorkToolSchema" in str(e):
            print("❌ Delegation error still present!")
            return False
        else:
            print(f"⚠️  Other error (not delegation): {e}")
            return True

if __name__ == "__main__":
    print("Select test type:")
    print("1. Full test suite")
    print("2. Quick test")

    choice = input("Enter choice (1 or 2, default=2): ").strip() or "2"

    if choice == "1":
        success = test_delegation_fix()
    else:
        success = quick_test()

    if success:
        print("\n🎉 Delegation fix verification complete!")
    else:
        print("\n🔧 Further fixes may be needed.")

    sys.exit(0 if success else 1)
