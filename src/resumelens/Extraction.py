import re
import json
import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATA_DIR = os.path.join(BASE_DIR, "data")
if DATA_DIR not in sys.path:
    sys.path.append(DATA_DIR)

from sample_resumes import SAMPLE_RESUMES


PATTERNS = {
    "contact_emails": re.compile(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    ),
    "contact_phones": re.compile(
        r"(?:\+?\d{1,3}[\s.-]?)?(?:\(?\d{2,4}\)?[\s.-]?)?\d{3,4}[\s.-]?\d{4}"
    ),
    "contact_links": re.compile(
        r"\b(?:https?:\/\/)?(?:www\.)?(?:linkedin\.com\/(?:in|profile)\/[A-Za-z0-9_-]+|github\.com\/[A-Za-z0-9_-]+)\b",
        re.IGNORECASE  # Case-insensitive
    ),
    "programming_languages": re.compile(
        r"(?i)(?:\b(?:python|javascript|typescript|js|ts|java|golang|rust|scala|ruby|php|kotlin|swift|r|sql|bash|shell|go)\b"
        r"|\bc\+\+(?=[^\w]|$)|(?:\bc#(?=[^\w]|$)))"
    ),

    
    "frameworks_and_libraries": re.compile(
        r"(?i)\b(?:react(?:\.js|js)?|angular|vue(?:\.js|js)?|node(?:\.js|js)?|django|spring(?:\s+boot)?"
        r"|express(?:\.js|js)?|flask|fastapi|next(?:\.js|js)?|pandas|numpy|scikit[\s-]learn|sklearn"
        r"|tensorflow|tensor[\s-]flow|pytorch|py[\s-]torch|keras|opencv"
        r"|(?:apache\s+)?spark|pyspark|flink|(?:apache\s+)?airflow|(?:apache\s+)?kafka|dbt)\b"
    ),

    "databases": re.compile(
        r"(?i)\b(?:postgres(?:ql)?|mysql|mongodb|mongo|redis|cassandra|sqlite|mariadb"
        r"|oracle(?:\s+database)?|sql[\s-]server|mssql|dynamodb|snowflake|bigquery|redshift|couchdb|neo4j|sql|nosql)\b"
    ),

    "academic_qualifications": re.compile(
        r"(?i)\b(?:bachelor(?:\'s)?(?:\s+degree)?|b\.?s(?:\.c?)?|undergraduate|pregrado|licenciatura|ingenier[ií]a|"
        r"master(?:\'s)?(?:\s+degree)?|m\.?s(?:\.c?)?|maestr[ií]a|ph\.?d\.?|doctorate|doctorado|diploma|certified|certification)\.?"
        r"(?:\s+(?:of|in|en|de)\s+(?:computer\s+science|software\s+engineering|systems\s+engineering|"
        r"data\s+science|artificial\s+intelligence|information\s+technology|inform[aá]tica|sistemas|"
        r"ciencias\s+de\s+la\s+computaci[oó]n|inteligencia\s+artificial))?"
    ),

    "professional_experience": re.compile(
        r"(?i)(?:\b\d{1,2}\+?\s*(?:years?|yrs?)(?:\s+of)?(?:\s+experience)?"
        r"|\b(?:(?:19|20)\d{2}\s*[-–—]\s*(?:(?:19|20)\d{2}|present|actualidad|current))\b"
        r"|\b(?:(?:junior|mid-level|senior|lead|principal)\s+)?(?:full\s*stack|machine\s*learning|data|devops|software|backend|frontend)\s+(?:developer|engineer|specialist|architect)\b)"
    ),

    "tools_and_technologies": re.compile(
        r"(?i)\b(?:git|github|gitlab|bitbucket|linux|unix|ubuntu|jira|confluence|trello"
        r"|postman|swagger|nginx|apache(?!\s+(?:spark|flink|kafka|airflow))|gradle|maven|npm|yarn|vite|webpack)\b"
    ),

    "cloud_and_containers": re.compile(
        r"(?i)\b(?:docker|kubernetes|k8s|podman|helm|openshift|terraform|ansible|jenkins"
        r"|circleci|argo(?:\s*cd)?|aws|amazon\s+web\s+services|azure|gcp|google\s+cloud(?:\s+platform)?|ci[\s/-]?cd)\b"
    ),
}


