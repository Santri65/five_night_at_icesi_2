# ResumeLens — Stage 3: Profile Classification with Finite Automata

## 1. Objective

Stage 3 classifies a candidate's extracted CV skills against four professional profiles using one deterministic finite automaton (DFA) per profile:

1. Full Stack Developer
2. Machine Learning Engineer
3. Data Engineer
4. UI Developer

The automata receive normalized skill labels, not the raw CV text. Regex extraction belongs to Stage 1, and spelling/name normalization belongs to Stage 2.

## 2. Input and normalization

`Extraction.py` returns categorized information such as programming languages, frameworks, databases, tools, and profile-specific skills. `normalize_skills()` collects those values and maps known variants to canonical symbols. Examples:

| CV spelling | Canonical symbol |
|---|---|
| `JS`, `JavaScript` | `JAVASCRIPT` |
| `TypeScript`, `TS` | `TYPESCRIPT` |
| `React.js`, `React` | `REACT` |
| `NodeJS`, `Node.js` | `NODE_JS` |
| `Postgres`, `PostgreSQL`, `SQL` | `SQL` |
| `Scikit-learn`, `sklearn` | `SCIKIT_LEARN` |
| `TensorFlow` | `TENSORFLOW` |
| `PyTorch` | `PYTORCH` |

Normalization is essential: two spellings of the same qualification should not be treated as different automaton symbols.

## 3. Canonical order

A CV may list its skills in any order. Before testing a profile, `canonical_profile_sequence()` arranges the skills according to the profile's stage order. This implements the project's canonical-order requirement.

For each stage, alternatives are different symbols that lead to the same next state. If a CV contains more than one alternative for the same stage, the implementation chooses the first available alternative in the order declared in `PROFILE_STAGES`. This ensures that, for example, a CV containing both Pandas and NumPy does not consume two transitions for one stage.

## 4. Formal definition

Each profile DFA is defined by the five-tuple

\[
M = (Q, \Sigma, \delta, q_0, F)
\]

- \(Q\): states representing progress through the profile's skill stages.
- \(\Sigma\): canonical skill symbols used by the profile.
- \(\delta\): transition function. A skill from the current stage moves the automaton to the next state.
- \(q_0\): initial state, before any required stage has been processed.
- \(F\): the set containing the final state, reached after every required stage is matched.

The implementation uses `DeterministicFiniteAutomaton` from `pyformlang.finite_automaton`.

### Why DFA?

We choose DFAs because the input is normalized and arranged into a defined order. At each stage, each alternative skill has exactly one destination: the next state. Several different symbols may lead to that same destination; this does not make the automaton nondeterministic. An NFA would be needed if the same symbol from one state could lead to multiple destinations. An ε-NFA would add transitions that consume no input, which this design does not require.

## 5. Profile stage definitions

A comma-separated list inside one stage means alternative labels for the same transition to the next state. The stages themselves must be processed in order.

### 5.1 Full Stack Developer

1. `JAVASCRIPT` or `TYPESCRIPT`
2. `REACT`, `ANGULAR`, or `VUE`
3. `NODE_JS`, `DJANGO`, `SPRING_BOOT`, or `BACKEND_OTHER`
4. `SQL` or `NOSQL`
5. `REST_APIS`
6. `GIT`

### 5.2 Machine Learning Engineer

1. `PYTHON`
2. `PANDAS` or `NUMPY`
3. `SCIKIT_LEARN`
4. `TENSORFLOW` or `PYTORCH`
5. `ML_MODEL_DEVELOPMENT`
6. `SQL`
7. `GIT`

### 5.3 Data Engineer

1. `PYTHON`
2. `SQL`
3. `APACHE_SPARK`
4. `ETL_PIPELINES`
5. `DATA_WAREHOUSING`
6. `GIT`

### 5.4 UI Developer

1. `HTML`
2. `CSS`
3. `JAVASCRIPT`
4. `REACT`
5. `RESPONSIVE_WEB_DESIGN`
6. `GIT`

These sequences reflect the skills defined for the project. A profile is accepted only when all its stages are represented in the canonical sequence.

## 6. Transition diagrams

The code creates one state for the beginning of each stage plus a final state. For example, the Full Stack DFA has seven states: `q0` through `q6`. Each transition advances one stage. The final state is drawn with a double circle.

The diagrams are generated using the same approach shown in `Pyformlang.ipynb`:

1. Build the DFA using `pyformlang`.
2. Convert it to a NetworkX graph with `to_networkx()`.
3. Create a left-to-right Graphviz diagram.
4. Render the diagram to PNG and preserve the state/transition representation.

To generate the four PNG diagrams from the project root:

```python
from src.resumelens.ProfileClassification import draw_all_automata

draw_all_automata(output_dir="docs/automata")
```

If the package layout uses `resumelens` directly rather than `src.resumelens`, use the import path that matches the project's existing Python configuration.

Graphviz's Python package alone may not be sufficient: the Graphviz system executable must also be installed and available on PATH.

## 7. Implementation overview

`ProfileClassification.py` contains:

- `PROFILE_STAGES`: the ordered stages and alternatives for each profile.
- `normalize_skills()`: gathers extracted values and maps recognized variants to canonical symbols.
- `create_profile_automaton()`: builds the DFA for one profile.
- `canonical_profile_sequence()`: orders a candidate's known skills according to a profile's stages.
- `classify_profile()`: tests the candidate against all four DFAs and returns the accepted profiles and diagnostic details.
- `draw_automaton()`: creates a diagram for one profile.
- `draw_all_automata()`: creates all four diagrams.

The expected profile stored in a sample résumé is used only to check the test result. It is not used by the classifier to decide the profile.

## 8. Running and testing

Run the Stage 1 extraction first, then run `ProfileClassification.py` from the project root. The smoke test extracts each sample CV, classifies it, and reports whether the sample's expected profile was accepted.

Install the Python dependencies if necessary:

```bash
pip install pyformlang networkx graphviz
```

Install the Graphviz application separately if diagram rendering is required. Diagram generation is optional for classification itself.

## 9. Scope and limitations

- The DFA evaluates the presence of the required profile stages in the project's canonical order; it does not assess skill proficiency or years of experience.
- This is a strict sequence model. If a required stage is absent, a later skill cannot compensate for it.
- A candidate can be accepted by more than one profile if their normalized skills satisfy more than one complete sequence.
- Unknown skills are ignored by this Stage 3 implementation.
- The alias map is a project-specific normalization layer. It should be kept consistent with Stage 2 rather than becoming a competing, separate normalization system.
- `SQL` is treated as the canonical `SQL` symbol whether extraction placed it in programming languages or databases.
