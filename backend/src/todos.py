from flask import Blueprint, request

from src.database import Todo, db

todos = Blueprint("todos", __name__, url_prefix="/api/v1/todos")

# Get all todos
@todos.get("/")
def get_todos():
    todos = Todo.query.all()

    return {
        "todos": [
            {
                "id": todo.id,
                "text": todo.text,
                "is_completed": todo.is_completed,
                "created_at": todo.created_at,
                "updated_at": todo.updated_at,
            }
            for todo in todos
        ]
    }, 200


# Create Todo
@todos.post("/")
def create_todo():
    text = request.get_json().get("text", "")

    if len(text) < 1:
        return {"error": "Invalid todo"}, 400

    todo = Todo(text=text)

    db.session.add(todo)
    db.session.commit()

    return {
        "message": "Todo created successfully",
        "todo": {"text": text, "created_at": todo.created_at, "id": todo.id},
    }, 201


# Update Todo
@todos.put("/<int:id>")
@todos.patch("/<int:id>")
def update_todo(id):
    text = request.get_json().get("text", "")

    todo = Todo.query.filter_by(id=id).first()

    if todo is None:
        return {"error": "Todo not found"}, 404

    if len(text) < 1:
        return {"error": "Invalid todo"}, 400

    todo.text = text
    db.session.commit()

    return {
        "message": "Todo successfully updated",
        "todo": {"text": text, "updated_at": todo.updated_at},
    }, 200


# Delete Todo
@todos.delete("/<int:id>")
def delete_todo(id):
    todo = Todo.query.filter_by(id=id).first()

    if todo is None:
        return {"error": "Todo not found"}, 404

    db.session.delete(todo)
    db.session.commit()

    return {"message": "Todo successfully deleted"}, 200


# Toggle completion
@todos.get("/toggle_completed/<int:id>")
def toggle_todo_completion(id):
    todo = Todo.query.filter_by(id=id).first()

    if todo is None:
        return {"error": "Todo not found"}, 404

    todo.is_completed = not todo.is_completed
    db.session.commit()

    return {
        "message": "Todo status toggled",
        "todo": {
            "text": todo.text,
            "is_completed": todo.is_completed,
            "updated_at": todo.updated_at,
        },
    }, 200
