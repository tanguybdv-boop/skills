# Multi-Agent System Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface Layer                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────┐   ┌──────────────────┐                │
│  │ AgentInterface   │   │  Web Interface   │                │
│  │ (Interactive)    │   │ (REST API)       │                │
│  └────────┬─────────┘   └────────┬─────────┘                │
│           │                      │                           │
└───────────┼──────────────────────┼──────────────────────────┘
            │                      │
            └──────────┬───────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                   Task Manager                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ Task Queue Management                               │    │
│  │ • Task submission                                   │    │
│  │ • Task prioritization                               │    │
│  │ • Dependency tracking                               │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ Agent Orchestration                                 │    │
│  │ • Agent capability matching                         │    │
│  │ • Load balancing                                    │    │
│  │ • Performance tracking                              │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└──────────────┬──────────────────────────────────────────────┘
               │
     ┌─────────┼─────────┬──────────────┐
     │         │         │              │
┌────▼──┐  ┌──▼────┐  ┌─▼─────┐  ┌────▼─────┐
│ File  │  │ Data  │  │Compute│  │  Custom  │
│Agent  │  │Agent  │  │Agent  │  │ Agents   │
└───────┘  └───────┘  └───────┘  └──────────┘
     │         │         │              │
     └─────────┼─────────┼──────────────┘
               │
┌──────────────▼──────────────────────────────────────────────┐
│                    Execution Layer                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  File Operations  │  Data Processing  │  Computation       │
│  ─────────────── │  ──────────────── │  ─────────────     │
│  • read           │  • filter         │  • calculate       │
│  • write          │  • transform      │  • math expr       │
│  • delete         │  • aggregate      │                    │
│  • list           │  • analyze        │                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Component Hierarchy

### 1. Task Class
```
Task
├── id: str
├── name: str
├── task_type: str
├── priority: int
├── params: Dict
├── status: TaskStatus
├── assigned_agent: str
├── dependencies: List[str]
└── result: TaskResult
```

### 2. TaskStatus Enum
```
TaskStatus
├── PENDING
├── ASSIGNED
├── IN_PROGRESS
├── COMPLETED
├── FAILED
└── CANCELLED
```

### 3. Agent (Abstract Base)
```
Agent
├── __init__(name, capabilities)
├── can_handle(task_type) → bool
├── execute(task) → TaskResult
└── get_status() → dict
```

### 4. TaskManager
```
TaskManager
├── agents: Dict[str, Agent]
├── tasks: Dict[str, Task]
├── task_queue: List[str]
├── execution_history: List[TaskResult]
├── register_agent(agent)
├── add_task(task) → str
├── execute_task(task_id) → TaskResult
├── execute_all() → List[TaskResult]
├── get_best_agent(task) → Agent
└── get_statistics() → dict
```

### 5. AgentInterface
```
AgentInterface
├── manager: TaskManager
├── task_counter: int
├── submit_task(...) → str
├── execute_task(task_id) → dict
├── execute_all() → List[dict]
├── register_agent(agent)
├── get_agents() → dict
├── get_tasks() → List[dict]
├── get_statistics() → dict
└── print_status()
```

## Data Flow Diagram

```
┌─────────────────┐
│  User Input     │
│  (Task Params)  │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│ AgentInterface.         │
│ submit_task()           │
│ • Creates Task object   │
│ • Assigns ID            │
│ • Adds to queue         │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ TaskManager             │
│ • Stores task           │
│ • Queues task_id        │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ get_best_agent()        │
│ • Find capable agents   │
│ • Pick least busy       │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ Agent.execute()         │
│ • Process task          │
│ • Generate result       │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ TaskResult              │
│ • Success flag          │
│ • Output data           │
│ • Execution time        │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ Update Task Status      │
│ • Mark COMPLETED/FAILED │
│ • Assign result         │
│ • Store in history      │
└─────────────────────────┘
```

## Built-in Agents

### FileAgent
- **Capabilities**: read, write, delete, list
- **Purpose**: File system operations
- **Task Params**:
  - action: 'read', 'write', 'delete', 'list'
  - path: file or directory path
  - content: (for write) file content

