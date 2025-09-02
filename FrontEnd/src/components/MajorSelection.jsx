import { useState, useEffect } from 'react';
import { MAJORS_LIST } from '../utils/majors';
import './MajorSelection.css';

export default function MajorSelection({ user, onMajorSelect }) {
  const [majors, setMajors] = useState([]);
  const [majorStats, setMajorStats] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    initializeMajors();
  }, []);

  const initializeMajors = async () => {
    try {
      // Use predefined majors list
      setMajors(MAJORS_LIST);
      
      // Try to fetch stats for each major, but don't fail if none exist
      const token = localStorage.getItem('token');
      const statsPromises = MAJORS_LIST.map(async (major) => {
        try {
          const statsResponse = await fetch(`http://localhost:8000/majors/${encodeURIComponent(major)}/stats`, {
            headers: {
              'Authorization': `Bearer ${token}`,
            },
          });
          if (statsResponse.ok) {
            return await statsResponse.json();
          }
        } catch (error) {
          // Silently ignore errors for stats - we'll show default values
        }
        return {
          major: major,
          total_classes: 0,
          total_users: 0,
          average_difficulty: 0
        };
      });

      const allStats = await Promise.all(statsPromises);
      const statsMap = {};
      allStats.forEach((stat, index) => {
        if (stat) {
          statsMap[MAJORS_LIST[index]] = stat;
        }
      });
      setMajorStats(statsMap);
    } catch (error) {
      console.error('Error initializing majors:', error);
      // Still show majors even if stats fail
      setMajors(MAJORS_LIST);
    } finally {
      setLoading(false);
    }
  };

  const filteredMajors = majors.filter(major =>
    major.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.reload();
  };

  const getDifficultyColor = (difficulty) => {
    if (difficulty === 0) return '#6c757d'; // No data - gray
    if (difficulty >= 8) return '#dc3545'; // High difficulty - red
    if (difficulty >= 6) return '#fd7e14'; // Medium-high difficulty - orange
    if (difficulty >= 4) return '#ffc107'; // Medium difficulty - yellow
    return '#28a745'; // Lower difficulty - green
  };

  if (loading) {
    return (
      <div className="major-selection-container">
        <div className="loading">Loading majors...</div>
      </div>
    );
  }

  return (
    <div className="major-selection-container">
      <header className="header">
        <div className="header-content">
          <div className="header-left">
            <h1>StudySync</h1>
            <p className="subtitle">Choose a major to explore class ratings</p>
          </div>
          <div className="header-right">
            <div className="user-info">
              <span className="welcome">Welcome, {user.display_name}!</span>
              <button onClick={handleLogout} className="logout-btn">Logout</button>
            </div>
          </div>
        </div>
      </header>

      <main className="main-content">
        <div className="search-section">
          <div className="search-box">
            <input
              type="text"
              placeholder="Search majors..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="search-input"
            />
          </div>
        </div>

        {error && <div className="error-message">{error}</div>}

        <div className="majors-grid">
          {filteredMajors.map((major) => {
            const stats = majorStats[major];
            return (
              <div
                key={major}
                className="major-card"
                onClick={() => onMajorSelect(major)}
              >
                <div className="major-header">
                  <h3 className="major-name">{major}</h3>
                  {major === user.major && (
                    <span className="your-major-badge">Your Major</span>
                  )}
                </div>

                <div className="major-stats">
                  <div className="stat">
                    <span className="stat-label">Classes</span>
                    <span className="stat-value">{stats ? stats.total_classes : 0}</span>
                  </div>
                  <div className="stat">
                    <span className="stat-label">Students</span>
                    <span className="stat-value">{stats ? stats.total_users : 0}</span>
                  </div>
                  <div className="stat">
                    <span className="stat-label">Avg Difficulty</span>
                    <span 
                      className="stat-value difficulty-rating"
                      style={{ color: getDifficultyColor(stats ? stats.average_difficulty : 0) }}
                    >
                      {stats && stats.average_difficulty > 0 ? `${stats.average_difficulty}/10` : 'No data'}
                    </span>
                  </div>
                </div>

                <div className="major-card-footer">
                  <span className="explore-text">Click to explore →</span>
                </div>
              </div>
            );
          })}
        </div>

        {filteredMajors.length === 0 && (
          <div className="no-results">
            <p>No majors found matching "{searchTerm}"</p>
          </div>
        )}
      </main>
    </div>
  );
}