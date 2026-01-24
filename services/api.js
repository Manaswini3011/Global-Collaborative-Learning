/**
 * API Service - Handles all backend API calls
 */

import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Unauthorized - clear token and redirect to login
      localStorage.removeItem('access_token')
      localStorage.removeItem('user_id')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Auth API
export const authAPI = {
  login: async (email, password) => {
    const response = await api.post('/api/login', { email, password })
    return response.data
  },
}

// Assessment API
export const assessmentAPI = {
  parseIntent: async (prompt) => {
    const response = await api.post('/api/parse-intent', { prompt })
    return response.data
  },

  getAssessment: async (assessmentId) => {
    const response = await api.get(`/api/assessment/${assessmentId}`)
    return response.data
  },

  editAssessment: async (assessmentId, updates) => {
    const response = await api.put(`/api/assessment/${assessmentId}`, updates)
    return response.data
  },

  submitAssessment: async (assessmentId) => {
    const response = await api.post('/api/assessment/submit', { assessment_id: assessmentId })
    return response.data
  },
}

// Statistics API
export const statisticsAPI = {
  getStatistics: async () => {
    const response = await api.get('/api/statistics')
    return response.data
  },
}

// Question Preview API
export const questionPreviewAPI = {
  previewQuestions: async (skills, questionTypes, difficulty, numQuestions = 10, durationMinutes = 30) => {
    const params = new URLSearchParams()
    if (skills && skills.length > 0) {
      skills.forEach(skill => params.append('skills', skill))
    }
    if (questionTypes && questionTypes.length > 0) {
      questionTypes.forEach(type => params.append('question_types', type))
    }
    if (difficulty) params.append('difficulty', difficulty)
    params.append('num_questions', numQuestions)
    params.append('duration_minutes', durationMinutes)
    
    const response = await api.get(`/api/questions/preview?${params.toString()}`)
    return response.data
  },
}

// Training API
export const trainingAPI = {
  trainModel: async (skill, difficulty, questionType) => {
    const params = {}
    if (skill) params.skill = skill
    if (difficulty) params.difficulty = difficulty
    if (questionType) params.question_type = questionType
    const response = await api.post('/api/train/model', null, { params })
    return response.data
  },
  
  analyzeQuestion: async (questionText) => {
    const response = await api.post('/api/analyze/question', null, {
      params: { question_text: questionText }
    })
    return response.data
  },
  
  generateQuestion: async (skill, difficulty, questionType, context = '') => {
    const response = await api.post('/api/generate/question', null, {
      params: { skill, difficulty, question_type: questionType, context }
    })
    return response.data
  },
}

export default api

