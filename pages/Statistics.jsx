import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import Navbar from '../components/Navbar'
import { statisticsAPI } from '../services/api'
import '../styles/Statistics.css'

const Statistics = () => {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  useEffect(() => {
    loadStatistics()
  }, [])

  const loadStatistics = async () => {
    try {
      const data = await statisticsAPI.getStatistics()
      setStats(data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load statistics')
    } finally {
      setLoading(false)
    }
  }

  const handleRefresh = () => {
    setLoading(true)
    loadStatistics()
  }

  if (loading) {
    return (
      <div className="statistics-page">
        <Navbar />
        <div className="container">
          <div className="loading-state">
            <span className="loading"></span>
            <p>Loading statistics...</p>
          </div>
        </div>
      </div>
    )
  }

  if (error || !stats) {
    return (
      <div className="statistics-page">
        <Navbar />
        <div className="container">
          <div className="error-message">{error || 'Failed to load statistics'}</div>
          <button className="btn btn-primary" onClick={handleRefresh}>Retry</button>
        </div>
      </div>
    )
  }

  return (
    <div className="statistics-page">
      <Navbar />
      <div className="container">
        <div className="statistics-header">
          <h1>Assessment Statistics</h1>
          <button className="btn btn-secondary" onClick={handleRefresh}>
            🔄 Refresh
          </button>
        </div>

        <div className="stats-grid">
          <div className="stat-card primary">
            <div className="stat-icon">📊</div>
            <div className="stat-value">{stats.total_assessments}</div>
            <div className="stat-label">Total Assessments</div>
          </div>

          <div className="stat-card success">
            <div className="stat-icon">✅</div>
            <div className="stat-value">{stats.finalized_assessments}</div>
            <div className="stat-label">Finalized</div>
          </div>

          <div className="stat-card warning">
            <div className="stat-icon">📝</div>
            <div className="stat-value">{stats.draft_assessments}</div>
            <div className="stat-label">Draft</div>
          </div>

          <div className="stat-card info">
            <div className="stat-icon">❓</div>
            <div className="stat-value">{stats.total_questions_used}</div>
            <div className="stat-label">Questions Used</div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">⏱️</div>
            <div className="stat-value">{stats.average_duration_minutes} min</div>
            <div className="stat-label">Avg Duration</div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">🔌</div>
            <div className="stat-value">{stats.api_statistics.total_calls}</div>
            <div className="stat-label">API Calls (7 days)</div>
          </div>
        </div>

        <div className="stats-sections">
          <div className="stats-section">
            <h2>Skills Distribution</h2>
            <div className="distribution-chart">
              {Object.entries(stats.skills_distribution || {}).map(([skill, count]) => (
                <div key={skill} className="distribution-item">
                  <div className="distribution-label">{skill}</div>
                  <div className="distribution-bar">
                    <div 
                      className="distribution-fill" 
                      style={{ width: `${(count / Math.max(...Object.values(stats.skills_distribution || {}))) * 100}%` }}
                    ></div>
                  </div>
                  <div className="distribution-value">{count}</div>
                </div>
              ))}
            </div>
          </div>

          <div className="stats-section">
            <h2>Difficulty Distribution</h2>
            <div className="difficulty-stats">
              {Object.entries(stats.difficulty_distribution || {}).map(([difficulty, count]) => (
                <div key={difficulty} className={`difficulty-item ${difficulty}`}>
                  <span className="difficulty-label">{difficulty.toUpperCase()}</span>
                  <span className="difficulty-count">{count}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="stats-section">
            <h2>API Usage</h2>
            <div className="api-stats">
              <div className="api-stat-item">
                <span>Gemini API Calls:</span>
                <strong>{stats.api_statistics.gemini_calls}</strong>
              </div>
              <div className="api-stat-item">
                <span>OpenAI API Calls:</span>
                <strong>{stats.api_statistics.openai_calls}</strong>
              </div>
              <div className="api-stat-item">
                <span>Avg Response Time:</span>
                <strong>{stats.api_statistics.avg_response_time_ms}ms</strong>
              </div>
              <div className="api-stat-item">
                <span>Unique Endpoints:</span>
                <strong>{stats.api_statistics.unique_endpoints}</strong>
              </div>
            </div>
          </div>

          <div className="stats-section">
            <h2>Recent Assessments</h2>
            <div className="recent-assessments">
              {stats.recent_assessments && stats.recent_assessments.length > 0 ? (
                stats.recent_assessments.map((assessment) => (
                  <div 
                    key={assessment.id} 
                    className="recent-item"
                    onClick={() => navigate(`/assessment/${assessment.id}`)}
                  >
                    <div className="recent-title">{assessment.title}</div>
                    <div className="recent-meta">
                      <span>{assessment.total_questions} questions</span>
                      <span>{assessment.total_duration_minutes} min</span>
                      <span className={`status-badge ${assessment.status}`}>{assessment.status}</span>
                    </div>
                  </div>
                ))
              ) : (
                <p className="no-data">No assessments yet</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Statistics

