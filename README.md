# 🤖 mcp-demo-spring-python

## 🧠 Application Agentique avec Spring AI, MCP Protocol, NodeJS, Python et LLMs (OpenAI, Claude, LLaMA)

---

### ❗ Problème à résoudre :

> **"Créer une architecture flexible et extensible d'agents IA capables d'interagir avec des outils externes via le protocole MCP, en multi-langage (Java, NodeJS, Python), pour permettre la résolution intelligente de requêtes complexes."**

---

### 🔍 Description

Cette application montre comment :

- Mettre en place des **serveurs MCP** (Spring Boot, NodeJS, Python)
- Intégrer un **client Spring AI** compatible avec Claude, LLaMA3.2 et OpenAI
- Créer un **agent intelligent** (`ToolCallbackProvider`, mémoire contextuelle, etc.)
- Appeler dynamiquement des **tools STDIO**
- **Tester via Swagger UI**, Postman ou Front Angular/Thymeleaf

---

### ✅ Fonctionnalités principales

- 📁 **Lecture / écriture fichiers** via `@modelcontextprotocol/server-filesystem`
- 🔁 **Communication STDIO** entre le client Java et les tools (NodeJS, Python)
- 🧠 **Utilisation de modèles LLM** en interaction avec des outils réels
- ✔️ **Test complet** avec Postman et Swagger
- 🎨 **Intégration UI** (Angular ou Thymeleaf)

---

### 🛠️ Stack technique

| Composant | Description |
|----------|-------------|
| ![Spring](https://cdn.jsdelivr.net/gh/devicons/devicon/icons/spring/spring-original.svg) **Spring Boot / Spring AI** | Agent IA et orchestration |
| 🧠 **LLMs** | OpenAI (GPT-4), Claude, LLaMA |
| 🟢 **NodeJS** | Tools MCP (file-system) exécutés via NPX |
| 🐍 **Python** | Tools MCP exécutés via `uv` |
| 📦 **MCP Protocol** | Standardisé pour outils multilangages |
| 📬 **Postman / Swagger** | Test et documentation des endpoints |
| 🌐 **Angular / Thymeleaf** | Interface utilisateur (UI) |

---

### 📂 Structure du projet

<img width="878" height="299" alt="image" src="https://github.com/user-attachments/assets/89f59fec-9575-45af-9518-47a6486d4128" />



---

### 📊 Diagramme de séquences

```mermaid
sequenceDiagram
    participant UI as User (Angular/Swagger)
    participant RestCtrl as REST Controller
    participant Agent as AI Agent
    participant LLM as LLM (OpenAI/Claude)
    participant MCPClient as MCP Client
    participant ToolNode as NodeJS Tool
    participant ToolPython as Python Tool

    UI->>RestCtrl: Sends a query
    RestCtrl->>Agent: Forwards the query
    Agent->>LLM: Sends prompt + context + tools
    LLM->>MCPClient: Chooses a tool (Node/Python)
    MCPClient->>ToolNode: STDIO call (e.g., npx)
    MCPClient->>ToolPython: STDIO call (e.g., uv)
    ToolNode-->>MCPClient: JSON response
    ToolPython-->>MCPClient: JSON response
    MCPClient-->>Agent: Raw result
    Agent-->>LLM: Observation
    LLM-->>Agent: Final answer
    Agent-->>RestCtrl: Result
    RestCtrl-->>UI: User response
```

### 📊 Diagramme de flux du projet

```mermaid
flowchart TD
    subgraph UI
        A[Utilisateur - Swagger / Angular]
    end

    subgraph API
        B[API REST Spring - RestController]
    end

    subgraph AI
        C[Agent IA - Spring AI]
        D[LLM - OpenAI / Claude / LLaMA]
    end

    subgraph MCP
        E[MCP Client - Java]
    end

    subgraph MCP_SERVERS
        F[Serveur MCP Node.js Tools: read_file, write_file…]
        G[Serveur MCP Python Tools:  get_employee_info]
        H[Serveur MCP Java Tools: stock]
    end

    %% Requête utilisateur jusqu’à la sélection du tool
    A --> B
    B --> C
    C --> D
    D --> E
    C --> E

    %% Appel du bon serveur selon le tool
    E --> F
    E --> G
    E --> H

    %% Retour du résultat
    F --> E
    G --> E
    H --> E
    E --> C
    C --> B
    B --> A
```
## 🔍 Résumé du workflow
👤 Utilisateur : Fait une requête via Swagger ou Angular.

🌐 API REST Spring : Reçoit et transmet la requête à l'agent IA.

🧠 Agent IA (Spring AI) : Analyse la demande et interroge le LLM si nécessaire.

🧠 LLM : Génère l'appel à un outil parmi ceux des serveurs MCP.

🔁 MCP Client (Java) : Transmet la commande au bon serveur MCP selon le choix du LLM.

## 🧰 Serveurs MCP disponibles
### ☕ Serveur MCP Java :
Company, Stock

### 🐍 Serveur MCP Python :
get_employee_info

### 🟢 Serveur MCP Node.js (outils filesystem) :
read_file, write_file, ...

### 🔄 Retour de réponse
📦 Le serveur MCP exécute l’outil et renvoie un résultat JSON.

📬 Le MCP Client reçoit la réponse et la transmet à l'agent IA.

💡 Le LLM complète la réponse avec le contexte.

📤 L'API Spring retourne la réponse finale à l'utilisateur.


# 🚀 Démarrage rapide

1. Clone du projet  
2. Configure `.env` avec ta clé OpenAI  
3. Lance le backend : `Spring Boot`  
4. Lance un outil via `npx` ou `uv`  
5. Teste via Swagger (`http://localhost:8066/swagger-ui.html`)

## 🧪 Exemple de requête

## Réponse
```json
POST /chat
{
  "query": "Crée un fichier nommé test.md avec le contenu Bonjour"
}

{
  "result": "Fichier test.md créé avec succès dans le répertoire autorisé"
}
```

# 🌐 Test de l'interface (Angular)

<img width="1006" height="554" alt="image" src="https://github.com/user-attachments/assets/7e4ea767-a72c-4a95-bca6-9e818a90df21" />

<img width="1004" height="841" alt="image" src="https://github.com/user-attachments/assets/665d327e-6a9a-4ba1-a6f0-1ec4b32ac0ee" />

