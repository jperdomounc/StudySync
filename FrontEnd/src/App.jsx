import { useState } from 'react';
import StudySyncForm from './components/StudySyncForm';
import NotesPage from './components/NotesPage';
import Navigation from './components/Navigation';

export default function App() {
  const [currentPage, setCurrentPage] = useState('schedule');

  const handlePageChange = (page) => {
    setCurrentPage(page);
  };

  return (
    <div className="app">
      <Navigation currentPage={currentPage} onPageChange={handlePageChange} />
      
      <main>
        {currentPage === 'schedule' && <StudySyncForm />}
        {currentPage === 'notes' && <NotesPage />}
      </main>
    </div>
  );
}
