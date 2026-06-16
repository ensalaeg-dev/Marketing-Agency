# 🛠️ Setup Guide: Egyptian Omnichannel Growth Specialist

This guide will walk you through setting up the complete environment, from the AI agents to the graphical interfaces and the self-hosted search engine.

---

## 📋 Prerequisites

Before starting, ensure you have the following installed:
- **Python 3.10 or 3.11**
- **Docker & Docker Compose**
- **Git**
- **An OpenAI API Key** (or compatible LLM provider)

---

## 🏗️ Step 1: Clone & Environment Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd "Marketing automation"
   ```

2. **Create a Virtual Environment (Optional but recommended):**
   ```bash
   python -m venv venv
   # Windows:
   .\venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🔑 Step 2: Configuration (.env)

Create a `.env` file in the root directory by copying the example:
```bash
cp .env.example .env
```

Open `.env` and fill in the following mandatory sections:

### AI & Search
- `OPENAI_API_KEY`: Your OpenAI key.
- `SEARXNG_URL`: Leave as `http://localhost:8080` (This is your Dockerized search engine).

### ERPNext (Source of Truth)
- `ERPNEXT_URL`: e.g., `https://erp.yourcompany.com`
- `ERPNEXT_API_KEY`: Generated from User > API Access in ERPNext.
- `ERPNEXT_API_SECRET`: Generated alongside the API Key.

### Messaging & Social (Destinations)
- `TELEGRAM_BOT_TOKEN`: From @BotFather.
- `META_ACCESS_TOKEN`: From Meta for Developers portal.
- `WHATSAPP_BEARER_TOKEN`: From WhatsApp Business API.

---

## 🐳 Step 3: Launching with Docker (Recommended)

The system is fully containerized. Running the following command will launch the Search Engine, the AI API, the Dashboard, and CrewUI all at once:

```bash
docker-compose up -d
```

### 📍 Access Points:
- **Streamlit Dashboard**: [http://localhost:8501](http://localhost:8501) (Approvals & DB Management)
- **CrewUI**: [http://localhost:3000](http://localhost:3000) (Visualizing Agent logic)
- **SearXNG**: [http://localhost:8080](http://localhost:8080) (Self-hosted Search Engine)
- **FastAPI**: [http://localhost:8000](http://localhost:8000) (The Agent Backend)

---

## 🤖 Step 4: AI Model Configuration (Optional but Recommended)

One of the most powerful features of this system is the **Omni-Model Architecture**. You can assign different AI models (Kimi, Gemini, OpenAI) to each agent.

1. **Launch the Dashboard**: `http://localhost:8501`
2. **Navigate to "Model Settings"**: In the sidebar.
3. **Assign Models**: 
   - Use **Kimi** (`kimi/moonshot-v1-8k`) for Discovery and Content to save costs.
   - Use **Gemini** (`gemini/gemini-1.5-pro`) for the **Media Director** to enable Imagen/Veo generation.
4. **Save**: Click "Save Configuration". This updates `agent_models.json` automatically.

---

## 🧪 Step 5: Verification Run

1. **Verify Search:** Open `http://localhost:8080` in your browser. If SearXNG appears, the Discovery Agent can now search the web for free.
2. **Verify Database:** Run the Dashboard (`http://localhost:8501`). You should see empty tables for Communities and Posts.
3. **Trigger Discovery:**
   Go to the "Run Crews" tab in the Dashboard and search for:
   - **Topic**: `Real Estate Alexandria`
   - **Platform**: `Facebook Groups`
   
   Wait for the agent to finish. Then check the "Communities" tab to see the results.

---

## 🇪🇬 Pro-Tips for the Egyptian Market

1. **Language**: The agents are pre-configured to output **Amiya (Egyptian Arabic)**. Ensure your LLM (GPT-4 recommended) supports Arabic well.
2. **SearXNG**: If discovery results are too broad, the agents automatically add Egyptian keywords like `مصر`, `القاهرة`, or `جروب`.
3. **Approvals**: Always use the **Streamlit Dashboard** to review content before it goes live. AI can sometimes use "slang" that might be too informal for certain brands.

---

## ❓ Troubleshooting

- **SearXNG Connection Error**: Ensure the Docker container `searxng` is running.
- **ERPNext 403/401**: Check your API Key/Secret permissions in ERPNext (ensure the user has 'Read' access to Campaigns and Items).
- **CrewUI not connecting**: Ensure the `api` service is healthy in Docker (`docker ps`).
