import { useState } from 'react';
import { MAJORS_LIST } from '../utils/majors';
import './Login.css';

export default function Login({ onLogin }) {
  const [isRegistering, setIsRegistering] = useState(false);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    major: '',
    grad_year: new Date().getFullYear() + 1
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const majors = MAJORS_LIST;

  const currentYear = new Date().getFullYear();
  const gradYears = Array.from({ length: 10 }, (_, i) => currentYear + i);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const validateEmail = (email) => {
    const uncPattern = /^[a-zA-Z0-9._%+-]+@(unc\.edu|live\.unc\.edu|ad\.unc\.edu)$/;
    return uncPattern.test(email.toLowerCase());
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    // Validate email
    if (!validateEmail(formData.email)) {
      setError('Please use a valid UNC email address (@unc.edu, @live.unc.edu, or @ad.unc.edu)');
      setLoading(false);
      return;
    }

    try {
      const endpoint = isRegistering ? '/auth/register' : '/auth/login';
      const payload = isRegistering ? formData : { 
        email: formData.email, 
        password: formData.password 
      };

      const response = await fetch(`http://localhost:8000${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (response.ok) {
        // Store token and user data
        localStorage.setItem('token', data.access_token);
        localStorage.setItem('user', JSON.stringify(data.user));
        onLogin(data.user);
      } else {
        setError(data.detail || 'Authentication failed');
      }
    } catch (error) {
      console.error('Auth error:', error);
      setError('Network error. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="login-header">
          <h1>StudySync</h1>
          <p className="tagline">UNC Class & Professor Ratings</p>
        </div>

        <div className="auth-toggle">
          <button 
            type="button"
            className={!isRegistering ? 'active' : ''}
            onClick={() => setIsRegistering(false)}
          >
            Sign In
          </button>
          <button 
            type="button"
            className={isRegistering ? 'active' : ''}
            onClick={() => setIsRegistering(true)}
          >
            Sign Up
          </button>
        </div>

        <form onSubmit={handleSubmit} className="auth-form">
          {error && <div className="error-message">{error}</div>}
          
          <div className="form-group">
            <label htmlFor="email">UNC Email</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="yourname@unc.edu"
              required
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder={isRegistering ? "At least 8 characters with letters and numbers" : "Enter your password"}
              required
              disabled={loading}
              minLength={isRegistering ? 8 : undefined}
            />
          </div>

          {isRegistering && (
            <>
              <div className="form-group">
                <label htmlFor="major">Major</label>
                <select
                  id="major"
                  name="major"
                  value={formData.major}
                  onChange={handleChange}
                  required
                  disabled={loading}
                >
                  <option value="">Select your major</option>
                  {majors.map(major => (
                    <option key={major} value={major}>{major}</option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="grad_year">Graduation Year</label>
                <select
                  id="grad_year"
                  name="grad_year"
                  value={formData.grad_year}
                  onChange={handleChange}
                  required
                  disabled={loading}
                >
                  {gradYears.map(year => (
                    <option key={year} value={year}>{year}</option>
                  ))}
                </select>
              </div>
            </>
          )}

          <button 
            type="submit" 
            className="submit-button"
            disabled={loading}
          >
            {loading ? 'Loading...' : (isRegistering ? 'Create Account' : 'Sign In')}
          </button>
        </form>

        <div className="login-footer">
          <p>
            {isRegistering ? 'Already have an account?' : "Don't have an account?"}{' '}
            <button 
              type="button"
              className="link-button"
              onClick={() => setIsRegistering(!isRegistering)}
            >
              {isRegistering ? 'Sign In' : 'Sign Up'}
            </button>
          </p>
        </div>
      </div>
    </div>
  );
}