import { useState } from 'react';
import './Navigation.css';

export default function Navigation({ currentPage, onPageChange }) {
  return (
    <nav className="navigation">
      <div className="nav-container">
        <div className="nav-brand">
          <h2>StudySync</h2>
        </div>
        
        <div className="nav-links">
          <button 
            onClick={() => onPageChange('schedule')}
            className={currentPage === 'schedule' ? 'nav-link active' : 'nav-link'}
          >
            📅 Schedule
          </button>
          <button 
            onClick={() => onPageChange('notes')}
            className={currentPage === 'notes' ? 'nav-link active' : 'nav-link'}
          >
            📝 Notes
          </button>
        </div>
      </div>
    </nav>
  );
}