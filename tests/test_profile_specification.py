import unittest
import sys
from pathlib import Path

from textx.exceptions import TextXError

BASE_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = BASE_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from data.sample_resumes import SAMPLE_RESUMES
from resumelens.Extraction import extract_resume_info
from resumelens.Normalization import normalize_resume
from resumelens.ProfileClassification import classify_profile
from resumelens.ProfileSpecification import (
    build_candidate_profile_source,
    parse_candidate_profile,
    render_candidate_markdown,
)


class ProfileSpecificationTests(unittest.TestCase):
    def test_parses_repeated_candidate_data(self):
        source = build_candidate_profile_source(
            "Test Candidate",
            {
                "contact_information": {
                    "emails": ["candidate@example.com", "work@example.com"],
                    "phones": ["+1 555-0100"],
                    "links": ["https://github.com/candidate"],
                },
                "professional_experience": ["Three years in software"],
                "academic_qualifications": ["B.S. in Computer Science"],
            },
            ["JAVASCRIPT", "REACT", "NODE_JS", "SQL", "GIT"],
            ["Full Stack Developer", "Machine Learning Engineer"],
        )

        profile = parse_candidate_profile(source)

        self.assertEqual(profile.name, "Test Candidate")
        self.assertEqual(len(profile.contact.entries), 4)
        self.assertEqual(len(profile.experience.entries), 1)
        self.assertEqual(len(profile.education.entries), 1)
        self.assertEqual(len(profile.skills.entries), 5)
        self.assertEqual(
            [entry.profile for entry in profile.classification.accepted_profiles],
            ["Full Stack Developer", "Machine Learning Engineer"],
        )

    def test_rejects_missing_required_section(self):
        source = 'candidate "Test Candidate" { contact {} }'

        with self.assertRaises(TextXError):
            parse_candidate_profile(source)

    def test_rejects_skill_that_violates_identifier_syntax(self):
        source = build_candidate_profile_source(
            "Test Candidate",
            {},
            ["INVALID-SKILL"],
            [],
        )

        with self.assertRaises(TextXError):
            parse_candidate_profile(source)

    def test_rejects_unknown_classified_profile(self):
        source = build_candidate_profile_source(
            "Test Candidate",
            {},
            [],
            ["UI Developer"],
        )

        with self.assertRaisesRegex(ValueError, "Unknown accepted profile"):
            parse_candidate_profile(source)

    def test_creates_markdown_from_validated_sample_pipeline(self):
        resume = SAMPLE_RESUMES[0]
        extracted = extract_resume_info(resume["raw_text"])
        normalized = normalize_resume(extracted)
        classification = classify_profile(normalized["normalized"])
        source = build_candidate_profile_source(
            resume["candidate_name"],
            extracted,
            normalized["normalized"],
            classification["accepted_profiles"],
        )

        markdown = render_candidate_markdown(parse_candidate_profile(source))

        self.assertIn("# Candidate: Wednesday Addams", markdown)
        self.assertIn("`JAVASCRIPT`", markdown)
        self.assertIn("- Full Stack Developer", markdown)


if __name__ == "__main__":
    unittest.main()
