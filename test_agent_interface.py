"""
Tests for Multi-Agent Interface
"""

import unittest
from multi_agent_interface import (
    AgentInterface,
    Agent,
    Task,
    TaskResult,
    TaskStatus,
    FileAgent,
    DataAgent,
    ComputeAgent,
    TaskManager,
)
import tempfile
import os


class TestAgent(unittest.TestCase):
    """Test basic agent functionality"""

    def test_file_agent_creation(self):
        agent = FileAgent()
        self.assertEqual(agent.name, "FileAgent")
        self.assertIn("read", agent.capabilities)

    def test_data_agent_creation(self):
        agent = DataAgent()
        self.assertEqual(agent.name, "DataAgent")
        self.assertIn("filter", agent.capabilities)

    def test_compute_agent_creation(self):
        agent = ComputeAgent()
        self.assertEqual(agent.name, "ComputeAgent")
        self.assertIn("calculate", agent.capabilities)


class TestFileAgent(unittest.TestCase):
    """Test FileAgent operations"""

    def setUp(self):
        self.agent = FileAgent()
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_can_handle(self):
        self.assertTrue(self.agent.can_handle("read"))
        self.assertTrue(self.agent.can_handle("write"))
        self.assertFalse(self.agent.can_handle("unknown"))

    def test_write_file(self):
        filepath = os.path.join(self.temp_dir, "test.txt")
        task = Task(
            id="test_1",
            name="Write test",
            task_type="write",
            params={"action": "write", "path": filepath, "content": "Hello, World!"},
        )

        result = self.agent.execute(task)
        self.assertTrue(result.success)
        self.assertEqual(self.agent.tasks_completed, 1)

        with open(filepath, "r") as f:
            content = f.read()
        self.assertEqual(content, "Hello, World!")

    def test_read_file(self):
        filepath = os.path.join(self.temp_dir, "test.txt")
        with open(filepath, "w") as f:
            f.write("Test content")

        task = Task(
            id="test_2",
            name="Read test",
            task_type="read",
            params={"action": "read", "path": filepath},
        )

        result = self.agent.execute(task)
        self.assertTrue(result.success)
        self.assertEqual(result.output, "Test content")

    def test_list_directory(self):
        task = Task(
            id="test_3",
            name="List test",
            task_type="list",
            params={"action": "list", "path": self.temp_dir},
        )

        result = self.agent.execute(task)
        self.assertTrue(result.success)
        self.assertIsInstance(result.output, list)


class TestDataAgent(unittest.TestCase):
    """Test DataAgent operations"""

    def setUp(self):
        self.agent = DataAgent()

    def test_filter_data(self):
        task = Task(
            id="test_4",
            name="Filter test",
            task_type="filter",
            params={
                "action": "filter",
                "data": [1, 2, 3, 4, 5],
                "condition": lambda x: x > 2,
            },
        )

        result = self.agent.execute(task)
        self.assertTrue(result.success)
        self.assertEqual(result.output, [3, 4, 5])

    def test_transform_data(self):
        task = Task(
            id="test_5",
            name="Transform test",
            task_type="transform",
            params={
                "action": "transform",
                "data": [1, 2, 3, 4, 5],
                "fn": lambda x: x ** 2,
            },
        )

        result = self.agent.execute(task)
        self.assertTrue(result.success)
        self.assertEqual(result.output, [1, 4, 9, 16, 25])

    def test_aggregate_data(self):
        task = Task(
            id="test_6",
            name="Aggregate test",
            task_type="aggregate",
            params={"action": "aggregate", "data": [1, 2, 3, 4, 5], "fn": sum},
        )

        result = self.agent.execute(task)
        self.assertTrue(result.success)
        self.assertEqual(result.output, 15)


class TestComputeAgent(unittest.TestCase):
    """Test ComputeAgent operations"""

    def setUp(self):
        self.agent = ComputeAgent()

    def test_calculate_expression(self):
        task = Task(
            id="test_7",
            name="Calculate test",
            task_type="calculate",
            params={
                "action": "calculate",
                "expression": "2 ** 10",
                "context": {},
            },
        )

        result = self.agent.execute(task)
        self.assertTrue(result.success)
        self.assertEqual(result.output, 1024)

    def test_calculate_with_context(self):
        task = Task(
            id="test_8",
            name="Calculate with context",
            task_type="calculate",
            params={
                "action": "calculate",
                "expression": "x + y",
                "context": {"x": 5, "y": 3},
            },
        )

        result = self.agent.execute(task)
        self.assertTrue(result.success)
        self.assertEqual(result.output, 8)


