### Stage 2 - Normalization

Stage 2 converts Stage 1 terms to canonical names, removes duplicates, and sorts them
according to the selected profile. Input terms are lowercased before translation.

Code: [`src/stage2/normalization.py`](../src/stage2/normalization.py)  
Run: `python src/stage2/normalization.py`

#### Transducer definition

The transformations are implemented with `pyformlang`. The deterministic transducer is:

**M = (Q, Σ, Γ, δ, ω, q0, F)**

- **Q** (states) = {q0, qf}. `q0` is the initial state; `qf` means the input token
  was recognized.
- **Σ** (input alphabet, |Σ| = 82) = {javascript, js, typescript, ts, python, java, go, golang,
  bash, shell, scala, sql, c++, cpp, c#, csharp, react, react.js, reactjs, angular,
  angular.js, angularjs, vue, vue.js, vuejs, node, node.js, nodejs, django, spring,
  spring boot, springboot, express, express.js, expressjs, pandas, numpy, scikit-learn,
  scikit learn, scikitlearn, sklearn, tensorflow, tensor flow, tensor-flow, pytorch,
  py torch, py-torch, spark, apache spark, pyspark, py spark, airflow, apache airflow,
  kafka, apache kafka, postgres, postgresql, mysql, mongodb, mongo, snowflake, bigquery,
  big query, nosql, no sql, git, github, git hub, linux, nginx, docker, kubernetes, k8s,
  terraform, ansible, jenkins, ci/cd, ci cd, ci-cd, aws, amazon web services, azure}.
- **Γ** (Gamma; output alphabet, |Γ| = 44) = {JAVASCRIPT, TYPESCRIPT, PYTHON, JAVA, GO, BASH,
  SCALA, SQL, C_PLUS_PLUS, C_SHARP, REACT, ANGULAR, VUE, NODE_JS, DJANGO, SPRING_BOOT,
  EXPRESS, PANDAS, NUMPY, SCIKIT_LEARN, TENSORFLOW, PYTORCH, SPARK, PYSPARK, AIRFLOW,
  KAFKA, POSTGRESQL, MYSQL, MONGODB, SNOWFLAKE, BIGQUERY, NOSQL, GIT, GITHUB, LINUX,
  NGINX, DOCKER, KUBERNETES, TERRAFORM, ANSIBLE, JENKINS, CI_CD, AWS, AZURE}.
- **δ** (transition relation) = {(q0, v, qf) | v ∈ Σ}. Equivalently,
  δ(q0, v) = qf for every v ∈ Σ; all other transitions are undefined.
- **ω** (output function) is defined for each transition (q0, v, qf) and returns its
  canonical name in Γ, as labeled after `/` on the diagram; e.g.,
  ω(q0, `js`, qf) = JAVASCRIPT and ω(q0, `postgres`, qf) = POSTGRESQL.
- **q0** (initial state) = q0.
- **F** (accepting states) = {qf}. A token is accepted exactly when its transition
  reaches qf.

Each input is one whole, lowercased token. The transducer is deterministic and has no
ε-transitions. Tokens outside Σ have no accepting transition and are reported as
`unrecognized`.

#### Canonicalization and transition diagram

Each edge shows accepted input variants and their canonical output. This diagram defines
the input and output alphabets and the output function.

```mermaid
stateDiagram-v2
    direction LR
    [*] --> q0
    q0 --> qf: javascript, js / JAVASCRIPT
    q0 --> qf: typescript, ts / TYPESCRIPT
    q0 --> qf: python / PYTHON
    q0 --> qf: java / JAVA
    q0 --> qf: go, golang / GO
    q0 --> qf: bash, shell / BASH
    q0 --> qf: scala / SCALA
    q0 --> qf: sql / SQL
    q0 --> qf: c++, cpp / C_PLUS_PLUS
    q0 --> qf: c#, csharp / C_SHARP
    q0 --> qf: react, react.js, reactjs / REACT
    q0 --> qf: angular, angular.js, angularjs / ANGULAR
    q0 --> qf: vue, vue.js, vuejs / VUE
    q0 --> qf: node, node.js, nodejs / NODE_JS
    q0 --> qf: django / DJANGO
    q0 --> qf: spring, spring boot, springboot / SPRING_BOOT
    q0 --> qf: express, express.js, expressjs / EXPRESS
    q0 --> qf: pandas / PANDAS
    q0 --> qf: numpy / NUMPY
    q0 --> qf: scikit-learn, scikit learn, scikitlearn, sklearn / SCIKIT_LEARN
    q0 --> qf: tensorflow, tensor flow, tensor-flow / TENSORFLOW
    q0 --> qf: pytorch, py torch, py-torch / PYTORCH
    q0 --> qf: spark, apache spark / SPARK
    q0 --> qf: pyspark, py spark / PYSPARK
    q0 --> qf: airflow, apache airflow / AIRFLOW
    q0 --> qf: kafka, apache kafka / KAFKA
    q0 --> qf: postgres, postgresql / POSTGRESQL
    q0 --> qf: mysql / MYSQL
    q0 --> qf: mongodb, mongo / MONGODB
    q0 --> qf: snowflake / SNOWFLAKE
    q0 --> qf: bigquery, big query / BIGQUERY
    q0 --> qf: nosql, no sql / NOSQL
    q0 --> qf: git / GIT
    q0 --> qf: github, git hub / GITHUB
    q0 --> qf: linux / LINUX
    q0 --> qf: nginx / NGINX
    q0 --> qf: docker / DOCKER
    q0 --> qf: kubernetes, k8s / KUBERNETES
    q0 --> qf: terraform / TERRAFORM
    q0 --> qf: ansible / ANSIBLE
    q0 --> qf: jenkins / JENKINS
    q0 --> qf: ci/cd, ci cd, ci-cd / CI_CD
    q0 --> qf: aws, amazon web services / AWS
    q0 --> qf: azure / AZURE
    qf --> [*]
```

Example: `JS, ReactJS, Node.js` becomes `JAVASCRIPT, REACT, NODE_JS`.

#### Profile sorting

Duplicates are removed. Known terms follow the profile order; other terms are placed last.

| Profile | Canonical order |
|---|---|
| Full Stack Developer | `JAVASCRIPT → TYPESCRIPT → REACT → ANGULAR → VUE → NODE_JS → EXPRESS → DJANGO → SPRING_BOOT → SQL → POSTGRESQL → MYSQL → MONGODB → NOSQL → GIT → GITHUB` |
| Machine Learning Engineer | `PYTHON → PANDAS → NUMPY → SCIKIT_LEARN → TENSORFLOW → PYTORCH → SQL → POSTGRESQL → GIT` |
| Data Engineer | `PYTHON → SCALA → SQL → SPARK → PYSPARK → AIRFLOW → KAFKA → POSTGRESQL → SNOWFLAKE → BIGQUERY → AWS → DOCKER → LINUX → GIT` |
| DevOps Engineer | `BASH → PYTHON → GO → DOCKER → KUBERNETES → TERRAFORM → ANSIBLE → JENKINS → CI_CD → AWS → AZURE → LINUX → NGINX → GIT → GITHUB` |
