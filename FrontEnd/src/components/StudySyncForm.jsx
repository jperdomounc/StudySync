import { useState } from 'react';
import { generateSchedule } from '../api/schedule';
import './StudySyncForm.css';

export default function StudySyncForm() {
  const [text, setText] = useState('');
  const [prefs, setPrefs] = useState({ earliest_time: "08:00", latest_time: "18:00" });
  const [results, setResults] = useState([]);

  const handleSubmit = async () => {
    const data = await generateSchedule(text, prefs);
    console.log("handle submit", data);
    setResults(data);
  };

  return (
    <div className="study-sync-container">
      <h1>📚 Study Sync</h1>
      <p>Create your perfect schedule with just a paste</p>
      <textarea placeholder="Paste your shopping cart here..." rows={10} onChange={(e) => setText(e.target.value)} />
      <div className="time-pickers">
        <label>Start: <input type="time" value={prefs.earliest_time} onChange={(e) => setPrefs({...prefs, earliest_time: e.target.value})} /></label>
        <label>End: <input type="time" value={prefs.latest_time} onChange={(e) => setPrefs({...prefs, latest_time: e.target.value})} /></label>
      </div>
      <button onClick={handleSubmit}>Generate Schedule</button>

      <ul>
        {results.map((c, i) => (
          <li key={i}>
            <strong>{c.title}</strong> — {c.instructor}<br />
            {c.days.join(', ')} {c.start_time}–{c.end_time}
          </li>
        ))}
      </ul>
    </div>
  );
}
