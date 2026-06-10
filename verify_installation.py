#!/usr/bin/env python
"""
Verify Multi-Agent System Installation
"""

import sys
import importlib

def check_module(name, package=None):
    """Check if a module is installed"""
    try:
        pkg = package or name
        importlib.import_module(pkg)
        print(f"✓ {name}")
        return True
    except ImportError:
        print(f"✗ {name} (not installed)")
        return False

def main():
    print("\n" + "="*60)
    print("MULTI-AGENT SYSTEM - INSTALLATION CHECK")
    print("="*60)
    
    print("\nCore Requirements:")
    results = []
    results.append(check_module("graphifyy"))
    results.append(check_module("flask"))
    results.append(check_module("networkx"))
    
    print("\nLocal Modules:")
    results.append(check_module("multi_agent_interface", "multi_agent_interface"))
    results.append(check_module("agent_examples", "agent_examples"))
    results.append(check_module("test_agent_interface", "test_agent_interface"))
    
    print("\nDocumentation:")
    import os
    docs = [
        "AGENT_INTERFACE_README.md",
        "ARCHITECTURE.md",
        "QUICKSTART.md",
    ]
    for doc in docs:
        if os.path.exists(doc):
            print(f"✓ {doc}")
            results.append(True)
        else:
            print(f"✗ {doc}")
            results.append(False)
    
    print("\n" + "="*60)
    if all(results):
        print("✓ All checks passed!")
        print("\nYou can now run:")
        print("  python run_interactive.py     # Interactive shell")
        print("  python agent_examples.py      # Example code")
        print("  python agent_web_interface.py # Web server")
        print("="*60 + "\n")
        return 0
    else:
        print("✗ Some checks failed")
        print("="*60 + "\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
