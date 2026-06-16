# 🏗️ Architecture Overview: Hierarchical Orchestrator

The Egyptian Omnichannel Community Growth Specialist is built using a **Hierarchical Orchestrator ("Team of Teams")** architecture. This design enables complex, multi-platform marketing operations while maintaining isolation between different platform workflows.

---

## 🔝 The Master Orchestrator
At the top of the hierarchy sits the **Orchestrator Manager Agent**.
- **Role**: CEO / Campaign Director.
- **Responsibility**: Receives high-level business goals (e.g., from ERPNext) and decomposes them into platform-specific tasks. It monitors the progress of all sub-teams and ensures overall campaign cohesion.
- **Process**: `CrewAI Process.hierarchical`.

---

## 👥 Platform Teams (The "Teams of Teams")
The system spawns independent sub-crews for each major engagement channel in Egypt.

### 1. Facebook Team
- **Agents**: Facebook Strategist, Facebook Copywriter.
- **Focus**: Navigating the specific cultural and moderation rules of Egyptian FB Groups and Pages.

### 2. WhatsApp Team
- **Agents**: WhatsApp Manager, WhatsApp Writer.
- **Focus**: High-conversion direct messaging and private community engagement.

### 3. Telegram Team
- **Agents**: Telegram Specialist, Telegram Creator.
- **Focus**: Leveraging Egyptian wholesale channels and link-heavy promotional formats.

### 4. Forums Team
- **Agents**: Forum Researcher, Forum Engagement Specialist.
- **Focus**: Identifying and participating in niche Egyptian web forums (e.g., industrial, real estate, automotive boards).

### 5. Media Team (Shared Service)
- **Agents**: Egyptian Creative Director.
- **Focus**: A specialized "internal agency" that generates high-end visual assets (Imagen/Veo/Runway) on demand for all other platform teams.

---

## 🧠 Omni-Model Intelligence
Every agent in the hierarchy can be assigned a different LLM "brain":
- **Cheap Models (Kimi)**: Used for high-volume research and repetitive writing.
- **High-Reasoning Models (GPT-4/Claude 3)**: Used for the Master Orchestrator and Creative Director roles.
- **Multimodal Models (Gemini)**: Used specifically for asset generation.

---

## 💾 State & Data Flow
1. **Inputs**: ERPNext (Campaigns/Products) or Manual CLI/UI.
2. **Orchestration**: Manager delegates to Platform Teams.
3. **Drafting**: Teams save findings to the **Standalone SQL DB**.
4. **Human-in-the-Loop**: Humans review/approve drafts via the **Streamlit Dashboard**.
5. **Publishing**: (TBD/API) Approved content is distributed via authorized platform APIs.
