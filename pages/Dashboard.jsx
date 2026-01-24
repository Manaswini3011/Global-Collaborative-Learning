import React from 'react'
import { Link } from 'react-router-dom'
import Navbar from '../components/Navbar'
import '../styles/Dashboard.css'

const Dashboard = () => {
  return (
    <div className="dashboard-page">
      <Navbar />
      <div className="dashboard-container">
        <div className="dashboard-header">
          <h1>Dashboard</h1>
          <p className="dashboard-subtitle">AI-Powered Assessment Generation</p>
        </div>

        <div className="dashboard-grid">
          <Link to="/intent" className="dashboard-card primary-card">
            <div className="card-icon">✨</div>
            <h2>Create New Assessment</h2>
            <p>Generate an assessment from natural language intent</p>
            <div className="card-arrow">→</div>
          </Link>

          <Link to="/statistics" className="dashboard-card">
            <div className="card-icon">📊</div>
            <h2>Assessment Analytics</h2>
            <p>View statistics and insights</p>
            <div className="card-arrow">→</div>
          </Link>

          <Link to="/settings" className="dashboard-card">
            <div className="card-icon">⚙️</div>
            <h2>Settings</h2>
            <p>Configure your preferences</p>
            <div className="card-arrow">→</div>
          </Link>
        </div>

        <div className="dashboard-info">
          <div className="info-card">
            <h3>How It Works</h3>
            <ol>
              <li>Enter your hiring intent in natural language</li>
              <li>AI parses and understands your requirements</li>
              <li>System generates a balanced assessment</li>
              <li>Preview, edit, and finalize your assessment</li>
            </ol>
          </div>

          <div className="info-card">
            <h3>Example Intent</h3>
            <div className="example-intent">
              <p className="terminal-line">"I want to test Java developer on OOP and multithreading for 30 minutes"</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard

