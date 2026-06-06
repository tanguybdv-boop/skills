"""
Examples of using the Multi-Agent Interface
"""

from multi_agent_interface import (
    AgentInterface,
    Agent,
    Task,
    TaskResult,
)


class LoggerAgent(Agent):
    """Custom agent for logging tasks"""

    def __init__(self):
        super().__init__("LoggerAgent", ["log", "alert"])

    def can_handle(self, task_type: str) -> bool:
        return task_type in self.capabilities

    def execute(self, task: Task) -> TaskResult:
        import time
        start = time.time()

        try:
            action = task.params.get("action")
            message = task.params.get("message")
            level = task.params.get("level", "INFO")

            output = f"[{level}] {message}"

            if action == "log":
                print(output)
            elif action == "alert":
                print(f"🚨 ALERT: {output}")

            self.tasks_completed += 1
            return TaskResult(
                task_id=task.id,
                success=True,
                output=output,
                agent_name=self.name,
                execution_time=time.time() - start,
            )
        except Exception as e:
            self.tasks_failed += 1
            return TaskResult(
                task_id=task.id,
                success=False,
                output=None,
                error=str(e),
                agent_name=self.name,
                execution_time=time.time() - start,
            )


class NotificationAgent(Agent):
    """Custom agent for sending notifications"""

    def __init__(self):
        super().__init__("NotificationAgent", ["email", "slack", "webhook"])

    def can_handle(self, task_type: str) -> bool:
        return task_type in self.capabilities

    def execute(self, task: Task) -> TaskResult:
        import time
        start = time.time()

        try:
            action = task.params.get("action")
            recipient = task.params.get("recipient")
            message = task.params.get("message")

            if action == "email":
                output = f"Email sent to {recipient}: {message}"
            elif action == "slack":
                output = f"Slack message sent to {recipient}: {message}"
            elif action == "webhook":
                output = f"Webhook triggered: {message}"
            else:
                raise ValueError(f"Unknown action: {action}")

            self.tasks_completed += 1
            return TaskResult(
                task_id=task.id,
                success=True,
                output=output,
                agent_name=self.name,
                execution_time=time.time() - start,
            )
        except Exception as e:
            self.tasks_failed += 1
            return TaskResult(
                task_id=task.id,
                success=False,
                output=None,
                error=str(e),
                agent_name=self.name,
                execution_time=time.time() - start,
            )


def example_1_basic_tasks():
    """Example 1: Basic task execution"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Task Execution")
    print("="*60)

    interface = AgentInterface()

    # Submit tasks
    task1 = interface.submit_task(
        "Process numbers",
        "filter",
        {
            "data": list(range(1, 11)),
            "condition": lambda x: x % 2 == 0,
        },
    )

    task2 = interface.submit_task(
        "Calculate fibonacci",
        "calculate",
        {
            "expression": "sum([1, 1, 2, 3, 5, 8, 13])",
            "context": {},
        },
    )

    # Execute all
    interface.execute_all()

    # Show results
    print("\nResults:")
    for task in interface.get_tasks():
        result = task.get("result") if isinstance(task, dict) else None
        print(f"  {task['name']}: {task['status']}")

    interface.print_status()


def example_2_custom_agents():
    """Example 2: Using custom agents"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Custom Agents")
    print("="*60)

    interface = AgentInterface()

    # Register custom agents
    interface.register_agent(LoggerAgent())
    interface.register_agent(NotificationAgent())

    # Submit tasks
    task1 = interface.submit_task(
        "Log startup",
        "log",
        {"action": "log", "message": "System started", "level": "INFO"},
    )

    task2 = interface.submit_task(
        "Alert critical error",
        "alert",
        {"action": "alert", "message": "Database connection failed"},
    )

    task3 = interface.submit_task(
        "Send notification",
        "email",
        {
            "action": "email",
            "recipient": "admin@example.com",
            "message": "Task completed successfully",
        },
    )

    # Execute all
    interface.execute_all()

    interface.print_status()


def example_3_mixed_workload():
    """Example 3: Mixed workload with multiple task types"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Mixed Workload")
    print("="*60)

    interface = AgentInterface()
    interface.register_agent(LoggerAgent())

    # Create a mix of different task types
    tasks = [
        interface.submit_task(
            "Start processing",
            "log",
            {"action": "log", "message": "Starting data pipeline"},
        ),
        interface.submit_task(
            "Filter large numbers",
            "filter",
            {
                "data": list(range(1, 101)),
                "condition": lambda x: x > 50,
            },
        ),
        interface.submit_task(
            "Calculate sum",
            "calculate",
            {"expression": "sum(range(1, 101))", "context": {}},
        ),
        interface.submit_task(
            "Completion notification",
            "log",
            {"action": "log", "message": "Pipeline completed successfully"},
        ),
    ]

    # Execute all tasks
    results = interface.execute_all()

    print("\nExecution Details:")
    for result in results:
        if result.get("success"):
            print(f"  ✓ {result.get('output', 'Task completed')}")
        else:
            print(f"  ✗ Error: {result.get('error')}")

    interface.print_status()


def example_4_priority_handling():
    """Example 4: Task priority (ordered execution)"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Priority Handling")
    print("="*60)

    interface = AgentInterface()

    # Submit tasks with different priorities
    priority_tasks = [
        (
            interface.submit_task(
                "Low priority task",
                "log",
                {"action": "log", "message": "This is low priority"},
                priority=1,
            ),
            1,
        ),
        (
            interface.submit_task(
                "High priority task",
                "log",
                {"action": "log", "message": "This is high priority"},
                priority=10,
            ),
            10,
        ),
        (
            interface.submit_task(
                "Medium priority task",
                "log",
                {"action": "log", "message": "This is medium priority"},
                priority=5,
            ),
            5,
        ),
    ]

    # Sort by priority and execute
    priority_tasks.sort(key=lambda x: x[1], reverse=True)

    print("\nExecuting tasks in priority order:")
    for task_id, priority in priority_tasks:
        result = interface.execute_task(task_id)
        print(f"  [Priority {priority}] {result.get('output')}")

    interface.print_status()


if __name__ == "__main__":
    example_1_basic_tasks()
    example_2_custom_agents()
    example_3_mixed_workload()
    example_4_priority_handling()
