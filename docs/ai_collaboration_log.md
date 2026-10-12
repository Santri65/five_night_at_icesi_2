## Ethical and Conceptual Use Statement

In accordance with the evaluation guidelines for Integrative Task 1, the team
used Generative Artificial Intelligence (GenAI) tools as programming
assistants, to support formal writing, and to refactor code. All code,
mathematical models (7-tuples, 5-tuples, and EBNF grammars), and design
decisions were audited, understood, and conceptually validated by the team
members.

---

## 2. Interaction and Prompt Log

- **Contribution:** The team manually designed the four required
  profiles (Full Stack, ML, Data Engineer, and DevOps), identifying that Full
  Stack and ML required optional skills (modeled with $\epsilon$-NFAs), while
  Data and DevOps required strict sequences (DFAs).
- **Prompt used:**
  > *"Analiza la inconsistencia donde Normalization traduce 'postgres' a 'POSTGRESQL', pero el automata de Full Stack solo tiene el simbolo SQL. Quiero que el automata acepte nativamente las alternativas de bases de datos ('SQL', 'POSTGRESQL', 'MYSQL', 'MONGODB', 'NOSQL') que estan en la Etapa 2 y con el diagrama del PDF.*
- **GenAI result:** A simplified refactoring proposal for
  `ProfileClassification.py`, connecting the output of `normalize_term()`
  directly to the symbols accepted by the automata.
- **Student validation:** Verification through unit tests in
  `test_pipeline_stages.py` using the official case
  `['JAVASCRIPT', 'REACT', 'NODE_JS', 'POSTGRESQL', 'GIT']`.

### 2

- **Contribution:** The team wrote an idea of the EBNF grammar in
  `candidate_profile.tx` and we needed toknow how it supports the
  course Learning Outcome.
- **Prompt used:**
  > *"Ayudame a organizar como la GFC de candidate_profile cumple con la parte 3 del pdf. Desarrolla la explicacion teorica de eliminacion de producciones inutiles, y la transformacion canonica a Forma de Chomsky y elimina el codigo muerto que pueda tener dentro, siguiendo el mismo formato del .md anteriro"*
- **GenAI result:** A theoretical outline and formal demonstration of the CNF
  transformation, incorporated into `docs/stage4_grammar.md`.
- **Student validation:** Review of the binary replacement rules $A \to BC$
  and terminal rules $A \to a$ against the CED III course notes.

### 3

- **Contribution:** The proposal to compare deterministic formal models
  with statistical models/LLMs for résumé screening.
- **Prompt used:**

  > *"Estructura un documento formal de revision de literatura (literature_review.md) que compare el uso de automatas, transductores y gramaticas contra LLMs en sistemas ATS, destacando determinismo, explicabilidad y resistencia a prompt injection. Guiate con:
  Chomsky, N. (1956). Three models for the description of language. IRE Transactions on Information Theory, 2(3), 113–124.
  Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2006). Introduction to Automata Theory, Languages, and Computation (3rd ed.). Pearson / Addison-Wesley.
  Jurafsky, D., & Martin, J. H. (2024). Speech and Language Processing (3rd ed. draft). Prentice Hall.
  Kleene, S. C. (1956). Representation of events in nerve nets and finite automata. Automata Studies, 3–41.
  Mohri, M. (1997). Finite-state transducers in language and speech processing. Computational Linguistics, 23(2), 269–311.
  Roche, E., & Schabes, Y. (1997). Finite-State Language Processing. MIT Press.
  Dejanović, I., Vaderna, R., Milosavljević, G., & Vuković, Ž. (2017). TextX: A Python tool for domain-specific languages implementation. Knowledge-Based Systems, 115, 1–4.
  Sipser, M. (2013). Introduction to the Theory of Computation (3rd ed.). Cengage Learning."*
- **GenAI result:** A structured draft of the document with academic
  references (Chomsky, Hopcroft, Mohri, and Jurafsky).
- **Student validation:** Adaptation of the content to ResumeLens's specific
  scope and four-stage architecture.

### 4w

- **Contribution:** The desired structure for an interactive console
  menu to test custom résumés or the sample batch.
- **Prompt used:**
  > *"Crea main.py como punto de entrada unificado y UI interactiva por terminal para que el usuario pueda evaluar cualquier CV en vivo o correr los 4 CVs muestra con un solo comando ademas de los tests."*
- **GenAI result:** Implementation of `main.py` with a CLI menu,
  step-by-step output, and a preview of Markdown reports.
- **Student validation:** Interactive execution and testing with valid and
  empty inputs.

### 5

- **Contribution:** The initial structure and idea of the documented part
- **Prompt used:**
  > *"Por favor siguiendo las refencias del archivo, ayudanos a construir el diseño del modulo del sistema y a reorganizar los .md de cada estado para darle mas orden, mismo formato, y claridad con profundizacion en su explicacion, y luego organiza mejor los diseños de tests"*
- **GenAI result:** Generates, module, stages 1-4 and test .md
- **Student validation:** Reading and reorganization
