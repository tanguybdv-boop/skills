#!/usr/bin/env python
"""
Interactive Multi-Agent System Shell
"""

import sys
from multi_agent_interface import AgentInterface, Agent, Task, TaskResult
from agent_examples import LoggerAgent, NotificationAgent
import json


def print_menu():
    print("\n" + "="*60)
    print("MULTI-AGENT SYSTEM - INTERACTIVE SHELL")
    print("="*60)
    print("\nCommands:")
    print("  1. List agents")
    print("  2. List tasks")
    print("  3. Submit task")
    print("  4. Execute task")
    print("  5. Execute all tasks")
    print("  6. View statistics")
    print("  7. View system status")
    print("  8. Help")
    print("  9. Exit")
    print("\nEnter command (1-9): ", end="")


def print_agents(interface):
    """Print all registered agents"""
    agents = interface.get_agents()
    print("\n" + "="*60)
    print("REGISTERED AGENTS")
    print("="*60)
    for name, info in agents.items():
        print(f"\n{name}")
        print(f"  Capabilities: {', '.join(info['capabilities'])}")
        print(f"  Completed tasks: {info['tasks_completed']}")
        print(f"  Failed tasks: {info['tasks_failed']}")
    print("="*60)


def print_tasks(interface):
    """Print all tasks"""
    tasks = interface.get_tasks()
    print("\n" + "="*60)
    print("TASKS")
    print("="*60)
    if not tasks:
        print("No tasks")
    else:
        for task in tasks:
            print(f"\n  ID: {task['id']}")
            print(f"  Name: {task['name']}")
            print(f"  Type: {task['task_type']}")
            print(f"  Status: {task['status']}")
            print(f"  Agent: {task['assigned_agent'] or 'Unassigned'}")
    print("="*60)


def submit_task(interface):
    """Submit a new task"""
    print("\n" + "="*60)
    print("SUBMIT TASK")
    print("="*60)

    print("\nAvailable task types:")
    print("  - calculate (expression, context)")
    print("  - log (message, level='INFO')")
    print("  - alert (message)")
    print("  - email (recipient, message)")

    name = input("Task name: ").strip()
    task_type = input("Task type: ").strip()
    priority = input("Priority (0=normal, higher=more urgent): ").strip()

    try:
        priority = int(priority) if priority else 0
    except ValueError:
        print("Invalid priority")
        return

    params = {}

    if task_type == "calculate":
        expression = input("Expression: ").strip()
        params = {"action": "calculate", "expression": expression, "context": {}}
    elif task_type in ["log", "alert"]:
        message = input("Message: ").strip()
        level = input("Level (INFO/WARNING/ERROR): ").strip() or "INFO"
        params = {"action": task_type, "message": message, "level": level}
    elif task_type == "email":
        recipient = input("Recipient: ").strip()
        message = input("Message: ").strip()
        params = {"action": task_type, "recipient": recipient, "message": message}

    try:
        task_id = interface.submit_task(name, task_type, params, priority)
        print(f"\n✓ Task created: {task_id}")
    except Exception as e:
        print(f"\n✗ Error: {e}")


def execute_single_task(interface):
    """Execute a single task"""
    tasks = interface.get_tasks()
    if not tasks:
        print("\nNo tasks available")
        return

    print("\n" + "="*60)
    print("EXECUTE TASK")
    print("="*60)
    print("\nPending tasks:")
    pending = [t for t in tasks if t["status"] == "pending"]
    if not pending:
        print("No pending tasks")
        return

    for i, task in enumerate(pending):
        print(f"  {i+1}. {task['name']} ({task['id']})")

    choice = input("\nSelect task (number): ").strip()
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(pending):
            task_id = pending[idx]["id"]
            result = interface.execute_task(task_id)
            print("\n✓ Task executed:")
            print(f"  Success: {result['success']}")
            print(f"  Output: {result['output']}")
            print(f"  Agent: {result['agent']}")
            print(f"  Time: {result['time']:.3f}s")
        else:
            print("Invalid selection")
    except ValueError:
        print("Invalid input")


def execute_all_tasks(interface):
    """Execute all pending tasks"""
    print("\n" + "="*60)
    print("EXECUTING ALL TASKS")
    print("="*60)

    results = interface.execute_all()
    if not results:
        print("No pending tasks")
        return

    print(f"\nExecuted {len(results)} task(s):")
    for result in results:
        status = "✓" if result["success"] else "✗"
        print(f"\n{status} {result['task_id']}")
        print(f"  Output: {result['output']}")
        print(f"  Agent: {result['agent']}")


def print_statistics(interface):
    """Print system statistics"""
    stats = interface.get_statistics()
    print("\n" + "="*60)
    print("STATISTICS")
    print("="*60)
    print(f"\nTotal tasks: {stats['total_tasks']}")
    print(f"  ✓ Completed: {stats['completed']}")
    print(f"  ✗ Failed: {stats['failed']}")
    print(f"  ⏳ Pending: {stats['pending']}")
    print(f"Total execution time: {stats['total_execution_time']:.3f}s")
    print("="*60)


def print_status(interface):
    """Print complete system status"""
    interface.print_status()


def print_help():
    """Print help information"""
    print("\n" + "="*60)
    print("HELP")
    print("="*60)
    print("""
1. List agents
   View all registered agents and their capabilities.

2. List tasks
   View all submitted tasks and their current status.

3. Submit task
   Create a new task. You'll be prompted for:
   - Task name
   - Task type (calculate, log, alert, email)
   - Priority level
   - Task-specific parameters

4. Execute task
   Execute a single pending task.

5. Execute all tasks
   Execute all pending tasks in sequence.

6. View statistics
   Display system statistics (task counts, execution time).

7. View system status
   Display complete system status (agents, tasks, stats).

8. Help
   Display this help message.

9. Exit
   Exit the program.

AVAILABLE TASK TYPES:
  - calculate: Evaluate mathematical expressions
  - log: Log messages
  - alert: Send alerts
  - email: Send emails

EXAMPLES:
  Name: Process data
  Type: calculate
  Expression: 2 ** 10
  Result: 1024
""")
    print("="*60)


def main():
    """Main interactive loop"""
    interface = AgentInterface()

    # Register custom agents
    interface.register_agent(LoggerAgent())
    interface.register_agent(NotificationAgent())

    print("\n" + "="*60)
    print("MULTI-AGENT SYSTEM")
    print("="*60)
    print("Welcome to the Multi-Agent System!")
    print("Type '8' for help or '9' to exit.")
    print("="*60)

    while True:
        print_menu()
        choice = input().strip()

        if choice == "1":
            print_agents(interface)
        elif choice == "2":
            print_tasks(interface)
        elif choice == "3":
            submit_task(interface)
        elif choice == "4":
            execute_single_task(interface)
        elif choice == "5":
            execute_all_tasks(interface)
        elif choice == "6":
            print_statistics(interface)
        elif choice == "7":
            print_status(interface)
        elif choice == "8":
            print_help()
        elif choice == "9":
            print("\nGoodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted. Goodbye!")
        sys.exit(0)
