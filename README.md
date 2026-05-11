# 🚀 Advanced Multi-Agent AI Blog Writer

A production-grade **Multi-Agent AI Content Generation Platform** built using **LangGraph**, **LangChain**, **FastAPI**, **Streamlit**, **Docker**, **AWS EC2**, and **GitHub Actions**.

This system autonomously performs:
- Intelligent routing
- Internet research
- Evidence synthesis
- Multi-agent orchestration
- Parallel section generation
- Markdown blog compilation
- Cloud deployment
- CI/CD automation
- LangSmith observability

---

# ✨ Features

## 🧠 Multi-Agent Architecture
Built using **LangGraph** with specialized agents:
- Router Agent
- Research Agent
- Orchestrator Agent
- Worker Agents
- Reducer Agent

---

## 🌐 Autonomous Research Routing
The system intelligently decides whether a topic requires:
- Closed-book generation
- Hybrid research generation
- Open-book internet research

using an LLM-based routing pipeline.

---

## 🔍 Tavily-Powered Research
For internet-aware topics:
- Performs live web search
- Extracts structured evidence
- Deduplicates sources
- Filters recent information
- Grounds claims with citations

---

## ⚡ Parallel Agent Execution
Multiple worker agents generate sections simultaneously using LangGraph fan-out/fan-in execution patterns.

---

## 📄 Markdown Blog Generation
Generates:
- Structured markdown blogs
- Technical sections
- Citations
- Code snippets
- Developer-focused content

Blogs are automatically saved locally as `.md` files.

---

## 🖥 Interactive Frontend
Built using **Streamlit**:
- User-provided API keys
- Real-time generation
- Saved blog viewer
- Markdown rendering
- Link extraction
- Error handling UI

---

## ⚙️ FastAPI Backend
Production-ready REST API handling:
- Blog generation
- Blog retrieval
- File serving
- Error management
- API orchestration

---

## 🐳 Dockerized Deployment
Entire application containerized using:
- Docker
- Docker Compose

Supports:
- Local development
- Cloud deployment
- Portable environments

---

## ☁️ AWS EC2 Deployment
Application deployed on:
- Ubuntu EC2 instance
- Public cloud infrastructure
- Dockerized runtime environment

---

## 🔄 CI/CD Automation
Implemented automated deployment pipeline using:
- GitHub Actions
- SSH-based deployment
- Auto pull + rebuild on push

Every push to GitHub automatically deploys the latest version to AWS EC2.

---

## 📊 LangSmith Observability
Integrated:
- LangSmith tracing
- Workflow visualization
- LLM call monitoring
- Agent execution debugging

---

# 🏗 System Architecture

```text
User
  ↓
Streamlit Frontend
  ↓
FastAPI Backend
  ↓
LangGraph Workflow
  ├── Router Agent
  ├── Research Agent
  ├── Orchestrator Agent
  ├── Parallel Worker Agents
  └── Reducer Agent
  ↓
Markdown Blog Output
```

---

# 🧩 Tech Stack

| Category | Technologies |
|---|---|
| AI Orchestration | LangGraph, LangChain |
| LLM Provider | OpenRouter |
| Research Engine | Tavily |
| Backend | FastAPI |
| Frontend | Streamlit |
| Containerization | Docker, Docker Compose |
| Cloud | AWS EC2 |
| CI/CD | GitHub Actions |
| Observability | LangSmith |
| Language | Python |

---

# 📂 Project Structure

```text
.
├── api/
│   └── main.py
│
├── app/
│   ├── nodes/
│   │   ├── router.py
│   │   ├── research.py
│   │   ├── orchestrator.py
│   │   ├── worker.py
│   │   └── reducer.py
│   │
│   ├── graph.py
│   ├── llm.py
│   ├── runner.py
│   └── schemas.py
│
├── ui/
│   └── app.py
│
├── data/
│   └── blogs/
│
├── Dockerfile.backend
├── Dockerfile.frontend
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# 🚀 Local Setup

## 1️⃣ Clone Repository

```bash
git clone https://github.com/dineshramv13/Advanced_Multi_Agent_Blog_Writer.git

cd Advanced_Multi_Agent_Blog_Writer
```

---

## 2️⃣ Create Environment File

Create `.env`

```env
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_key
LANGCHAIN_PROJECT=blog-writer-app
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Run Backend

```bash
uvicorn api.main:app --reload
```

Backend:
```text
http://localhost:8000
```

---

## 5️⃣ Run Frontend

```bash
streamlit run ui/app.py
```

Frontend:
```text
http://localhost:8501
```

---

# 🐳 Docker Setup

## Build & Run

```bash
docker compose up --build
```

Frontend:
```text
http://localhost:8501
```

Backend:
```text
http://localhost:8000
```

---

# ☁️ AWS Deployment

Deployed using:
- AWS EC2 Ubuntu Instance
- Docker Compose
- GitHub Actions CI/CD

---

# 🔄 CI/CD Workflow

On every GitHub push:
1. GitHub Actions triggers
2. SSH into EC2
3. Pull latest code
4. Rebuild Docker containers
5. Restart services automatically

---

# 📸 Example Capabilities

✅ AI weekly news roundups  
✅ Technical tutorials  
✅ System design blogs  
✅ Research-grounded articles  
✅ Multi-section developer blogs  
✅ Parallel content generation  

---

# 🔐 API Key Handling

User provides:
- OpenRouter API Key
- Tavily API Key

System retains:
- LangSmith observability keys securely on server

---

# 🧠 Key Engineering Concepts Demonstrated

- Multi-Agent Systems
- AI Workflow Orchestration
- LLM Routing
- Structured Outputs
- Parallel Execution
- CI/CD Automation
- Cloud Deployment
- Containerization
- Production API Design
- Observability & Tracing

---

# 📈 Future Improvements

- Authentication system
- Database integration
- Redis caching
- Streaming responses
- WebSockets
- Kubernetes deployment
- Multi-user sessions
- RAG support
- Vector database integration

---

# 👨‍💻 Author

Dinesh Ram

GitHub:
https://github.com/dineshramv13

---

# ⭐ If you found this project interesting, consider starring the repository!
