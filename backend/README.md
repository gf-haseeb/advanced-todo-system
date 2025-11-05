# REST API Backend

Complete REST API backend for the Advanced Task Management Suite.

## 🚀 Quick Start

### 1. Install Backend Dependencies

```bash
pip install -r backend/requirements.txt
```

### 2. Run the Server

```bash
python -m backend.app
```

Server will start on `http://localhost:5000`

### 3. Test the API

Health check:
```bash
curl http://localhost:5000/api/v1/health
```

---

## 📚 API Documentation

### Base URL
```
http://localhost:5000/api/v1
```

### All Endpoints

#### Health Check
**GET** `/health`
```bash
curl http://localhost:5000/api/v1/health
```

#### Tasks - Get All
**GET** `/tasks`
```bash
curl http://localhost:5000/api/v1/tasks
```

#### Tasks - Get One
**GET** `/tasks/<task_id>`
```bash
curl http://localhost:5000/api/v1/tasks/1
```

#### Tasks - Create
**POST** `/tasks`
```bash
curl -X POST http://localhost:5000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "list_id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "priority": "medium"
  }'
```

#### Tasks - Update
**PUT** `/tasks/<task_id>`
```bash
curl -X PUT http://localhost:5000/api/v1/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "completed", "priority": "high"}'
```

#### Tasks - Delete
**DELETE** `/tasks/<task_id>`
```bash
curl -X DELETE http://localhost:5000/api/v1/tasks/1
```

#### Tasks - Move to Another List
**POST** `/tasks/<task_id>/move`
```bash
curl -X POST http://localhost:5000/api/v1/tasks/1/move \
  -H "Content-Type: application/json" \
  -d '{
    "source_list_id": 1,
    "target_list_id": 2
  }'
```

#### Lists - Get All
**GET** `/lists`
```bash
curl http://localhost:5000/api/v1/lists
```

#### Lists - Get One
**GET** `/lists/<list_id>`
```bash
curl http://localhost:5000/api/v1/lists/1
```

#### Lists - Create
**POST** `/lists`
```bash
curl -X POST http://localhost:5000/api/v1/lists \
  -H "Content-Type: application/json" \
  -d '{"name": "Work", "description": "Work tasks"}'
```

#### Lists - Update
**PUT** `/lists/<list_id>`
```bash
curl -X PUT http://localhost:5000/api/v1/lists/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated name"}'
```

#### Lists - Delete
**DELETE** `/lists/<list_id>`
```bash
curl -X DELETE http://localhost:5000/api/v1/lists/1
```

---

## 📊 Response Format

All responses follow this format:

**Success:**
```json
{
  "success": true,
  "data": {...},
  "message": "Optional message",
  "count": 1
}
```

**Error:**
```json
{
  "success": false,
  "error": "Error message"
}
```

---

## 🧪 Testing

Run tests locally:
```bash
pytest tests/test_api.py -v
```

With coverage:
```bash
pytest tests/test_api.py --cov=backend --cov-report=html
```

---

## 🛠️ Project Structure

```
backend/
├── __init__.py        (Package marker)
├── app.py             (Main Flask app - 11 endpoints)
├── config.py          (Configuration settings)
├── requirements.txt   (Dependencies: Flask, Flask-CORS)
└── README.md          (This file)
```

---

## 🔗 Integration

The backend connects to `my_todo_lib` library and exposes all functionality via REST API:

- ✅ Task CRUD operations
- ✅ List CRUD operations
- ✅ Move task between lists
- ✅ Auto-save persistence
- ✅ Error handling
- ✅ CORS enabled for web frontends

---

## 📝 Error Codes

| Code | Meaning | Reason |
|------|---------|--------|
| 200 | OK | Request successful |
| 201 | Created | Resource created |
| 400 | Bad Request | Invalid input |
| 404 | Not Found | Resource not found |
| 500 | Server Error | Internal error |

---

## 🚀 Next Steps

1. Run the server: `python -m backend.app`
2. Test endpoints with curl or Postman
3. Create a frontend (React, Vue.js)
4. Deploy to cloud (Heroku, AWS, etc.)

---

**Status**: ✅ Ready to use  
**Created**: 5 November 2025
