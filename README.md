# Formal Language-Based Resume Screening

ResumeLens is an automated résumé-screening system developed for **Computación y Estructuras Discretas III (2026-2) — Integrative Task 1** at Universidad Icesi.

The application leverages formal language theory across four distinct pipeline stages to extract, normalize, classify, and validate candidate qualifications against four professional profiles:
1. **Full Stack Developer** (Reference Profile)
2. **Machine Learning Engineer** (Reference Profile)
3. **Data Engineer** (Team Profile — AI/Data)
4. **DevOps Engineer** (Team Profile — Software Engineering)

---

## Team & Environment

- **Team Members:** Nicholas Solis and Santiago Cabal
- **Course Code:** 09772 / 09834 — Computación y Estructuras Discretas III (2026-2)
- **IDE:** Visual Studio Code
- **Python Version:** Python 3.14+

---

## Quick Start & Setup

### 1. Clone & Set Up Virtual Environment

From PowerShell in the project directory:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

*(If PowerShell script execution is restricted, invoke the virtual environment Python interpreter directly: `.\.venv\Scripts\python.exe`)*

### 2. Run the Interactive UI (Recommended)

ResumeLens includes a full command-line user interface (UI) to run sample batches or test arbitrary résumé text in real time:

```powershell
python main.py
```

### 3. Run the Automated Headless Pipeline

To run the complete batch pipeline over the 4 sample résumés non-interactively:

```powershell
python main.py --run-all
```

Or execute the four stage scripts in sequential order:
```powershell
python src\resumelens\Extraction.py
python src\resumelens\Normalization.py
python src\resumelens\ProfileClassification.py
python src\resumelens\ProfileSpecification.py
```

### 4. Run the Automated Test Suite

```powershell
python main.py --test
# Or directly with unittest:
python -m unittest discover -s tests -p "test_*.py"
```

---

## Architectural Pipeline Overview

```text
[Raw CV Text] 
      │
      ▼ (Stage 1: Regex Extraction - Python re)
[Categorized Info] (output/extracted_resumes.json)
      │
      ▼ (Stage 2: Transducer Normalization - pyformlang FST)
[Canonical Symbols] (output/normalized_resumes.json)
      │
      ▼ (Stage 3: Pattern Recognition - pyformlang DFA & ε-NFA)
[Profile Classification Verdicts]
      │
      ▼ (Stage 4: DSL Validation - textX Context-Free Grammar)
[Structured Candidate Profiles & Markdown Reports] (output/candidate_profiles/)
```

---

## Complete Project Documentation (`docs/`)

All theoretical formalizations and design documents are located in `docs/`:

- **[Literature Review](docs/literature_review.md):** Academic state-of-the-art review on Applicant Tracking Systems, comparing formal language models vs. statistical LLM approaches.
- **[Stage 1 — Regex Extraction](docs/stage1_regex.md):** Formal definitions of regular languages $L(R)$ and pattern specifications for 9 extraction categories.
- **[Stage 2 — FST Normalization](docs/stage2_normalization.md):** 7-tuple definition $M = (Q, \Sigma, \Gamma, \delta, \omega, q_0, F)$, transducer transition diagrams, and canonical sorting rules.
- **[Stage 3 — Finite Automata Classification](docs/stage3_automata.md):** 5-tuple definitions $M = (Q, \Sigma, \delta, q_0, F)$, justification of DFA vs. $\epsilon$-NFA, and transition diagrams.
- **[Stage 4 — CFG Language Specification](docs/stage4_grammar.md):** EBNF grammar, terminal/non-terminal alphabet, AST representation, and theoretical analysis of **RAA3 (Grammar Simplification & Chomsky Normal Form)**.
- **[Module Design & Architecture](docs/module_design.md):** Module responsibilities, functional contracts, and end-to-end data flow diagrams.
- **[Test Cases & Verification Scenarios](docs/test_cases.md):** Comprehensive catalog of test cases covering all stages, optional transitions, and edge cases.
- **[AI Collaboration Log](docs/ai_collaboration_log.md):** Formal record of generative AI collaboration (Level 3 IAG) detailing prompts, contributions, and conceptual validations.
