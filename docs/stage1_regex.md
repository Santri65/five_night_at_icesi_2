# Stage 1: Resume Information Extraction (Regular Expressions)

## 1. Objective

The first stage of ResumeLens extracts relevant candidate information from unstructured résumé text using Python regular expressions (`re`). It identifies candidate contact channels, qualifications, and competencies without determining equivalence or judging suitability.

Extracted data is cleaned, deduplicated, and preserved in structured formats:
- `output/extracted_resumes.json`: Machine-readable structured payload.
- `output/extracted_resumes_summary.txt`: Human-readable summary report.

---

## 2. Formal Pattern Definitions and Languages $L(R)$

Every regex $R$ defines a regular language $L(R)$ over the ASCII/Unicode character alphabet $\Sigma_{\text{text}}$.

---

### 2.1 Contact Information

#### 2.1.1 Email Addresses
- **Regular Expression:**
  ```regex
  \b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b
  ```
- **Pattern Description:** Matches standard RFC-compliant email strings with valid username characters, the `@` delimiter, followed by domain segments separated by dots and ending with a top-level domain (`.com`, `.edu`, etc.).
- **Example Matches:** `wednesday.addams@nevermore.edu`, `mj.watson@dailybugle.com`

#### 2.1.2 Phone Numbers
- **Regular Expression:**
  ```regex
  (?:\+?\d{1,3}[\s.-]?)?(?:\(?\d{2,4}\)?[\s.-]?)?\d{3,4}[\s.-]?\d{4}
  ```
- **Pattern Description:** Matches local and international phone formats with optional country code (`+1`, `+57`), optional parentheses for area codes, and standard digit groups separated by spaces, dots, or hyphens.
- **Example Matches:** `+1 555-0199`, `(123) 456-7890`, `+57 312 987 6543`

#### 2.1.3 Professional Links (GitHub / LinkedIn)
- **Regular Expression:**
  ```regex
  \b(?:https?:\/\/)?(?:www\.)?(?:linkedin\.com\/(?:in|profile)\/[A-Za-z0-9_-]+|github\.com\/[A-Za-z0-9_-]+)\b
  ```
- **Pattern Description:** Identifies professional profile URLs pointing to developer profiles on GitHub or LinkedIn, handling optional schemes (`https://`) and subdomains (`www.`).
- **Example Matches:** `https://github.com/wednesday-addams`, `linkedin.com/in/mary-jane-watson`

---

### 2.2 Programming Languages
- **Regular Expression:**
  ```regex
  (?i)(?:\b(?:python|javascript|typescript|js|ts|java|golang|rust|scala|ruby|php|kotlin|swift|r|sql|bash|shell|go)\b|\bc\+\+(?=[^\w]|$)|(?:\bc#(?=[^\w]|$)))
  ```
- **Pattern Description:** Uses `(?i)` for case-insensitivity. Word boundaries `\b` ensure short keywords like `r` or `go` do not match inside regular words (`algorithm`, `google`). Non-word lookaheads `(?=[^\w]|$)` handle symbols like `C++` and `C#`.
- **Example Matches:** `Python`, `JavaScript`, `TypeScript`, `SQL`, `Go`, `Scala`, `Bash`

---

### 2.3 Frameworks and Libraries
- **Regular Expression:**
  ```regex
  (?i)\b(?:react(?:\.js|js)?|angular|vue(?:\.js|js)?|node(?:\.js|js)?|django|spring(?:\s+boot)?|express(?:\.js|js)?|flask|fastapi|next(?:\.js|js)?|pandas|numpy|scikit[\s-]learn|sklearn|tensorflow|tensor[\s-]flow|pytorch|py[\s-]torch|keras|opencv|(?:apache\s+)?spark|pyspark|flink|(?:apache\s+)?airflow|(?:apache\s+)?kafka|dbt)\b
  ```
- **Pattern Description:** Captures frontend frameworks (React, Angular, Vue), backend platforms (Node.js, Express, Django, Spring Boot), data libraries (Pandas, NumPy, Spark), and machine learning toolkits (Scikit-learn, TensorFlow, PyTorch).
- **Example Matches:** `React.js`, `Node.js`, `Pandas`, `NumPy`, `Scikit-learn`, `TensorFlow`, `Apache Spark`

---

### 2.4 Databases
- **Regular Expression:**
  ```regex
  (?i)\b(?:postgres(?:ql)?|mysql|mongodb|mongo|redis|cassandra|sqlite|mariadb|oracle(?:\s+database)?|sql[\s-]server|mssql|dynamodb|snowflake|bigquery|redshift|couchdb|neo4j|sql|nosql)\b
  ```
