# AI-Powered Multi-Model Recommendation Engine

An automated, event-driven recommendation system that integrates multiple Large Language Models (OpenAI, Gemini, and Claude) to provide real-time content suggestions. This project leverages FastAPI for the backend, Notion as a CMS, and Zapier for workflow automation.

## 🚀 Features

- **Multi-Model Support:** Side-by-side recommendations from OpenAI (GPT), Google Gemini, and Anthropic Claude.
- **Event-Driven Architecture:** Triggered automatically when new data is added to Notion via Zapier webhooks.
- **FastAPI Backend:** Asynchronous and high-performance routing layer.
- **Notion Integration:** Uses Notion as both a database and a management interface.
- **Automated Workflows:** Zero manual sync required thanks to Zapier middleware.
- **Fallback Mechanism:** Local tag-matching algorithm to handle API downtime or rate limits.
- **Dockerized:** Easy deployment using Docker and Docker Compose.

## 🏗️ Architecture

1.  **Data Layer (Notion):** Stores item catalogs and user preferences.
2.  **Automation (Zapier):** Listens for changes in Notion and sends webhooks to the backend.
3.  **Application (FastAPI):** Processes the webhook, queries LLMs in parallel, and returns recommendations.
4.  **AI Layer:** OpenAI, Gemini, and Claude APIs.

## 📂 Project Structure

- `main.py`: FastAPI application entry point and webhook handlers.
- `ai_service.py`: Integration logic for different LLM providers.
- `notion_service.py`: Notion API interactions.
- `models.py`: Pydantic models for data validation.
- `setup_notion.py`: Utility to initialize Notion database structure.
- `docker-compose.yml`: Container orchestration.

## 📦 Getting Started

### 1. Prerequisites
- Python 3.10+
- API Keys for OpenAI, Gemini, Claude, and Notion.
- A Zapier account.

### 2. Environment Setup
Copy `.env.example` to `.env` and fill in your API keys:
```bash
cp .env.example .env
```

### 3. Running with Docker
```bash
docker-compose up --build
```

### 4. Running Locally
```bash
pip install -r requirements.txt
python main.py
```

## 📜 Documentation
For a detailed technical overview, see the [IEEE Report (English)](IEEE_Report_EN.md) or the [IEEE Report (Turkish)](IEEE_Report_TR.md).

## 📄 License
This project is licensed under the MIT License.
