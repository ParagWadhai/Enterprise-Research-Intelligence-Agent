# Enterprise Research Intelligence Agent

An AI-powered Enterprise Research Agent that conducts structured research,
collects information from public sources, builds a reusable knowledge base,
analyses evidence, compares findings, detects contradictions, and generates
traceable research conclusions.

The system is designed as a complete enterprise AI application rather than
a simple chatbot or LLM wrapper.

---

## 1. Overview

The Enterprise Research Intelligence Agent converts an open-ended business
research question into a structured, evidence-based research report.

For example:

> How is generative AI changing financial services?

The application automatically:

1. Creates a structured research plan
2. Generates focused research questions
3. Collects information from public sources
4. Stores research sources and documents
5. Splits documents into searchable chunks
6. Builds a vector-based knowledge layer
7. Retrieves relevant evidence
8. Extracts important findings
9. Classifies findings
10. Assigns confidence scores
11. Links findings to supporting evidence
12. Compares findings
13. Detects supporting and contradictory evidence
14. Generates a final research conclusion
15. Stores the resulting research artifacts

---

## 2. Key Objective

The objective is not to build:

> "ChatGPT with web search"

Instead, the application maintains a reusable research knowledge base
containing:

- Research sessions
- Research questions
- Sources
- Documents
- Document chunks
- Findings
- Evidence references
- Comparisons
- Contradictions
- Conclusions

This allows research results to remain available after the original
research request has completed.

---

## 3. Application Architecture

The application follows a layered enterprise AI architecture.

```text
┌─────────────────────────────────────────────┐
│               USER INTERFACE                │
│                                             │
│             Streamlit Dashboard             │
└──────────────────────┬──────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────┐
│             APPLICATION/API LAYER           │
│                                             │
│                  FastAPI                    │
│                                             │
│  Research Sessions                          │
│  Research Planning                          │
│  Source Collection                          │
│  Knowledge Building                         │
│  Analysis                                   │
│  Comparison                                 │
│  Synthesis                                  │
└──────────────────────┬──────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────┐
│             AI INTELLIGENCE LAYER           │
│                                             │
│              Groq LLM API                   │
│                                             │
│  Research Planner                           │
│  Evidence Analyzer                          │
│  Finding Classification                     │
│  Confidence Estimation                      │
│  Evidence Comparator                        │
│  Contradiction Detection                    │
│  Research Synthesizer                       │
└──────────────────────┬──────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────┐
│            DATA & KNOWLEDGE LAYER           │
│                                             │
│       SQLite + SQLAlchemy + FAISS           │
│                                             │
│  Research Sessions                          │
│  Research Questions                         │
│  Sources                                    │
│  Documents                                  │
│  Chunks                                     │
│  Findings                                   │
│  Comparisons                                │
│  Conclusions                                │
└──────────────────────┬──────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────┐
│        EXTERNAL RESEARCH / DATA             │
│                                             │
│            Public Web Sources               │
└─────────────────────────────────────────────┘
```

---

## 4. End-to-End Research Pipeline

```text
Research Question
        │
        ▼
Research Planning
        │
        ▼
Focused Research Questions
        │
        ▼
Source Collection
        │
        ▼
Document Processing
        │
        ▼
Chunking
        │
        ▼
Knowledge Base
        │
        ▼
Vector Retrieval
        │
        ▼
Evidence Analysis
        │
        ▼
Finding Classification
        │
        ▼
Evidence Comparison
        │
        ▼
Contradiction Detection
        │
        ▼
Research Synthesis
        │
        ▼
Final Research Report
```

Each stage has a specific responsibility and intermediate results are
persisted in the database.

---

## 5. Main Components

### 5.1 Streamlit Frontend

The Streamlit application provides the user interface for:

- Entering research questions
- Starting research
- Viewing research progress
- Viewing generated research questions
- Viewing findings
- Viewing final conclusions
- Viewing recommendations
- Viewing risks
- Viewing research confidence

---

### 5.2 FastAPI Backend

FastAPI provides the application and API layer.

The backend separates business logic from the frontend and exposes APIs
for each major research operation.

---

### 5.3 Research Planner

The research planner converts a broad research question into a small set
of focused research questions.

The system limits the generated research questions to approximately
3-5 high-value questions to control research cost, execution time, and
unnecessary source collection.

Example:

```text
Main Question:

How is generative AI changing financial services?

Research Questions:

1. What generative AI technologies are being deployed?
2. What measurable business benefits have been reported?
3. What is the current adoption level?
4. What risks and implementation challenges exist?
5. What emerging developments could shape the industry?
```

---

## 6. Source Collection

For every research question, the source collection service searches public
information and collects relevant sources.

Each source can contain:

```text
Source
├── Title
├── URL
├── Publisher
├── Quality Score
└── Research Session
```

