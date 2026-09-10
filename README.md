# AI Agent & LLM Application Platform

A multi-module AI application platform built as a capstone project to explore the progression from basic LLM applications to **AI agents, Retrieval-Augmented Generation (RAG), Model Context Protocol (MCP), and Deep Agent architectures**.

The project provides a single Streamlit interface where users can experiment with different patterns for building practical AI-powered applications.

## Overview

The project demonstrates five progressively more capable AI application patterns:

1. **Basic AI Chat** — Direct conversational interaction with an OpenAI language model.
2. **Search-Enabled Chat** — An AI agent that can use Tavily to retrieve current information from the web.
3. **RAG** — Upload PDF documents and ask questions grounded in their content using semantic retrieval.
4. **MCP Agent** — Connect an AI agent to external tools and services through the Model Context Protocol.
5. **Deep Agent Skill Architecture** — An agent capable of planning tasks, working with files, and loading specialized Skills when needed.

The goal was not simply to build a chatbot, but to understand how increasingly capable **LLM-powered products and agentic workflows** are designed and integrated.

## Key Features

### 1. Basic AI Chat

A conversational AI interface built with LangChain and OpenAI.

Features include:

* Conversational message history
* Configurable assistant personality
* LangGraph-based message/state handling
* Streamlit chat interface
* Conversation starter prompts
* Reusable response formatting

### 2. Search-Enabled AI Agent

The basic chatbot is extended into an agent capable of using external web search.

**Technologies:**

* LangChain Agents
* OpenAI
* Tavily Search
* Streamlit

The agent can determine when web search is useful and incorporate retrieved information into its response.

### 3. Retrieval-Augmented Generation

The RAG module allows users to upload PDF documents and ask questions about their contents.

The pipeline follows:

```text
PDF Upload
    ↓
PDF Text Extraction
    ↓
Document Chunking
    ↓
OpenAI Embeddings
    ↓
FAISS Vector Store
    ↓
Semantic Retrieval
    ↓
Relevant Context
    ↓
LLM Response
```

This allows responses to be grounded in the user's uploaded documents rather than relying only on the language model's existing knowledge.

**Technologies:**

* LangChain
* OpenAI Embeddings
* FAISS
* PyPDF
* Recursive Character Text Splitter

### 4. MCP Agent

The MCP module demonstrates how an AI agent can interact with external tools using the **Model Context Protocol**.

The application can connect to an MCP server and dynamically discover the tools exposed by that server.

```text
User Request
     ↓
LLM Agent
     ↓
MCP Client
     ↓
MCP Server
     ↓
External Tool / Service
     ↓
Tool Result
     ↓
LLM Response
```

This provides a foundation for connecting AI applications to external services such as productivity tools, databases, communication platforms, and other APIs.

The implementation uses:

* Model Context Protocol
* `langchain-mcp-adapters`
* LangChain Agents
* OpenAI
* Async tool execution

## 5. Deep Agent Skill Architecture

The final module explores a more advanced agent architecture using `deepagents`.

The agent combines:

* Task planning
* Todo management
* File workspace operations
* Specialized Skills
* Document processing
* Spreadsheet analysis
* PDF processing

### Skill-based Architecture

Instead of giving the agent every instruction and capability at once, specialized Skills are progressively loaded based on the task.

Currently included Skills:

```text
skills/
├── data-analysis/
│   └── SKILL.md
├── excel-spreadsheet/
│   └── SKILL.md
├── pdf-extract/
│   └── SKILL.md
└── word-document/
    └── SKILL.md
```

For example, a request involving an Excel dataset can activate the data-analysis and spreadsheet capabilities, while a PDF-related task can use the PDF Skill.

This demonstrates a modular approach to building AI agents that can be extended by adding new Skills without redesigning the entire application.

## Architecture

At a high level, the application follows this structure:

```text
                    ┌─────────────────────┐
                    │    Streamlit UI     │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
        Basic Chat        Search Agent         RAG
              │                │                │
              │             Tavily          FAISS
              │                │                │
              └────────────────┼────────────────┘
                               │
                               ▼
                         MCP Agent
                               │
                         MCP Server
                               │
                               ▼
                       External Tools
                              
                              
                       Deep Agent Layer
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
           Planning       Workspace          Skills
                                               │
                            ┌──────────────────┼───────────────┐
                            ▼                  ▼               ▼
                         Excel               PDF             Word
                                              
```

## Project Structure

