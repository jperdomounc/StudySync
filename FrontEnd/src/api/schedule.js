import axios from 'axios';

export const generateSchedule = async (pastedText, preferences) => {
  const res = await axios.post('http://localhost:8000/generate_schedule', {
    pasted_text: pastedText,
    preferences
  });
  console.log("generateSchedule");
  return res.data;
};

export const optimizeSchedule = async (pastedText, preferences) => {
  const res = await axios.post('http://localhost:8000/optimize_schedule', {
    pasted_text: pastedText,
    preferences
  });
  console.log("optimizeSchedule");
  return res.data;
};

export const addCourseToSchedule = async (existingSchedule, newCourseTitle, availableCourses) => {
  const res = await axios.post('http://localhost:8000/add_course_to_schedule', {
    existing_schedule: existingSchedule,
    new_course_title: newCourseTitle,
    available_courses: availableCourses
  });
  console.log("addCourseToSchedule");
  return res.data;
};
