import sys
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = BASE_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from data.sample_resumes import SAMPLE_RESUMES
from resumelens.Extraction import extract_resume_info
from resumelens.Normalization import normalize_resume, normalize_term
from resumelens.ProfileClassification import (
    OPTIONAL_PROFILE_STAGES,
    PROFILE_STAGES,
    classify_profile,
    classify_profile_by_name,
)


class ExtractionStageTests(unittest.TestCase):
    def test_extracts_contact_and_profile_skills(self):
        result = extract_resume_info(
            "wednesday.addams@nevermore.edu +1 555-0199 "
            "https://github.com/wednesday-addams "
            "JS React.js NodeJS Postgres Git REST APIs ETL Pipelines "
            "Data Warehousing Machine-learning model development"
        )

        self.assertIn(
            "wednesday.addams@nevermore.edu",
            result["contact_information"]["emails"],
        )
        self.assertIn("+1 555-0199", result["contact_information"]["phones"])
        self.assertTrue(result["contact_information"]["links"])
        self.assertTrue(result["programming_languages"])
        self.assertTrue(result["frameworks_and_libraries"])
        self.assertTrue(result["databases"])
        self.assertTrue(result["tools_and_technologies"])
        self.assertEqual(
            set(result["profile_specific_skills"]),
            {
                "REST APIs",
                "ETL Pipelines",
                "Data Warehousing",
                "Machine-learning model development",
            },
        )

    def test_missing_contact_information_produces_empty_lists(self):
        result = extract_resume_info("A candidate with technical experience.")

        self.assertEqual(result["contact_information"]["emails"], [])
        self.assertEqual(result["contact_information"]["phones"], [])
        self.assertEqual(result["contact_information"]["links"], [])


class NormalizationStageTests(unittest.TestCase):
    def test_maps_documented_variants_to_canonical_symbols(self):
        examples = {
            "JS": "JAVASCRIPT",
            "React.js": "REACT",
            "NodeJS": "NODE_JS",
            "Postgres": "POSTGRESQL",
            "sklearn": "SCIKIT_LEARN",
            "Tensor Flow": "TENSORFLOW",
            "Apache Spark": "APACHE_SPARK",
            "ETL Pipelines": "ETL_PIPELINES",
            "REST APIs": "REST_APIS",
        }

        for raw, expected in examples.items():
            with self.subTest(raw=raw):
                self.assertEqual(normalize_term(raw), expected)

    def test_deduplicates_aliases_and_reports_unknown_terms(self):
        result = normalize_resume(
            {
                "programming_languages": ["JS", "JavaScript", "unknown-tool"],
                "frameworks_and_libraries": ["React.js"],
            }
        )

        self.assertEqual(result["normalized"].count("JAVASCRIPT"), 1)
        self.assertIn("REACT", result["normalized"])
        self.assertEqual(result["unrecognized"], ["unknown-tool"])

    def test_reports_no_output_for_unknown_term(self):
        self.assertIsNone(normalize_term("unknown-tool"))


class ClassificationStageTests(unittest.TestCase):
    def test_all_sample_resumes_match_their_expected_profiles(self):
        for resume in SAMPLE_RESUMES:
            with self.subTest(candidate=resume["candidate_name"]):
                extracted = extract_resume_info(resume["raw_text"])
                result = classify_profile(extracted)
                self.assertEqual(
                    result["accepted_profiles"],
                    [resume["target_profile"]],
                )

    def test_accepts_official_full_stack_example_with_or_without_rest_apis(self):
        official_example = ["JavaScript", "React.js", "NodeJS", "Postgres", "Git"]

        self.assertTrue(
            classify_profile_by_name(
                official_example, "Full Stack Developer"
            )["accepted"]
        )
        self.assertTrue(
            classify_profile_by_name(
                official_example + ["REST APIs"], "Full Stack Developer"
            )["accepted"]
        )

    def test_accepts_official_machine_learning_example_and_optional_stages(self):
        official_example = [
            "Python",
            "Pandas",
            "TensorFlow",
            "PostgreSQL",
            "Git",
        ]

        self.assertTrue(
            classify_profile_by_name(
                official_example, "Machine Learning Engineer"
            )["accepted"]
        )
        self.assertTrue(
            classify_profile_by_name(
                official_example
                + ["Scikit-learn", "Machine-learning model development"],
                "Machine Learning Engineer",
            )["accepted"]
        )

    def test_rejects_each_profile_when_a_required_stage_is_missing(self):
        for profile, stages in PROFILE_STAGES.items():
            optional_stages = OPTIONAL_PROFILE_STAGES.get(profile, set())

            for index, _ in enumerate(stages):
                if index in optional_stages:
                    continue
                incomplete_skills = [
                    alternatives[0]
                    for stage_index, alternatives in enumerate(stages)
                    if stage_index not in optional_stages and stage_index != index
                ]
                with self.subTest(profile=profile, missing_stage=index):
                    self.assertFalse(
                        classify_profile_by_name(
                            incomplete_skills, profile
                        )["accepted"]
                    )

    def test_skill_order_does_not_change_classification(self):
        skills = [
            "JavaScript",
            "React.js",
            "NodeJS",
            "Postgres",
            "Git",
        ]

        self.assertTrue(
            classify_profile_by_name(
                list(reversed(skills)), "Full Stack Developer"
            )["accepted"]
        )

    def test_unknown_skill_does_not_block_a_complete_profile(self):
        skills = [
            "JavaScript",
            "React.js",
            "NodeJS",
            "Postgres",
            "Git",
            "unknown-tool",
        ]

    def test_accepts_pdf_canonical_sequence_directly(self):
        pdf_full_stack_seq = ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"]
        self.assertTrue(
            classify_profile_by_name(pdf_full_stack_seq, "Full Stack Developer")["accepted"]
        )

        pdf_ml_seq = ["PYTHON", "PANDAS", "TENSORFLOW", "POSTGRESQL", "GIT"]
        self.assertTrue(
            classify_profile_by_name(pdf_ml_seq, "Machine Learning Engineer")["accepted"]
        )

    def test_accepts_alternative_databases_in_full_stack(self):
        for db in ["SQL", "POSTGRESQL", "MYSQL", "MONGODB", "NOSQL"]:
            with self.subTest(database=db):
                skills = ["JAVASCRIPT", "REACT", "NODE_JS", db, "GIT"]
                self.assertTrue(
                    classify_profile_by_name(skills, "Full Stack Developer")["accepted"]
                )


if __name__ == "__main__":
    unittest.main()