def clean_and_deduplicate(matches):
    seen = set()
    result = []
    for item in matches:
        if isinstance(item, tuple):
            item = next((sub for sub in item if sub), "")
        cleaned = item.strip()
        if cleaned and cleaned.lower() not in seen:
            seen.add(cleaned.lower())
            result.append(cleaned)
    return result


def extract_resume_info(resume_text):

    return {
        "contact_information": {
            "emails": clean_and_deduplicate(PATTERNS["contact_emails"].findall(resume_text)),
            "phones": clean_and_deduplicate(PATTERNS["contact_phones"].findall(resume_text)),
            "links": clean_and_deduplicate(PATTERNS["contact_links"].findall(resume_text)),
        },
        "programming_languages": clean_and_deduplicate(PATTERNS["programming_languages"].findall(resume_text)),
        "frameworks_and_libraries": clean_and_deduplicate(PATTERNS["frameworks_and_libraries"].findall(resume_text)),
        "databases": clean_and_deduplicate(PATTERNS["databases"].findall(resume_text)),
        "academic_qualifications": clean_and_deduplicate(PATTERNS["academic_qualifications"].findall(resume_text)),
        "professional_experience": clean_and_deduplicate(PATTERNS["professional_experience"].findall(resume_text)),
        "tools_and_technologies": clean_and_deduplicate(PATTERNS["tools_and_technologies"].findall(resume_text)),
        "cloud_and_containers": clean_and_deduplicate(PATTERNS["cloud_and_containers"].findall(resume_text)),
    }


def save_to_json_file(data, filepath):

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"[OK] Saved JSON: {filepath}")


def save_to_text_file(candidates, filepath):

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("RESUMELENS - STAGE 1 EXTRACTION REPORT\n")
        f.write("=" * 50 + "\n\n")

        for c in candidates:
            f.write(f"Candidate: {c['candidate_name']} ({c['target_profile']})\n")
            f.write("-" * 50 + "\n")
            info = c["extracted_info"]
            f.write(f"1. Contact:       {info['contact_information']}\n")
            f.write(f"2. Languages:     {', '.join(info['programming_languages'])}\n")
            f.write(f"3. Frameworks:    {', '.join(info['frameworks_and_libraries'])}\n")
            f.write(f"4. Databases:     {', '.join(info['databases'])}\n")
            f.write(f"5. Education:     {', '.join(info['academic_qualifications'])}\n")
            f.write(f"6. Experience:    {', '.join(info['professional_experience'])}\n")
            f.write(f"7. Tools:         {', '.join(info['tools_and_technologies'])}\n")
            f.write(f"8. Cloud/DevOps:  {', '.join(info['cloud_and_containers'])}\n")
            f.write("\n" + "=" * 50 + "\n\n")

    print(f"[OK] Saved TXT Summary: {filepath}")

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print(" RESUMELENS - STAGE 1: REGEX EXTRACTION")
    print("=" * 60 + "\n")

    results = []

    for resume in SAMPLE_RESUMES:
        name = resume["candidate_name"]
        profile = resume["target_profile"]
        text = resume["raw_text"]

        print(f"Processing: {name} [{profile}]")
        extracted = extract_resume_info(text)

        results.append({
            "candidate_name": name,
            "target_profile": profile,
            "extracted_info": extracted
        })

    json_output = os.path.join(BASE_DIR, "output", "extracted_resumes.json")
    txt_output = os.path.join(BASE_DIR, "output", "extracted_resumes_summary.txt")

    print("\nSaving results...")
    save_to_json_file(results, json_output)
    save_to_text_file(results, txt_output)

    print("\nStage 1 completed successfully!\n")