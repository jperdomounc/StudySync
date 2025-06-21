import axios from 'axios';

export const generateSchedule = async (pastedText, preferences) => {
  const res = await axios.post('http://localhost:8000/generate_schedule', {
    pasted_text: pastedText,
    preferences
  });
  console.log("generateSchedule");
  return res.data;
};
