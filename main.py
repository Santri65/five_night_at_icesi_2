#!/usr/bin/env python3
"""
ResumeLens — Interactive Command-Line Interface (UI) and Pipeline Runner
Formal Language-Based Resume Screening System
Integrative Task 1 - Computación y Estructuras Discretas III (2026-2)
"""

import os
import sys
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"
for d in (str(BASE_DIR), str(SRC_DIR)):
    if d not in sys.path:
        sys.path.insert(0, d)

from data.sample_resumes import SAMPLE_RESUMES
from resumelens.Extraction import extract_resume_info, save_to_json_file, save_to_text_file
from resumelens.Normalization import normalize_resume
from resumelens.ProfileClassification import classify_profile, draw_all_automata
from resumelens.ProfileSpecification import (
    build_candidate_profile_source,
    parse_candidate_profile,
    render_candidate_markdown,
    generate_candidate_profiles,
)

OUTPUT_DIR = BASE_DIR / "output"
PROFILES_OUTPUT_DIR = OUTPUT_DIR / "candidate_profiles"

#run all 4 resumes
def run_full_pipeline():
    
    print("\n" + "=" * 60)
    print(" [1/4] STAGE 1: REGEX INFORMATION EXTRACTION")
    print("=" * 60)
    extraction_results = []
    for resume in SAMPLE_RESUMES:
        name = resume["candidate_name"]
        profile = resume["target_profile"]
        print(f" -> Extracting: {name} ({profile})...")
        extracted = extract_resume_info(resume["raw_text"])
        extraction_results.append({
            "candidate_name": name,
            "target_profile": profile,
            "extracted_info": extracted,
        })

    json_extracted = OUTPUT_DIR / "extracted_resumes.json"
    txt_extracted = OUTPUT_DIR / "extracted_resumes_summary.txt"
    save_to_json_file(extraction_results, str(json_extracted))
    save_to_text_file(extraction_results, str(txt_extracted))

    print("\n" + "=" * 60)
    print(" [2/4] STAGE 2: FINITE-STATE TRANSDUCER (FST) NORMALIZATION")
    print("=" * 60)
    normalization_results = []
    for item in extraction_results:
        name = item["candidate_name"]
        profile = item["target_profile"]
        norm_data = normalize_resume(item["extracted_info"])
        normalization_results.append({
            "candidate_name": name,
            "target_profile": profile,
            **norm_data,
        })
        print(f" -> {name} [{profile}]")
        print(f"    Normalized skills: {', '.join(norm_data['normalized'])}")
        if norm_data["unrecognized"]:
            print(f"    [!] Unrecognized terms: {norm_data['unrecognized']}")

    json_normalized = OUTPUT_DIR / "normalized_resumes.json"
    save_to_json_file(normalization_results, str(json_normalized))

    print("\n" + "=" * 60)
    print(" [3/4] STAGE 3: FINITE AUTOMATA PROFILE CLASSIFICATION")
    print("=" * 60)
    for item in normalization_results:
        name = item["candidate_name"]
        expected = item["target_profile"]
        clf = classify_profile(item["normalized"])
        accepted = clf["accepted_profiles"]
        status = "PASSED" if expected in accepted else "FAILED"
        print(f" -> Candidate: {name}")
        print(f"    Target Profile  : {expected}")
        print(f"    Accepted Models : {accepted or 'None'}")
        print(f"    Status          : [{status}]")

    print("\n" + "=" * 60)
    print(" [4/4] STAGE 4: DSL (textX) VALIDATION & MARKDOWN GENERATION")
    print("=" * 60)
    generated = generate_candidate_profiles(output_dir=PROFILES_OUTPUT_DIR)
    print(f"\n[SUCCESS] Pipeline completed successfully!")
    print(f"Generated candidate markdown reports in: {PROFILES_OUTPUT_DIR}")
    for _, md_path in generated:
        print(f"  - {md_path.name}")

