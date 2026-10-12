import json
import re
import sys
from pathlib import Path

from textx import metamodel_from_file

BASE_DIR = Path(__file__).resolve().parents[2]
SRC_DIR = BASE_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from resumelens.ProfileClassification import PROFILE_STAGES, classify_profile

GRAMMAR_PATH = Path(__file__).with_name("candidate_profile.tx")
EXTRACTED_PATH = BASE_DIR / "output" / "extracted_resumes.json"
NORMALIZED_PATH = BASE_DIR / "output" / "normalized_resumes.json"
OUTPUT_DIR = BASE_DIR / "output" / "candidate_profiles"

PROFILE_METAMODEL = metamodel_from_file(str(GRAMMAR_PATH))


def _quoted(value):
    return json.dumps(str(value), ensure_ascii=False)


def build_candidate_profile_source(
    candidate_name,
    extracted_info,
    normalized_skills,
    accepted_profiles,
):
    contact = extracted_info.get("contact_information", {})
    lines = [f"candidate {_quoted(candidate_name)} {{"]
    lines.append("    contact {")
    for entry_type, key in (
        ("email", "emails"),
        ("phone", "phones"),
        ("link", "links"),
    ):
        for value in contact.get(key, []):
            lines.append(f"        {entry_type} {_quoted(value)};")
    lines.append("    }")

    for section, key in (
        ("experience", "professional_experience"),
        ("education", "academic_qualifications"),
    ):
        lines.append(f"    {section} {{")
        for value in extracted_info.get(key, []):
            lines.append(f"        item {_quoted(value)};")
        lines.append("    }")

    lines.append("    skills {")
    for skill in normalized_skills:
        lines.append(f"        skill {skill};")
    lines.append("    }")

    lines.append("    classification {")
    for profile in accepted_profiles:
        lines.append(f"        accepted {_quoted(profile)};")
    lines.append("    }")
    lines.append("}")
    return "\n".join(lines) + "\n"


def parse_candidate_profile(source):
    profile = PROFILE_METAMODEL.model_from_str(source)
    if not profile.name.strip():
        raise ValueError("Candidate name cannot be empty.")

    for accepted in profile.classification.accepted_profiles:
        if accepted.profile not in PROFILE_STAGES:
            raise ValueError(f"Unknown accepted profile: {accepted.profile}")

    return profile


def _markdown_text(value):
    text = str(value).replace("\r", " ").replace("\n", " ")
    return re.sub(r"([\\`*_{}\[\]<>|])", r"\\\1", text)


def render_candidate_markdown(profile):
    lines = [f"# Candidate: {_markdown_text(profile.name)}", "", "## Contact"]
    contact_labels = {
        "EmailEntry": "Email",
        "PhoneEntry": "Phone",
        "LinkEntry": "Link",
    }
    for entry in profile.contact.entries:
        lines.append(
            f"- **{contact_labels[type(entry).__name__]}:** "
            f"{_markdown_text(entry.value)}"
        )
    if not profile.contact.entries:
        lines.append("- None provided")

    lines.extend(["", "## Professional experience"])
    lines.extend(
        f"- {_markdown_text(entry.value)}"
        for entry in profile.experience.entries
    )
    if not profile.experience.entries:
        lines.append("- None provided")

    lines.extend(["", "## Education"])
    lines.extend(
        f"- {_markdown_text(entry.value)}"
        for entry in profile.education.entries
    )
    if not profile.education.entries:
        lines.append("- None provided")

    lines.extend(["", "## Normalized skills"])
    lines.extend(f"- `{entry.value}`" for entry in profile.skills.entries)
    if not profile.skills.entries:
        lines.append("- None provided")

    lines.extend(["", "## Profile classification"])
    if profile.classification.accepted_profiles:
        lines.extend(
            f"- {_markdown_text(accepted.profile)}"
            for accepted in profile.classification.accepted_profiles
        )
    else:
        lines.append("- No profile pattern accepted")

    return "\n".join(lines) + "\n"


def _load_records():
    with EXTRACTED_PATH.open(encoding="utf-8") as file:
        extracted_records = json.load(file)
    with NORMALIZED_PATH.open(encoding="utf-8") as file:
        normalized_records = json.load(file)

    normalized_by_name = {}
    for record in normalized_records:
        name = record["candidate_name"]
        if name in normalized_by_name:
            raise ValueError(f"Duplicate normalized candidate name: {name}")
        normalized_by_name[name] = record

    return extracted_records, normalized_by_name


def generate_candidate_profiles(output_dir=OUTPUT_DIR):
    extracted_records, normalized_by_name = _load_records()
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    generated = []

    for index, candidate in enumerate(extracted_records, start=1):
        name = candidate["candidate_name"]
        normalized = normalized_by_name.get(name)
        if normalized is None:
            raise ValueError(f"No normalized record found for candidate: {name}")

        classification = classify_profile(normalized["normalized"])
        source = build_candidate_profile_source(
            name,
            candidate["extracted_info"],
            normalized["normalized"],
            classification["accepted_profiles"],
        )
        profile = parse_candidate_profile(source)
        markdown = render_candidate_markdown(profile)
        slug = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_") or "candidate"
        stem = f"{index:02d}_{slug}"
        source_path = output_dir / f"{stem}.profile"
        markdown_path = output_dir / f"{stem}.md"

        source_path.write_text(source, encoding="utf-8")
        markdown_path.write_text(markdown, encoding="utf-8")
        generated.append((source_path, markdown_path))
        print(f"[OK] Validated profile: {source_path}")
        print(f"[OK] Generated Markdown: {markdown_path}")

    return generated


if __name__ == "__main__":
    generate_candidate_profiles()
