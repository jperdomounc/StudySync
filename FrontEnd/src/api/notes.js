import axios from 'axios';

const BASE_URL = 'http://localhost:8000';

export const getAllNotes = async () => {
  const response = await axios.get(`${BASE_URL}/notes`);
  return response.data;
};

export const createNote = async (noteData) => {
  const response = await axios.post(`${BASE_URL}/notes`, noteData);
  return response.data;
};

export const deleteNote = async (noteId) => {
  const response = await axios.delete(`${BASE_URL}/notes/${noteId}`);
  return response.data;
};

export const getNotesByCourse = async (course) => {
  const response = await axios.get(`${BASE_URL}/notes/course/${course}`);
  return response.data;
};