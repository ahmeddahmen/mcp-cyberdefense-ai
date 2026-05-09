# 🛡️ CyberDefense AI Agent with MCP

> **Projet MPI1 — Faculté des Sciences de Sfax | 2025-2026**  
> Enseignant : Yassine Masmoudi

An autonomous AI agent for cyber defense, built with **Spring Boot**, **Spring AI**, **Python MCP Servers**, and **Angular 18**. The agent uses **LLaMA 3.3 70B** (via Groq) to analyze network activity and SSH logs in real time using the **Model Context Protocol (MCP)**.

---

## 🎯 Project Objectives

- Understand the foundations of agentic AI systems and their application to cybersecurity
- Design and implement MCP servers dedicated to cyber defense
- Connect these servers to an LLM using a Spring AI MCP client
- Automate surveillance, analysis, and incident response tasks

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Angular Frontend                      │
│                   localhost:4200                         │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTP POST /chat/send
┌──────────────────────▼──────────────────────────────────┐
│              Spring Boot MCP Client                      │
│                  localhost:8066                          │
│         Spring AI + LLaMA 3.3 via Groq API              │
└──────────┬───────────────────────────┬───────────────────┘
           │ stdio (MCP)               │ stdio (MCP)
┌──────────▼──────────┐   ┌───────────▼──────────────────┐
│  network_server.py  │   │       log_server.py           │
│  Network Surveillance│   │      Log Analysis             │
│  ─────────────────  │   │  ──────────────────────────   │
│  • scan_ports       │   │  • parse_auth_logs            │
│  • check_connections│   │  • detect_bruteforce          │
│  • ping_host        │   │  • get_failed_logins          │
│  • get_network_stats│   │  • search_log_pattern         │
└─────────────────────┘   └──────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| LLM | LLaMA 3.3 70B via Groq API |
| MCP Client | Spring Boot 3.5 + Spring AI 1.0 |
| MCP Servers | Python 3.11 + FastMCP |
| Frontend | Angular 18 + Bootstrap 5 |
| Build | Maven + Angular CLI |

---

## 📁 Project Structure

```
mcp-cyberdefense-ai/
├── mcp-client/                    # Spring Boot MCP Client
│   └── src/main/java/com/elfn/mcpclient/
│       ├── agents/AIAgent.java    # AI Agent with tool callbacks
│       ├── controllers/           # REST + Web controllers
│       ├── config/WebConfig.java  # Async timeout config
│       └── McpClientApplication.java
├── mcp-servers/                   # Python MCP Servers
│   ├── network_server.py          # Network surveillance tools
│   ├── log_server.py              # Log analysis tools
│   └── requirements.txt
├── chat-ai-frontend/              # Angular 18 Frontend
│   └── src/app/
│       ├── chat/                  # Chat component (dark theme)
│       └── services/chat.service.ts
└── openclaw_config.json           # MCP client configuration
```

---

## 🚀 Getting Started

### Prerequisites

- Java 17+
- Python 3.11+
- Node.js 18+ & npm
- A [Groq API key](https://console.groq.com/keys) (free)

### 1. Install Python dependencies

```bash
cd mcp-servers
pip install -r requirements.txt
```

### 2. Configure the API key

Edit `mcp-client/src/main/resources/application.properties`:

```properties
spring.ai.openai.api-key=YOUR_GROQ_API_KEY
spring.ai.openai.base-url=https://api.groq.com/openai
spring.ai.openai.chat.options.model=llama-3.3-70b-versatile
```

### 3. Start the backend

```bash
cd mcp-client
./mvnw spring-boot:run   # Linux/Mac
.\mvnw.cmd spring-boot:run  # Windows
```

### 4. Start the frontend

```bash
cd chat-ai-frontend
npm install
npm start
```

### 5. Open the app

Navigate to **http://localhost:4200**

---

## 🔧 MCP Tools

### 🌐 Network Surveillance (`network_server.py`)

| Tool | Description |
|------|-------------|
| `scan_ports(host, port_range)` | Scan open ports on a target host (max 50 ports) |
| `check_connections()` | List active connections and detect suspicious ones |
| `ping_host(host)` | Check host availability and response time |
| `get_network_stats()` | Get network I/O statistics |

### 📋 Log Analysis (`log_server.py`)

| Tool | Description |
|------|-------------|
| `parse_auth_logs(n_lines)` | Parse SSH auth logs and detect failures |
| `detect_bruteforce(threshold)` | Identify IPs exceeding failed login threshold |
| `get_failed_logins()` | List targeted usernames and source IPs |
| `search_log_pattern(pattern, logfile)` | Regex search in log files |

---

## 💬 Usage Scenarios

Once the app is running, use the quick action buttons or type naturally:

- 🔍 **"Analyse les logs SSH et détecte les tentatives de force brute"**
- 🌐 **"Scanne les ports de localhost et liste les ports ouverts"**
- 🔗 **"Y a-t-il des connexions réseau suspectes actives ?"**
- 📊 **"Génère un rapport de sécurité résumant l'état actuel du système"**

---

## ⚠️ Notes

- On **Windows**, `/var/log/auth.log` is not available — the log server uses realistic simulated SSH logs
- Groq free tier: **100,000 tokens/day** — wait between requests to avoid rate limits
- Port scanning is limited to **50 ports max** to avoid timeouts

---

## 📄 License

This project was created for educational purposes as part of the MPI1 scripting course at Faculté des Sciences de Sfax.

---

## 👤 Author

**Ahmed Dahmen** — [@ahmeddahmen](https://github.com/ahmeddahmen)
**Khalil Mhiri** — [@khalilmhiri](https://github.com/khalil-mhiri-cyber)
**Molka Hdhili** -[@molkahdhili](/https://github.com/molka-hdhili)
**Omar bannour** -[@Omarbannour](/https://github.com/Omar_bannour)

