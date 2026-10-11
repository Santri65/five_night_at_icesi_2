### 1. Contact Information

#### Regular Expressions
- **Email:**
  ```regex
  \b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b
  ```
- **Phone Number:**
  ```regex
  (?:\+?\d{1,3}[\s.-]?)?(?:\(?\d{2,4}\)?[\s.-]?)?\d{3,4}[\s.-]?\d{4}
  ```
- **Professional Links (GitHub / LinkedIn):**
  ```regex
  \b(?:https?:\/\/)?(?:www\.)?(?:linkedin\.com\/(?:in|profile)\/[A-Za-z0-9_-]+|github\.com\/[A-Za-z0-9_-]+)\b
  ```

#### Pattern Description
- **Email:** Matches standard email formats starting with valid username characters, followed by `@`, domain labels separated by dots, and a top-level domain (`.com`, `.edu`).
- **Phone:** Recognizes local and international phone numbers with optional country code (`+1`, `+57`), optional parentheses for area codes, and standard digit groups separated by spaces, dots, or dashes.
- **Links:** Identifies professional profile URLs pointing to `github.com` or `linkedin.com` profiles.

**Examples:**
- `wednesday.addams@nevermore.edu`, `+1 555-0199`, `https://github.com/wednesday-addams`

---

### 2. Programming Languages

#### Regular Expression
```regex
(?i)(?:\b(?:python|javascript|typescript|js|ts|java|golang|rust|scala|ruby|php|kotlin|swift|r|sql|bash|shell|go)\b|\bc\+\+(?=[^\w]|$)|(?:\bc#(?=[^\w]|$)))
```

#### Pattern Description
- Uses `(?i)` for case-insensitivity.
- Word boundaries `\b` ensure short keywords like `r` or `go` do not match inside regular words (`algorithm`, `google`).
- Uses lookahead `(?=[^\w]|$)` for `C++` and `C#` because the symbols `+` and `#` are non-word characters in regex.
- Covers languages across all 4 profiles (Full Stack, ML Engineer, Data Engineer, DevOps).

**Examples:**
- `Python`, `JS`, `TypeScript`, `SQL`, `Go`, `Scala`, `Bash`, `C++`

---

### 3. Frameworks and Libraries

#### Regular Expression
```regex
(?i)\b(?:react(?:\.js|js)?|angular|vue(?:\.js|js)?|node(?:\.js|js)?|django|spring(?:\s+boot)?|express(?:\.js|js)?|flask|fastapi|next(?:\.js|js)?|pandas|numpy|scikit[\s-]learn|sklearn|tensorflow|tensor[\s-]flow|pytorch|py[\s-]torch|keras|opencv|(?:apache\s+)?spark|pyspark|flink|(?:apache\s+)?airflow|(?:apache\s+)?kafka|dbt)\b
```

#### Pattern Description
- Detects web frameworks (Full Stack), machine learning libraries (ML Engineer), and distributed data frameworks (Data Engineer).
- Handles alternative spellings and naming variations like `React.js` / `React`, `scikit-learn` / `sklearn`, and `Apache Spark` / `Spark`.

**Examples:**
- `React.js`, `NodeJS`, `Pandas`, `NumPy`, `Scikit-learn`, `TensorFlow`, `Apache Spark`, `Airflow`

---

### 4. Databases

#### Regular Expression
```regex
(?i)\b(?:postgres(?:ql)?|mysql|mongodb|mongo|redis|cassandra|sqlite|mariadb|oracle(?:\s+database)?|sql[\s-]server|mssql|dynamodb|snowflake|bigquery|redshift|couchdb|neo4j|sql|nosql)\b
```

#### Pattern Description
- Recognizes relational databases (`PostgreSQL`, `MySQL`), NoSQL databases (`MongoDB`, `Redis`, `Cassandra`), and cloud data warehouses (`Snowflake`, `BigQuery`).
- Captures general database terms (`SQL`, `NoSQL`) and common abbreviations (`Postgres`, `MSSQL`).

