"""
ResumeLens - Stage 3: Profile classification with deterministic finite automata.

Input: extracted skills (strings or the dictionary produced by Extraction.py).
Each profile is represented as an ordered sequence of stages. Alternatives in
one stage are different symbols leading to the same next state.

The CV's skill order is not trusted: skills are normalized and arranged in
the profile's canonical order before the DFA evaluates them.
"""

import re
import os
import sys
from collections.abc import Mapping

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SRC_DIR = os.path.join(BASE_DIR, "src")
for directory in (BASE_DIR, SRC_DIR):
    if directory not in sys.path:
        sys.path.insert(0, directory)

from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    State,
    Symbol,
)

# Each tuple is one stage. Items inside a tuple are alternatives for that stage.
PROFILE_STAGES = {
    "Full Stack Developer": [
        ("JAVASCRIPT", "TYPESCRIPT"),
        ("REACT", "ANGULAR", "VUE"),
        ("NODE_JS", "DJANGO", "SPRING_BOOT", "BACKEND_OTHER"),
        ("SQL", "NOSQL"),
        ("REST_APIS",),
        ("GIT",),
    ],
    "Machine Learning Engineer": [
        ("PYTHON",),
        ("PANDAS", "NUMPY"),
        ("SCIKIT_LEARN",),
        ("TENSORFLOW", "PYTORCH"),
        ("ML_MODEL_DEVELOPMENT",),
        ("SQL",),
        ("GIT",),
    ],
    "Data Engineer": [
        ("PYTHON",),
        ("SQL",),
        ("APACHE_SPARK",),
        ("ETL_PIPELINES",),
        ("DATA_WAREHOUSING",),
        ("GIT",),
    ],
    "UI Developer": [
        ("HTML",),
        ("CSS",),
        ("JAVASCRIPT",),
        ("REACT",),
        ("RESPONSIVE_WEB_DESIGN",),
        ("GIT",),
    ],
}

# Normalized labels and their common written variants.
ALIASES = {
    "JAVASCRIPT": {"javascript", "java script", "js"},
    "TYPESCRIPT": {"typescript", "type script", "ts"},
    "REACT": {"react", "react.js", "reactjs"},
    "ANGULAR": {"angular", "angular.js", "angularjs"},
    "VUE": {"vue", "vue.js", "vuejs"},
    "NODE_JS": {"node.js", "nodejs", "node"},
    "DJANGO": {"django"},
    "SPRING_BOOT": {"spring boot", "springboot"},
    "BACKEND_OTHER": {
        "express", "express.js", "flask", "fastapi", "next.js",
        "similar backend technology", "backend technology",
    },
    "SQL": {
        "sql", "postgres", "postgresql", "mysql", "sqlite", "mariadb",
        "oracle", "sql server", "mssql",
    },
    "NOSQL": {
        "nosql", "mongodb", "mongo", "redis", "cassandra", "dynamodb",
        "couchdb", "neo4j",
    },
    "REST_APIS": {"rest api", "rest apis", "restful api", "restful apis"},
    "GIT": {"git"},
    "PYTHON": {"python"},
    "PANDAS": {"pandas"},
    "NUMPY": {"numpy"},
    "SCIKIT_LEARN": {"scikit-learn", "scikit learn", "sklearn"},
    "TENSORFLOW": {"tensorflow", "tensor flow"},
    "PYTORCH": {"pytorch", "py torch"},
    "ML_MODEL_DEVELOPMENT": {
        "machine-learning model development",
        "machine learning model development",
        "machine-learning models",
        "machine learning models",
        "predictive models",
        "developing predictive models",
    },
    "APACHE_SPARK": {"apache spark", "spark", "pyspark"},
    "ETL_PIPELINES": {"etl pipeline", "etl pipelines", "etl"},
    "DATA_WAREHOUSING": {"data warehousing", "data warehouse"},
    "HTML": {"html", "html5"},
    "CSS": {"css", "css3"},
    "RESPONSIVE_WEB_DESIGN": {
        "responsive web design", "responsive design", "responsive layouts",
    },
}

# Compile aliases longest-first to avoid matching short variants inside longer ones.
_ALIAS_LOOKUP = {}
for canonical, variants in ALIASES.items():
    for variant in variants:
        _ALIAS_LOOKUP[variant] = canonical


def _normalize_text(value):
    """Normalize punctuation/spacing while preserving meaningful words."""
    value = value.lower().strip()
    value = value.replace("–", "-").replace("—", "-")
    value = re.sub(r"\s+", " ", value)
    return value.strip(" .,:;()[]{}")


def _collect_strings(value):
    """Recursively collect strings from an Extraction.py result dictionary."""
    if isinstance(value, str):
        yield value
    elif isinstance(value, Mapping):
        for child in value.values():
            yield from _collect_strings(child)
    elif isinstance(value, (list, tuple, set)):
        for child in value:
            yield from _collect_strings(child)


def normalize_skills(skills_or_extracted_info):
    """
    Return a set of canonical skill symbols.

    Accepts a list/set of extracted strings or the full extracted_info mapping.
    """
    found = set()
    for raw in _collect_strings(skills_or_extracted_info):
        normalized = _normalize_text(raw)

        # Exact aliases first.
        if normalized in _ALIAS_LOOKUP:
            found.add(_ALIAS_LOOKUP[normalized])
            continue

        # Extraction output may contain a longer sentence or a skill phrase.
        # Match aliases on word-like boundaries, longest variants first.
        for alias in sorted(_ALIAS_LOOKUP, key=len, reverse=True):
            pattern = r"(?<!\w)" + re.escape(alias) + r"(?!\w)"
            if re.search(pattern, normalized):
                found.add(_ALIAS_LOOKUP[alias])

    return found


