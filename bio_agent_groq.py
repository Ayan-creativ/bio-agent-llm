#  Bio-Agent — Groq + Llama 3.3 70B (Free Tier, No Credit Card)

# ── STEP 1: Install dependencies ────────────────────────────
!pip install --quiet --upgrade \
    langchain \
    langchain-groq \
    langchain-community \
    biopython \
    langgraph

# ── STEP 2: Imports ─────────────────────────────────────────
import os
from Bio import Entrez, SeqIO
from langchain_core.tools import tool
from langchain_groq import ChatGroq                         # ← Groq swap
from langgraph.prebuilt import create_react_agent

# ── STEP 3: API Key setup ────────────────────────────────────
# Get your FREE key at: https://console.groq.com → API Keys → Create
print(" Paste your Groq API Key:")
os.environ["GROQ_API_KEY"] = input()

Entrez.email = ""   # ← put your email here (NCBI requirement)

# ── STEP 4: Define Bio-Tools (Hands) ────────────────────────

@tool
def get_protein_info(protein_id: str) -> str:
    """Search NCBI for a Protein ID and return the name and sequence length."""
    try:
        handle = Entrez.efetch(db="protein", id=protein_id, rettype="gb", retmode="text")
        record = SeqIO.read(handle, "genbank")
        handle.close()
        return (
            f"Protein Name: {record.description} | "
            f"Sequence Length: {len(record.seq)} amino acids"
        )
    except Exception as e:
        return f"NCBI Error: {str(e)}"


@tool
def get_gene_summary(gene_name: str) -> str:
    """Search NCBI Gene database for a gene name and return a short summary."""
    try:
        search_handle = Entrez.esearch(db="gene", term=f"{gene_name}[Gene Name] AND Homo sapiens[Organism]")
        search_results = Entrez.read(search_handle)
        search_handle.close()

        if not search_results["IdList"]:
            return f"No gene found for '{gene_name}' in Homo sapiens."

        gene_id = search_results["IdList"][0]
        fetch_handle = Entrez.efetch(db="gene", id=gene_id, rettype="gene_table", retmode="text")
        summary = fetch_handle.read(2000)   # first 2000 chars is enough
        fetch_handle.close()
        return f"Gene ID: {gene_id}\n{summary[:800]}"
    except Exception as e:
        return f"NCBI Gene Error: {str(e)}"

# ── STEP 5: The Brain (Groq — Llama 3.3 70B, FREE) ──────────
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

# ── STEP 6: Assemble the Agent ───────────────────────────────
tools = [get_protein_info, get_gene_summary]

agent_instruction = (
    "You are an expert Bioinformatics AI Agent. "
    "Use your tools to answer the user's question accurately. "
    "Always reason step-by-step before calling a tool."
)

bio_agent = create_react_agent(llm, tools=tools, prompt=agent_instruction)

# ── STEP 7: Run Queries ──────────────────────────────────────
print("\n Bio-Agent is scanning the NCBI database...\n")

# ── Query 1: Protein fetch (Hemoglobin β — from our original context) ───
query_protein = "What is the name and length of the protein with NCBI ID 'NP_000508'?"

# ── Query 2: Gene summary (BRCA1 — the tumour suppressor gene) ──────────
query_gene = "Look up the gene summary for BRCA1 in Homo sapiens and explain its biological significance."

for label, query in [("PROTEIN FETCH — NP_000508", query_protein),
                     ("GENE SUMMARY — BRCA1",      query_gene)]:
    print(f"\n{'='*50}")
    print(f"🔬 {label}")
    print(f"{'='*50}")
    try:
        result = bio_agent.invoke({"messages": [("user", query)]})
        print(result["messages"][-1].content)
    except Exception as e:
        print(f"❌ Error: {e}")

# ============================================================
#  💡My next LEVEL-UP IDEAS:
#  1. Adding a PubMed RAG summarizer tool !
#  2. Connect to AlphaFold API for structure prediction
#  3. Pass my own LSTM model as a tool: @tool def predict_with_lstm(...)
# ============================================================
