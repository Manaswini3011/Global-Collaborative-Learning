import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import Navbar from '../components/Navbar'
import { assessmentAPI } from '../services/api'
import '../styles/IntentInput.css'

const IntentInput = () => {
  const [prompt, setPrompt] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    e.stopPropagation()
    
    if (!prompt.trim()) {
      setError('Please enter an intent prompt')
      return
    }

    setError('')
    setLoading(true)

    try {
      const response = await assessmentAPI.parseIntent(prompt)
      if (response && response.assessment_id) {
        navigate(`/assessment/${response.assessment_id}`)
      } else {
        throw new Error('Invalid response from server')
      }
    } catch (err) {
      console.error('Parse intent error:', err)
      setError(err.response?.data?.detail || err.message || 'Failed to parse intent. Please try again.')
    } finally {
      setLoading(false)
    }
  }
  
  const handleExampleClick = (example) => {
    setPrompt(example)
    setError('')
  }

  const examplePrompts = [
    "I want to test Java developer on OOP and multithreading for 30 minutes",
    "Create a 45-minute assessment for Python developer focusing on algorithms and data structures",
    "Test senior JavaScript engineer on system design and API development for 60 minutes",
    "Generate an easy-level assessment for junior developer covering basic programming concepts"
  ]

  return (
    <div className="intent-page">
      <Navbar />
      <div className="intent-container">
        <div className="intent-header">
          <h1>Create Assessment from Intent</h1>
          <p>Describe your hiring needs in natural language</p>
        </div>

        <form onSubmit={handleSubmit} className="intent-form">
          <div className="form-group">
            <label htmlFor="prompt">Assessment Intent</label>
            <textarea
              id="prompt"
              className="textarea intent-textarea"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Example: I want to test Java developer on OOP and multithreading for 30 minutes"
              required
            />
          </div>

          {error && <div className="error-message">{error}</div>}

          <div className="form-actions">
            <button
              type="submit"
              className="btn btn-primary"
              disabled={loading || !prompt.trim()}
            >
              {loading ? (
                <>
                  <span className="loading"></span>
                  <span style={{ marginLeft: '8px' }}>Generating Assessment...</span>
                </>
              ) : (
                'Generate Assessment'
              )}
            </button>
          </div>
        </form>

        <div className="examples-section">
          <h3>Example Intents</h3>
          <div className="examples-grid">
            {examplePrompts.map((example, idx) => (
              <div
                key={idx}
                className="example-card"
                onClick={() => handleExampleClick(example)}
                role="button"
                tabIndex={0}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault()
                    handleExampleClick(example)
                  }
                }}
              >
                <p>{example}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default IntentInput

