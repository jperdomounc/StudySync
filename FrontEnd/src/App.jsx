import { useState, useEffect } from 'react';
import Login from './components/Login';
import MajorSelection from './components/MajorSelection';
import MajorPage from './components/MajorPage';

export default function App() {
  const [user, setUser] = useState(null);
  const [currentView, setCurrentView] = useState('login');
  const [selectedMajor, setSelectedMajor] = useState(null);

  useEffect(() => {
    // Check if user is already logged in
    const token = localStorage.getItem('token');
    const savedUser = localStorage.getItem('user');
    
    if (token && savedUser) {
      try {
        const userData = JSON.parse(savedUser);
        setUser(userData);
        setCurrentView('majorSelection');
      } catch (error) {
        console.error('Error parsing saved user data:', error);
        localStorage.removeItem('token');
        localStorage.removeItem('user');
      }
    }
  }, []);

  const handleLogin = (userData) => {
    setUser(userData);
    setCurrentView('majorSelection');
  };

  const handleMajorSelect = (major) => {
    setSelectedMajor(major);
    setCurrentView('majorPage');
  };

  const handleBackToMajors = () => {
    setSelectedMajor(null);
    setCurrentView('majorSelection');
  };

  if (!user) {
    return <Login onLogin={handleLogin} />;
  }

  return (
    <div className="app">
      {currentView === 'majorSelection' && (
        <MajorSelection 
          user={user} 
          onMajorSelect={handleMajorSelect} 
        />
      )}
      {currentView === 'majorPage' && selectedMajor && (
        <MajorPage 
          user={user}
          major={selectedMajor}
          onBack={handleBackToMajors}
        />
      )}
    </div>
  );
}
