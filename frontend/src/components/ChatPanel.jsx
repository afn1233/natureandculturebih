import { useState } from 'react'
import Markdown from 'react-markdown'
import { sendChat } from '../api'

function ChatPanel() {
  const [open, setOpen] = useState(false)
  const [messages, setMessages] = useState([
    { role: 'ai', text: 'Hello! Ask me anything about your saved locations in Bosnia & Herzegovina.' }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSend = async () => {
    if (!input.trim() || loading) return
    const userMessage = input.trim()
    setInput('')
    setMessages(prev => [...prev, { role: 'user', text: userMessage }])
    setLoading(true)
    try {
      const data = await sendChat(userMessage)
      setMessages(prev => [...prev, { role: 'ai', text: data.response }])
    } catch (err) {
      setMessages(prev => [...prev, { role: 'ai', text: 'Sorry, something went wrong. Please try again.' }])
    } finally {
      setLoading(false)
    }
  }

  const handleKey = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div>
      {open && (
        <div style={{position: 'fixed', bottom: '90px', right: '28px', width: '340px', height: '440px', backgroundColor: 'white', borderRadius: '16px', boxShadow: '0 20px 60px rgba(0,0,0,0.18)', display: 'flex', flexDirection: 'column', overflow: 'hidden', border: '1px solid #e8ddd0', zIndex: 99}}>
          <div style={{backgroundColor: '#1e3a2f', padding: '14px 18px'}}>
            <div style={{fontFamily: 'Playfair Display, serif', color: '#f5f0e8', fontSize: '15px'}}>Ask about BiH</div>
            <div style={{fontSize: '11px', color: 'rgba(245,240,232,0.5)'}}>Powered by Claude AI</div>
          </div>
          <div style={{flex: 1, padding: '16px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '10px', backgroundColor: '#fafafa'}}>
            {messages.map((msg, i) => (
              <div key={i} style={{maxWidth: '82%', padding: '10px 13px', borderRadius: '12px', fontSize: '13px', lineHeight: '1.5', alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start', backgroundColor: msg.role === 'user' ? '#1e3a2f' : 'white', color: msg.role === 'user' ? '#f5f0e8' : '#1a1a1a', border: msg.role === 'ai' ? '1px solid #e8ddd0' : 'none'}}>
                {msg.role === 'ai' ? <Markdown>{msg.text}</Markdown> : msg.text}
              </div>
            ))}
            {loading && (
              <div style={{alignSelf: 'flex-start', padding: '10px 13px', borderRadius: '12px', backgroundColor: 'white', border: '1px solid #e8ddd0', fontSize: '13px', color: '#b8a898'}}>
                thinking...
              </div>
            )}
          </div>
          <div style={{display: 'flex', gap: '8px', padding: '12px', borderTop: '1px solid #e8ddd0', backgroundColor: 'white'}}>
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKey}
              placeholder="Ask about your saved places..."
              style={{flex: 1, border: '1px solid #e8ddd0', borderRadius: '8px', padding: '8px 12px', fontSize: '13px', color: '#000000', backgroundColor: 'white', outline: 'none'}}
            />
            <button
              onClick={handleSend}
              disabled={loading}
              style={{backgroundColor: '#c8893a', border: 'none', borderRadius: '8px', width: '36px', color: 'white', cursor: 'pointer', fontSize: '14px'}}
            >
              up
            </button>
          </div>
        </div>
      )}
      <button
        onClick={() => setOpen(!open)}
        style={{position: 'fixed', bottom: '28px', right: '28px', width: '54px', height: '54px', backgroundColor: '#c8893a', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', cursor: 'pointer', boxShadow: '0 6px 24px rgba(200,137,58,0.45)', zIndex: 100, border: 'none', color: 'white', fontSize: '22px'}}
      >
        {open ? 'x' : '+'}
      </button>
    </div>
  )
}

export default ChatPanel
