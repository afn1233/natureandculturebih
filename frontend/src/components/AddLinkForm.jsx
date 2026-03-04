import { useState } from 'react'
import { createLink } from '../api'
import { getStats } from '../api'

function AddLinkForm({ onSuccess }) {
  const [formData, setFormData] = useState({
    title: '',
    url: '',
    description: ''
  })
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  const [stats, setStats] = useState(null)

  useState(() => {
    getStats().then(setStats).catch(() => {})
  }, [])

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!formData.title || !formData.url) return
    setSaving(true)
    setError('')
    try {
      await createLink(formData)
      setFormData({ title: '', url: '', description: '' })
      const newStats = await getStats()
      setStats(newStats)
      onSuccess()
    } catch (err) {
      setError('Failed to save location')
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="rounded-xl p-6" style={{backgroundColor: '#1e3a2f'}}>
      <h2 className="font-display text-lg font-bold mb-1" style={{color: '#f5f0e8'}}>
        Add New Location
      </h2>
      <p className="text-xs mb-6" style={{color: 'rgba(245,240,232,0.5)'}}>
        Paste a link and describe the place
      </p>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-xs uppercase tracking-wider mb-1" style={{color: 'rgba(245,240,232,0.6)'}}>
            Title
          </label>
          <input
            type="text"
            value={formData.title}
            onChange={(e) => setFormData({...formData, title: e.target.value})}
            placeholder="e.g. Stari Most, Mostar"
            required
            className="w-full px-3 py-2 rounded-lg text-black"
            style={{
              backgroundColor: 'rgba(255,255,255,0.9)',
              border: '1px solid rgba(255,255,255,0.1)',
              color: '#000000'
            }}
          />
        </div>

        <div>
          <label className="block text-xs uppercase tracking-wider mb-1" style={{color: 'rgba(245,240,232,0.6)'}}>
            URL
          </label>
          <input
            type="url"
            value={formData.url}
            onChange={(e) => setFormData({...formData, url: e.target.value})}
            placeholder="https://..."
            required
            className="w-full px-3 py-2 rounded-lg"
            style={{
              backgroundColor: 'rgba(255,255,255,0.9)',
              border: '1px solid rgba(255,255,255,0.1)',
              color: '#000000'
            }}
          />
        </div>

        <div>
          <label className="block text-xs uppercase tracking-wider mb-1" style={{color: 'rgba(245,240,232,0.6)'}}>
            Description
          </label>
          <textarea
            value={formData.description}
            onChange={(e) => setFormData({...formData, description: e.target.value})}
            placeholder="What makes this place worth visiting?"
            rows={3}
            className="w-full px-3 py-2 rounded-lg resize-none"
            style={{
              backgroundColor: 'rgba(255,255,255,0.9)',
              border: '1px solid rgba(255,255,255,0.1)',
              color: '#000000'
            }}
          />
        </div>

        {error && (
          <p className="text-red-400 text-xs">{error}</p>
        )}

        <button
          type="submit"
          disabled={saving}
          className="w-full py-3 rounded-lg text-sm font-medium text-white transition-all duration-200 hover:opacity-90"
          style={{backgroundColor: '#c8893a'}}
        >
          {saving ? 'Saving...' : 'Save Location'}
        </button>
      </form>

      {stats && (
        <div className="mt-6 pt-6" style={{borderTop: '1px solid rgba(255,255,255,0.1)'}}>
          <h3 className="font-display text-sm mb-3" style={{color: '#f5f0e8'}}>My Stats</h3>
          <div className="grid grid-cols-2 gap-3">
            <div className="rounded-lg p-3 text-center" style={{backgroundColor: 'rgba(255,255,255,0.06)', border: '1px solid rgba(255,255,255,0.1)'}}>
              <div className="font-display text-2xl" style={{color: '#c8893a'}}>{stats.total_links}</div>
              <div className="text-xs mt-1" style={{color: 'rgba(245,240,232,0.5)'}}>Locations</div>
            </div>
            <div className="rounded-lg p-3 text-center" style={{backgroundColor: 'rgba(255,255,255,0.06)', border: '1px solid rgba(255,255,255,0.1)'}}>
              <div className="font-display text-2xl" style={{color: '#c8893a'}}>{stats.total_weather_updates}</div>
              <div className="text-xs mt-1" style={{color: 'rgba(245,240,232,0.5)'}}>Weather Updates</div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default AddLinkForm