"""
Multi-Agent Interface for Task Delegation
Provides a flexible system for managing multiple agents and delegating tasks
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Type
from datetime import datetime
import json


class TaskStatus(Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class TaskResult:
    task_id: str
    success: bool
    output: Any
    error: Optional[str] = None
    agent_name: Optional[str] = None
    execution_time: float = 0.0


@dataclass
class Task:
    id: str
    name: str
    task_type: str
    priority: int = 0
    params: Dict[str, Any] = field(default_factory=dict)
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[TaskResult] = None
    created_at: datetime = field(default_factory=datetime.now)
    assigned_agent: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "task_type": self.task_type,
            "priority": self.priority,
            "params": self.params,
            "status": self.status.value,
            "assigned_agent": self.assigned_agent,
            "dependencies": self.dependencies,
        }


class Agent(ABC):
    """Base agent class"""

    def __init__(self, name: str, capabilities: List[str]):
        self.name = name
        self.capabilities = capabilities
        self.tasks_completed = 0
        self.tasks_failed = 0

    @abstractmethod
    def can_handle(self, task_type: str) -> bool:
        """Check if agent can handle task type"""
        pass

    @abstractmethod
    def execute(self, task: Task) -> TaskResult:
        """Execute a task"""
        pass

    def get_status(self) -> dict:
        return {
            "name": self.name,
            "capabilities": self.capabilities,
            "tasks_completed": self.tasks_completed,
            "tasks_failed": self.tasks_failed,
        }


class FileAgent(Agent):
    """Agent for file operations"""

    def __init__(self):
        super().__init__("FileAgent", ["read", "write", "delete", "list"])

    def can_handle(self, task_type: str) -> bool:
        return task_type in self.capabilities

    def execute(self, task: Task) -> TaskResult:
        import time
        start = time.time()

        try:
            action = task.params.get("action")

            if action == "read":
                with open(task.params["path"], "r") as f:
                    output = f.read()
            elif action == "write":
                with open(task.params["path"], "w") as f:
                    f.write(task.params["content"])
                output = f"File written: {task.params['path']}"
            elif action == "delete":
                import os
                os.remove(task.params["path"])
                output = f"File deleted: {task.params['path']}"
            elif action == "list":
                import os
                output = os.listdir(task.params.get("path", "."))
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


class DataAgent(Agent):
    """Agent for data processing"""

    def __init__(self):
        super().__init__("DataAgent", ["process", "transform", "filter", "aggregate"])

    def can_handle(self, task_type: str) -> bool:
        return task_type in self.capabilities

    def execute(self, task: Task) -> TaskResult:
        import time
        start = time.time()

        try:
            action = task.params.get("action")
            data = task.params.get("data", [])

            if action == "filter":
                condition = task.params.get("condition")
                output = [x for x in data if condition(x)]
            elif action == "transform":
                transform_fn = task.params.get("fn")
                output = [transform_fn(x) for x in data]
            elif action == "aggregate":
                agg_fn = task.params.get("fn")
                output = agg_fn(data)
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


class ComputeAgent(Agent):
    """Agent for computational tasks"""

    def __init__(self):
        super().__init__("ComputeAgent", ["calculate", "analyze", "optimize"])

    def can_handle(self, task_type: str) -> bool:
        return task_type in self.capabilities

    def execute(self, task: Task) -> TaskResult:
        import time
        start = time.time()

        try:
            action = task.params.get("action")

            if action == "calculate":
                expression = task.params.get("expression")
                output = eval(expression, {"__builtins__": {}}, task.params.get("context", {}))
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


class TaskManager:
    """Manages task queue and agent assignment"""

    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.tasks: Dict[str, Task] = {}
        self.task_queue: List[str] = []
        self.execution_history: List[TaskResult] = []

    def register_agent(self, agent: Agent) -> None:
        """Register an agent"""
        self.agents[agent.name] = agent

    def add_task(self, task: Task) -> str:
        """Add a task to the queue"""
        self.tasks[task.id] = task
        self.task_queue.append(task.id)
        return task.id

    def get_best_agent(self, task: Task) -> Optional[Agent]:
        """Find the best agent for a task"""
        capable_agents = [
            agent for agent in self.agents.values()
            if agent.can_handle(task.task_type)
        ]

        if not capable_agents:
            return None

        return min(capable_agents, key=lambda a: a.tasks_failed / (a.tasks_completed + 1))

    def execute_task(self, task_id: str) -> TaskResult:
        """Execute a single task"""
        task = self.tasks.get(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")

        agent = self.get_best_agent(task)
        if not agent:
            return TaskResult(
                task_id=task.id,
                success=False,
                output=None,
                error=f"No agent capable of handling task type: {task.task_type}",
            )

        task.status = TaskStatus.ASSIGNED
        task.assigned_agent = agent.name
        task.status = TaskStatus.IN_PROGRESS

        result = agent.execute(task)

        task.status = TaskStatus.COMPLETED if result.success else TaskStatus.FAILED
        task.result = result
        self.execution_history.append(result)

        return result

    def execute_all(self) -> List[TaskResult]:
        """Execute all pending tasks"""
        results = []
        for task_id in self.task_queue:
            if self.tasks[task_id].status == TaskStatus.PENDING:
                result = self.execute_task(task_id)
                results.append(result)
        return results

    def get_agent_status(self) -> Dict[str, dict]:
        """Get status of all agents"""
        return {name: agent.get_status() for name, agent in self.agents.items()}

    def get_task_status(self, task_id: str) -> dict:
        """Get status of a specific task"""
        task = self.tasks.get(task_id)
        if not task:
            return {}
        return task.to_dict()

    def get_statistics(self) -> dict:
        """Get execution statistics"""
        return {
            "total_tasks": len(self.tasks),
            "completed": sum(1 for t in self.tasks.values() if t.status == TaskStatus.COMPLETED),
            "failed": sum(1 for t in self.tasks.values() if t.status == TaskStatus.FAILED),
            "pending": sum(1 for t in self.tasks.values() if t.status == TaskStatus.PENDING),
            "total_execution_time": sum(r.execution_time for r in self.execution_history),
        }


class AgentInterface:
    """User interface for the multi-agent system"""

    def __init__(self):
        self.manager = TaskManager()
        self.task_counter = 0
        self._setup_default_agents()

    def _setup_default_agents(self):
        """Setup default agents"""
        self.manager.register_agent(FileAgent())
        self.manager.register_agent(DataAgent())
        self.manager.register_agent(ComputeAgent())

    def register_agent(self, agent: Agent) -> None:
        """Register a custom agent"""
        self.manager.register_agent(agent)

    def submit_task(
        self,
        name: str,
        task_type: str,
        params: Dict[str, Any],
        priority: int = 0,
    ) -> str:
        """Submit a new task"""
        task_id = f"task_{self.task_counter}"
        self.task_counter += 1

        task = Task(
            id=task_id,
            name=name,
            task_type=task_type,
            priority=priority,
            params=params,
        )

        return self.manager.add_task(task)

    def execute_task(self, task_id: str) -> dict:
        """Execute a specific task"""
        result = self.manager.execute_task(task_id)
        return {
            "success": result.success,
            "output": result.output,
            "error": result.error,
            "agent": result.agent_name,
            "time": result.execution_time,
        }

    def execute_all(self) -> List[dict]:
        """Execute all pending tasks"""
        results = self.manager.execute_all()
        return [
            {
                "task_id": r.task_id,
                "success": r.success,
                "output": r.output,
                "error": r.error,
                "agent": r.agent_name,
                "time": r.execution_time,
            }
            for r in results
        ]

    def get_agents(self) -> dict:
        """Get all registered agents"""
        return self.manager.get_agent_status()

    def get_tasks(self) -> List[dict]:
        """Get all tasks"""
        return [task.to_dict() for task in self.manager.tasks.values()]

    def get_statistics(self) -> dict:
        """Get system statistics"""
        return self.manager.get_statistics()

    def print_status(self):
        """Print system status"""
        stats = self.get_statistics()
        agents = self.get_agents()

        print("\n" + "="*60)
        print("MULTI-AGENT SYSTEM STATUS")
        print("="*60)
        print(f"\nTasks: {stats['total_tasks']} total")
        print(f"  ✓ Completed: {stats['completed']}")
        print(f"  ✗ Failed: {stats['failed']}")
        print(f"  ⏳ Pending: {stats['pending']}")
        print(f"  Total execution time: {stats['total_execution_time']:.2f}s")

        print(f"\nRegistered Agents:")
        for agent_name, status in agents.items():
            print(f"  • {agent_name}")
            print(f"    Capabilities: {', '.join(status['capabilities'])}")
            print(f"    Completed: {status['tasks_completed']}")
            print(f"    Failed: {status['tasks_failed']}")
        print("="*60 + "\n")


if __name__ == "__main__":
    interface = AgentInterface()

    task1 = interface.submit_task(
        "List files",
        "list",
        {"path": "/home/user/skills"},
    )

    task2 = interface.submit_task(
        "Filter data",
        "filter",
        {"data": [1, 2, 3, 4, 5, 6], "condition": lambda x: x > 3},
    )

    task3 = interface.submit_task(
        "Calculate",
        "calculate",
        {"expression": "2 ** 10", "context": {}},
    )

    interface.execute_all()
    interface.print_status()

    print("Task Results:")
    for task in interface.get_tasks():
        print(f"\n{task['name']} ({task['id']})")
        print(f"  Status: {task['status']}")
        print(f"  Agent: {task['assigned_agent']}")
