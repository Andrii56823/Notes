from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import schemas
from database import SessionLocal
from typing import List
import auth

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(prefix="/notes", tags=["notes"])

@router.post("/create", response_model=schemas.NoteOut)
def new_note(note: schemas.Note, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_note = models.Note(title=note.title, content=note.content, owner_id=current_user.id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@router.get("/all", response_model=list[schemas.NoteOut])
def get_all_notes(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    query = db.query(models.Note).filter(models.Note.owner_id == current_user.id).all()
    return query

@router.put("/{note_id}", response_model=schemas.NoteOut)
def update_note(note_id: int, note: schemas.Note, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user) ):
    db_note = db.query(models.Note).filter(models.Note.id == note_id, models.Note.owner_id == current_user.id).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    db_note.title = note.title
    db_note.content = note.content
    db.commit()
    db.refresh(db_note)
    return db_note

@router.delete("/{note_id}")
def del_note(note_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_note = db.query(models.Note).filter(models.Note.id == note_id, models.Note.owner_id == current_user.id).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(db_note)
    db.commit()
    return {"message": f"Note {note_id} deleted"}

