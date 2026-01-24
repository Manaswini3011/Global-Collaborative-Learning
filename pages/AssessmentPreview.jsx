import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import Navbar from '../components/Navbar'
import { assessmentAPI } from '../services/api'
import '../styles/AssessmentPreview.css'

const AssessmentPreview = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const [assessment, setAssessment] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    loadAssessment()
  }, [id])

  const loadAssessment = async () => {
    try {
      const data = await assessmentAPI.getAssessment(id)
      setAssessment(data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load assessment')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="assessment-page">
        <Navbar />
        <div className="container">
          <div className="loading-state">
            <span className="loading"></span>
            <p>Loading assessment...</p>
          </div>
        </div>
      </div>
    )
  }

  if (error || !assessment) {
    return (
      <div className="assessment-page">
        <Navbar />
        <div className="container">
          <div className="error-message">{error || 'Assessment not found'}</div>
        </div>
      </div>
    )
  }

  return (
    <div className="assessment-page">
      <Navbar />
      <div className="container">
        <div className="assessment-header">
          <h1>{assessment.title}</h1>
          <div className="assessment-meta">
            <span>Duration: {assessment.total_duration_minutes} minutes</span>
            <span>Questions: {assessment.total_questions}</span>
            <span>Status: {assessment.status}</span>
          </div>
        </div>

        <div className="questions-section">
          <h2>Selected Questions</h2>
          <p className="questions-subtitle">Questions grouped by difficulty level</p>
          
          {(() => {
            // Group questions by difficulty
            const questionsByDifficulty = {
              easy: [],
              medium: [],
              hard: []
            }
            
            assessment.questions.forEach((question) => {
              const difficulty = question.difficulty || 'medium'
              if (questionsByDifficulty[difficulty]) {
                questionsByDifficulty[difficulty].push(question)
              }
            })
            
            const difficultyOrder = ['easy', 'medium', 'hard']
            const difficultyLabels = {
              easy: '🟢 Easy',
              medium: '🟡 Medium',
              hard: '🔴 Hard'
            }
            
            return difficultyOrder.map((difficulty) => {
              const questions = questionsByDifficulty[difficulty]
              if (questions.length === 0) return null
              
              return (
                <div key={difficulty} className="difficulty-group">
                  <div className="difficulty-header">
                    <h3>{difficultyLabels[difficulty]}</h3>
                    <span className="difficulty-count">{questions.length} question{questions.length !== 1 ? 's' : ''}</span>
                  </div>
                  <div className="questions-list">
                    {questions.map((question, idx) => (
                      <div key={question.id} className="question-card">
                        <div className="question-header">
                          <span className="question-number">Q{idx + 1}</span>
                          <div className="question-badges">
                            <span className="badge skill">{question.skill}</span>
                            <span className={`badge difficulty ${question.difficulty}`}>
                              {question.difficulty}
                            </span>
                            <span className="badge type">{question.question_type}</span>
                          </div>
                        </div>
                        <h3>{question.title}</h3>
                        <p>{question.description}</p>
                        <div className="question-footer">
                          <span>⏱ {question.estimated_time_minutes} min</span>
                          {question.tags && question.tags.length > 0 && (
                            <div className="tags">
                              {question.tags.map((tag, i) => (
                                <span key={i} className="tag">{tag}</span>
                              ))}
                            </div>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )
            })
          })()}
        </div>

        {assessment.explainability_preview && (
          <div className="explainability-section">
            <h2>Why These Questions?</h2>
            <div className="explainability-card">
              <p>{assessment.explainability_preview}</p>
            </div>
          </div>
        )}

        <div className="actions-section">
          <button
            className="btn btn-secondary"
            onClick={(e) => {
              e.preventDefault()
              navigate(`/assessment/${id}/edit`)
            }}
          >
            Edit Assessment
          </button>
          <button
            className="btn btn-primary"
            onClick={(e) => {
              e.preventDefault()
              navigate(`/assessment/${id}/summary`)
            }}
          >
            Finalize & Submit
          </button>
        </div>
      </div>
    </div>
  )
}

export default AssessmentPreview