- **Pattern Description:** Recognizes relational engines (`PostgreSQL`, `MySQL`), NoSQL databases (`MongoDB`, `Redis`), and data warehouses (`Snowflake`, `BigQuery`).
- **Example Matches:** `PostgreSQL`, `Postgres`, `SQL`, `MongoDB`, `Snowflake`

---

### 2.5 Academic Qualifications
- **Regular Expression:**
  ```regex
  (?i)\b(?:bachelor(?:\'s)?(?:\s+degree)?|b\.?s(?:\.c?)?|undergraduate|pregrado|licenciatura|ingenier[ií]a|master(?:\'s)?(?:\s+degree)?|m\.?s(?:\.c?)?|maestr[ií]a|ph\.?d\.?|doctorate|doctorado|diploma|certified|certification)\.?(?:\s+(?:of|in|en|de)\s+(?:computer\s+science|software\s+engineering|systems\s+engineering|data\s+science|artificial\s+intelligence|information\s+technology|inform[aá]tica|sistemas|ciencias\s+de\s+la\s+computaci[oó]n|inteligencia\s+artificial))?
  ```
- **Pattern Description:** Recognizes degree titles (`Bachelor`, `B.S.`, `Master`, `M.S.`, `Ingeniería`) optionally linked via prepositions to computer science or engineering domains.
- **Example Matches:** `Bachelor of Computer Science`, `M.S. in Artificial Intelligence`, `Ingenieria de Sistemas`

---

### 2.6 Professional Experience
- **Regular Expression:**
  ```regex
  (?i)(?:\b\d{1,2}\+?\s*(?:years?|yrs?)(?:\s+of)?(?:\s+experience)?|\b(?:(?:19|20)\d{2}\s*[-–—]\s*(?:(?:19|20)\d{2}|present|actualidad|current))\b|\b(?:(?:junior|mid-level|senior|lead|principal)\s+)?(?:full\s*stack|machine\s*learning|data|devops|software|backend|frontend)\s+(?:developer|engineer|specialist|architect)\b)
  ```
- **Pattern Description:** Captures experience duration phrases (e.g., `3 years of experience`), date ranges (`2018 - 2022`), and formal engineering titles.
- **Example Matches:** `3 years of experience`, `2018 - 2022`, `4 years of experience`

---

### 2.7 Tools and Technologies
- **Regular Expression:**
  ```regex
  (?i)\b(?:git|github|gitlab|bitbucket|linux|unix|ubuntu|jira|confluence|trello|postman|swagger|nginx|apache(?!\s+(?:spark|flink|kafka|airflow))|gradle|maven|npm|yarn|vite|webpack)\b
  ```
- **Pattern Description:** Matches developer tooling (`Git`, `GitHub`, `Postman`, `Nginx`, `Linux`). Uses a negative lookahead to prevent `apache` from colliding with `Apache Spark`.
- **Example Matches:** `Git`, `GitHub`, `Linux`, `Nginx`

---

### 2.8 Cloud and Containers (DevOps / Data Engineer)
- **Regular Expression:**
  ```regex
  (?i)\b(?:docker|kubernetes|k8s|podman|helm|openshift|terraform|ansible|jenkins|circleci|argo(?:\s*cd)?|aws|amazon\s+web\s+services|azure|gcp|google\s+cloud(?:\s+platform)?|ci[\s/-]?cd)\b
  ```
- **Pattern Description:** Matches container tools (`Docker`, `Kubernetes`), infrastructure as code (`Terraform`, `Ansible`), CI/CD automation (`Jenkins`, `CI/CD`), and cloud providers (`AWS`, `Azure`).
- **Example Matches:** `Docker`, `Kubernetes`, `Terraform`, `Ansible`, `Jenkins`, `CI/CD`, `AWS`

---

### 2.9 Profile-Specific Skills
- **Regular Expression:**
  ```regex
  (?i)\b(?:rest(?:ful)?\s+apis?|etl(?:\s+pipelines?)?|data\s+warehousing|machine[\s-]+learning\s+model\s+development|machine[\s-]+learning\s+models?|predictive\s+models?|developing\s+predictive\s+models?)\b
  ```
- **Pattern Description:** Extracts specialized role requirements that Stage 2 normalizes to canonical symbols (`REST_APIS`, `ETL_PIPELINES`, `DATA_WAREHOUSING`, `ML_MODEL_DEVELOPMENT`).
- **Example Matches:** `REST APIs`, `ETL Pipelines`, `Data Warehousing`, `Machine-learning model development`