The collected sources are persisted in the database.

This allows the application to maintain a reusable research history instead
of immediately discarding retrieved information.

---

## 7. Knowledge Base

Collected source content is processed into documents and chunks.

```text
Source
   │
   ▼
Document
   │
   ▼
Text Chunks
   │
   ▼
Embeddings
   │
   ▼
FAISS Vector Store
```

The vector retrieval layer allows the application to find relevant evidence
for a research query.

The knowledge base is separated from the LLM layer so that stored research
information does not depend on a single model provider.

---

## 8. Evidence Retrieval

The retrieval API searches the knowledge base for relevant information.

```http
GET /api/v1/research/{session_id}/search
```

The response includes:

- Chunk ID
- Document ID
- Source ID
- Retrieved content
- Similarity score
- Source metadata

Example:

```json
{
  "chunk_id": 3141,
  "document_id": 118,
  "source_id": 144,
  "content": "...",
  "score": 0.76,
  "source": {
    "title": "Example Research Source",
    "url": "https://example.com"
  }
}
```

---

## 9. Evidence Analysis

The evidence analyzer uses retrieved evidence to extract important
research findings.

Each finding contains:

```text
Finding
├── Finding ID
├── Finding text
├── Category
├── Classification
├── Confidence
└── Evidence references
```

Example:

```json
{
  "finding": "AI-powered computer vision improves quality inspection.",
  "category": "Technology",
  "classification": "Benefit",
  "confidence": 0.90,
  "evidence": [
    {
      "chunk_id": 2545,
      "source_id": 122
    }
  ]
}
```

The analyzer is instructed to use only the supplied evidence and not
invent unsupported facts.

---

## 10. Finding Classification

Findings can be classified into categories such as:

```text
Technology
Operations
Benefits
Risks
Adoption
Cost
Customer Experience
Workforce
Strategy
```

Possible classifications include:

```text
Adoption
Emerging
Benefit
Risk
Trend
Challenge
Evidence
```

Each finding receives a confidence score between:

```text
0.0 - 1.0
```

---

## 11. Evidence Comparison

The comparison layer evaluates relationships between findings.

Supported relationship types include:

```text
support
contradiction
partial_agreement
```

The system prioritizes meaningful relationships rather than comparing
every possible pair of findings.

Example:

```text
Finding A
    │
    ├── support ───────────────► Finding B
    │
    ├── contradiction ────────► Finding C
    │
    └── partial_agreement ────► Finding D
```

Each comparison contains:

```text
Finding A
Finding B
Comparison Type
Description
Severity
```

Severity can be:

```text
low
medium
high
```

---

## 12. Contradiction Detection

The application does not treat different wording as a contradiction.

A contradiction is identified only when findings make materially
incompatible claims about the same subject, context, and conditions.

This helps prevent false contradiction detection caused by differences
in wording or perspective.

---

## 13. Research Synthesis

The synthesis layer generates the final research report from stored
findings and evidence comparisons.

The final report contains:

```text
Executive Summary
Conclusion
Reasoning
Recommendations
Risks
Confidence
```

The conclusion is generated from the research artifacts rather than
directly from the original user question.

---

## 14. Traceability

Traceability is a core feature of the application.

The system maintains the relationship:

```text
Research Question
       │
       ▼
Research Finding
       │
       ▼
Evidence Reference
       │
       ▼
Chunk
       │
       ▼
Document
       │
       ▼
Source
       │
       ▼
Source URL
```

This allows a reviewer to understand where a finding originated.

Example:

```text
Finding #15
      │
      ├── Chunk #2545
      │       └── Source #122
      │
      └── Chunk #3140
              └── Source #144
```

This provides evidence traceability for generated conclusions.

---

## 15. API Endpoints

The application provides APIs for the complete research workflow.

### Create Research

```http
POST /api/v1/research
```

Creates a new research session.

---

### Collect Sources

```http
POST /api/v1/research/{session_id}/collect-sources
```

Collects sources for the generated research questions.

---

### Get Research Session

```http
GET /api/v1/research/{session_id}
```

Returns the research session and its associated research questions.

---

### Build Knowledge Base

```http
POST /api/v1/research/{session_id}/build-knowledge
```

Processes stored sources and builds the searchable knowledge base.

---

### Search Knowledge

```http
GET /api/v1/research/{session_id}/search
```

Retrieves relevant evidence from the knowledge base.

---

### Analyze Evidence

```http
POST /api/v1/research/{session_id}/analyze
```

Extracts and classifies research findings from retrieved evidence.

---

### Compare Evidence

```http
POST /api/v1/research/{session_id}/compare
```

Compares findings and identifies meaningful relationships.

---

### Synthesize Research

```http
POST /api/v1/research/{session_id}/synthesize
```

Generates the final research report.

---

### Run Complete Research

