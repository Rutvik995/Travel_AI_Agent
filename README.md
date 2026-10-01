# ARVEX – AI Travel Agent 🌍

A premium multi-agent AI travel planner built with **LangGraph**, **CrewAI**, and a beautiful chatbot frontend.

## Features
- 🤖 **Multi-agent architecture** – LangGraph routes between a conversational LLM and a CrewAI planning crew
- 🔍 **Web search** – Serper-powered agents find offbeat spots and real-time booking info
- 💬 **Premium chat UI** – Dark glassmorphism design with animated starfield, markdown rendering, typing indicators
- 🌐 **OpenRouter** – Works with any model available on OpenRouter (GPT-4o-mini by default)

## Setup

### 1. Clone & install dependencies
```bash
git clone https://github.com/Rutvik995/Travel_AI_Agent.git
cd Travel_AI_Agent
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

### 2. Configure API keys
```bash
cp .env.example .env
# Edit .env and fill in your keys
```

Required keys:
| Key | Where to get |
|-----|-------------|
| `OPENROUTER_API_KEY` | [openrouter.ai/keys](https://openrouter.ai/keys) |
| `SERPER_API_KEY` | [serper.dev](https://serper.dev) (free tier) |

### 3. Run
```bash
python app.py
```
Open **http://localhost:5000** in your browser.

## Architecture
```
User → Flask API → LangGraph Router (OpenRouter/gpt-4o-mini)
                        ↓ (if trip planning needed)
                   CrewAI Crew
                   ├── SearchAgent (SerperDevTool)
                   └── BookingAgent (SerperDevTool)
                        ↓
                   Full itinerary returned to user
```

## Tech Stack
- **Backend**: Python, Flask, LangGraph, CrewAI
- **LLM**: OpenRouter (configurable model)
- **Search**: SerperDevTool
- **Frontend**: HTML/CSS/JS with glassmorphism UI
