import axios from 'axios';

export const generateSchedule = async (pastedText, preferences) => {
  const response = await axios.post('http://localhost:8000/generate_schedule', {
    pasted_text: pastedText,
    preferences,
  });
  return response.data;
};
