# 🌿 PredFit: Your Health, Predicted.

> **An Agentic AI Ecosystem for Early Lifestyle Disease Prediction via Multi-Agent Consensus.**

[![Hackathon](https://img.shields.io/badge/Hackathon-2026-green.svg)]()
[![AI-Agents](https://img.shields.io/badge/AI--Agents-Multi--Agent--Orchestration-blue)]()
[![Tech-Stack](https://img.shields.io/badge/Stack-FastAPI%20|%20Next.js%20|%20LangChain-lightgrey)]()

---

## 📌 Overview
**PredFit** is a proactive health intelligence platform designed to catch chronic diseases before they manifest clinically. Unlike traditional trackers, PredFit uses a **"Medical Board" of AI Specialists** to analyze your lifestyle, biometrics, and habits. By simulating a professional medical consultation through agentic debate, the system provides highly accurate, explainable risk scores for Diabetes, Hypertension, CVD, and more.

## The PredFit Edge

### 🎙️ The "Health Call" (Passive Logging)
PredFit eliminates "logging fatigue." Using **Twilio AI Voice Agents**, the system calls you at your preferred time to chat about your day.
* **Natural Conversations:** Just tell the AI what you ate or how you slept.
* **Automated Structuring:** The system extracts nutritional data, stress levels, and activity metrics from speech and updates your dashboard instantly.

### 🏛️ The AI Consilium (Specialist Panel)
The core innovation of PredFit is the **Forum Discussion**. Five specialized agents analyze your data and "debate" your health status:
* **CardioBot:** Monitors heart health and hypertension.
* **GlucoBot:** Tracks blood sugar trends and diabetic risk.
* **FitBot:** Analyzes activity and sedentary patterns.
* **NutriBot:** Evaluates dietary impact on biometrics.
* **SleepBot:** Specializes in circadian rhythm and recovery.
* **The Consensus Agent:** Acts as the "Chief Medical Officer" to finalize your **0–100 Risk Score** based on the agents' debate.

### 📊 Predictive Intelligence Dashboard
* **Real-Time Risk Gauges:** Visualized tracking of disease trajectories.
* **Habit Management:** Personalized interventions (e.g., the "4D Technique" for smoking) that adapt based on your logged progress.
* **Explainable AI:** Every risk score comes with a "Reasoning Trace"—know exactly why your score moved.

---

## 🛠️ Technical Architecture

### **The Multi-Agent Workflow**
1.  **Ingestion:** Data flows in via Web UI or the **Twilio Voice Call** interface.
2.  **Specialist Review:** Each specialist agent processes the data through their specific medical lens.
3.  **Cross-Agent Debate:** Agents interact in a shared memory space (The Forum) to identify overlapping risks.
4.  **Consensus:** The final risk score is updated via WebSockets to the frontend.

### **The Stack**
* **Frontend:** Next.js 14, Tailwind CSS, Framer Motion (Forest Green/Dark Mode).
* **Backend:** FastAPI / Node.js.
* **Orchestration:** LangChain / CrewAI / AutoGen.
* **Infrastructure:** PostgreSQL + TimescaleDB (Time-series data).
* **Telephony:** Twilio API for outbound autonomous calling.

---

## 📈 Roadmap
- [ ] **Wearable Sync:** Integration with Apple Health, Google Fit, and Fitbit APIs.
- [ ] **Nudge Agent:** Real-time push notifications and "Emergency Calls" if risk thresholds are crossed.
- [ ] **ML Core:** Implementing XGBoost and Neural Networks to replace initial rule-based scoring.
- [ ] **Genomics:** Optional upload for genetic predisposition mapping.

---

## 💰 Monetization (Stripe Integrated)
* **Free:** Basic dashboard + 3 risk categories.
* **Pro ($9.99/mo):** Full Specialist Panel + **AI Health Calls**.
* **Geek ($19.99/mo):** API Access, Family Tracking, and Genetic Data Integration.

---

## ⚙️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone [https://github.com/RohitKattimani/predfit.git](https://github.com/RohitKattimani/predfit.git)
   cd predfit
2. **Environment Configuration**
   ```bash
   OPENAI_API_KEY=your_openai_key
   TWILIO_ACCOUNT_SID=your_twilio_sid
   TWILIO_AUTH_TOKEN=your_twilio_token
   STRIPE_SECRET_KEY=your_stripe_key
   DATABASE_URL=your_database_url
3. **Install & Run Frontend**
  ```bash
   cd frontend
   npm install
   npm run dev
