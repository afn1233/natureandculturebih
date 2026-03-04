import { useState } from 'react'
import { updateLink, deleteLink } from '../api'

function LinkCard({ link, onRefresh }) {
  const [editing, setEditing] = useState(false)
  const [saving, setSaving] = useState(false)
  const [editData, setEditData] = useState({
    title: link.title,
    url: link.url,
    description: link.description || ''
  })

  const formatDate = (dateStr) => {
    return new Date(dateStr).toLocaleDateString('en-US', {
      month: 'short', day: 'numeric', year: 'numeric'
    })
  }

  const getWeatherBadge = () => {
    if (!link.latest_weather) return null
    const w = link.latest_weather.weather_data
    const temp = w.temperature || w.temp || ''
    const desc = w.description || w.condition || ''
    return temp + (temp ? 'C ' : '') + desc
  }

  const handleSave = async () => {
    setSaving(true)
    try {
      await updateLink(link.id, editData)
      setEditing(false)
      onRefresh()
    } catch (err) {
      alert('Failed to update link')
    } finally {
      setSaving(false)
    }
  }

  const handleDelete = async () => {
    if (!window.confirm('Delete this location?')) return
    try {
      await deleteLink(link.id)
      onRefresh()
    } catch (err) {
      alert('Failed to delete link')
    }
  }

  const weatherBadge = getWeatherBadge()

  if (editing) {
    return (
      <div className="bg-white rounded-xl p-5 mb-4" style={{border: '2px solid #c8893a'}}>
        <div className="space-y-3">
          <div>
            <label style={{color: '#b8a898'}}>Title</label>
            <input type="text" value={editData.title} onChange={(e) => setEditData({...editData, title: e.target.value})} className="w-full px-3 py-2 rounded-lg" style={{border: '1px solid #e8ddd0', color: '#000000'}} />
          </div>
          <div>
            <label style={{color: '#b8a898'}}>URL</label>
            <input type="url" value={editData.url} onChange={(e) => setEditData({...editData, url: e.target.value})} className="w-full px-3 py-2 rounded-lg" style={{border: '1px solid #e8ddd0', color: '#000000'}} />
          </div>
          <div>
            <label style={{color: '#b8a898'}}>Description</label>
            <textarea value={editData.description} onChange={(e) => setEditData({...editData, description: e.target.value})} rows={3} className="w-full px-3 py-2 rounded-lg resize-none" style={{border: '1px solid #e8ddd0', color: '#000000'}} />
          </div>
          <div className="flex gap-2">
            <button onClick={handleSave} disabled={saving} className="px-4 py-2 rounded-lg text-sm text-white" style={{backgroundColor: '#c8893a'}}>{saving ? 'Saving...' : 'Save'}</button>
            <button onClick={() => setEditing(false)} className="px-4 py-2 rounded-lg text-sm" style={{backgroundColor: '#f5f0e8', color: '#1e3a2f'}}>Cancel</button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-xl p-5 mb-4" style={{border: '1px solid #e8ddd0'}}>
      <div className="flex items-start justify-between mb-2">
        <h3 className="font-medium text-base pr-4" style={{color: '#1e3a2f'}}>{link.title}</h3>
        <div className="flex gap-2">
          <button onClick={() => setEditing(true)} className="px-3 py-1 rounded-lg text-xs" style={{border: '1px solid #e8ddd0', color: '#b8a898'}}>Edit</button>
          <button onClick={handleDelete} className="px-3 py-1 rounded-lg text-xs" style={{color: '#c0392b', backgroundColor: '#fff5f5'}}>Delete</button>
        </div>
      </div>
      <p className="text-xs mb-2 truncate" style={{color: '#c8893a'}}>{link.url}</p>
      {link.description && (
        <p className="text-sm mb-3" style={{color: '#6b6b6b'}}>{link.description}</p>
      )}
      <div className="flex items-center justify-between">
        <span className="text-xs" style={{color: '#b8a898'}}>{formatDate(link.created_at)}</span>
        {weatherBadge && (
          <span className="text-xs px-2 py-1 rounded-full" style={{backgroundColor: '#e8f4f8', color: '#2980b9'}}>{weatherBadge}</span>
        )}
      </div>
    </div>
  )
}

export default LinkCard
