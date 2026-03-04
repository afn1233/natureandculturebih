// Dashboard.jsx - Main page showing all tourist links
import { useState, useEffect } from 'react'
import { useAuth } from '../App'
import { getLinks } from '../api'
import LinkCard from '../components/LinkCard'
import AddLinkForm from '../components/AddLinkForm'
import ChatPanel from '../components/ChatPanel'

function Dashboard() {
  const { user, logout } = useAuth()
  const [links, setLinks] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  // Fetch links when page loads
  const fetchLinks = async () => {
    try {
      setLoading(true)
      const data = await getLinks()
      setLinks(data)
    } catch (err) {
      setError('Failed to load links')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchLinks()
  }, [])

  return (
    <div className="min-h-screen" style={{ backgroundColor: '#f5f0e8' }}>
      {/* Header */}
      <header style={{ backgroundColor: '#1e3a2f', borderBottom: '2px solid #c8893a' }}>
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <h1 className="font-display text-xl font-bold" style={{ color: '#f5f0e8' }}>
              Nature & Culture <span style={{ color: '#c8893a' }}>BiH</span>
            </h1>
          </div>
          <div className="flex items-center gap-4">
            <span className="text-sm" style={{ color: 'rgba(245,240,232,0.6)' }}>
              {user?.email}
            </span>
            <button
              onClick={logout}
              className="text-sm px-4 py-1.5 rounded-full transition-all duration-200 hover:opacity-80"
              style={{
                backgroundColor: 'rgba(255,255,255,0.1)',
                border: '1px solid rgba(255,255,255,0.2)',
                color: '#f5f0e8'
              }}
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      {/* Main content */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">

          {/* Left panel - Links list */}
          <div className="lg:col-span-2">
            <div className="mb-6">
              <h2 className="font-display text-2xl font-bold" style={{ color: '#1e3a2f' }}>
                My Tourist Links
              </h2>
              <p className="text-sm mt-1" style={{ color: '#b8a898' }}>
                Manage your saved locations across Bosnia & Herzegovina
              </p>
            </div>

            {/* Loading state */}
            {loading && (
              <div className="flex items-center justify-center py-20">
                <div className="text-center">
                  <div className="w-8 h-8 border-2 border-amber-500 border-t-transparent rounded-full animate-spin mx-auto mb-3"
                    style={{ borderColor: '#c8893a', borderTopColor: 'transparent' }}
                  ></div>
                  <p style={{ color: '#b8a898' }}>Loading your locations...</p>
                </div>
              </div>
            )}

            {/* Error state */}
            {error && (
              <div className="p-4 rounded-lg bg-red-50 border border-red-200 text-red-600">
                {error}
              </div>
            )}

            {/* Empty state */}
            {!loading && !error && links.length === 0 && (
              <div className="text-center py-20">
                <p className="text-4xl mb-4">🏔️</p>
                <p className="font-display text-xl mb-2" style={{ color: '#1e3a2f' }}>
                  No locations yet
                </p>
                <p style={{ color: '#b8a898' }}>
                  Add your first tourist location using the form →
                </p>
              </div>
            )}

            {/* Links list */}
            {!loading && links.map(link => (
              <LinkCard
                key={link.id}
                link={link}
                onRefresh={fetchLinks}
              />
            ))}
          </div>

          {/* Right panel - Add form + Stats */}
          <div className="lg:col-span-1">
            <AddLinkForm onSuccess={fetchLinks} />
          </div>
        </div>
      </div>

      {/* Chat panel */}
      <ChatPanel />
    </div>
  )
}

export default Dashboard