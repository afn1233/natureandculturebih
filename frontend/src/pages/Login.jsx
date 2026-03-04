// Login.jsx - Welcome screen with email login
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../App'
import { login } from '../api'

function Login() {
  const [email, setEmail] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const { login: authLogin } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!email) return

    setLoading(true)
    setError('')

    try {
      const user = await login(email)
      authLogin(user)
      navigate('/dashboard')
    } catch (err) {
      setError('Something went wrong. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center" style={{ backgroundColor: '#1e3a2f' }}>
      {/* Background pattern */}
      <div className="absolute inset-0 opacity-5">
        <div className="absolute inset-0" style={{
          backgroundImage: 'radial-gradient(circle at 25px 25px, white 2px, transparent 0)',
          backgroundSize: '50px 50px'
        }}></div>
      </div>

      <div className="relative z-10 w-full max-w-md px-8">
        {/* Logo */}
        <div className="text-center mb-10">
          <h1 className="font-display text-5xl font-bold mb-3" style={{ color: '#f5f0e8' }}>
            Nature & Culture
          </h1>
          <h2 className="font-display text-3xl" style={{ color: '#c8893a' }}>
            BiH
          </h2>
          <p className="mt-4 text-sm" style={{ color: 'rgba(245,240,232,0.5)' }}>
            Discover the beauty of Bosnia & Herzegovina
          </p>
        </div>

        {/* Login form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label
              htmlFor="email"
              className="block text-xs font-medium uppercase tracking-widest mb-2"
              style={{ color: 'rgba(245,240,232,0.6)' }}
            >
              Email Address
            </label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              required
              className="w-full px-4 py-3 rounded-lg text-black outline-none transition-all duration-200"
              style={{
                backgroundColor: 'rgba(255,255,255,0.9)',
                border: '2px solid transparent',
                color: '#000000'
              }}
              onFocus={(e) => e.target.style.borderColor = '#c8893a'}
              onBlur={(e) => e.target.style.borderColor = 'transparent'}
            />
          </div>

          {error && (
            <p className="text-red-400 text-sm text-center">{error}</p>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 rounded-lg font-medium text-white transition-all duration-200 hover:opacity-90"
            style={{ backgroundColor: '#c8893a' }}
          >
            {loading ? 'Entering...' : 'Enter Bosnia'}
          </button>
        </form>

        <p className="text-center mt-6 text-xs" style={{ color: 'rgba(245,240,232,0.3)' }}>
          No password needed — just your email
        </p>
      </div>
    </div>
  )
}

export default Login