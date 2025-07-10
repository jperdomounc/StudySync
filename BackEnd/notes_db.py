"""Simple in-memory database for notes"""
import json
import os
from datetime import datetime
from typing import List, Optional
from models import Note, NoteCreate

class NotesDatabase:
    def __init__(self, db_file: str = "notes.json"):
        self.db_file = db_file
        self.notes = []
        self.next_id = 1
        self.load_notes()
    
    def load_notes(self):
        """Load notes from JSON file"""
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r') as f:
                    data = json.load(f)
                    self.notes = data.get('notes', [])
                    self.next_id = data.get('next_id', 1)
            except Exception as e:
                print(f"Error loading notes: {e}")
                self.notes = []
                self.next_id = 1
    
    def save_notes(self):
        """Save notes to JSON file"""
        try:
            data = {
                'notes': self.notes,
                'next_id': self.next_id
            }
            with open(self.db_file, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving notes: {e}")
    
    def create_note(self, note_data: NoteCreate) -> Note:
        """Create a new note"""
        note = {
            'id': self.next_id,
            'title': note_data.title,
            'content': note_data.content,
            'course': note_data.course,
            'tags': note_data.tags,
            'created_at': datetime.now().isoformat()
        }
        
        self.notes.append(note)
        self.next_id += 1
        self.save_notes()
        
        return Note(**note)
    
    def get_all_notes(self) -> List[Note]:
        """Get all notes sorted by creation date (newest first)"""
        sorted_notes = sorted(self.notes, key=lambda x: x['created_at'], reverse=True)
        return [Note(**note) for note in sorted_notes]
    
    def get_note_by_id(self, note_id: int) -> Optional[Note]:
        """Get a specific note by ID"""
        for note in self.notes:
            if note['id'] == note_id:
                return Note(**note)
        return None
    
    def delete_note(self, note_id: int) -> bool:
        """Delete a note by ID"""
        for i, note in enumerate(self.notes):
            if note['id'] == note_id:
                del self.notes[i]
                self.save_notes()
                return True
        return False
    
    def get_notes_by_course(self, course: str) -> List[Note]:
        """Get all notes for a specific course"""
        course_notes = [
            note for note in self.notes 
            if note['course'].lower() == course.lower()
        ]
        sorted_notes = sorted(course_notes, key=lambda x: x['created_at'], reverse=True)
        return [Note(**note) for note in sorted_notes]

# Global database instance
notes_db = NotesDatabase()