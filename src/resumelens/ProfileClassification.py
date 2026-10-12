import os
import re
import sys
from collections.abc import Mapping
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
SRC_DIR = BASE_DIR / "src"
for directory in (str(BASE_DIR), str(SRC_DIR)):
    if directory not in sys.path:
        sys.path.insert(0, directory)

from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    Epsilon,
    EpsilonNFA,
    State,
    Symbol,
)
from resumelens.Normalization import normalize_term


def canonicalize_profile_name(profile_name):
    if profile_name is None:
        return None
    return str(profile_name).strip()


PROFILE_STAGES = {
    "Full Stack Developer": [
        ("JAVASCRIPT", "TYPESCRIPT"),
        ("REACT", "ANGULAR", "VUE"),
        ("NODE_JS", "DJANGO", "SPRING_BOOT", "EXPRESS"),
        ("SQL", "POSTGRESQL", "MYSQL", "MONGODB", "NOSQL"),
        ("REST_APIS",),
        ("GIT", "GITHUB"),
    ],
    "Machine Learning Engineer": [
        ("PYTHON",),
        ("PANDAS", "NUMPY"),
        ("SCIKIT_LEARN",),
        ("TENSORFLOW", "PYTORCH"),
        ("ML_MODEL_DEVELOPMENT",),
        ("SQL", "POSTGRESQL"),
        ("GIT", "GITHUB"),
    ],
    "Data Engineer": [
        ("PYTHON", "SCALA"),
        ("SQL", "POSTGRESQL"),
        ("APACHE_SPARK",),
        ("ETL_PIPELINES",),
        ("DATA_WAREHOUSING",),
        ("GIT", "GITHUB"),
    ],
    "DevOps Engineer": [
        ("BASH",),
        ("PYTHON",),
        ("GO",),
        ("DOCKER",),
        ("KUBERNETES",),
        ("TERRAFORM",),
        ("ANSIBLE",),
        ("JENKINS",),
        ("CI_CD",),
        ("AWS", "AZURE"),
        ("LINUX",),
        ("NGINX",),
        ("GIT", "GITHUB"),
    ],
}

OPTIONAL_PROFILE_STAGES = {
    "Full Stack Developer": {4},
    "Machine Learning Engineer": {2, 4},
}

_PROFILE_SKILL_SYMBOLS = {
    skill
    for stages in PROFILE_STAGES.values()
    for alternatives in stages
    for skill in alternatives
}


def _collect_strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, Mapping):
        for child in value.values():
            yield from _collect_strings(child)
    elif isinstance(value, (list, tuple, set)):
        for child in value:
            yield from _collect_strings(child)


def normalize_skills(skills_or_extracted_info):

    found = set()
    for raw in _collect_strings(skills_or_extracted_info):
        raw_upper = raw.strip().upper()
        if raw_upper in _PROFILE_SKILL_SYMBOLS:
            found.add(raw_upper)
            continue

        canon = normalize_term(raw)
        if canon and canon in _PROFILE_SKILL_SYMBOLS:
            found.add(canon)

    return found


def create_profile_automaton(profile_name):
    
    profile_name = canonicalize_profile_name(profile_name)
    if profile_name not in PROFILE_STAGES:
        raise ValueError(
            f"Unknown profile: {profile_name}. "
            f"Expected one of: {', '.join(PROFILE_STAGES)}"
        )

    stages = PROFILE_STAGES[profile_name]
    optional_stages = OPTIONAL_PROFILE_STAGES.get(profile_name, set())
    automaton = (
        EpsilonNFA()
        if optional_stages
        else DeterministicFiniteAutomaton()
    )

    states = [State(f"q{i}") for i in range(len(stages) + 1)]
    automaton.add_start_state(states[0])
    automaton.add_final_state(states[-1])

    for index, alternatives in enumerate(stages):
        for skill in alternatives:
            automaton.add_transition(
                states[index],
                Symbol(skill),
                states[index + 1],
            )
        if index in optional_stages:
            automaton.add_transition(
                states[index],
                Epsilon(),
                states[index + 1],
            )

    return automaton


def canonical_profile_sequence(profile_name, normalized_skills):
    
    profile_name = canonicalize_profile_name(profile_name)
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
   
    normalized = normalize_skills(skills_or_extracted_info)
    accepted_profiles = []
    details = {}

    for profile_name in PROFILE_STAGES:
        sequence = canonical_profile_sequence(profile_name, normalized)
        automaton = create_profile_automaton(profile_name)
        optional_stages = OPTIONAL_PROFILE_STAGES.get(profile_name, set())
        required_stages = len(PROFILE_STAGES[profile_name]) - len(optional_stages)
        matched_required_stages = sum(
            any(skill in normalized for skill in alternatives)
            for index, alternatives in enumerate(PROFILE_STAGES[profile_name])
            if index not in optional_stages
        )
        accepted = (
            automaton.accepts([Symbol(skill) for skill in sequence])
            and matched_required_stages == required_stages
        )

        details[profile_name] = {
            "accepted": accepted,
            "sequence": sequence,
            "expected_stages": len(PROFILE_STAGES[profile_name]),
            "matched_stages": len(sequence),
            "required_stages": required_stages,
            "matched_required_stages": matched_required_stages,
        }
        if accepted:
            accepted_profiles.append(profile_name)

    return {
        "normalized_skills": sorted(normalized),
        "accepted_profiles": accepted_profiles,
        "details": details,
    }