**Examples:**
- `Postgres`, `MySQL`, `MongoDB`, `Snowflake`, `BigQuery`, `SQL`

---

### 5. Academic Qualifications

#### Regular Expression
```regex
(?i)\b(?:bachelor(?:\'s)?(?:\s+degree)?|b\.?s(?:\.c?)?|undergraduate|pregrado|licenciatura|ingenier[ií]a|master(?:\'s)?(?:\s+degree)?|m\.?s(?:\.c?)?|maestr[ií]a|ph\.?d\.?|doctorate|doctorado|diploma|certified|certification)\.?(?:\s+(?:of|in|en|de)\s+(?:computer\s+science|software\s+engineering|systems\s+engineering|data\s+science|artificial\s+intelligence|information\s+technology|inform[aá]tica|sistemas|ciencias\s+de\s+la\s+computaci[oó]n|inteligencia\s+artificial))?
```

#### Pattern Description
- Recognizes degree abbreviations (`B.S.`, `M.S.`, `Ph.D.`) and full degree levels (`Bachelor`, `Master`, `Ingeniería`).
- Optionally matches the connected field of study via prepositions (`of`, `in`, `en`, `de`) linked to computer science or engineering domains.

**Examples:**
- `Bachelor of Computer Science`, `M.S. in Artificial Intelligence`, `Ingenieria de Sistemas`, `B.S. in Software Engineering`

---

### 6. Professional Experience

#### Regular Expression
```regex
(?i)(?:\b\d{1,2}\+?\s*(?:years?|yrs?)(?:\s+of)?(?:\s+experience)?|\b(?:(?:19|20)\d{2}\s*[-–—]\s*(?:(?:19|20)\d{2}|present|actualidad|current))\b|\b(?:(?:junior|mid-level|senior|lead|principal)\s+)?(?:full\s*stack|machine\s*learning|data|devops|software|backend|frontend)\s+(?:developer|engineer|specialist|architect)\b)
```

#### Pattern Description
- Matches experience duration phrases (e.g., `3 years of experience`, `5+ years`).
- Matches employment date ranges (e.g., `2018 - 2022`).
- Matches formalized job titles requiring both seniority modifier and role noun (e.g., `Senior UI Developer`, `Full Stack Developer`).

**Examples:**
- `3 years of experience`, `2018 - 2022`, `Senior UI Developer`

---

### 7. Tools and Technologies

#### Regular Expression
```regex
(?i)\b(?:git|github|gitlab|bitbucket|linux|unix|ubuntu|jira|confluence|trello|postman|swagger|nginx|apache(?!\s+(?:spark|flink|kafka|airflow))|gradle|maven|npm|yarn|vite|webpack)\b
```

#### Pattern Description
- Matches version control systems (`Git`, `GitHub`), developer tools (`Postman`, `Swagger`), and operating systems (`Linux`, `Ubuntu`).
- Uses a negative lookahead `(?!\s+spark...)` so that `apache` only matches web servers/tools, without stealing from frameworks like `Apache Spark`.

**Examples:**
- `Git`, `GitHub`, `Linux`, `Jira`, `Postman`, `Nginx`

---

### 8. Cloud and Containers (DevOps / Data Engineer)

#### Regular Expression
```regex
(?i)\b(?:docker|kubernetes|k8s|podman|helm|openshift|terraform|ansible|jenkins|circleci|argo(?:\s*cd)?|aws|amazon\s+web\s+services|azure|gcp|google\s+cloud(?:\s+platform)?|ci[\s/-]?cd)\b
```

#### Pattern Description
- Specifically designed for the **DevOps** and **Data Engineer** profiles.
- Matches container platforms (`Docker`, `Kubernetes`, `K8s`), cloud infrastructure (`AWS`, `Azure`, `GCP`), Infrastructure as Code (`Terraform`, `Ansible`), and CI/CD tools (`Jenkins`, `CI/CD`).

**Examples:**
- `Docker`, `Kubernetes`, `K8s`, `Terraform`, `AWS`, `Azure`, `Jenkins`, `CI/CD`