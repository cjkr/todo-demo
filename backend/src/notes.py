from flask import Blueprint, request

from src.database import Note, db

notes = Blueprint("notes", __name__, url_prefix="/api/v1/notes")

# Get all notes
@notes.get("/")
def get_notes():
    notes = Note.query.all()

    return {
        "data": [
            {
                "text": note.text,
                "is_completed": note.is_completed,
                "created_at": note.created_at,
                "updated_at": note.updated_at,
            }
            for note in notes
        ]
    }, 200


# Create Note
@notes.post("/")
def create_note():
    text = request.get_json().get("text", "")

    if len(text) < 1:
        return {"error": "Invalid note"}, 400

    note = Note(text=text)

    db.session.add(note)
    db.session.commit()

    return {
        "message": "Note created successfully",
        "note": {"text": text, "created_at": note.created_at},
    }, 201


# Update Note
@notes.put("/<int:id>")
@notes.patch("/<int:id>")
def update_note(id):
    text = request.get_json().get("text", "")

    note = Note.query.filter_by(id=id).first()

    if note is None:
        return {"error": "Note not found"}, 404

    if len(text) < 1:
        return {"error": "Invalid note"}, 400

    note.text = text
    db.session.commit()

    return {
        "message": "Note successfully updated",
        "note": {"text": text, "updated_at": note.updated_at},
    }, 200


# Delete Note
@notes.delete("/<int:id>")
def delete_note(id):
    note = Note.query.filter_by(id=id).first()

    if note is None:
        return {"error": "Note not found"}, 404

    db.session.delete(note)
    db.session.commit()

    return {"message": "Note successfully deleted"}, 200
