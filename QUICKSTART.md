# Quick Start - Multi-Agent Interface

## Installation

```bash
pip install -r requirements_agents.txt
```

## 5-Minute Overview

### 1. Basic Usage

```python
from multi_agent_interface import AgentInterface

# Create interface
interface = AgentInterface()

# Submit a task
task_id = interface.submit_task(
    name="Calculate",
    task_type="calculate",
    params={
        "action": "calculate",
        "expression": "2 + 2",
        "context": {}
    }
)

# Execute it
result = interface.execute_task(task_id)
print(result)  # {'success': True, 'output': 4, ...}
```

### 2. Custom Agent

```python
from multi_agent_interface import Agent, Task, TaskResult
import time

class MyAgent(Agent):
    def __init__(self):
        super().__init__("MyAgent", ["my_task"])
    
    def can_handle(self, task_type):
        return task_type in self.capabilities
    
    def execute(self, task: Task) -> TaskResult:
        start = time.time()
        try:
            output = f"Processing: {task.params['data']}"
            self.tasks_completed += 1
            return TaskResult(
                task_id=task.id,
                success=True,
                output=output,
                agent_name=self.name,
                execution_time=time.time() - start
            )
        except Exception as e:
            self.tasks_failed += 1
            return TaskResult(
                task_id=task.id,
                success=False,
                output=None,
                error=str(e),
                agent_name=self.name,
                execution_time=time.time() - start
            )

# Register and use
interface.register_agent(MyAgent())

task_id = interface.submit_task(
    name="My Task",
    task_type="my_task",
    params={"data": "Hello"}
)

interface.execute_task(task_id)
```

### 3. Built-in Agents

#### FileAgent
```python
# Read file
task_id = interface.submit_task(
    "Read file",
    "read",
    {"action": "read", "path": "/path/to/file.txt"}
)

# Write file
task_id = interface.submit_task(
    "Write file",
    "write",
    {
        "action": "write",
        "path": "/path/to/file.txt",
        "content": "Hello, World!"
    }
)

# List directory
task_id = interface.submit_task(
    "List files",
    "list",
    {"action": "list", "path": "/path"}
)
```

#### DataAgent
```python
# Filter data
task_id = interface.submit_task(
    "Filter",
    "filter",
    {
        "action": "filter",
        "data": [1, 2, 3, 4, 5],
        "condition": lambda x: x > 2
    }
)

# Transform data
task_id = interface.submit_task(
    "Transform",
    "transform",
    {
        "action": "transform",
        "data": [1, 2, 3],
        "fn": lambda x: x ** 2
    }
)

# Aggregate data
task_id = interface.submit_task(
    "Sum",
    "aggregate",
    {
        "action": "aggregate",
        "data": [1, 2, 3, 4, 5],
        "fn": sum
    }
)
```

#### ComputeAgent
```python
# Calculate
task_id = interface.submit_task(
    "Fibonacci",
    "calculate",
    {
        "action": "calculate",
        "expression": "sum([1, 1, 2, 3, 5, 8])",
        "context": {}
    }
)
```

## Running Examples

### Run All Examples
```bash
python agent_examples.py
```

### Interactive Shell
```bash
python run_interactive.py
```

### Web Interface
```bash
pip install flask
python agent_web_interface.py
# Visit http://localhost:5000
```

### Run Tests
```bash
python -m unittest test_agent_interface -v
```

## API Examples

### Using the REST API

```bash
# Health check
curl http://localhost:5000/api/health

# Get agents
curl http://localhost:5000/api/agents

# Submit task
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Calculate",
    "task_type": "calculate",
    "params": {
      "action": "calculate",
      "expression": "10 ** 2",
      "context": {}
    }
  }'

# Get tasks
curl http://localhost:5000/api/tasks

# Execute task
curl -X POST http://localhost:5000/api/tasks/task_0/execute

# Get statistics
curl http://localhost:5000/api/statistics
```

## Common Patterns

### Batch Processing
```python
# Submit multiple tasks
task_ids = []
for i in range(10):
    task_id = interface.submit_task(
        f"Task {i}",
        "calculate",
        {
            "action": "calculate",
            "expression": f"{i} + {i}",
            "context": {}
        }
    )
    task_ids.append(task_id)

# Execute all
results = interface.execute_all()
print(f"Completed {len(results)} tasks")
```

### Priority Handling
```python
# High priority
interface.submit_task(
    "Urgent",
    "log",
    {"action": "log", "message": "Urgent task"},
    priority=10
)

# Normal priority
interface.submit_task(
    "Normal",
    "log",
    {"action": "log", "message": "Normal task"},
    priority=0
)
```

### Error Handling
```python
result = interface.execute_task(task_id)

if result['success']:
    print(f"Success: {result['output']}")
else:
    print(f"Error: {result['error']}")
```

### Status Checking
```python
# Get all tasks
tasks = interface.get_tasks()

# Get specific task
for task in tasks:
    if task['id'] == 'task_0':
        print(f"Status: {task['status']}")
        print(f"Agent: {task['assigned_agent']}")

# Get statistics
stats = interface.get_statistics()
print(f"Completed: {stats['completed']}/{stats['total_tasks']}")
```

## Troubleshooting

### Task Failed
Check the error message in the result:
```python
result = interface.execute_task(task_id)
if not result['success']:
    print(result['error'])
```

### No Agent Found
Make sure the task_type matches an agent's capabilities:
```python
agents = interface.get_agents()
for name, info in agents.items():
    print(f"{name}: {info['capabilities']}")
```

### Lambda Issues
When using DataAgent with lambda functions, make sure the lambda is passed directly (not serialized):
```python
# ✓ Good - pass function directly
interface.submit_task(
    "Filter",
    "filter",
    {"action": "filter", "data": [1, 2, 3], "condition": lambda x: x > 1}
)

# ✗ Bad - don't serialize lambdas
params = json.dumps({"condition": "lambda x: x > 1"})
```

## Files

- `multi_agent_interface.py` - Core system
- `agent_examples.py` - Example agents and usage
- `agent_web_interface.py` - REST API server
- `test_agent_interface.py` - Unit tests
- `run_interactive.py` - Interactive shell
- `AGENT_INTERFACE_README.md` - Full documentation
- `QUICKSTART.md` - This file

## Next Steps

1. Read `AGENT_INTERFACE_README.md` for detailed documentation
2. Run examples: `python agent_examples.py`
3. Try interactive shell: `python run_interactive.py`
4. Create your own agents
5. Deploy with Flask: `python agent_web_interface.py`
