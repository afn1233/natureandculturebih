# 🌿 Nature & Culture BiH

A full-stack tourist location manager for **Bosnia and Herzegovina** — discover, manage, and explore locations with AI-powered chat, real-time weather, and automated data collection.

🔗 **Live App:** [natureandculturebih.vercel.app](https://natureandculturebih.vercel.app)  
🔗 **Backend API:** [natureandculturebih-production.up.railway.app](https://natureandculturebih-production.up.railway.app)

---

## ✨ Features

- 🔐 **Email-based authentication** — register and login with just your email
- 📍 **Location management** — add, edit, and delete tourist locations across BiH
- 🤖 **AI Chat Assistant** — ask questions about your saved locations, powered by Claude (Anthropic) with RAG
- 🌤️ **Live weather data** — real-time weather for Mostar, Bihać, and Sarajevo, updated every hour
- 📊 **MCP Statistics** — platform stats exposed via Model Context Protocol
- ⚡ **N8N Automation** — scheduled workflow that fetches weather data automatically every hour

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | ReactJS + Vite + Tailwind CSS |
| Backend | Python 3.11 + FastAPI |
| Database | PostgreSQL |
| AI / LLM | Anthropic Claude (claude-sonnet) |
| Embeddings | Hash-based (SHA-256, 1536-dim) |
| Automation | N8N (hourly weather collection) |
| Weather API | OpenWeatherMap |
| Hosting (FE) | Vercel |
| Hosting (BE) | Railway |

---

## 🚀 Getting Started (Local Development)

### Prerequisites
- Docker & Docker Compose
- Node.js 18+

### Run locally

```bash
# Clone the repository
git clone https://github.com/afn1233/natureandculturebih.git
cd natureandculturebih

# Start backend + database
docker compose up --build

# In a separate terminal, start the frontend
cd frontend
npm install
npm run dev
```

The app will be available at **http://localhost:5173**

---

## 📁 Project Structure

```
natureandculturebih/
├── backend/
│   ├── main.py              # FastAPI app entry point
│   ├── models.py            # SQLAlchemy database models
│   ├── embeddings.py        # Hash-based embedding generation
│   └── routers/
│       ├── auth.py          # User authentication
│       ├── links.py         # Location CRUD + embeddings
│       ├── chat.py          # RAG pipeline + Claude AI chat
│       ├── webhook.py       # N8N weather webhook receiver
│       └── mcp.py           # MCP statistics server
├── frontend/
│   └── src/
│       ├── pages/           # Login, Dashboard, Chat
│       └── components/      # LocationCard, Navbar, etc.
├── docker-compose.yml
└── README.md
```

---

## 🤖 How RAG Works

1. When a location is saved, a **1536-dimensional hash-based embedding** is generated and stored in PostgreSQL
2. On each chat message, the query is embedded and compared against all stored locations using **cosine similarity**
3. The **top 3 most relevant locations** are retrieved and injected as context into the Claude prompt
4. Claude generates a response grounded in the user's actual saved locations

---

## 🌤️ Weather Automation (N8N)

An N8N workflow runs **every hour** and:
1. Fetches current weather from OpenWeatherMap for **Mostar**, **Bihać**, and **Sarajevo**
2. POSTs the data (temperature + description) to the `/webhook/weather` endpoint
3. The backend stores it and serves it alongside each location in the API response

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/login` | Login or register with email |
| GET | `/links` | Get all user locations |
| POST | `/links` | Create a new location |
| PUT | `/links/{id}` | Update a location |
| DELETE | `/links/{id}` | Delete a location |
| POST | `/chat` | Send message to AI assistant |
| POST | `/webhook/weather` | Receive weather data from N8N |
| GET | `/stats` | MCP platform statistics |
| GET | `/health` | Health check |

---

## 📄 Environment Variables

```env
DATABASE_URL=postgresql://...
ANTHROPIC_API_KEY=sk-ant-...
```

---

## 📚 Course

Developed as a final project for the **Software Engineering** course at  
**International Burch University** — Faculty of Information Technologies  
Instructor: Assist. Prof. Dr. Becir Isakovic

---

## 👤 Author

**Afan** — [github.com/afn1233](https://github.com/afn1233)