```http
POST /api/v1/research/{session_id}/run
```

Runs the complete research pipeline.

```text
Planning
   ↓
Source Collection
   ↓
Knowledge Base
   ↓
Evidence Analysis
   ↓
Evidence Comparison
   ↓
Final Synthesis
```

---

## 16. Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Frontend | Streamlit |
| Backend | FastAPI |
| API Server | Uvicorn |
| LLM | Groq API |
| LLM Model | openai/gpt-oss-120b |
| Database | SQLite |
| ORM | SQLAlchemy |
| Vector Store | FAISS |
| Validation | Pydantic |
| Testing | Pytest |

---

## 17. Project Structure

```text
enterprise-research-agent/
│
├── app/
│   │
│   ├── ai/
│   │   └── llm.py
│   │
│   ├── agents/
│   │   └── state.py
│   │
│   ├── analysis/
│   │   ├── finding_analyzer.py
│   │   ├── evidence_comparator.py
│   │   └── synthesizer.py
│   │
│   ├── api/
│   │   └── research.py
│   │
│   ├── database/
│   │   ├── database.py
│   │   ├── models.py
│   │   └── repository.py
│   │
│   ├── research/
│   │   └── planner.py
│   │
│   ├── schemas/
│   │   ├── finding.py
│   │   └── research.py
│   │
│   ├── services/
│   │   ├── research_service.py
│   │   ├── research_execution.py
│   │   ├── knowledge_service.py
│   │   ├── analysis_service.py
│   │   ├── comparison_service.py
│   │   ├── synthesis_service.py
│   │   └── research_status.py
│   │
│   └── main.py
│
├── frontend/
│   └── app.py
│
├── tests/
│   └── ...
│
├── data/
│   └── research.db
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
├── pytest.ini
└── README.md
```

---

## 18. Installation

### Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd enterprise-research-agent
```

---

### Create Virtual Environment

#### Windows

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 19. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 20. Environment Configuration

Create a `.env` file in the project root.

```env
APP_NAME=Enterprise Research Intelligence Agent
APP_ENV=development

DATABASE_URL=sqlite:///./data/research.db

GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=openai/gpt-oss-120b
```

Never commit the real `.env` file or API keys to GitHub.

Use `.env.example` as the configuration template.

---

## 21. Run Backend

Start the FastAPI backend:

```bash
uvicorn app.main:app --reload
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 22. Run Frontend

Open another terminal and activate the virtual environment.

Then run:

```bash
streamlit run frontend/app.py
```

The Streamlit application will open in the browser.

---

## 23. Example Research Questions

The application can dynamically process different research questions.

### Retail

```text
How is AI transforming retail operations?
```

### Manufacturing

```text
What AI technologies are changing manufacturing?
```

### Financial Services

```text
How is generative AI changing financial services?
```

### Healthcare

```text
How is AI transforming healthcare operations?
```

### Supply Chain

```text
How is AI changing supply chain management?
```

The same application pipeline processes each question without requiring
hard-coded answers.

---

## 24. Surprise Research Question

The application supports the surprise-record evaluation.

A new research question can be entered without modifying the application
code.

For example:

```text
How is AI transforming healthcare operations?
```

The system dynamically creates:

```text
Research Questions
        ↓
New Sources
        ↓
New Knowledge
        ↓
New Findings
        ↓
New Comparisons
        ↓
New Conclusion
```

This demonstrates that the application is not dependent on pre-generated
answers.

---

## 25. Database Model

The application stores research artifacts using a relational database.

The main entities include:

```text
ResearchSession
      │
      ├── ResearchQuestion
      │
      ├── Source
      │      │
      │      └── Document
      │             │
      │             └── Chunk
      │
      ├── Finding
      │      │
      │      └── Evidence Reference
      │
      ├── Contradiction / Comparison
      │
      └── Conclusion
```

The database provides persistence across research operations.

---

## 26. Scalability

The current implementation is a working prototype designed with modular
services.

For larger workloads, the synchronous pipeline can be converted into an
asynchronous job-based architecture.

For example:

```text
Client
   │
   ▼
FastAPI
   │
   ▼
Research Job
   │
   ▼
Message Queue
   │
   ├──────────────┐
   ▼              ▼
Worker 1       Worker 2
   │              │
   ├── Sources    ├── Sources
   ├── Analysis   ├── Analysis
   └── Synthesis  └── Synthesis
          │
          ▼
    Persistent Storage
```

For a significantly larger workload:

- Research jobs can be queued
- Multiple workers can process jobs concurrently
- Source collection can be parallelized
- Document processing can be batched
- Embeddings can be generated incrementally
- Vector indexes can be partitioned or replaced with a scalable vector
  database
- SQLite can be migrated to PostgreSQL
- API requests can return a job/session ID immediately
- Intermediate pipeline results can be persisted independently