```text
project_code_new_ui/
│
├── Home.py
│
├── pages/
│   ├── 1_Basic_Chatbot.py
│   ├── 2_Chatbot_Agent.py
│   ├── 3_RAG.py
│   ├── 4_MCP_Agent.py
│   └── 5_Deep_Agent_Skill_Architecture.py
│
├── skills/
│   ├── data-analysis/
│   │   └── SKILL.md
│   ├── excel-spreadsheet/
│   │   └── SKILL.md
│   ├── pdf-extract/
│   │   └── SKILL.md
│   └── word-document/
│       └── SKILL.md
│
├── utils/
│   ├── formatting.py
│   ├── starters.py
│   ├── styles.py
│   └── __init__.py
│
├── .streamlit/
│   └── config.toml
│
├── requirements.txt
└── runtime.txt
```

## Technology Stack

| Category         | Technologies                        |
| ---------------- | ----------------------------------- |
| Language         | Python                              |
| UI               | Streamlit                           |
| LLMs             | OpenAI                              |
| LLM Framework    | LangChain                           |
| Agent Framework  | LangGraph, DeepAgents               |
| RAG              | LangChain, FAISS, OpenAI Embeddings |
| PDF Processing   | PyPDF                               |
| Web Search       | Tavily                              |
| Tool Integration | Model Context Protocol (MCP)        |
| Documents        | python-docx                         |
| Spreadsheets     | pandas, openpyxl                    |
| PDF Generation   | fpdf2                               |
| Data Analysis    | pandas, matplotlib                  |

## Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd project_code_new_ui
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run Home.py
```

The application will open in your browser.

## API Keys

The application uses API keys for different modules.

### OpenAI

An OpenAI API key is required for the LLM-powered modules.

### Tavily

A Tavily API key is required for the Search-Enabled Chat module.

The application provides fields on the Home page for entering the required keys.

**Important:** Never commit API keys, `.env` files, or other credentials to GitHub.

## How to Use

### Basic AI Chat

1. Enter your OpenAI API key.
2. Open **Basic AI Chat**.
3. Enter a message.
4. Continue the conversation using the chat interface.

### Search-Enabled Chat

1. Configure your OpenAI and Tavily API keys.
2. Open **Search-Enabled Chat**.
3. Ask a question that requires current information.
4. The agent can use Tavily search to retrieve relevant web information.

### RAG

1. Open the RAG module.
2. Upload a PDF.
3. Allow the application to process and index the document.
4. Ask questions about the uploaded content.

### MCP Agent

1. Configure your OpenAI API key.
2. Provide an MCP server URL.
3. Provide the required authentication token if applicable.
4. Connect to the MCP server.
5. Ask the agent to perform tasks using the available MCP tools.

### Deep Agent

1. Open the Deep Agent Skill Architecture module.
2. Upload files or provide a task.
3. The agent plans the task.
4. Relevant Skills are loaded when needed.
5. The agent performs file and data operations.
6. Results are returned through the Streamlit interface.

## Engineering Highlights

This project focuses on practical AI application engineering rather than model training.

Key engineering concepts demonstrated include:

* LLM application architecture
* Agent-based workflows
* Tool calling
* Retrieval-Augmented Generation
* Vector similarity search
* Embedding-based document retrieval
* MCP-based integrations
* Dynamic tool discovery
* Skill-based agent architecture
* Task planning
* File workspace management
* Session-state management
* Modular Streamlit application design
* Reusable UI components
* Safe rendering of model-generated Markdown and links

## Design Approach

The application was intentionally structured as a progression:

```text
LLM
 ↓
LLM + Tools
 ↓
LLM + Retrieval
 ↓
LLM + External Tool Ecosystem
 ↓
Planning Agent + Workspace + Skills
```

This progression makes it possible to compare different approaches to building AI-powered applications and understand where each architecture is useful.

## Future Improvements

Potential extensions include:

* Persistent conversation storage
* Authentication and user accounts
* More MCP integrations
* Additional Skills
* Streaming agent responses
* Improved observability and tracing
* Evaluation datasets for measuring agent/RAG performance
* Persistent vector databases
* Production deployment
* More robust secret management

## Project Context

This project was developed as a **capstone project** to apply concepts from an LLM/AI application engineering curriculum.

It combines multiple concepts into one practical application rather than treating LLMs, RAG, agents, and tool integrations as isolated exercises.

## License

This project is intended primarily as a learning and portfolio project. Add a license here if you plan to distribute or reuse the code publicly.
