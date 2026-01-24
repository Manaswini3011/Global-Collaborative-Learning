import React from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import IntentInput from './pages/IntentInput'
import AssessmentPreview from './pages/AssessmentPreview'
import EditAssessment from './pages/EditAssessment'
import FinalSummary from './pages/FinalSummary'
import Statistics from './pages/Statistics'
import Settings from './pages/Settings'
import ProtectedRoute from './components/ProtectedRoute'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/intent"
          element={
            <ProtectedRoute>
              <IntentInput />
            </ProtectedRoute>
          }
        />
        <Route
          path="/assessment/:id"
          element={
            <ProtectedRoute>
              <AssessmentPreview />
            </ProtectedRoute>
          }
        />
        <Route
          path="/assessment/:id/edit"
          element={
            <ProtectedRoute>
              <EditAssessment />
            </ProtectedRoute>
          }
        />
        <Route
          path="/assessment/:id/summary"
          element={
            <ProtectedRoute>
              <FinalSummary />
            </ProtectedRoute>
          }
        />
        <Route
          path="/statistics"
          element={
            <ProtectedRoute>
              <Statistics />
            </ProtectedRoute>
          }
        />
        <Route
          path="/settings"
          element={
            <ProtectedRoute>
              <Settings />
            </ProtectedRoute>
          }
        />
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </Router>
  )
}

export default App

