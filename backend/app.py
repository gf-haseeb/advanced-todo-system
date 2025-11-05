"""Flask REST API for advanced-task-management-suite."""

from flask import Flask, jsonify, request
from flask_cors import CORS
from my_todo_lib.manager import TaskManager
from my_todo_lib.core.task import Task
from my_todo_lib.core.constants import (
    TaskStatus,
    Priority,
)
from backend.config import (
    DEBUG,
    HOST,
    PORT,
    CORS_ORIGINS,
    API_PREFIX,
)

# Initialize Flask app
app = Flask(__name__)
CORS(app, origins=CORS_ORIGINS)

# Initialize TaskManager
manager = TaskManager()


# =====================================================================
# Health Check Endpoint
# =====================================================================

@app.route(f'{API_PREFIX}/health', methods=['GET'])
def health_check() -> dict:
    """Check API health and status.

    Returns:
        dict: Health status information with timestamp.
    """
    return jsonify({
        'status': 'healthy',
        'message': 'API is running',
        'version': '0.1.0'
    }), 200


# =====================================================================
# Task Endpoints
# =====================================================================

@app.route(f'{API_PREFIX}/tasks', methods=['GET'])
def get_all_tasks() -> tuple:
    """Get all tasks across all lists.

    Returns:
        tuple: JSON response with list of tasks and HTTP status code.
    """
    try:
        all_tasks = []
        for task_list in manager.get_lists():
            tasks = manager.get_tasks(task_list.id)
            all_tasks.extend(tasks)
        
        tasks_data = [{'id': t.id, 'title': t.title, 'status': t.status, 
                       'priority': t.priority} for t in all_tasks]
        return jsonify({
            'success': True,
            'data': tasks_data,
            'count': len(tasks_data)
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route(f'{API_PREFIX}/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id: int) -> tuple:
    """Get a specific task by ID.

    Args:
        task_id (int): The task ID to retrieve.

    Returns:
        tuple: JSON response with task data and HTTP status code.
    """
    try:
        # Search across all lists
        for task_list in manager.get_lists():
            task = manager.get_task(task_list.id, task_id)
            if task:
                return jsonify({
                    'success': True,
                    'data': {'id': task.id, 'title': task.title, 
                            'status': task.status, 'priority': task.priority}
                }), 200
        
        return jsonify({
            'success': False,
            'error': f'Task {task_id} not found'
        }), 404

    except KeyError as e:
        return jsonify({
            'success': False,
            'error': f'Task not found: {str(e)}'
        }), 404

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route(f'{API_PREFIX}/tasks', methods=['POST'])
def create_task() -> tuple:
    """Create a new task.

    Request Body:
        {
            "list_id": 1,
            "title": "Task title",
            "description": "Optional description",
            "priority": "high"
        }

    Returns:
        tuple: JSON response with created task and HTTP status 201.
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body is empty'
            }), 400

        if 'list_id' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required field: list_id'
            }), 400

        if 'title' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required field: title'
            }), 400

        task = Task(
            title=data['title'],
            description=data.get('description', '')
        )
        manager.add_task_to_list(data['list_id'], task)
        manager.save()

        return jsonify({
            'success': True,
            'message': 'Task created successfully',
            'data': {'id': task.id, 'title': task.title, 
                    'status': task.status, 'priority': task.priority}
        }), 201

    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

    except KeyError as e:
        return jsonify({
            'success': False,
            'error': f'Invalid list: {str(e)}'
        }), 404

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route(f'{API_PREFIX}/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id: int) -> tuple:
    """Update an existing task.

    Args:
        task_id (int): The task ID to update.

    Request Body (all optional):
        {
            "title": "New title",
            "description": "New description",
            "status": "in_progress",
            "priority": "high"
        }

    Returns:
        tuple: JSON response with updated task and HTTP status 200.
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body is empty'
            }), 400

        # Find task in all lists and update it
        for task_list in manager.get_lists():
            task = manager.get_task(task_list.id, task_id)
            if task:
                manager.update_task(task_list.id, task_id, **data)
                return jsonify({
                    'success': True,
                    'message': 'Task updated successfully',
                    'data': {'id': task.id, 'title': task.title, 
                            'status': task.status, 'priority': task.priority}
                }), 200
        
        return jsonify({
            'success': False,
            'error': f'Task {task_id} not found'
        }), 404

    except KeyError as e:
        return jsonify({
            'success': False,
            'error': f'Task not found: {str(e)}'
        }), 404

    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route(f'{API_PREFIX}/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id: int) -> tuple:
    """Delete a task.

    Args:
        task_id (int): The task ID to delete.

    Returns:
        tuple: JSON response with success message and HTTP status 200.
    """
    try:
        # Find and delete task from all lists
        for task_list in manager.get_lists():
            task = manager.get_task(task_list.id, task_id)
            if task:
                manager.delete_task(task_list.id, task_id)
                return jsonify({
                    'success': True,
                    'message': f'Task {task_id} deleted successfully'
                }), 200
        
        return jsonify({
            'success': False,
            'error': f'Task {task_id} not found'
        }), 404

    except KeyError as e:
        return jsonify({
            'success': False,
            'error': f'Task not found: {str(e)}'
        }), 404

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route(f'{API_PREFIX}/tasks/<int:task_id>/move', methods=['POST'])
def move_task(task_id: int) -> tuple:
    """Move a task to another list.

    Args:
        task_id (int): The task ID to move.

    Request Body:
        {
            "source_list_id": 1,
            "target_list_id": 2
        }

    Returns:
        tuple: JSON response with moved task and HTTP status 200.
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body is empty'
            }), 400

        if 'source_list_id' not in data or 'target_list_id' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required fields: source_list_id, target_list_id'
            }), 400

        task = manager.move_task_to_list(
            source_list_id=data['source_list_id'],
            task_id=task_id,
            target_list_id=data['target_list_id']
        )

        return jsonify({
            'success': True,
            'message': 'Task moved successfully',
            'data': task.to_dict()
        }), 200

    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

    except KeyError as e:
        return jsonify({
            'success': False,
            'error': f'Resource not found: {str(e)}'
        }), 404

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# =====================================================================
# List Endpoints
# =====================================================================

@app.route(f'{API_PREFIX}/lists', methods=['GET'])
def get_all_lists() -> tuple:
    """Get all task lists.

    Returns:
        tuple: JSON response with list of all lists and HTTP status code.
    """
    try:
        lists = manager.get_lists()
        lists_data = [{'id': tl.id, 'name': tl.name, 'description': tl.description} 
                     for tl in lists]

        return jsonify({
            'success': True,
            'data': lists_data,
            'count': len(lists_data)
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route(f'{API_PREFIX}/lists/<int:list_id>', methods=['GET'])
def get_list(list_id: int) -> tuple:
    """Get a specific list by ID.

    Args:
        list_id (int): The list ID to retrieve.

    Returns:
        tuple: JSON response with list data and HTTP status code.
    """
    try:
        task_list = manager.get_list(list_id)

        if not task_list:
            return jsonify({
                'success': False,
                'error': f'List {list_id} not found'
            }), 404

        return jsonify({
            'success': True,
            'data': {'id': task_list.id, 'name': task_list.name,
                    'description': task_list.description}
        }), 200

    except KeyError as e:
        return jsonify({
            'success': False,
            'error': f'List not found: {str(e)}'
        }), 404

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route(f'{API_PREFIX}/lists', methods=['POST'])
def create_list() -> tuple:
    """Create a new list.

    Request Body:
        {
            "name": "Work",
            "description": "Work-related tasks"
        }

    Returns:
        tuple: JSON response with created list and HTTP status 201.
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body is empty'
            }), 400

        if 'name' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required field: name'
            }), 400

        task_list = manager.create_list(
            name=data['name'],
            description=data.get('description', '')
        )

        return jsonify({
            'success': True,
            'message': 'List created successfully',
            'data': {'id': task_list.id, 'name': task_list.name,
                    'description': task_list.description}
        }), 201

    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route(f'{API_PREFIX}/lists/<int:list_id>', methods=['PUT'])
def update_list(list_id: int) -> tuple:
    """Update an existing list.

    Args:
        list_id (int): The list ID to update.

    Request Body (all optional):
        {
            "name": "New name",
            "description": "New description"
        }

    Returns:
        tuple: JSON response with updated list and HTTP status 200.
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body is empty'
            }), 400

        task_list = manager.get_list(list_id)
        if not task_list:
            return jsonify({
                'success': False,
                'error': f'List {list_id} not found'
            }), 404

        # Update using rename_list for name
        if 'name' in data:
            manager.rename_list(list_id, data['name'])
        
        # Update description if provided (check if method exists)
        if 'description' in data and hasattr(task_list, 'description'):
            task_list.description = data['description']

        task_list = manager.get_list(list_id)
        return jsonify({
            'success': True,
            'message': 'List updated successfully',
            'data': {'id': task_list.id, 'name': task_list.name,
                    'description': task_list.description}
        }), 200

    except KeyError as e:
        return jsonify({
            'success': False,
            'error': f'List not found: {str(e)}'
        }), 404

    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route(f'{API_PREFIX}/lists/<int:list_id>', methods=['DELETE'])
def delete_list(list_id: int) -> tuple:
    """Delete a list and all its tasks.

    Args:
        list_id (int): The list ID to delete.

    Returns:
        tuple: JSON response with success message and HTTP status 200.
    """
    try:
        manager.delete_list(list_id)

        return jsonify({
            'success': True,
            'message': f'List {list_id} deleted successfully'
        }), 200

    except KeyError as e:
        return jsonify({
            'success': False,
            'error': f'List not found: {str(e)}'
        }), 404

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# =====================================================================
# Error Handlers
# =====================================================================

@app.errorhandler(400)
def bad_request(error) -> tuple:
    """Handle 400 Bad Request errors."""
    return jsonify({
        'success': False,
        'error': 'Bad request',
        'message': str(error)
    }), 400


@app.errorhandler(404)
def not_found(error) -> tuple:
    """Handle 404 Not Found errors."""
    return jsonify({
        'success': False,
        'error': 'Resource not found',
        'message': str(error)
    }), 404


@app.errorhandler(500)
def internal_error(error) -> tuple:
    """Handle 500 Internal Server Error."""
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'message': str(error)
    }), 500


# =====================================================================
# Main Entry Point
# =====================================================================

if __name__ == '__main__':
    print(f"🚀 Starting API server on http://{HOST}:{PORT}")
    print(f"📚 API endpoints available at http://{HOST}:{PORT}{API_PREFIX}")
    print(f"Health check: http://{HOST}:{PORT}{API_PREFIX}/health")
    app.run(host=HOST, port=PORT, debug=DEBUG)
