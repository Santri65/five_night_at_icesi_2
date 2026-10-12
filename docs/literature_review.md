# Literature Review

## 1. Introduction and Context

In modern recruitment, Applicant Tracking Systems (ATS) handle thousands of résumés per job opening. Recruiters face the challenge of screening diverse candidate profiles while ensuring fair, transparent, and reproducible qualification checks. Some use Large Language Models (LLMs) and dense semantic embeddings for candidate screening, these statistical methods introduce substantial risks, liek: hallucinations, wrong scoring, prompt vulnerabilities, hidden demographic bias, and etc.

So **ResumeLens** explores a complementary, formal foundation: the application of **Formal Language Theory (FLT)** to candidate screening, decomposing the screening pipeline into regular expressions, finite-state transducers, finite automata, and context-free grammars, the system determines if it checks for a specifyc profile.

---

## 2. Formal Language Models compared to Statistical & Deep Learning Methods

| Feature | Formal Language Theory | Statistical NLP / Large Language Models |
| :--- | :--- | :--- |
| **Determinism** | **100% Deterministic:** Identical input always yields identical state transitions and acceptance results. | **Probabilistic / Non-deterministic:** Temperature and sampling lead to variance across runs. |
| **Explainability** | **Fully Auditable:** Every classification traces to an exact automaton path or grammar derivation tree. | **Black-Box:** Decision boundaries in latent embedding spaces cannot be directly audited. |
| **Security & Injection** | **Immune to Prompt Injection:** Input tokens are strictly parsed as formal alphabet symbols ($\Sigma$) althou this is a problem if we dont take into account other forms of presentacion or writing. | **Vulnerable:** Adversarial text embedded in invisible white fonts can hijack model decisions. |


---

## 3. Methodological Foundations by Pipeline Stage

- 3.1 Information Extraction via Regular Expressions: Regular languages represent the first level of the Chomsky hierarchy (Type 3). As formalized by Kleene (1956) and expanded by Hopcroft et al. (2006), regular expressions define languages recognized by deterministic finite automata.

- 3.2 Canonicalization via Finite-State Transducers: In technical résumés, synonymy and orthographic variants are rampant (e.g., `JS` vs. `JavaScript`, `Postgres` vs. `PostgreSQL`). A Finite-State Transducer (Mohri, 1997; Roche & Schabes, 1997) is an automaton with an input alphabet $\Sigma$ and an output alphabet $\Gamma$, modeling a rational relation:
$
R \subseteq \Sigma^* \times \Gamma^*
$
Using an FST guarantees that any recognized spelling variant translates into a unique, canonical symbol in $\Gamma$, mapping heterogeneous user vocabularies to formal profile vocabularies in linear time.

- 3.3 Pattern Recognition via Finite Automata: Qualification profiles demand combinations and sequences of competencies (e.g., frontend $\to$ backend $\to$ database $\to$ version control). By structuring profiles as Finite Automata $M = (Q, \Sigma, \delta, q_0, F)$

- 3.4 Structured Representation via Context-Free Grammars (CFG): Context-free grammars (Chomsky, 1956) define languages with hierarchical and recursive structures (Type 2). Implementing a Domain-Specific Language (DSL) via PEG/EBNF through textX (Dejanović et al., 2017)

---

## 5. References

1. **Chomsky, N.** (1956). *Three models for the description of language*. IRE Transactions on Information Theory, 2(3), 113–124.
2. **Hopcroft, J. E., Motwani, R., & Ullman, J. D.** (2006). *Introduction to Automata Theory, Languages, and Computation* (3rd ed.). Pearson / Addison-Wesley.
3. **Jurafsky, D., & Martin, J. H.** (2024). *Speech and Language Processing* (3rd ed. draft). Prentice Hall.
4. **Kleene, S. C.** (1956). *Representation of events in nerve nets and finite automata*. Automata Studies, 3–41.
5. **Mohri, M.** (1997). *Finite-state transducers in language and speech processing*. Computational Linguistics, 23(2), 269–311.
6. **Roche, E., & Schabes, Y.** (1997). *Finite-State Language Processing*. MIT Press.
7. **Dejanović, I., Vaderna, R., Milosavljević, G., & Vuković, Ž.** (2017). *TextX: A Python tool for domain-specific languages implementation*. Knowledge-Based Systems, 115, 1–4.
8. **Sipser, M.** (2013). *Introduction to the Theory of Computation* (3rd ed.). Cengage Learning.
