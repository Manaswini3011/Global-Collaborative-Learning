import React, { useState, useEffect, useCallback } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import Navbar from '../components/Navbar'
import { assessmentAPI, questionPreviewAPI } from '../services/api'
import '../styles/EditAssessment.css'

const EditAssessment = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const [assessment, setAssessment] = useState(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  
  const [duration, setDuration] = useState(30)
  const [difficulty, setDifficulty] = useState('medium')
  const [numQuestions, setNumQuestions] = useState(3)
  const [skills, setSkills] = useState([])
  const [questionTypes, setQuestionTypes] = useState(['coding'])
  
  // Preview questions state
  const [previewQuestions, setPreviewQuestions] = useState(null)
  const [loadingPreview, setLoadingPreview] = useState(false)
  const [showPreview, setShowPreview] = useState(false)

  useEffect(() => {
    loadAssessment()
  }, [id])

  const loadAssessment = async () => {
    try {
      const data = await assessmentAPI.getAssessment(id)
      setAssessment(data)
      setDuration(data.total_duration_minutes)
      setNumQuestions(data.total_questions)
      setDifficulty(data.configuration?.difficulty || 'medium')
      setQuestionTypes(data.configuration?.question_types || ['coding'])
      
      // Extract unique skills from questions
      const uniqueSkills = [...new Set(data.questions.map(q => q.skill))]
      setSkills(uniqueSkills)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load assessment')
    } finally {
      setLoading(false)
    }
  }
  
  // Preview questions from database when skills or question types change
  const previewQuestionsFromDB = useCallback(async () => {
    if (skills.length === 0 || questionTypes.length === 0) {
      setPreviewQuestions(null)
      setShowPreview(false)
      return
    }
    
    setLoadingPreview(true)
    setError('')
    
    try {
      const result = await questionPreviewAPI.previewQuestions(
        skills,
        questionTypes,
        difficulty,
        numQuestions,
        duration
      )
      setPreviewQuestions(result)
      setShowPreview(true)
    } catch (err) {
      console.error('Preview error:', err)
      // Don't show error for preview, just hide preview
      setPreviewQuestions(null)
      setShowPreview(false)
    } finally {
      setLoadingPreview(false)
    }
  }, [skills, questionTypes, difficulty, numQuestions, duration])
  
  // Auto-preview when skills or question types change
  useEffect(() => {
    if (!loading && skills.length > 0 && questionTypes.length > 0) {
      const timer = setTimeout(() => {
        previewQuestionsFromDB()
      }, 500) // Debounce for 500ms
      
      return () => clearTimeout(timer)
    }
  }, [skills, questionTypes, difficulty, numQuestions, duration, loading, previewQuestionsFromDB])

  const handleSave = async (e) => {
    if (e) {
      e.preventDefault()
      e.stopPropagation()
    }
    
    setSaving(true)
    setError('')

    try {
      const updates = {
        duration,
        difficulty,
        num_questions: numQuestions,
        skills: skills.length > 0 ? skills : undefined,
        question_types: questionTypes
      }
      
      const updatedAssessment = await assessmentAPI.editAssessment(id, updates)
      
      // Navigate to preview after successful update
      if (updatedAssessment) {
        navigate(`/assessment/${id}`)
      }
    } catch (err) {
      console.error('Edit error:', err)
      setError(err.response?.data?.detail || 'Failed to update assessment')
    } finally {
      setSaving(false)
    }
  }
  
  const handleCancel = (e) => {
    if (e) {
      e.preventDefault()
    }
    navigate(`/assessment/${id}`)
  }

  const availableSkills = ['java', 'python', 'javascript', 'oop', 'multithreading', 'algorithms', 'arrays', 'linked-lists', 'graphs', 'design']
  const availableQuestionTypes = ['coding', 'mcq', 'debugging', 'system_design']

  if (loading) {
    return (
      <div className="edit-page">
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

  return (
    <div className="edit-page">
      <Navbar />
      <div className="container">
        <div className="edit-header">
          <h1>Edit Assessment</h1>
          <p>Modify assessment parameters and regenerate questions</p>
        </div>

        {error && <div className="error-message">{error}</div>}

        <div className="edit-form">
          <div className="form-row">
            <div className="form-group">
              <label>Duration (minutes)</label>
              <input
                type="number"
                className="input"
                value={duration}
                onChange={(e) => setDuration(parseInt(e.target.value) || 30)}
                min="15"
                max="180"
              />
            </div>

            <div className="form-group">
              <label>Number of Questions</label>
              <input
                type="number"
                className="input"
                value={numQuestions}
                onChange={(e) => setNumQuestions(parseInt(e.target.value) || 3)}
                min="1"
                max="20"
              />
            </div>

            <div className="form-group">
              <label>Difficulty</label>
              <select
                className="input"
                value={difficulty}
                onChange={(e) => setDifficulty(e.target.value)}
              >
                <option value="easy">Easy</option>
                <option value="medium">Medium</option>
                <option value="hard">Hard</option>
              </select>
            </div>
          </div>

          <div className="form-group">
            <label>Skills</label>
            <div className="checkbox-group">
              {availableSkills.map(skill => (
                <label key={skill} className="checkbox-label">
                  <input
                    type="checkbox"
                    checked={skills.includes(skill)}
                    onChange={(e) => {
                      if (e.target.checked) {
                        setSkills([...skills, skill])
                      } else {
                        setSkills(skills.filter(s => s !== skill))
                      }
                      // Trigger preview update
                      setTimeout(() => previewQuestionsFromDB(), 100)
                    }}
                  />
                  <span>{skill}</span>
                </label>
              ))}
            </div>
          </div>

          <div className="form-group">
            <label>Question Types</label>
            <div className="checkbox-group">
              {availableQuestionTypes.map(type => (
                <label key={type} className="checkbox-label">
                  <input
                    type="checkbox"
                    checked={questionTypes.includes(type)}
                    onChange={(e) => {
                      if (e.target.checked) {
                        setQuestionTypes([...questionTypes, type])
                      } else {
                        setQuestionTypes(questionTypes.filter(t => t !== type))
                      }
                      // Trigger preview update
                      setTimeout(() => previewQuestionsFromDB(), 100)
                    }}
                  />
                  <span>{type.replace('_', ' ')}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Preview Questions Section */}
          {showPreview && previewQuestions && (
            <div className="preview-section">
              <div className="preview-header">
                <h3>Preview Questions from Database</h3>
                <button
                  type="button"
                  className="btn btn-small"
                  onClick={() => setShowPreview(false)}
                >
                  Hide Preview
                </button>
              </div>
              
              {loadingPreview ? (
                <div className="loading-state">
                  <span className="loading"></span>
                  <p>Loading questions from database...</p>
                </div>
              ) : (
                <>
                  <div className="preview-summary">
                    <p>
                      <strong>Total:</strong> {previewQuestions.total} questions found
                      {' | '}
                      <span className="difficulty-badge easy">Easy: {previewQuestions.summary.easy}</span>
                      {' | '}
                      <span className="difficulty-badge medium">Medium: {previewQuestions.summary.medium}</span>
                      {' | '}
                      <span className="difficulty-badge hard">Hard: {previewQuestions.summary.hard}</span>
                    </p>
                  </div>
                  
                  <div className="preview-questions">
                    {Object.entries(previewQuestions.grouped_by_difficulty).map(([diff, questions]) => {
                      if (questions.length === 0) return null
                      return (
                        <div key={diff} className="preview-difficulty-group">
                          <h4 className={`difficulty-${diff}`}>
                            {diff.charAt(0).toUpperCase() + diff.slice(1)} ({questions.length})
                          </h4>
                          <div className="preview-questions-list">
                            {questions.slice(0, 5).map((q, idx) => (
                              <div key={q.id || idx} className="preview-question-item">
                                <span className="question-title">{q.title}</span>
                                <span className="question-skill">{q.skill}</span>
                                <span className="question-time">{q.estimated_time_minutes} min</span>
                              </div>
                            ))}
                            {questions.length > 5 && (
                              <div className="preview-more">+ {questions.length - 5} more questions</div>
                            )}
                          </div>
                        </div>
                      )
                    })}
                  </div>
                </>
              )}
            </div>
          )}
          
          {skills.length > 0 && questionTypes.length > 0 && !showPreview && (
            <div className="preview-trigger">
              <button
                type="button"
                className="btn btn-secondary"
                onClick={previewQuestionsFromDB}
                disabled={loadingPreview}
              >
                {loadingPreview ? 'Loading...' : 'Preview Questions from Database'}
              </button>
            </div>
          )}

          <div className="form-actions">
            <button
              type="button"
              className="btn btn-secondary"
              onClick={handleCancel}
            >
              Cancel
            </button>
            <button
              type="button"
              className="btn btn-primary"
              onClick={handleSave}
              disabled={saving}
            >
              {saving ? (
                <>
                  <span className="loading"></span>
                  <span style={{ marginLeft: '8px' }}>Updating...</span>
                </>
              ) : (
                'Save Changes'
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default EditAssessment

