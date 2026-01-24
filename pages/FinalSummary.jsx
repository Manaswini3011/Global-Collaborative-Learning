import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import Navbar from '../components/Navbar'
import { assessmentAPI } from '../services/api'
import '../styles/FinalSummary.css'

const FinalSummary = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const [assessment, setAssessment] = useState(null)
  const [submitting, setSubmitting] = useState(false)
  const [submitted, setSubmitted] = useState(false)
  const [finalExplainability, setFinalExplainability] = useState('')
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

  const handleSubmit = async (e) => {
    if (e) {
      e.preventDefault()
      e.stopPropagation()
    }
    
    setSubmitting(true)
    setError('')

    try {
      const assessmentId = parseInt(id)
      if (!assessmentId || isNaN(assessmentId)) {
        throw new Error('Invalid assessment ID')
      }
      
      const response = await assessmentAPI.submitAssessment(assessmentId)
      setFinalExplainability(response.final_explainability)
      setSubmitted(true)
      
      // Reload assessment to get updated status
      await loadAssessment()
      
      // Log successful submission
      console.log('Assessment submitted successfully:', assessmentId)
    } catch (err) {
      console.error('Submit error:', err)
      setError(err.response?.data?.detail || err.message || 'Failed to submit assessment')
    } finally {
      setSubmitting(false)
    }
  }

  if (loading) {
    return (
      <div className="summary-page">
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

  if (error && !assessment) {
    return (
      <div className="summary-page">
        <Navbar />
        <div className="container">
          <div className="error-message">{error}</div>
        </div>
      </div>
    )
  }

  return (
    <div className="summary-page">
      <Navbar />
      <div className="container">
        <div className="summary-header">
          <h1>Final Assessment Summary</h1>
          <p>Review and finalize your assessment</p>
        </div>

        {assessment && (
          <>
            <div className="summary-card">
              <h2>Assessment Details</h2>
              <div className="summary-grid">
                <div className="summary-item">
                  <span className="label">Title:</span>
                  <span className="value">{assessment.title}</span>
                </div>
                <div className="summary-item">
                  <span className="label">Duration:</span>
                  <span className="value">
                    {(() => {
                      // Calculate total time from questions
                      const totalTime = assessment.questions?.reduce((sum, q) => sum + (q.estimated_time_minutes || 0), 0) || 0
                      return totalTime > 0 ? `${totalTime} minutes (from questions)` : `${assessment.total_duration_minutes} minutes`
                    })()}
                  </span>
                </div>
                <div className="summary-item">
                  <span className="label">Questions:</span>
                  <span className="value">{assessment.total_questions}</span>
                </div>
                <div className="summary-item">
                  <span className="label">Status:</span>
                  <span className={`value status-${submitted ? 'submitted' : assessment.status}`}>
                    {submitted ? 'submitted' : (assessment.status || 'draft')}
                  </span>
                </div>
              </div>
            </div>

            <div className="questions-summary">
              <h2>Selected Questions</h2>
              <div className="questions-list-compact">
                {assessment.questions.map((question, idx) => (
                  <div key={question.id} className="question-item">
                    <span className="q-num">Q{idx + 1}</span>
                    <div className="q-details">
                      <h4>{question.title}</h4>
                      <div className="q-meta">
                        <span>{question.skill}</span>
                        <span>{question.difficulty}</span>
                        <span>{question.estimated_time_minutes} min</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {submitted && finalExplainability && (
              <div className="explainability-final">
                <h2>Final Explainability Report</h2>
                <div className="explainability-content">
                  <p>{finalExplainability}</p>
                </div>
              </div>
            )}

            {!submitted && (
              <div className="submit-section">
                {error && <div className="error-message">{error}</div>}
                <div className="submit-actions">
                  <button
                    type="button"
                    className="btn btn-secondary"
                    onClick={(e) => {
                      e.preventDefault()
                      navigate(`/assessment/${id}`)
                    }}
                  >
                    Go Back
                  </button>
                  <button
                    type="button"
                    className="btn btn-primary submit-btn"
                    onClick={handleSubmit}
                    disabled={submitting}
                  >
                    {submitting ? (
                      <>
                        <span className="loading"></span>
                        <span style={{ marginLeft: '8px' }}>Finalizing...</span>
                      </>
                    ) : (
                      'Finalize & Submit Assessment'
                    )}
                  </button>
                </div>
              </div>
            )}

            {submitted && (
              <div className="success-section">
                <div className="success-card">
                  <div className="success-icon">✓</div>
                  <h2>Assessment Finalized Successfully!</h2>
                  <p>Your assessment has been created and is ready to use.</p>
                  <button
                    className="btn btn-primary"
                    onClick={() => navigate('/dashboard')}
                  >
                    Return to Dashboard
                  </button>
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  )
}

export default FinalSummary