The application is therefore designed so that scaling does not require
redesigning the complete business logic.

---

## 27. LLM Provider Abstraction

The LLM integration is isolated in:

```text
app/ai/llm.py
```

The research services do not directly depend on the Groq SDK.

This makes it possible to replace the model provider without rewriting
the complete research pipeline.

Possible future implementations include:

```text
Groq
  ↓
Open-source local model
  ↓
Ollama
  ↓
vLLM
  ↓
Another compatible model provider
```

The stored research knowledge remains independent from the LLM provider.

---

## 28. Free Technology Requirement

The application uses technologies that are available without purchasing
commercial software licenses.

Core components include:

- Python
- FastAPI
- Streamlit
- SQLAlchemy
- SQLite
- FAISS
- Pydantic
- Pytest

The current LLM inference uses the Groq API.

The application requires a valid Groq API key for the configured LLM.

If the external LLM service becomes unavailable or changes its pricing,
the LLM integration can be replaced with another compatible model provider
or a locally hosted open-source model.

The research database, retrieval architecture, services, APIs, and frontend
do not depend on Groq-specific business logic.

---

## 29. Security

API keys and environment-specific configuration must never be committed
to source control.

The repository uses:

```text
.env
```

for local secrets and:

```text
.env.example
```

for configuration documentation.

The `.gitignore` file should exclude:

```text
.env
venv/
__pycache__/
*.pyc
data/*.db
```

---

## 30. Testing

Run the test suite using:

```bash
pytest
```

Tests should cover important application components such as:

- Research planning
- Source collection
- Knowledge building
- Retrieval
- Finding extraction
- Evidence comparison
- Synthesis
- API endpoints

---

## 31. Enterprise Design Principles

The application follows several enterprise AI design principles.

### Separation of Concerns

Each stage has a dedicated service.

```text
Planning
Source Collection
Knowledge Building
Analysis
Comparison
Synthesis
```

---

### Persistent State

Research artifacts are stored instead of keeping all information only
inside an LLM conversation.

---

### Evidence-Based Reasoning

AI analysis operates on retrieved evidence rather than relying only on
general model knowledge.

---

### Traceability

Findings maintain references to the chunks and sources supporting them.

---

### Explainability

The final report includes reasoning, confidence, recommendations, risks,
and evidence relationships.

---

### Provider Independence

The LLM provider is isolated from application business logic.

---

### Dynamic Research

The application can accept new research questions without modifying
hard-coded application logic.

---

## 32. What the Application Does NOT Do

This project is intentionally different from a simple chatbot.

It does not primarily:

- Return hard-coded answers
- Display static HTML results
- Depend on manually executed prompts
- Store all intelligence inside one giant prompt
- Use a PowerPoint as the application
- Use manually populated spreadsheets as the knowledge base
- Simply forward a user question to an LLM

Instead, the backend performs a multi-stage research workflow with
persistent storage, retrieval, evidence analysis, comparison, and synthesis.

---

## 33. Example Final Output

A completed research session produces a report containing:

```text
Final Research Report

Executive Summary
        │
        ▼
Conclusion
        │
        ▼
Reasoning
        │
        ▼
Recommendations
        │
        ▼
Risks
        │
        ▼
Research Confidence
        │
        ▼
Evidence Traceability
```

---

## 34. Evaluation Scenario

The application is designed for the following evaluation flow:

```text
Evaluator
   │
   ▼
Enter New Research Question
   │
   ▼
Frontend
   │
   ▼
FastAPI
   │
   ▼
Research Planning
   │
   ▼
External Research
   │
   ▼
Knowledge Base
   │
   ▼
AI Evidence Analysis
   │
   ▼
Evidence Comparison
   │
   ▼
Synthesis
   │
   ▼
Persistent Research Results
   │
   ▼
Final Report
```

The evaluator can provide a previously unseen research question and the
application processes it dynamically.

---

## 35. Future Improvements

Potential production-scale improvements include:

- Asynchronous background workers
- Distributed job queues
- PostgreSQL migration
- Production vector database
- Redis caching
- Parallel source collection
- Batch embedding generation
- Source quality ranking
- Improved duplicate detection
- Advanced citation management
- Authentication and authorization
- API rate limiting
- Observability and monitoring
- Model fallback routing
- Local LLM support
- Multi-language research
- Scheduled research updates
- Research report export

These improvements can be introduced without changing the fundamental
research workflow.

---

## 36. Author

**Parag Wadhai**

Enterprise AI Research Intelligence Agent

Built using Python, FastAPI, Streamlit, FAISS, SQLAlchemy, SQLite,
Pydantic, and Groq LLM API.

---

## 37. License

This project is intended as an assessment/demo application.

Individual third-party libraries and services remain subject to their
respective licenses and terms of use.