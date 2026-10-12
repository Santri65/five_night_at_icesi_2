# Test Cases and Verification Scenarios

All tests can be executed automatically via:
```powershell
python main.py --test
# or alternatively:
python -m unittest discover -s tests -p "test_*.py"
```

---

## 2. Stage 1 — Regex Extraction Test Scenarios

| Scenario ID | Test Input | Expected Result | Verification Target |
| :--- | :--- | :--- | :--- |
| **EX-01** | `wednesday.addams@nevermore.edu` | Extracted under `contact_information.emails` | Valid email syntax parsing. |
| **EX-02** | `+1 555-0199` | Extracted under `contact_information.phones` | International phone formatting. |
| **EX-03** | `https://github.com/wednesday-addams` | Extracted under `contact_information.links` | Developer profile URL parsing. |
| **EX-04** | `JS, React.js, NodeJS, Postgres, Git` | Extracted into categories: languages, frameworks, databases, and tools | Multi-category boundary isolation. |
| **EX-05** | `REST APIs, ETL Pipelines, Data Warehousing, Machine-learning model development` | Extracted under `profile_specific_skills` | Specialized compound skill detection. |
| **EX-06** | Plain text without contact information | Returns empty lists without throwing exceptions | Graceful missing-field handling. |

---

## 3. Stage 2 — FST Normalization Test Scenarios

| Scenario ID | Input Token | Canonical Output ($\Gamma$) | Verification Target |
| :--- | :--- | :--- | :--- |
| **NO-01** | `JS`, `Javascript` | `JAVASCRIPT` | Case & abbreviation folding. |
| **NO-02** | `React.js`, `ReactJS` | `REACT` | Extension suffix removal. |
| **NO-03** | `NodeJS`, `Node.js` | `NODE_JS` | Standard delimiter insertion. |
| **NO-04** | `Postgres`, `PostgreSQL` | `POSTGRESQL` | Database vendor normalization. |
| **NO-05** | `sklearn`, `scikit learn`, `Scikit-learn` | `SCIKIT_LEARN` | Machine learning library aliases. |
| **NO-06** | `Tensor Flow`, `TensorFlow` | `TENSORFLOW` | Space-delimited alias folding. |
| **NO-07** | `REST APIs`, `restful api` | `REST_APIS` | Pluralization and acronym folding. |
| **NO-08** | `Apache Spark`, `PySpark` | `APACHE_SPARK` | Ecosystem tool unification. |
| **NO-09** | `ETL Pipelines`, `etl` | `ETL_PIPELINES` | Pipeline phrase mapping. |
| **NO-10** | `Data Warehousing` | `DATA_WAREHOUSING` | Multi-word skill mapping. |
| **NO-11** | `Machine-learning model development` | `ML_MODEL_DEVELOPMENT` | Hyphenated role skill mapping. |
| **NO-12** | `unknown-tool` | `None` / recorded in `unrecognized` | Out-of-alphabet rejection. |

---

## 4. Stage 3 — Finite Automata Classification Test Scenarios

| Scenario ID | Input Skills | Profile Tested | Expected Verdict |
| :--- | :--- | :--- | :--- |
| **CL-01** | `PYTHON, PANDAS, TENSORFLOW, POSTGRESQL, GIT` *(PDF Pág. 5)* | Machine Learning Engineer | **ACCEPTED** (skips Scikit-learn & ML model dev via $\epsilon$) |
| **CL-02** | `Python, Pandas, Scikit-learn, TensorFlow, ML Model Dev, SQL, Git` | Machine Learning Engineer | **ACCEPTED** (all optional stages consumed) |
| **CL-03** | `Pandas, Scikit-learn, TensorFlow, SQL, Git` (Missing Python) | Machine Learning Engineer | **REJECTED** (missing initial required stage) |
| **CL-04** | `Python, Scikit-learn, TensorFlow, SQL, Git` (Missing Pandas/NumPy) | Machine Learning Engineer | **REJECTED** (missing data framework stage) |
| **CL-05** | `Python, Pandas, Scikit-learn, SQL, Git` (Missing ML framework) | Machine Learning Engineer | **REJECTED** (missing core framework stage) |
| **CL-06** | `Python, Pandas, TensorFlow, Git` (Missing SQL/Postgres) | Machine Learning Engineer | **REJECTED** (missing database stage) |
| **CL-07** | `Python, Pandas, TensorFlow, SQL` (Missing Git) | Machine Learning Engineer | **REJECTED** (missing final version control stage) |
| **CL-08** | Sample CVs for Wednesday, Mary Jane, Carlos, Alex | Respective Profile | **ACCEPTED** (100% precision on sample corpus) |
| **CL-09** | Any required stage omitted from any profile | Any Profile | **REJECTED** (strict stage requirement enforcement) |
| **CL-10** | Reversed skill order in input text | Full Stack Developer | **ACCEPTED** (canonical profile sorting normalizes order) |
| **CL-11** | Full Stack skills + `unknown-tool` | Full Stack Developer | **ACCEPTED** (unrelated noise does not block valid path) |
| **CL-12** | `JAVASCRIPT, REACT, NODE_JS, POSTGRESQL, GIT` *(PDF Pág. 4)* | Full Stack Developer | **ACCEPTED** (bypasses optional `REST_APIS` via $\epsilon$) |
| **CL-13** | `JAVASCRIPT, REACT, NODE_JS, POSTGRESQL, REST_APIS, GIT` | Full Stack Developer | **ACCEPTED** (consumes optional `REST_APIS`) |
| **CL-14** | `JAVASCRIPT, REACT, NODE_JS, db, GIT` with $db \in \{\texttt{SQL}, \texttt{POSTGRESQL}, \texttt{MYSQL}, \texttt{MONGODB}, \texttt{NOSQL}\}$ | Full Stack Developer | **ACCEPTED** (validates all database alternatives) |

---

## 5. Stage 4 — DSL and textX Grammar Test Scenarios

| Scenario ID | Test Input | Expected Result | Verification Target |
| :--- | :--- | :--- | :--- |
| **DSL-01** | DSL with repeated contacts, experiences, education, and skills | Successfully parsed into AST | Repetition syntax `{ ... }` validation. |
| **DSL-02** | DSL missing the required `skills { }` section | Parse error (`TextXSyntaxError`) | Mandatory section requirement. |
| **DSL-03** | DSL containing skill with invalid token syntax (`INVALID-SKILL`) | Parse error (`TextXSyntaxError`) | Lexical identifier syntax (`ID`). |
| **DSL-04** | DSL declaring unsupported profile `accepted "UI Developer";` | Semantic error (`ValueError`) | Profile domain restriction check. |
| **DSL-05** | Complete sample CV processed through Stages 1–4 | Emits formatted `.profile` and `.md` | End-to-end serialization and Markdown generation. |
