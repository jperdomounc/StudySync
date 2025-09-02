import { useState, useEffect } from 'react';
import './MajorPage.css';

export default function MajorPage({ user, major, onBack }) {
  const [classRankings, setClassRankings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showSubmissionForm, setShowSubmissionForm] = useState(false);
  const [submissionType, setSubmissionType] = useState('difficulty'); // 'difficulty' or 'professor'
  const [searchTerm, setSearchTerm] = useState('');

  // Form states
  const [difficultyForm, setDifficultyForm] = useState({
    class_code: '',
    class_name: '',
    difficulty_rating: 5,
    professor: '',
    semester: `${new Date().getMonth() < 6 ? 'Spring' : 'Fall'} ${new Date().getFullYear()}`
  });

  const [professorForm, setProfessorForm] = useState({
    professor: '',
    class_code: '',
    rating: 3.0,
    review: '',
    semester: `${new Date().getMonth() < 6 ? 'Spring' : 'Fall'} ${new Date().getFullYear()}`
  });

  useEffect(() => {
    fetchClassRankings();
  }, [major]);

  const fetchClassRankings = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:8000/majors/${encodeURIComponent(major)}/classes`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const rankings = await response.json();
        setClassRankings(rankings);
      } else {
        setError('Failed to load class rankings');
      }
    } catch (error) {
      console.error('Error fetching class rankings:', error);
      setError('Network error. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmitDifficulty = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem('token');
      const payload = {
        ...difficultyForm,
        major: user.major
      };

      const response = await fetch('http://localhost:8000/submissions/difficulty', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(payload),
      });

      if (response.ok) {
        alert('Difficulty rating submitted successfully!');
        setShowSubmissionForm(false);
        setDifficultyForm({
          class_code: '',
          class_name: '',
          difficulty_rating: 5,
          professor: '',
          semester: `${new Date().getMonth() < 6 ? 'Spring' : 'Fall'} ${new Date().getFullYear()}`
        });
        fetchClassRankings(); // Refresh data
      } else {
        const errorData = await response.json();
        alert(errorData.detail || 'Failed to submit rating');
      }
    } catch (error) {
      console.error('Error submitting difficulty:', error);
      alert('Network error. Please try again.');
    }
  };

  const handleSubmitProfessorRating = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem('token');
      const payload = {
        ...professorForm,
        major: user.major
      };

      const response = await fetch('http://localhost:8000/submissions/professor', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(payload),
      });

      if (response.ok) {
        alert('Professor rating submitted successfully!');
        setShowSubmissionForm(false);
        setProfessorForm({
          professor: '',
          class_code: '',
          rating: 3.0,
          review: '',
          semester: `${new Date().getMonth() < 6 ? 'Spring' : 'Fall'} ${new Date().getFullYear()}`
        });
        fetchClassRankings(); // Refresh data
      } else {
        const errorData = await response.json();
        alert(errorData.detail || 'Failed to submit rating');
      }
    } catch (error) {
      console.error('Error submitting professor rating:', error);
      alert('Network error. Please try again.');
    }
  };

  const getDifficultyColor = (difficulty) => {
    if (difficulty >= 8) return '#dc3545';
    if (difficulty >= 6) return '#fd7e14';
    if (difficulty >= 4) return '#ffc107';
    return '#28a745';
  };

  const getRatingStars = (rating) => {
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 >= 0.5;
    return '★'.repeat(fullStars) + (hasHalfStar ? '☆' : '') + '☆'.repeat(5 - Math.ceil(rating));
  };

  const filteredRankings = classRankings.filter(ranking =>
    ranking.class_code.toLowerCase().includes(searchTerm.toLowerCase()) ||
    ranking.class_name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return (
      <div className="major-page-container">
        <div className="loading">Loading class rankings...</div>
      </div>
    );
  }

  return (
    <div className="major-page-container">
      <header className="major-header">
        <div className="header-content">
          <div className="header-left">
            <button onClick={onBack} className="back-btn">← Back to Majors</button>
            <h1>{major}</h1>
            <p className="subtitle">Class difficulty rankings and professor ratings</p>
          </div>
          <div className="header-actions">
            <button 
              onClick={() => {
                setSubmissionType('difficulty');
                setShowSubmissionForm(true);
              }}
              className="submit-btn difficulty-btn"
            >
              Rate a Class
            </button>
            <button 
              onClick={() => {
                setSubmissionType('professor');
                setShowSubmissionForm(true);
              }}
              className="submit-btn professor-btn"
            >
              Rate a Professor
            </button>
          </div>
        </div>
      </header>

      <main className="main-content">
        <div className="search-section">
          <input
            type="text"
            placeholder="Search classes..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
        </div>

        {error && <div className="error-message">{error}</div>}

        <div className="rankings-list">
          {filteredRankings.map((ranking, index) => (
            <div key={ranking.class_code} className="class-card">
              <div className="class-header">
                <div className="class-info">
                  <div className="rank-badge">#{index + 1}</div>
                  <div className="class-details">
                    <h3 className="class-code">{ranking.class_code}</h3>
                    <p className="class-name">{ranking.class_name}</p>
                  </div>
                </div>
                <div className="difficulty-score">
                  <span 
                    className="difficulty-value"
                    style={{ color: getDifficultyColor(ranking.average_difficulty) }}
                  >
                    {ranking.average_difficulty}/10
                  </span>
                  <span className="difficulty-label">Difficulty</span>
                  <span className="submission-count">({ranking.total_submissions} reviews)</span>
                </div>
              </div>

              <div className="professors-section">
                <h4 className="professors-title">Professors</h4>
                <div className="professors-list">
                  {ranking.professors.map((prof) => (
                    <div key={prof.name} className="professor-item">
                      <div className="professor-info">
                        <span className="professor-name">{prof.name}</span>
                        <div className="professor-rating">
                          <span className="rating-stars">
                            {getRatingStars(prof.avg_rating)}
                          </span>
                          <span className="rating-value">
                            {prof.avg_rating > 0 ? `${prof.avg_rating}/5` : 'No ratings'}
                          </span>
                          {prof.rating_count > 0 && (
                            <span className="rating-count">({prof.rating_count})</span>
                          )}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>

        {filteredRankings.length === 0 && !loading && (
          <div className="no-results">
            <p>No classes found matching "{searchTerm}"</p>
            {user.major === major && (
              <p>Be the first to submit a class rating!</p>
            )}
          </div>
        )}
      </main>

      {/* Submission Form Modal */}
      {showSubmissionForm && (
        <div className="modal-overlay" onClick={() => setShowSubmissionForm(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>{submissionType === 'difficulty' ? 'Rate Class Difficulty' : 'Rate Professor'}</h2>
              <button onClick={() => setShowSubmissionForm(false)} className="close-btn">×</button>
            </div>

            {submissionType === 'difficulty' ? (
              <form onSubmit={handleSubmitDifficulty} className="submission-form">
                <div className="form-group">
                  <label>Class Code</label>
                  <input
                    type="text"
                    placeholder="e.g., COMP 550"
                    value={difficultyForm.class_code}
                    onChange={(e) => setDifficultyForm({...difficultyForm, class_code: e.target.value})}
                    required
                  />
                </div>
                
                <div className="form-group">
                  <label>Class Name</label>
                  <input
                    type="text"
                    placeholder="e.g., Algorithms and Data Structures"
                    value={difficultyForm.class_name}
                    onChange={(e) => setDifficultyForm({...difficultyForm, class_name: e.target.value})}
                    required
                  />
                </div>

                <div className="form-group">
                  <label>Professor</label>
                  <input
                    type="text"
                    placeholder="Professor name"
                    value={difficultyForm.professor}
                    onChange={(e) => setDifficultyForm({...difficultyForm, professor: e.target.value})}
                    required
                  />
                </div>

                <div className="form-group">
                  <label>Difficulty Rating: {difficultyForm.difficulty_rating}/10</label>
                  <input
                    type="range"
                    min="1"
                    max="10"
                    value={difficultyForm.difficulty_rating}
                    onChange={(e) => setDifficultyForm({...difficultyForm, difficulty_rating: parseInt(e.target.value)})}
                    className="range-slider"
                  />
                  <div className="range-labels">
                    <span>Easy</span>
                    <span>Very Hard</span>
                  </div>
                </div>

                <div className="form-group">
                  <label>Semester</label>
                  <input
                    type="text"
                    value={difficultyForm.semester}
                    onChange={(e) => setDifficultyForm({...difficultyForm, semester: e.target.value})}
                    required
                  />
                </div>

                <button type="submit" className="submit-form-btn">Submit Rating</button>
              </form>
            ) : (
              <form onSubmit={handleSubmitProfessorRating} className="submission-form">
                <div className="form-group">
                  <label>Professor Name</label>
                  <input
                    type="text"
                    placeholder="Professor name"
                    value={professorForm.professor}
                    onChange={(e) => setProfessorForm({...professorForm, professor: e.target.value})}
                    required
                  />
                </div>

                <div className="form-group">
                  <label>Class Code</label>
                  <input
                    type="text"
                    placeholder="e.g., COMP 550"
                    value={professorForm.class_code}
                    onChange={(e) => setProfessorForm({...professorForm, class_code: e.target.value})}
                    required
                  />
                </div>

                <div className="form-group">
                  <label>Rating: {professorForm.rating}/5</label>
                  <input
                    type="range"
                    min="1"
                    max="5"
                    step="0.1"
                    value={professorForm.rating}
                    onChange={(e) => setProfessorForm({...professorForm, rating: parseFloat(e.target.value)})}
                    className="range-slider"
                  />
                  <div className="range-labels">
                    <span>Poor</span>
                    <span>Excellent</span>
                  </div>
                </div>

                <div className="form-group">
                  <label>Review (Optional)</label>
                  <textarea
                    placeholder="Share your experience with this professor..."
                    value={professorForm.review}
                    onChange={(e) => setProfessorForm({...professorForm, review: e.target.value})}
                    rows="4"
                    maxLength="1000"
                  />
                </div>

                <div className="form-group">
                  <label>Semester</label>
                  <input
                    type="text"
                    value={professorForm.semester}
                    onChange={(e) => setProfessorForm({...professorForm, semester: e.target.value})}
                    required
                  />
                </div>

                <button type="submit" className="submit-form-btn">Submit Rating</button>
              </form>
            )}
          </div>
        </div>
      )}
    </div>
  );
}