# Egyptian Omnichannel Community Growth Specialist (CrewAI)

A production-ready autonomous marketing system designed to discover, engage, and grow brands within Egyptian online communities. It leverages a **Hierarchical Orchestrator** ("Team of Teams") to coordinate efforts across specialized platform teams.

## 🚀 Key Features

- **Hierarchical Orchestration**: A central Manager Agent delegates tasks to isolated platform teams (Facebook, WhatsApp, etc.).
- **Omni-Model Architecture**: Dynamically switch between **Kimi**, **Gemini**, **OpenAI**, and **Anthropic** for each agent via a user-friendly GUI.
- **Multimodal Media Creation**: Autonomous image and video generation using **Gemini Imagen/Veo**, **Runway**, and **DALL-E 3**.
- **Egyptian Market Localization**: Authentic **Amiya Masriya** copywriting and governorate-level cultural intelligence.
- **Unlimited Search**: Integrated with **SearXNG** for free, unlimited internet-wide discovery.

## 🏗️ Architecture: The "Team of Teams"

The system operates as a hierarchical AI organization:
1.  **Master Orchestrator**: Receives the high-level campaign goal and manages the platform incidents.
2.  **Facebook Team**: Specialized in Egyptian FB groups and viral trends.
3.  **WhatsApp Team**: Specialized in private communities and direct engagement.
4.  **Telegram Team**: Specialized in wholesale/retail channels.
5.  **Forums Team**: Specialized in niche Egyptian web forums.
6.  **Media Team**: A shared service providing visuals for all platforms.

## 🖥️ GUI Options

The system now supports two graphical interfaces for different needs:

### 1. Custom Streamlit Dashboard (Data Management)
Best for approving posts, reviewing discovered communities, and managing the "Human-in-the-Loop" workflow.
- **Run Locally:** `streamlit run dashboard.py`
- **Access via Docker:** `http://localhost:8501`

### 2. CrewUI (Workflow Visualization)
Best for monitoring agent thought processes and triggering crews via a standard web interface.
- **Access via Docker:** `http://localhost:3000`

## 🛠️ Installation

### 1. Prerequisites
- Python 3.10+
- [Docker & Docker Compose](https://www.docker.com/)
- ERPNext Instance with API Access
- OpenAI API Key

### 2. Fast Setup (Docker Compose)
The easiest way to run the entire stack (SearXNG, API, Dashboard, and CrewUI) is via Docker Compose:
```bash
docker-compose up -d
```
This will launch:
- **SearXNG** (Search Engine) at `http://localhost:8080`
- **FastAPI Backend** at `http://localhost:8000`
- **Streamlit Dashboard** at `http://localhost:8501`
- **CrewUI** at `http://localhost:3000`

### 3. Manual Setup
If you prefer running without Docker:
```bash
# Install dependencies
pip install -r requirements.txt

# Start Search Engine (Required for Discovery)
docker run -d -p 8080:8080 searxng/searxng

# Start Dashboard
streamlit run dashboard.py
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env` and fill in your credentials:
```bash
cp .env.example .env
```
Key variables to set:
- `OPENAI_API_KEY`: Your LLM provider key.
- `SEARXNG_URL`: Defaults to `http://localhost:8080`.
- `DATABASE_URL`: Defaults to local SQLite.
- `ERPNEXT_URL`, `ERPNEXT_API_KEY`, `ERPNEXT_API_SECRET`.
- `META_ACCESS_TOKEN`, `TELEGRAM_BOT_TOKEN`, `WHATSAPP_BEARER_TOKEN`.

## 📖 Usage

The system is controlled via a CLI in `main.py`.

### A. Discover New Communities
Find Egyptian communities related to a specific topic and save them to the database.
```bash
python main.py discover --topic "Wholesale Furniture" --platform "Facebook Groups"
```

### B. Generate Localized Content
Draft a post for a specific community based on current ERPNext campaigns and Alexandria's cultural tone.
```bash
python main.py generate --governorate "Alexandria" --community_url "https://facebook.com/groups/alex-furniture-market"
```

## 📂 Project Structure
- `agents/`: CrewAI agent definitions with Egyptian personas.
- `tasks/`: Discovery and Content task configurations.
- `crews/`: Orchestrators for micro-crews.
- `integrations/`: API wrappers for ERPNext, Meta, WhatsApp, and Telegram.
- `tools/`: Custom tools for DB and SearXNG search.
- `community_database/`: SQLAlchemy models and migrations.
- `tests/`: Unit tests for core database logic.

## 🛡️ Security & Approvals
- **Manual Mode**: By default, posts are saved as `Needs Approval`. A human must change the status in the `posts` table to `Approved` before the Publishing agent can pick it up.
- **Credentials**: Never hardcode secrets. Always use the `.env` file.

## 🇪🇬 Egyptian Market Localization
The agents are prompted to understand:
- **Governorate Differences**: (Cairo vs. Alexandria vs. Upper Egypt).
- **Dialect**: Uses "Amiya Masriya" for high engagement.
- **Timing**: Respects local events (Ramadan, Eids, Friday prayers).
