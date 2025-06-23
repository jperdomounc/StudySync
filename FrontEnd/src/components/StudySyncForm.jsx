import { useState } from 'react';
import { generateSchedule } from '../api/schedule';
import logo from '../studySyncLogo.png';
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

        <button onClick={handleSubmit}>Generate Schedule</button>

        {results.length > 0 && (
          <div className="results">
            <h2>Your Schedule</h2>
            <ul>
              {results.map((c, i) => (
                <li key={i}>
                  <strong>{c.title}</strong><br />
                  <span>{c.instructor}</span><br />
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