def create_profile_automaton(profile_name):
    """Build a DFA for one profile using the profile's ordered stages."""
    if profile_name not in PROFILE_STAGES:
        raise ValueError(
            f"Unknown profile: {profile_name}. "
            f"Expected one of: {', '.join(PROFILE_STAGES)}"
        )

    stages = PROFILE_STAGES[profile_name]
    dfa = DeterministicFiniteAutomaton()

    states = [State(f"q{i}") for i in range(len(stages) + 1)]
    dfa.add_start_state(states[0])
    dfa.add_final_state(states[-1])

    for index, alternatives in enumerate(stages):
        for skill in alternatives:
            dfa.add_transition(
                states[index],
                Symbol(skill),
                states[index + 1],
            )

    return dfa


def canonical_profile_sequence(profile_name, normalized_skills):
    """
    Order the CV skills according to the profile's canonical stages.

    For a stage with alternatives, select one present alternative in the order
    listed in PROFILE_STAGES. This prevents a CV listing both Pandas and NumPy
    from consuming two transitions for the same stage.
    """
    if profile_name not in PROFILE_STAGES:
        raise ValueError(f"Unknown profile: {profile_name}")

    sequence = []
    for alternatives in PROFILE_STAGES[profile_name]:
        selected = next(
            (skill for skill in alternatives if skill in normalized_skills),
            None,
        )
        if selected is not None:
            sequence.append(selected)

    return sequence


def classify_profile(skills_or_extracted_info):
    """
    Return all profiles whose DFA accepts the candidate's available skills.

    A profile is accepted only when every stage has a matching skill.
    The result includes the normalized skills and per-profile test details.
    """
    normalized = normalize_skills(skills_or_extracted_info)
    accepted_profiles = []
    details = {}

    for profile_name in PROFILE_STAGES:
        sequence = canonical_profile_sequence(profile_name, normalized)
        dfa = create_profile_automaton(profile_name)
        accepted = dfa.accepts([Symbol(skill) for skill in sequence])

        # The sequence must include one symbol per stage; this explicit check
        # also makes the required-skill rule easy to understand.
        accepted = accepted and len(sequence) == len(PROFILE_STAGES[profile_name])

        details[profile_name] = {
            "accepted": accepted,
            "sequence": sequence,
            "expected_stages": len(PROFILE_STAGES[profile_name]),
            "matched_stages": len(sequence),
        }
        if accepted:
            accepted_profiles.append(profile_name)

    return {
        "normalized_skills": sorted(normalized),
        "accepted_profiles": accepted_profiles,
        "details": details,
    }


def draw_automaton(profile_name, output_dir=None, view=False):
    """
    Draw one DFA using Graphviz, in the same style as the Pyformlang notebook.
    Saves PNG and DOT when output_dir is provided; returns the Digraph object.
    """
    import graphviz

    dfa = create_profile_automaton(profile_name)
    graph = dfa.to_networkx()

    dot = graphviz.Digraph(
        name=profile_name.replace(" ", "_"),
        engine="dot",
        format="png",
    )
    dot.attr(rankdir="LR", splines="true", nodesep="0.45", ranksep="0.65")
    dot.attr("node", fontname="Helvetica", style="filled", fillcolor="#DCEAFE",
             color="#4472C4", fontcolor="#17365D")
    dot.attr("edge", fontname="Helvetica", fontsize="10")

    dot.node("__start__", label="", shape="none", width="0", height="0")

    for node, data in graph.nodes(data=True):
        node_id = str(node)
        if node_id.startswith("starting_"):
            continue

        is_final = data.get("is_final", False)
        dot.node(
            node_id,
            label=node_id,
            shape="doublecircle" if is_final else "circle",
        )

    for source, target, data in graph.edges(data=True):
        source_id = str(source)
        target_id = str(target)

        if source_id.startswith("starting_"):
            dot.edge("__start__", target_id)
        else:
            label = str(data.get("label", ""))
            dot.edge(source_id, target_id, label=label)

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        safe_name = re.sub(r"[^A-Za-z0-9_-]+", "_", profile_name).lower()
        dot.render(
            filename=safe_name,
            directory=output_dir,
            cleanup=True,
            view=view,
        )

    return dot


def draw_all_automata(output_dir="docs/automata", view=False):
    """Generate a PNG diagram for each of the four profile DFAs."""
    return {
        profile_name: draw_automaton(
            profile_name,
            output_dir=output_dir,
            view=view,
        )
        for profile_name in PROFILE_STAGES
    }


if __name__ == "__main__":
    # Smoke test using the sample CVs and the Stage 1 extractor.
    from data.sample_resumes import SAMPLE_RESUMES
    from resumelens.Extraction import extract_resume_info

    print("RESUMELENS - STAGE 3: DFA PROFILE CLASSIFICATION")
    print("=" * 55)

    for resume in SAMPLE_RESUMES:
        extracted_info = extract_resume_info(resume["raw_text"])
        result = classify_profile(extracted_info)

        print(f"\nCandidate: {resume['candidate_name']}")
        print(f"Expected profile (test data): {resume['target_profile']}")
        print(f"Normalized skills: {result['normalized_skills']}")
        print(f"Accepted profiles: {result['accepted_profiles'] or 'None'}")

        expected_is_accepted = resume["target_profile"] in result["accepted_profiles"]
        print(f"Expected profile accepted: {expected_is_accepted}")

    # Uncomment to export diagrams when Graphviz is installed:
    # draw_all_automata(output_dir=os.path.join(BASE_DIR, "docs", "automata"))
