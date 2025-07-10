import { useState } from 'react';
import { generateSchedule, optimizeSchedule, addCourseToSchedule } from '../api/schedule';
import logo from '../studySyncLogo.png';
import './StudySyncForm.css';

export default function StudySyncForm() {
  const [text, setText] = useState('');
  const [prefs, setPrefs] = useState({ earliest_time: "08:00", latest_time: "18:00" });
  const [results, setResults] = useState([]);
  const [optimizedResults, setOptimizedResults] = useState(null);
  const [selectedSchedule, setSelectedSchedule] = useState(null);
  const [addCourseTitle, setAddCourseTitle] = useState('');
  const [mode, setMode] = useState('basic'); // 'basic', 'optimized', 'add-course'

  const handleSubmit = async () => {
    const data = await generateSchedule(text, prefs);
    console.log("handle submit", data);
    setResults(data);
  };

  const handleOptimize = async () => {
    const data = await optimizeSchedule(text, prefs);
    console.log("optimize submit", data);
    setOptimizedResults(data);
    setMode('optimized');
  };

  const handleAddCourse = async () => {
    if (!selectedSchedule || !addCourseTitle.trim()) return;
    
    const allCourses = await generateSchedule(text, prefs);
    const newSchedule = await addCourseToSchedule(selectedSchedule, addCourseTitle, allCourses);
    console.log("add course", newSchedule);
    setSelectedSchedule(newSchedule);
  };

  return (
    <main className="form-wrapper">
      <section className={`card ${results.length > 0 ? 'has-results' : ''}`}>
        <div className="logo-header">
          <img src={logo} alt="Study Sync logo" className="logo" />
          <h1>Study Sync</h1>
        </div>
        <p className="subtitle">Paste your shopping cart to generate your ideal UNC schedule.</p>

        <textarea
          placeholder="Paste your shopping cart here..."
          rows={8}
          value={text}
          onChange={(e) => setText(e.target.value)}
        />

        <div className="time-inputs">
          <div className="time-block">
            <label>Start Time</label>
            <input type="time" value={prefs.earliest_time} onChange={(e) => setPrefs({ ...prefs, earliest_time: e.target.value })} />
          </div>
          <div className="time-block">
            <label>End Time</label>
            <input type="time" value={prefs.latest_time} onChange={(e) => setPrefs({ ...prefs, latest_time: e.target.value })} />
          </div>
        </div>

        <div className="button-group">
          <button onClick={handleSubmit}>Generate Schedule</button>
          <button onClick={handleOptimize} className="optimize-btn">
            Optimize with Ratings
          </button>
        </div>

        {results.length > 0 && mode === 'basic' && (
          <div className="results">
            <h2>Your Schedule</h2>
            <ul>
              {results.map((c, i) => (
                <li key={i}>
                  <strong>{c.title}</strong><br />
                  <span>{c.instructor}</span><br />
                  <span>{c.days.join(', ')} | {c.start_time} – {c.end_time}</span>
                  {c.rating && <span className="rating">⭐ {c.rating}</span>}
                </li>
              ))}
            </ul>
          </div>
        )}

        {optimizedResults && mode === 'optimized' && (
          <div className="results">
            <h2>Optimized Schedules (Found {optimizedResults.total_found})</h2>
            {optimizedResults.schedules.map((schedule, scheduleIndex) => (
              <div key={scheduleIndex} className="schedule-option">
                <h3>
                  Option {scheduleIndex + 1}
                  <button 
                    onClick={() => {
                      setSelectedSchedule(schedule);
                      setMode('add-course');
                    }}
                    className="select-btn"
                  >
                    Select & Add Course
                  </button>
                </h3>
                <ul>
                  {schedule.map((c, i) => (
                    <li key={i}>
                      <strong>{c.title}</strong><br />
                      <span>{c.instructor}</span>
                      {c.rating && <span className="rating">⭐ {c.rating}</span>}
                      <br />
                      <span>{c.days.join(', ')} | {c.start_time} – {c.end_time}</span>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        )}

        {selectedSchedule && mode === 'add-course' && (
          <div className="results">
            <h2>Add Course to Schedule</h2>
            <div className="add-course-section">
              <input
                type="text"
                placeholder="Enter course title (e.g., CHEM 101)"
                value={addCourseTitle}
                onChange={(e) => setAddCourseTitle(e.target.value)}
              />
              <button onClick={handleAddCourse}>Add Course</button>
            </div>
            
            <h3>Current Schedule</h3>
            <ul>
              {selectedSchedule.map((c, i) => (
                <li key={i}>
                  <strong>{c.title}</strong><br />
                  <span>{c.instructor}</span>
                  {c.rating && <span className="rating">⭐ {c.rating}</span>}
                  <br />
                  <span>{c.days.join(', ')} | {c.start_time} – {c.end_time}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </section>
    </main>
  );
}
