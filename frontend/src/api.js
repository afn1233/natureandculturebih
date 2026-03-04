// api.js - All API calls in one place
// Every function here talks to the FastAPI backend

const API_URL = ''

// Helper to get user ID from localStorage
const getUserId = () => localStorage.getItem('user_id')

// Helper for headers including user ID
const getHeaders = () => ({
  'Content-Type': 'application/json',
  'X-User-Id': getUserId()
})

// ── Auth ──────────────────────────────────────────────────
export const login = async (email) => {
  const response = await fetch(`${API_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email })
  })
  if (!response.ok) throw new Error('Login failed')
  return response.json()
}

// ── Links ─────────────────────────────────────────────────
export const getLinks = async () => {
  const response = await fetch(`${API_URL}/links`, {
    headers: getHeaders()
  })
  if (!response.ok) throw new Error('Failed to fetch links')
  return response.json()
}

export const createLink = async (data) => {
  const response = await fetch(`${API_URL}/links`, {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify(data)
  })
  if (!response.ok) throw new Error('Failed to create link')
  return response.json()
}

export const updateLink = async (id, data) => {
  const response = await fetch(`${API_URL}/links/${id}`, {
    method: 'PUT',
    headers: getHeaders(),
    body: JSON.stringify(data)
  })
  if (!response.ok) throw new Error('Failed to update link')
  return response.json()
}

export const deleteLink = async (id) => {
  const response = await fetch(`${API_URL}/links/${id}`, {
    method: 'DELETE',
    headers: getHeaders()
  })
  if (!response.ok) throw new Error('Failed to delete link')
}

// ── Chat ──────────────────────────────────────────────────
export const sendChat = async (message) => {
  const response = await fetch(`${API_URL}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message,
      user_id: getUserId()
    })
  })
  if (!response.ok) throw new Error('Failed to send message')
  return response.json()
}

// ── MCP Stats ─────────────────────────────────────────────
export const getStats = async () => {
  const response = await fetch(`${API_URL}/mcp/stats?user_id=${getUserId()}`, {
    headers: { 'Content-Type': 'application/json' }
  })
  if (!response.ok) throw new Error('Failed to fetch stats')
  return response.json()
}