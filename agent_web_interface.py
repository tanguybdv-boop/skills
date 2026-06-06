"""
Web Interface for Multi-Agent System
REST API using Flask
"""

from flask import Flask, request, jsonify
from multi_agent_interface import AgentInterface, Agent, Task, TaskResult
import json
from datetime import datetime


app = Flask(__name__)
interface = AgentInterface()


@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok"}), 200


@app.route("/api/agents", methods=["GET"])
def get_agents():
    """Get all registered agents"""
    return jsonify(interface.get_agents()), 200


@app.route("/api/agents/register", methods=["POST"])
def register_agent():
    """Register a new agent (placeholder)"""
    data = request.json
    return jsonify({"message": "Agent registration endpoint"}), 201


@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    """Get all tasks"""
    tasks = interface.get_tasks()
    return jsonify({"tasks": tasks}), 200


@app.route("/api/tasks", methods=["POST"])
def submit_task():
    """Submit a new task"""
    data = request.json

    required_fields = ["name", "task_type", "params"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        task_id = interface.submit_task(
            name=data["name"],
            task_type=data["task_type"],
            params=data["params"],
            priority=data.get("priority", 0),
        )
        return jsonify({"task_id": task_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/tasks/<task_id>", methods=["GET"])
def get_task(task_id):
    """Get task status"""
    tasks = interface.get_tasks()
    task = next((t for t in tasks if t["id"] == task_id), None)

    if not task:
        return jsonify({"error": "Task not found"}), 404

    return jsonify(task), 200


@app.route("/api/tasks/<task_id>/execute", methods=["POST"])
def execute_task(task_id):
    """Execute a specific task"""
    try:
        result = interface.execute_task(task_id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/tasks/execute-all", methods=["POST"])
def execute_all_tasks():
    """Execute all pending tasks"""
    try:
        results = interface.execute_all()
        return jsonify({"results": results}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/statistics", methods=["GET"])
def get_statistics():
    """Get system statistics"""
    stats = interface.get_statistics()
    return jsonify(stats), 200


@app.route("/api/status", methods=["GET"])
def get_status():
    """Get complete system status"""
    return jsonify(
        {
            "agents": interface.get_agents(),
            "statistics": interface.get_statistics(),
            "timestamp": datetime.now().isoformat(),
        }
    ), 200


@app.route("/api/tasks/batch", methods=["POST"])
def submit_batch_tasks():
    """Submit multiple tasks at once"""
    data = request.json

    if not isinstance(data, list):
        return jsonify({"error": "Expected list of tasks"}), 400

    task_ids = []
    for task_data in data:
        try:
            task_id = interface.submit_task(
                name=task_data["name"],
                task_type=task_data["task_type"],
                params=task_data["params"],
                priority=task_data.get("priority", 0),
            )
            task_ids.append(task_id)
        except Exception as e:
            return jsonify({"error": f"Failed to create task: {str(e)}"}), 400

    return jsonify({"task_ids": task_ids}), 201


@app.route("/api/dashboard", methods=["GET"])
def dashboard():
    """Get dashboard data"""
    stats = interface.get_statistics()
    agents = interface.get_agents()
    tasks = interface.get_tasks()

    # Group tasks by status
    tasks_by_status = {}
    for task in tasks:
        status = task["status"]
        if status not in tasks_by_status:
            tasks_by_status[status] = []
        tasks_by_status[status].append(task)

    return jsonify(
        {
            "statistics": stats,
            "agents": agents,
            "tasks_by_status": tasks_by_status,
            "timestamp": datetime.now().isoformat(),
        }
    ), 200


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    print("\n" + "="*60)
    print("MULTI-AGENT WEB INTERFACE")
    print("="*60)
    print("\nAvailable endpoints:")
    print("  GET  /api/health")
    print("  GET  /api/agents")
    print("  GET  /api/tasks")
    print("  POST /api/tasks")
    print("  GET  /api/tasks/<id>")
    print("  POST /api/tasks/<id>/execute")
    print("  POST /api/tasks/execute-all")
    print("  GET  /api/statistics")
    print("  GET  /api/status")
    print("  POST /api/tasks/batch")
    print("  GET  /api/dashboard")
    print("\nStarting server on http://127.0.0.1:5000")
    print("="*60 + "\n")

    app.run(debug=True, port=5000)
