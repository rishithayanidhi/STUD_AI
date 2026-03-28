# STUAI Frontend

Modern React + Vite frontend for the Autonomous Operations Demo.

## ✨ Features

- 🎯 Submit tickets for AI classification
- 📊 Real-time dashboard with statistics
- 🔗 Full integration with FastAPI backend
- ⚡ Lightning-fast Vite development server
- 📱 Fully responsive design

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ (with npm)
- Backend running at `http://localhost:8000`

### Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will automatically open at `http://localhost:3000`

## 📋 How to Use

1. **Start the Backend First**
   ```bash
   # In another terminal, from project root
   python main.py
   ```

2. **Start Frontend**
   ```bash
   npm run dev
   ```

3. **Submit Tickets**
   - Enter an issue description (e.g., "Database connection timeout")
   - Optional: Add additional context
   - Click "Submit Ticket"
   - Watch the AI classify it in real-time!

4. **View Results**
   - AI Classification (Category, Priority, Team, Confidence)
   - Suggested Actions
   - Execution Log
   - Similar Past Tickets

## 🎥 Demo Flow

Perfect for YouTube demo:

```
1. Show ticket form
2. Submit: "Database connection timeout in production"
3. AI instantly classifies:
   - Category: Incident
   - Priority: Critical
   - Team: DevOps
   - Action: [Suggested fix]
4. View dashboard with stats
5. Submit multiple tickets
6. Show pattern recognition with similar tickets
```

## 🛠️ Build for Production

```bash
npm run build
# Output will be in dist/ directory
```

## 🔌 API Integration

Frontend connects to backend at:
- **Base URL**: `http://localhost:8000`
- **Submit Ticket**: `POST /ticket`
- **Get Tickets**: `GET /memory/tickets`
- **Health Check**: `GET /health`

All API calls configured in `src/api/ticketAPI.js`

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Header.jsx          # Header with backend status
│   │   ├── TicketForm.jsx      # Ticket submission form
│   │   ├── TicketResult.jsx    # AI classification display
│   │   └── Dashboard.jsx       # Statistics dashboard
│   ├── api/
│   │   └── ticketAPI.js        # Backend API service
│   ├── App.jsx                 # Main app component
│   ├── main.jsx                # React entry point
│   └── index.css               # Styling
├── index.html                  # HTML entry point
├── package.json                # Dependencies
├── vite.config.js              # Vite configuration
└── README.md                   # This file
```

## 🎨 Customization

### Change Backend URL
Edit `src/api/ticketAPI.js`:
```js
const API_BASE = 'http://localhost:8000'; // Change here
```

### Modify Styling
Edit `src/index.css` - uses CSS variables for easy theming:
```css
:root {
  --primary: #2563eb;    /* Main color */
  --success: #10b981;    /* Success color */
  --danger: #ef4444;     /* Error color */
}
```

## 🐛 Troubleshooting

**Backend Connection Error?**
- Ensure `python main.py` is running
- Check backend is on `http://localhost:8000`
- Browser console (F12) shows full error

**Port 3000 Already in Use?**
Edit `vite.config.js`:
```js
server: {
  port: 3001,  // Change to different port
}
```

**CORS Error?**
Backend already has CORS enabled, but verify in `main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Should be set
)
```

## 📝 License

Same as parent project.

## 🚀 Ready for Demo!

You now have a complete AI ops platform:
- **Backend**: FastAPI + Ollama AI
- **Frontend**: React + Vite
- **Demo**: Instant ticket classification with beautiful UI

Perfect for YouTube! 🎬