def classify_profile_by_name(skills_or_extracted_info, profile_name):
    
    profile_name = canonicalize_profile_name(profile_name)
    if profile_name not in PROFILE_STAGES:
        raise ValueError(
            f"Unknown profile: {profile_name}. Expected one of: "
            f"{', '.join(PROFILE_STAGES)}"
        )

    normalized = normalize_skills(skills_or_extracted_info)
    sequence = canonical_profile_sequence(profile_name, normalized)
    automaton = create_profile_automaton(profile_name)
    optional_stages = OPTIONAL_PROFILE_STAGES.get(profile_name, set())
    required_stages = len(PROFILE_STAGES[profile_name]) - len(optional_stages)
    matched_required_stages = sum(
        any(skill in normalized for skill in alternatives)
        for index, alternatives in enumerate(PROFILE_STAGES[profile_name])
        if index not in optional_stages
    )
    accepted = (
        automaton.accepts([Symbol(skill) for skill in sequence])
        and matched_required_stages == required_stages
    )

    return {
        "profile": profile_name,
        "normalized_skills": sorted(normalized),
        "sequence": sequence,
        "accepted": accepted,
        "required_stages": required_stages,
        "matched_required_stages": matched_required_stages,
    }


def _render_automaton_matplotlib(profile_name, output_png_path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    automaton = create_profile_automaton(profile_name)
    graph = automaton.to_networkx()

    nodes = [n for n, d in graph.nodes(data=True) if not str(n).startswith("starting_")]
    nodes.sort(key=lambda x: int(str(x)[1:]) if str(x)[1:].isdigit() else 999)

    fig, ax = plt.subplots(figsize=(max(8, len(nodes) * 1.8), 3.2))
    pos = {node: (i * 2.2, 0) for i, node in enumerate(nodes)}

    edge_labels = {}
    for u, v, data in graph.edges(data=True):
        if str(u).startswith("starting_"):
            continue
        label = data.get("label", "")
        if (u, v) not in edge_labels:
            edge_labels[(u, v)] = []
        if label:
            edge_labels[(u, v)].append(str(label))

    for node in nodes:
        is_final = graph.nodes[node].get("is_final", False)
        x, y = pos[node]
        circle = plt.Circle((x, y), 0.38, color="#DCEAFE", ec="#2563EB", lw=2, zorder=2)
        ax.add_patch(circle)
        if is_final:
            inner = plt.Circle((x, y), 0.30, fill=False, ec="#2563EB", lw=1.5, zorder=3)
            ax.add_patch(inner)
        ax.text(x, y, str(node), ha="center", va="center", fontsize=11, fontweight="bold", color="#1E3A8A", zorder=4)



    ax.annotate("", xy=(pos[nodes[0]][0] - 0.38, 0), xytext=(pos[nodes[0]][0] - 1.1, 0),
                arrowprops=dict(arrowstyle="->", lw=2, color="#2563EB"))

    for (u, v), labels in edge_labels.items():
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        text_label = " / ".join(labels)
        ax.annotate("", xy=(x2 - 0.38, y2), xytext=(x1 + 0.38, y1),
                    arrowprops=dict(arrowstyle="->", lw=1.6, color="#475569"))
        mid_x = (x1 + x2) / 2
        ax.text(mid_x, y1 + 0.45, text_label, ha="center", va="bottom", fontsize=7.5,
                color="#0F172A", bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#CBD5E1", lw=0.8))

    ax.set_xlim(-1.6, len(nodes) * 2.2)
    ax.set_ylim(-1.0, 1.8)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(f"Automaton: {profile_name}", fontsize=13, fontweight="bold", pad=12)
    plt.tight_layout()
    plt.savefig(output_png_path, dpi=200, bbox_inches="tight")
    plt.close()


def draw_automaton(profile_name, output_dir=None, view=False):
    safe_name = re.sub(r"[^A-Za-z0-9_-]+", "_", profile_name).lower()
    rendered_png = False
    try:
        import graphviz
        automaton = create_profile_automaton(profile_name)
        graph = automaton.to_networkx()

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
            dot.render(
                filename=safe_name,
                directory=output_dir,
                cleanup=True,
                view=view,
            )
            
            
            
            
            print(f"[OK] Diagram rendered via Graphviz: {output_dir}/{safe_name}.png")
            rendered_png = True
        return dot

    except Exception:
        if output_dir:
            raw_dot = os.path.join(output_dir, safe_name)
            if os.path.exists(raw_dot):
                try:
                    os.remove(raw_dot)
                except OSError:
                    pass
            os.makedirs(output_dir, exist_ok=True)
            out_png = os.path.join(output_dir, f"{safe_name}.png")
            _render_automaton_matplotlib(profile_name, out_png)
            print(f"[OK] Diagram rendered via Matplotlib: {out_png}")
            return None
        return None


def draw_all_automata(output_dir="docs/automata", view=False):
    return {
        profile_name: draw_automaton(
            profile_name,
            output_dir=output_dir,
            view=view,
        )
        for profile_name in PROFILE_STAGES
    }


if __name__ == "__main__":
    from data.sample_resumes import SAMPLE_RESUMES
    from resumelens.Extraction import extract_resume_info

    print("RESUMELENS - STAGE 3: FINITE AUTOMATA PROFILE CLASSIFICATION")
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