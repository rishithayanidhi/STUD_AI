# 🎥 STUAI YouTube Demo Guide

Complete step-by-step guide to record a professional demo video of the Autonomous Operations platform.

## 📋 Pre-Recording Checklist

- [ ] Restart computer (clean state)
- [ ] Close unnecessary applications
- [ ] Maximize VS Code for recording
- [ ] Test recording software (OBS, ScreenFlow, etc.)
- [ ] Have demo outline ready
- [ ] Ensure good lighting and clear audio

---

## ⏱️ Demo Timeline (5-7 minutes)

### **Segment 1: Introduction (0:00-1:00)**

**Narration:**
> "Today I'm showing you STUAI - an AI-powered autonomous operations platform that uses Ollama and FastAPI to classify and handle support tickets automatically. Watch how AI instantly categorizes issues and suggests actions."

**On Screen:**
- Show GitHub repo: https://github.com/rishithayanidhi/STUD_AI
- Open project in VS Code
- Show folder structure (highlight frontend, backend, docker files)

---

### **Segment 2: Start Backend (1:00-2:00)**

**Narration:**
> "First, let's start the backend server with Ollama AI enabled."

**Commands to Run:**

```powershell
# Terminal 1
cd c:\Users\ASUS\Desktop\STUAI
.\.venv\Scripts\Activate.ps1
python main.py
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**On Screen:**
- Show server starting
- Point out "Uvicorn running on port 8000"

---

### **Segment 3: Start Frontend (2:00-3:00)**

**Narration:**
> "Now let's launch the React frontend. It's built with Vite for fast development and has a modern UI."

**Commands to Run:**

```powershell
# Terminal 2
cd c:\Users\ASUS\Desktop\STUAI\frontend
npm install
npm run dev
```

**Expected Output:**
```
➜  Local:   http://localhost:3000/
```

**On Screen:**
- Show browser opening to http://localhost:3000
- Close npm terminal to clean up screen
- Show beautiful dashboard with connected status ✅

---

### **Segment 4: Demo Ticket Submission (3:00-5:00)**

**Narration:**
> "Now the exciting part - let's submit a ticket and watch the AI classify it in real-time."

**Test Case 1: Critical Database Issue**

1. Click in "Issue Description" field
2. Type: `Database connection timeout in production - unable to connect to primary database`
3. Click "Submit Ticket" button
4. **PAUSE** - Let it process (2-3 seconds)
5. Show the AI results:
   - ✅ Category: **Incident**
   - ✅ Priority: **Critical**
   - ✅ Team: **DevOps**
   - ✅ Confidence: **90%+**
   - ✅ Action: Shows suggested fix

**Narration while waiting:**
> "The AI is analyzing this production database issue... It instantly determined this is a critical incident requiring DevOps team attention. See the suggested action? The system is learning from similar past issues."

---

**Test Case 2: Feature Request**

1. Clear form (refresh page or new input)
2. Type: `Need new feature for two-factor authentication in user login`
3. Click "Submit Ticket"
4. Show results:
   - Category: **Change/Request**
   - Priority: **Medium**
   - Team: **Backend/Frontend**

**Narration:**
> "Here's a feature request. Notice how the AI correctly categorizes it as a change request with medium priority. Different classification, different team assignment."

---

**Test Case 3: UI Bug**

1. Type: `Frontend button styling is broken on mobile devices`
2. Submit
3. Show:
   - Category: **Incident**
   - Priority: **High**
   - Team: **Frontend**

**Narration:**
> "And here's a UI bug. The AI correctly identifies it as a frontend issue."

---

### **Segment 5: Dashboard Statistics (5:00-6:00)**

**Narration:**
> "Look at the dashboard on the right. After just three tickets, the system is already showing statistics and patterns."

**On Screen:**
- Scroll to dashboard
- Show:
  - "3 Total Tickets"
  - Incidents: 2
  - Changes: 1
  - By Priority: Critical (1), High (1), Medium (1)
  - "Recent Tickets" list showing all submissions

**Narration:**
> "This is where teams see real-time insights into their operational load."

---

### **Segment 6: Closing/Call-to-Action (6:00-7:00)**

**Narration:**
> "This is STUAI - combining the power of:
> - **Ollama** for local AI inference (privacy-first)
> - **FastAPI** for high-performance backend
> - **React + Vite** for modern frontend
> - **PostgreSQL + Redis** for production data
>
> Perfect for autonomous ops, ticket classification, and intelligent routing. The code is fully open source on GitHub with Docker, Kubernetes deployment files, and complete documentation.
>
> Like and subscribe for more AI ops content. Link in description!"

**On Screen:**
- Show GitHub repo
- Show Swagger docs at http://localhost:8000/docs
- Show Docker files in project
- Final screenshot of dashboard

---

## 📺 Video Recording Tips

### **OBS Settings (Recommended)**
- Resolution: **1920x1080** (1080p)
- Frame Rate: **60 FPS**
- Bitrate: **8000 kbps**
- Output: **H.264**

### **Screen Layout**
```
┌─────────────────────────────────────┐
│      Browser (Frontend)    (60%)    │
│  http://localhost:3000              │
│                                     │
│─────────────────────────────────────│
│ VS Code (Backend logs)    (40%)      │
│                                     │
└─────────────────────────────────────┘
```

### **Verbal Tips**
- Speak clearly and slowly
- Pause for 2-3 seconds after each action for viewers to see results
- Use emoji in narration: 🤖 AI, ⚡ Fast, 🎯 Accurate
- Build excitement: "Watch what happens next..."

---

## 🎬 Sample Video Script

### **Full Narration**

---

**[INTRO]**

"Hey everyone! Today I'm excited to show you STUAI - an autonomous operations platform that uses AI to automatically classify and route support tickets. This is running completely locally using Ollama, so everything stays on your machine.

Here's the problem it solves: ops teams get hundreds of tickets daily, and manual classification wastes hours. STUAI solves this with AI that learns from your past tickets."

---

**[START BACKEND]**

"Let's start the backend. It's a FastAPI server running Ollama, which gives us powerful local AI."

*[Show python main.py starting]*

"Server is live on port 8000."

---

**[START FRONTEND]**

"Now the frontend - built with React and Vite for a snappy experience."

*[Show npm run dev starting]*

"And it's already open in the browser. See that green status indicator? Backend is connected and ready."

---

**[FIRST TICKET]**

"Now for the magic. Let me submit a critical production issue."

*[Type and submit]*

"Watch as the AI instantly classifies this... It's a Critical database incident for the DevOps team. That would take a human 5-10 minutes of analysis. The AI did it in 2 seconds.

Notice the confidence score - 90%. The system knows when it's certain and when it might need human review."

---

**[SECOND TICKET]**

"Let's try a feature request."

*[Submit new ticket]*

"Completely different classification - a Change request for the backend team. The AI understands context."

---

**[THIRD TICKET]**

"One more - a UI bug."

*[Submit]*

"Sent to Frontend team, marked High priority. Three tickets, three different classifications, 100% accurate."

---

**[DASHBOARD]**

"Look at the dashboard - it's tracking patterns, showing statistics in real-time. This is exactly what ops leads need to see: ticket volume, priority distribution, team load."

---

**[CLOSING]**

"This is production-ready. It includes Docker Compose for local development, Kubernetes manifests for cloud deployment, full monitoring setup, and everything documented.

The best part? It's all open source. Link in the description.

If you found this valuable, hit Like and Subscribe for more autonomous ops content. Thanks for watching!"

---

## 🎯 Alternative Demo Ideas

### **Variation 1: Speed Demo (3 minutes)**
- Just show fast ticket submission
- Emphasize speed: "2 second classification vs 10 minute manual review"
- Good for shorts/reels

### **Variation 2: Deep Dive (15 minutes)**
- Show source code (agent.py getting ticket classification)
- Explain Ollama integration
- Show database storage
- Explain training/learning mechanism

### **Variation 3: Deployment Demo**
- Show Docker compose setup
- Show Kubernetes deployment
- Show API documentation
- Talk about production readiness

---

## ✅ Post-Recording Checklist

- [ ] Render video in highest quality
- [ ] Add intro/outro (branding)
- [ ] Add thumbnail with "AI", "ops", "automation" keywords
- [ ] Write compelling title: "AI that auto-routes 100 tickets/hour | Autonomous Ops Demo"
- [ ] Add timestamps in description
- [ ] Link to GitHub repo
- [ ] Add relevant tags: #AI #DevOps #Automation #OpenSource
- [ ] Share on Twitter/LinkedIn with demo link

---

## 📊 YouTube SEO Keywords

```
Autonomous Operations
AI Ticket Classification  
DevOps Automation
Ollama Local LLM
FastAPI Backend
React Frontend
Machine Learning Operations
Incident Management
Open Source AI
```

---

## 🚀 You're Ready!

Everything is set up and connected. Your demo will show:
✅ Modern React UI
✅ Real-time AI classification
✅ Professional backend
✅ Full working integration
✅ Production-ready code

Good luck with your video! 🎬

---

**Save this guide in your repo:**
```bash
cp DEMO_GUIDE.md docs/DEMO_GUIDE.md
```

Happy filming! 🎥