#Interactive resume testin
def test_custom_resume():
    print("\n" + "-" * 60)
    print(" INTERACTIVE RESUME SCREENING")
    print("-" * 60)
    name = input("Candidate Name (or press Enter for 'Jane Doe'): ").strip() or "Jane Doe"
    print("\nEnter or paste the resume text below.")
    print("Type 'END' on a new line and press Enter when finished:")

    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip() == "END":
            break
        lines.append(line)

    raw_text = "\n".join(lines)
    if not raw_text.strip():
        print("[!] No text provided. Aborting test.")
        return

    print("\n--- [STAGE 1] Regex Extraction ---")
    extracted = extract_resume_info(raw_text)
    print(f"Emails found       : {extracted['contact_information']['emails']}")
    print(f"Phones found       : {extracted['contact_information']['phones']}")
    print(f"Links found        : {extracted['contact_information']['links']}")
    print(f"Languages detected : {extracted['programming_languages']}")
    print(f"Frameworks detected: {extracted['frameworks_and_libraries']}")
    print(f"Databases detected : {extracted['databases']}")
    print(f"Tools detected     : {extracted['tools_and_technologies']}")
    print(f"Experience items   : {extracted['professional_experience']}")
    print(f"Education items    : {extracted['academic_qualifications']}")

    print("\n--- [STAGE 2] FST Normalization ---")
    norm_data = normalize_resume(extracted)
    print(f"Canonical skills   : {norm_data['normalized']}")
    if norm_data["unrecognized"]:
        print(f"Unrecognized terms : {norm_data['unrecognized']}")

    print("\n--- [STAGE 3] Automata Classification ---")
    classification = classify_profile(norm_data["normalized"])
    print(f"Accepted profiles  : {classification['accepted_profiles'] or 'None'}")
    for prof, details in classification["details"].items():
        state = "ACCEPTED" if details["accepted"] else "REJECTED"
        print(f"  * {prof:<28}: [{state}] (matched {details['matched_stages']} of {details['expected_stages']} stages)")

    print("\n--- [STAGE 4] Candidate Profile DSL & Markdown Rendering ---")
    try:
        source = build_candidate_profile_source(
            name,
            extracted,
            norm_data["normalized"],
            classification["accepted_profiles"],
        )
        profile_model = parse_candidate_profile(source)
        markdown = render_candidate_markdown(profile_model)

        slug = "".join(c if c.isalnum() else "_" for c in name.lower()).strip("_")
        out_file = PROFILES_OUTPUT_DIR / f"interactive_{slug}.md"
        PROFILES_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        out_file.write_text(markdown, encoding="utf-8")
        print(f"[OK] Profile parsed successfully and validated by textX!")
        print(f"[OK] Markdown report generated: {out_file}\n")
        print("Generated Markdown preview:")
        print("-" * 40)
        print(markdown.strip())
        print("-" * 40)
    except Exception as e:
        print(f"[!] Error validating or rendering profile: {e}")

#Run tesst
def run_unit_tests():
    import unittest
    print("\n" + "=" * 60)
    print(" RUNNING AUTOMATED UNIT TESTS")
    print("=" * 60 + "\n")
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=str(BASE_DIR / "tests"), pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    if result.wasSuccessful():
        print("\n[OK] All unit tests passed successfully!")
    else:
        print("\n[FAIL] Some tests failed. Check log above.")

#Render automatas diagram
def render_automata():
    print("\n" + "=" * 60)
    print(" RENDERING FINITE AUTOMATA DIAGRAMS")
    print("=" * 60)
    out_dir = str(BASE_DIR / "docs" / "automata")
    draw_all_automata(output_dir=out_dir)
    print(f"[OK] Finished automaton diagram generation in {out_dir}")

#menu
def interactive_menu():
    while True:
        print("Select an option:")
        print("  1. Run complete pipeline on sample resumes (Stages 1 to 4)")
        print("  2. Test a custom resume interactively (paste text)")
        print("  3. Run automated test suite (unittest)")
        print("  4. Render automata diagrams (Graphviz PNG)")
        print("  5. Exit")
        print()
        choice = input("Enter choice (1-5): ").strip()

        if choice == "1":
            run_full_pipeline()
        elif choice == "2":
            test_custom_resume()
        elif choice == "3":
            run_unit_tests()
        elif choice == "4":
            render_automata()
        elif choice == "5":
            print("\nExiting ResumeLens. Goodbye!\n")
            break
        else:
            print("[!] Invalid option. Please choose between 1 and 5.")

        input("\nPress Enter to return to main menu...")


def main():
    parser = argparse.ArgumentParser(description="ResumeLens Screening Pipeline")
    parser.add_argument("--run-all", action="store_true", help="Run full pipeline non-interactively")
    parser.add_argument("--test", action="store_true", help="Run unit tests non-interactively")
    args = parser.parse_args()

    if args.run_all:
        run_full_pipeline()
    elif args.test:
        run_unit_tests()
    else:
        interactive_menu()


if __name__ == "__main__":
    main()