### DataAgent
- **Capabilities**: process, transform, filter, aggregate
- **Purpose**: Data manipulation
- **Task Params**:
  - action: 'filter', 'transform', 'aggregate'
  - data: list of items
  - condition/fn: operation function

### ComputeAgent
- **Capabilities**: calculate, analyze, optimize
- **Purpose**: Mathematical calculations
- **Task Params**:
  - action: 'calculate'
  - expression: math expression string
  - context: variables dict

## Agent Selection Algorithm

```python
def get_best_agent(task):
    # Filter agents by capability
    capable = [a for a in agents if a.can_handle(task.type)]
    
    if not capable:
        return None
    
    # Select by success rate (completion - failures)
    return min(capable, key=lambda a: a.failed / (a.completed + 1))
```

## Execution Flow

```
Task Submitted
     │
     ▼
Validate Task
     │
     ├─ Invalid? ─► Return Error
     │
     ▼
Find Available Agent
     │
     ├─ No Agent? ─► Return Error
     │
     ▼
Assign Task to Agent
     │
     ▼
Agent Executes Task
     │
     ├─ Success? ─────┐
     │                │
     │ Yes            No
     │                │
     ▼                ▼
Update Status    Mark as Failed
(COMPLETED)      (FAILED)
     │                │
     └────────┬───────┘
              │
              ▼
Record Result
     │
     ▼
Update Statistics
     │
     ▼
Return TaskResult
```

## Request/Response Cycle (REST API)

```
┌─────────────────────┐
│  HTTP Client        │
│  (Browser/CLI)      │
└──────────┬──────────┘
           │
           │ POST /api/tasks
           │ {name, task_type, params}
           │
           ▼
┌──────────────────────────────┐
│  Flask Web Server            │
│  submit_task()               │
└──────────┬───────────────────┘
           │
           │ task_id
           │
           ▼
┌──────────────────────────────┐
│  TaskManager                 │
│  add_task()                  │
└──────────┬───────────────────┘
           │
           │ Returns task_id
           │
           ▼
┌──────────────────────────────┐
│  HTTP Response (201 Created) │
│  {task_id: "task_0"}         │
└──────────────────────────────┘
```

## Concurrency Model

Current: **Sequential Execution**
- Tasks executed one at a time
- Agent processes each task fully
- Results stored in order

Future: **Async Execution**
- Multiple tasks per agent
- Parallel agent execution
- Event-driven architecture

## Scalability Considerations

### Current Limits
- ~100 concurrent tasks (memory)
- ~50 agents (reasonable)
- Single-threaded execution

### Optimization Opportunities
1. **Async/await** for concurrent execution
2. **Task batching** for similar tasks
3. **Agent pooling** for resource management
4. **Database persistence** for task history
5. **Redis** for distributed task queue

## Extension Points

### Creating Custom Agents
Inherit from `Agent` and implement:
- `can_handle(task_type)` 
- `execute(task)` → `TaskResult`

### Custom Task Types
1. Define task_type name
2. Implement handler agent
3. Register with interface

### Custom Execution Modes
1. Modify `TaskManager.get_best_agent()`
2. Implement custom routing logic
3. Add metrics/monitoring

## Configuration

```python
# Agent-specific configuration
interface = AgentInterface()
interface.manager.agents["FileAgent"].timeout = 30
interface.manager.agents["ComputeAgent"].max_retries = 3

# Task Manager configuration
interface.manager.task_queue.max_size = 1000
```

## Monitoring & Observability

```python
# Get statistics
stats = interface.get_statistics()
# {
#   'total_tasks': 100,
#   'completed': 85,
#   'failed': 10,
#   'pending': 5,
#   'total_execution_time': 42.5
# }

# Get agent status
agents = interface.get_agents()
# {
#   'FileAgent': {
#     'tasks_completed': 50,
#     'tasks_failed': 2,
#     'capabilities': ['read', 'write', ...]
#   },
#   ...
# }

# Get task history
results = interface.manager.execution_history
```
