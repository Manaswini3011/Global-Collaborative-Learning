import React, { useState, useEffect } from 'react'
import Navbar from '../components/Navbar'
import '../styles/Settings.css'

const Settings = () => {
  const [settings, setSettings] = useState({
    defaultDuration: 30,
    defaultDifficulty: 'medium',
    defaultNumQuestions: 3,
    autoSave: true,
    notifications: true,
    theme: 'dark'
  })
  const [saving, setSaving] = useState(false)
  const [message, setMessage] = useState('')

  useEffect(() => {
    // Load saved settings from localStorage
    const saved = localStorage.getItem('assessmentSettings')
    if (saved) {
      try {
        setSettings({ ...settings, ...JSON.parse(saved) })
      } catch (e) {
        console.error('Failed to load settings', e)
      }
    }
  }, [])

  const handleChange = (key, value) => {
    setSettings(prev => ({ ...prev, [key]: value }))
  }

  const handleSave = () => {
    setSaving(true)
    setMessage('')
    
    // Simulate API call
    setTimeout(() => {
      localStorage.setItem('assessmentSettings', JSON.stringify(settings))
      setSaving(false)
      setMessage('Settings saved successfully!')
      setTimeout(() => setMessage(''), 3000)
    }, 500)
  }

  const handleReset = () => {
    const defaultSettings = {
      defaultDuration: 30,
      defaultDifficulty: 'medium',
      defaultNumQuestions: 3,
      autoSave: true,
      notifications: true,
      theme: 'dark'
    }
    setSettings(defaultSettings)
    localStorage.setItem('assessmentSettings', JSON.stringify(defaultSettings))
    setMessage('Settings reset to defaults!')
    setTimeout(() => setMessage(''), 3000)
  }

  return (
    <div className="settings-page">
      <Navbar />
      <div className="container">
        <div className="settings-header">
          <h1>Settings</h1>
          <p>Configure your assessment preferences</p>
        </div>

        {message && (
          <div className={`message ${message.includes('success') ? 'success' : ''}`}>
            {message}
          </div>
        )}

        <div className="settings-content">
          <div className="settings-section">
            <h2>Default Assessment Settings</h2>
            
            <div className="setting-item">
              <label>Default Duration (minutes)</label>
              <input
                type="number"
                className="input"
                value={settings.defaultDuration}
                onChange={(e) => handleChange('defaultDuration', parseInt(e.target.value) || 30)}
                min="15"
                max="180"
              />
              <p className="setting-hint">Default time limit for new assessments</p>
            </div>

            <div className="setting-item">
              <label>Default Difficulty</label>
              <select
                className="input"
                value={settings.defaultDifficulty}
                onChange={(e) => handleChange('defaultDifficulty', e.target.value)}
              >
                <option value="easy">Easy</option>
                <option value="medium">Medium</option>
                <option value="hard">Hard</option>
              </select>
              <p className="setting-hint">Default difficulty level for assessments</p>
            </div>

            <div className="setting-item">
              <label>Default Number of Questions</label>
              <input
                type="number"
                className="input"
                value={settings.defaultNumQuestions}
                onChange={(e) => handleChange('defaultNumQuestions', parseInt(e.target.value) || 3)}
                min="1"
                max="20"
              />
              <p className="setting-hint">Default number of questions per assessment</p>
            </div>
          </div>

          <div className="settings-section">
            <h2>Preferences</h2>
            
            <div className="setting-item">
              <div className="setting-toggle">
                <label>Auto-save Assessments</label>
                <label className="switch">
                  <input
                    type="checkbox"
                    checked={settings.autoSave}
                    onChange={(e) => handleChange('autoSave', e.target.checked)}
                  />
                  <span className="slider"></span>
                </label>
              </div>
              <p className="setting-hint">Automatically save assessment drafts</p>
            </div>

            <div className="setting-item">
              <div className="setting-toggle">
                <label>Notifications</label>
                <label className="switch">
                  <input
                    type="checkbox"
                    checked={settings.notifications}
                    onChange={(e) => handleChange('notifications', e.target.checked)}
                  />
                  <span className="slider"></span>
                </label>
              </div>
              <p className="setting-hint">Receive notifications for assessment updates</p>
            </div>
          </div>

          <div className="settings-actions">
            <button className="btn btn-secondary" onClick={handleReset}>
              Reset to Defaults
            </button>
            <button 
              className="btn btn-primary" 
              onClick={handleSave}
              disabled={saving}
            >
              {saving ? 'Saving...' : 'Save Settings'}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Settings

