# bio-agent-llm
Agentic Bioinformatics AI using LangGraph + Groq + NCBI tools
# bio-agent-llm
Agentic Bioinformatics AI using LangGraph + Groq + NCBI tools
# Bio-Agent — Agentic Bioinformatics with LLMs

> An AI-powered bioinformatics agent that autonomously queries the NCBI database using a ReAct (Reason + Act) loop — built with LangGraph, Groq (Llama 3.3 70B), and Biopython.

---

# What is this?

Bio-Agent is a **portfolio project** demonstrating the intersection of classical bioinformatics workflows and modern **Generative AI / Agentic AI** development.

Instead of writing rigid scripts that call NCBI directly, this project uses an **LLM as a reasoning engine** — the model decides *which tool to call*, *with what input*, and *how to interpret the result* — mimicking how a senior bioinformatician would approach a research query.

# Architecture

User Query
    │
    ▼
┌─────────────────────────────────────┐
│         LLM Brain (Llama 3.3 70B)   │  ← Groq API (free tier)
│         ReAct Loop via LangGraph    │
└────────────┬────────────────────────┘
             │ decides which tool to call
     ┌───────┴────────┐
     ▼                ▼
┌──────────┐    ┌──────────────┐
│  Tool 1  │    │   Tool 2     │
│  NCBI    │    │  NCBI Gene   │
│  Protein │    │  Database    │
│  Fetch   │    │  Summary     │
└──────────┘    └──────────────┘
     │                │
     └───────┬────────┘
             ▼
      Observation fed
      back to LLM
             │
             ▼
      Final Scientific
         Answer
```

*Three core components:*
*The Brain* — `ChatGroq` with `llama-3.3-70b-versatile`, `temperature=0` for deterministic scientific output
- The Tools (Hands) — Python functions decorated with `@tool` that connect to NCBI via Biopython's `Entrez` module
-The Orchestrator — `create_react_agent` from LangGraph handles the Thought → Action → Observation loop automatically

---

#Tech Stack

| Component | Technology |
|---|---|
| LLM | Llama 3.3 70B via Groq API |
| Agent Framework | LangGraph (`create_react_agent`) |
| LLM Interface | LangChain Core |
| Bioinformatics | Biopython (`Entrez`, `SeqIO`) |
| Database | NCBI Protein + Gene databases |
| Runtime | Google Colab / Python 3.10+ |

---

#Quickstart

#1. Get a free Groq API key
Sign up at [console.groq.com](https://console.groq.com) → API Keys → Create Key. No credit card required.

#2. Open in Google Colab
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/)

Upload `bio_agent_groq.py` and run all cells.

# 3. Install dependencies
```bash
pip install langchain langchain-groq langchain-community biopython langgraph
```

### 4. Run
```python
# The agent will autonomously:
# 1. Reason about what tools it needs
# 2. Call NCBI Protein DB → fetch NP_000508 (Hemoglobin β)
# 3. Call NCBI Gene DB → summarize BRCA1 in Homo sapiens
# 4. Return a structured scientific report
```
## 🔬 Example Queries & Output

**Query 1 — Protein Fetch**
```
Input:  "What is the name and length of the protein with NCBI ID 'NP_000508'?"

Output: The protein NP_000508 is Hemoglobin subunit beta [Homo sapiens].
        Sequence length: 147 amino acids.
```

**Query 2 — Gene Summary**
```
Input:  "Look up the gene summary for BRCA1 in Homo sapiens and explain
         its biological significance."

Output: BRCA1 (Gene ID: 672) is a tumour suppressor located on chromosome
        17q21. It encodes a DNA repair protein critical for homologous
        recombination. Pathogenic variants are strongly associated with
        hereditary breast and ovarian cancer syndrome (HBOC).
```

---

## 📁 Repository Structure

```
bio-agent-llm/
│
├── bio_agent_groq.py      # Main agent — paste into Colab and run
├── requirements.txt       # Python dependencies
└── README.md              # You are here
```

---
##  Roadmap / Level-Up Ideas

- [ ] **RAG Research Summarizer** — PubMed abstract retrieval via FAISS vector store
- [ ] **AlphaFold Integration** — call AlphaFold API as a third agent tool for structure prediction
- [ ] **AMR Transcriptomics Tool** — plug in a trained LSTM model as `@tool def predict_amr_resistance(...)`
- [ ] **Streamlit / Gradio UI** — wrap the agent in a web interface
- [ ] **Multi-agent pipeline** — one agent fetches, another interprets, another writes a report

---

##  About

Built by **Ayan** — BSc Microbiology · MSc Medical Biotechnology & Bioinformatics

Previously a **Bioinformatics Specialist** at Bioquicks, where I worked on genome data analysis pipelines. This project represents my transition from classical bioinformatics scripting into **Generative AI and Agentic AI development** — applying LLM orchestration to real biological research workflows.

---

## 📄 License

MIT License — free to use, fork, and build upon.

---

*If you found this useful, drop a ⭐ — it helps with visibility!*
