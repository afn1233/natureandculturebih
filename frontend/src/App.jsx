// App.jsx - Main app component with routing and auth context
import { useState, useEffect, createContext, useContext } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'

// Auth context - stores user info and shares it across all components
export const AuthContext = createContext(null)

export function useAuth() {
  return useContext(AuthContext)
}

function App() {
  const [user, setUser] = useState(null)

  // Check if user is already logged in when app loads
  useEffect(() => {
    const userId = localStorage.getItem('user_id')
    const userEmail = localStorage.getItem('user_email')
    if (userId && userEmail) {
      setUser({ id: userId, email: userEmail })
    }
  }, [])

  const login = (userData) => {
    // Save user to state and localStorage
    setUser(userData)
    localStorage.setItem('user_id', userData.id)
    localStorage.setItem('user_email', userData.email)
  }

  const logout = () => {
    // Clear user from state and localStorage
    setUser(null)
    localStorage.removeItem('user_id')
    localStorage.removeItem('user_email')
  }

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      <BrowserRouter>
        <Routes>
          <Route
            path="/"
            element={user ? <Navigate to="/dashboard" /> : <Login />}
          />
          <Route
            path="/dashboard"
            element={user ? <Dashboard /> : <Navigate to="/" />}
          />
        </Routes>
      </BrowserRouter>
    </AuthContext.Provider>
  )
}

export default App