# 🌍 ARVEX — AI TRAVEL AGENT

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=24&pause=1000&color=38BDF8&center=true&vCenter=true&width=600&lines=Multi-Agent+Travel+Planning+System;Powered+by+LangGraph+%26+CrewAI;Automated+Custom+Itineraries" alt="Typing SVG" />
</p>

---

## 📌 Overview

**[Travel_AI_Agent](https://github.com/Rutvik995/Travel_AI_Agent)** is a premium multi-agent AI travel planning assistant built with **LangGraph**, **CrewAI**, and a Flask chatbot interface. It generates automated, customized day-by-day itineraries based on specific user constraints.

---

## 🛠 Tech Stack

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-000000?style=for-the-badge&logo=langchain&logoColor=white)
![OpenRouter](https://img.shields.io/badge/OpenRouter-API-8E7CC3?style=for-the-badge&logo=openai&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)

---

## ✨ Features

- 🤖 **Multi-Agent Architecture:** Powered by **LangGraph** to dynamically route between a conversational LLM and a **CrewAI** planning crew.
- 🔍 **Real-Time Web Search:** Integrates Serper-powered agents to discover offbeat spots, local attractions, and live booking details.
- 💬 **Premium Glassmorphism UI:** Dark-themed chat interface featuring an animated starfield, markdown rendering, and typing indicators.
- 🌐 **OpenRouter Integration:** Flexible LLM routing supporting models like `gpt-4o-mini`.

---

## 🏗 Architecture & Flow

```text
 User ➔ Flask API ➔ LangGraph Router (OpenRouter / gpt-4o-mini)
                      │ (if trip planning needed)
                      ▼
                 CrewAI Crew
                 ├── SearchAgent (SerperDevTool)
                 └── BookingAgent (SerperDevTool)
                      │
                      ▼
                 Full custom itinerary returned to user