class TestTaskManager(unittest.TestCase):
    """Test TaskManager"""

    def setUp(self):
        self.manager = TaskManager()
        self.manager.register_agent(FileAgent())
        self.manager.register_agent(DataAgent())
        self.manager.register_agent(ComputeAgent())

    def test_register_agent(self):
        self.assertEqual(len(self.manager.agents), 3)
        self.assertIn("FileAgent", self.manager.agents)

    def test_add_task(self):
        task = Task(
            id="test_9",
            name="Test task",
            task_type="filter",
            params={"data": [1, 2, 3]},
        )

        task_id = self.manager.add_task(task)
        self.assertEqual(task_id, "test_9")
        self.assertIn("test_9", self.manager.tasks)

    def test_get_best_agent(self):
        task = Task(
            id="test_10",
            name="Test",
            task_type="filter",
            params={"data": [1, 2, 3]},
        )

        agent = self.manager.get_best_agent(task)
        self.assertIsNotNone(agent)
        self.assertEqual(agent.name, "DataAgent")

    def test_statistics(self):
        task = Task(
            id="test_11",
            name="Test",
            task_type="calculate",
            params={
                "action": "calculate",
                "expression": "2 ** 5",
                "context": {},
            },
        )

        self.manager.add_task(task)
        self.manager.execute_task("test_11")

        stats = self.manager.get_statistics()
        self.assertEqual(stats["total_tasks"], 1)
        self.assertEqual(stats["completed"], 1)


class TestAgentInterface(unittest.TestCase):
    """Test AgentInterface"""

    def setUp(self):
        self.interface = AgentInterface()

    def test_submit_task(self):
        task_id = self.interface.submit_task(
            name="Test",
            task_type="calculate",
            params={"action": "calculate", "expression": "1 + 1", "context": {}},
        )

        self.assertTrue(task_id.startswith("task_"))

    def test_get_agents(self):
        agents = self.interface.get_agents()
        self.assertIn("FileAgent", agents)
        self.assertIn("DataAgent", agents)

    def test_get_tasks(self):
        self.interface.submit_task(
            name="Test",
            task_type="filter",
            params={"data": [1, 2, 3], "condition": lambda x: x > 1},
        )

        tasks = self.interface.get_tasks()
        self.assertEqual(len(tasks), 1)

    def test_execute_task(self):
        task_id = self.interface.submit_task(
            name="Test",
            task_type="calculate",
            params={"action": "calculate", "expression": "2 + 2", "context": {}},
        )

        result = self.interface.execute_task(task_id)
        self.assertTrue(result["success"])
        self.assertEqual(result["output"], 4)

    def test_execute_all(self):
        self.interface.submit_task(
            name="Test 1",
            task_type="calculate",
            params={"action": "calculate", "expression": "2 + 2", "context": {}},
        )
        self.interface.submit_task(
            name="Test 2",
            task_type="calculate",
            params={"action": "calculate", "expression": "3 + 3", "context": {}},
        )

        results = self.interface.execute_all()
        self.assertEqual(len(results), 2)
        self.assertTrue(all(r["success"] for r in results))

    def test_statistics(self):
        self.interface.submit_task(
            name="Test",
            task_type="calculate",
            params={"action": "calculate", "expression": "2 + 2", "context": {}},
        )
        self.interface.execute_all()

        stats = self.interface.get_statistics()
        self.assertEqual(stats["total_tasks"], 1)
        self.assertEqual(stats["completed"], 1)


class TestTaskResult(unittest.TestCase):
    """Test TaskResult"""

    def test_task_result_success(self):
        result = TaskResult(
            task_id="test",
            success=True,
            output="Success",
            agent_name="TestAgent",
            execution_time=0.5,
        )

        self.assertTrue(result.success)
        self.assertEqual(result.output, "Success")

    def test_task_result_failure(self):
        result = TaskResult(
            task_id="test",
            success=False,
            output=None,
            error="Something went wrong",
            agent_name="TestAgent",
        )

        self.assertFalse(result.success)
        self.assertEqual(result.error, "Something went wrong")


class TestTaskStatus(unittest.TestCase):
    """Test TaskStatus enum"""

    def test_task_status_values(self):
        self.assertEqual(TaskStatus.PENDING.value, "pending")
        self.assertEqual(TaskStatus.IN_PROGRESS.value, "in_progress")
        self.assertEqual(TaskStatus.COMPLETED.value, "completed")


if __name__ == "__main__":
    unittest.main(verbosity=2)
