import { useState, useEffect } from 'react';
import { getAllNotes, createNote, deleteNote } from '../api/notes';
import './NotesPage.css';

export default function NotesPage() {
  const [notes, setNotes] = useState([]);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newNote, setNewNote] = useState({
    title: '',
    content: '',
    course: '',
    tags: ''
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [filter, setFilter] = useState('');

  useEffect(() => {
    loadNotes();
  }, []);

  const loadNotes = async () => {
    try {
      setLoading(true);
      const data = await getAllNotes();
      setNotes(data);
    } catch (err) {
      setError('Failed to load notes');
      console.error('Error loading notes:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateNote = async (e) => {
    e.preventDefault();
    
    // Validate content length (max 5000 characters)
    if (newNote.content.length > 5000) {
      setError('Note content too long (max 5000 characters)');
      return;
    }
    
    if (!newNote.title.trim() || !newNote.content.trim()) {
      setError('Title and content are required');
      return;
    }

    try {
      const noteData = {
        ...newNote,
        tags: newNote.tags.split(',').map(tag => tag.trim()).filter(tag => tag)
      };
      
      await createNote(noteData);
      setNewNote({ title: '', content: '', course: '', tags: '' });
      setShowCreateForm(false);
      setError('');
      loadNotes();
    } catch (err) {
      setError('Failed to create note');
      console.error('Error creating note:', err);
    }
  };

  const handleDeleteNote = async (noteId) => {
    if (!window.confirm('Are you sure you want to delete this note?')) return;
    
    try {
      await deleteNote(noteId);
      loadNotes();
    } catch (err) {
      setError('Failed to delete note');
      console.error('Error deleting note:', err);
    }
  };

  const filteredNotes = notes.filter(note =>
    note.title.toLowerCase().includes(filter.toLowerCase()) ||
    note.course.toLowerCase().includes(filter.toLowerCase()) ||
    note.tags.some(tag => tag.toLowerCase().includes(filter.toLowerCase()))
  );

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="notes-page">
      <header className="notes-header">
        <h1>📝 Class Notes</h1>
        <p>Share and discover study notes with your classmates</p>
      </header>

      <div className="notes-actions">
        <div className="search-section">
          <input
            type="text"
            placeholder="Search notes by title, course, or tags..."
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            className="search-input"
          />
        </div>
        
        <button 
          onClick={() => setShowCreateForm(!showCreateForm)}
          className="create-note-btn"
        >
          {showCreateForm ? 'Cancel' : '+ New Note'}
        </button>
      </div>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {showCreateForm && (
        <form onSubmit={handleCreateNote} className="create-note-form">
          <h3>Create New Note</h3>
          
          <input
            type="text"
            placeholder="Note title"
            value={newNote.title}
            onChange={(e) => setNewNote({...newNote, title: e.target.value})}
            maxLength={100}
            required
          />
          
          <input
            type="text"
            placeholder="Course (e.g., CHEM 101)"
            value={newNote.course}
            onChange={(e) => setNewNote({...newNote, course: e.target.value})}
            maxLength={50}
          />
          
          <input
            type="text"
            placeholder="Tags (comma-separated)"
            value={newNote.tags}
            onChange={(e) => setNewNote({...newNote, tags: e.target.value})}
            maxLength={200}
          />
          
          <textarea
            placeholder="Note content (max 5000 characters)"
            value={newNote.content}
            onChange={(e) => setNewNote({...newNote, content: e.target.value})}
            maxLength={5000}
            rows={8}
            required
          />
          
          <div className="character-count">
            {newNote.content.length}/5000 characters
          </div>
          
          <div className="form-actions">
            <button type="submit" className="submit-btn">
              Create Note
            </button>
            <button 
              type="button" 
              onClick={() => setShowCreateForm(false)}
              className="cancel-btn"
            >
              Cancel
            </button>
          </div>
        </form>
      )}

      <div className="notes-container">
        {loading ? (
          <div className="loading">Loading notes...</div>
        ) : filteredNotes.length === 0 ? (
          <div className="no-notes">
            {filter ? 'No notes match your search' : 'No notes available. Create the first one!'}
          </div>
        ) : (
          <div className="notes-grid">
            {filteredNotes.map(note => (
              <div key={note.id} className="note-card">
                <div className="note-header">
                  <h3>{note.title}</h3>
                  <button 
                    onClick={() => handleDeleteNote(note.id)}
                    className="delete-btn"
                    title="Delete note"
                  >
                    ×
                  </button>
                </div>
                
                {note.course && (
                  <div className="note-course">
                    📚 {note.course}
                  </div>
                )}
                
                <div className="note-content">
                  {note.content.length > 200 
                    ? `${note.content.substring(0, 200)}...` 
                    : note.content
                  }
                </div>
                
                {note.tags && note.tags.length > 0 && (
                  <div className="note-tags">
                    {note.tags.map(tag => (
                      <span key={tag} className="tag">
                        {tag}
                      </span>
                    ))}
                  </div>
                )}
                
                <div className="note-meta">
                  <span className="note-date">
                    {formatDate(note.created_at)}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}