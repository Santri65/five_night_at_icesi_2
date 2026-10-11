import json
import os
import sys

from pyformlang.fst import FiniteStateTransducer as FST

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

VARIANTS = {
    "JAVASCRIPT": ["javascript", "js"],
    "TYPESCRIPT": ["typescript", "ts"],
    "PYTHON": ["python"],
    "JAVA": ["java"],
    "GO": ["go", "golang"],
    "BASH": ["bash", "shell"],
    "SCALA": ["scala"],
    "SQL": ["sql"],
    "C_PLUS_PLUS": ["c++", "cpp"],
    "C_SHARP": ["c#", "csharp"],
    # frameworks y librerias
    "REACT": ["react", "react.js", "reactjs"],
    "ANGULAR": ["angular", "angular.js", "angularjs"],
    "VUE": ["vue", "vue.js", "vuejs"],
    "NODE_JS": ["node", "node.js", "nodejs"],
    "DJANGO": ["django"],
    "SPRING_BOOT": ["spring", "spring boot", "springboot"],
    "EXPRESS": ["express", "express.js", "expressjs"],
    "PANDAS": ["pandas"],
    "NUMPY": ["numpy"],
    "SCIKIT_LEARN": ["scikit-learn", "scikit learn", "scikitlearn", "sklearn"],
    "TENSORFLOW": ["tensorflow", "tensor flow", "tensor-flow"],
    "PYTORCH": ["pytorch", "py torch", "py-torch"],
    "SPARK": ["spark", "apache spark"],
    "PYSPARK": ["pyspark", "py spark"],
    "AIRFLOW": ["airflow", "apache airflow"],
    "KAFKA": ["kafka", "apache kafka"],
    "POSTGRESQL": ["postgres", "postgresql"],
    "MYSQL": ["mysql"],
    "MONGODB": ["mongodb", "mongo"],
    "SNOWFLAKE": ["snowflake"],
    "BIGQUERY": ["bigquery", "big query"],
    "NOSQL": ["nosql", "no sql"],
    "GIT": ["git"],
    "GITHUB": ["github", "git hub"],
    "LINUX": ["linux"],
    "NGINX": ["nginx"],
    "DOCKER": ["docker"],
    "KUBERNETES": ["kubernetes", "k8s"],
    "TERRAFORM": ["terraform"],
    "ANSIBLE": ["ansible"],
    "JENKINS": ["jenkins"],
    "CI_CD": ["ci/cd", "ci cd", "ci-cd"],
    "AWS": ["aws", "amazon web services"],
    "AZURE": ["azure"],
}
PROFILE_ORDER = {
    "Full Stack Developer": ["JAVASCRIPT", "TYPESCRIPT", "REACT", "ANGULAR", "VUE", "NODE_JS", "EXPRESS",
                             "DJANGO", "SPRING_BOOT", "SQL", "POSTGRESQL", "MYSQL", "MONGODB", "NOSQL",
                             "GIT", "GITHUB"],
    "Machine Learning Engineer": ["PYTHON", "PANDAS", "NUMPY", "SCIKIT_LEARN", "TENSORFLOW", "PYTORCH",
                                  "SQL", "POSTGRESQL", "GIT"],
    "Data Engineer": ["PYTHON", "SCALA", "SQL", "SPARK", "PYSPARK", "AIRFLOW", "KAFKA", "POSTGRESQL",
                      "SNOWFLAKE", "BIGQUERY", "AWS", "DOCKER", "LINUX", "GIT"],
    "DevOps Engineer": ["BASH", "PYTHON", "GO", "DOCKER", "KUBERNETES", "TERRAFORM", "ANSIBLE", "JENKINS",
                        "CI_CD", "AWS", "AZURE", "LINUX", "NGINX", "GIT", "GITHUB"],
}

BUCKETS = ["programming_languages", "frameworks_and_libraries", "databases",
           "tools_and_technologies", "cloud_and_containers"]

def build_transducer():
    fst = FST()
    fst.add_transitions([("q0", v, "qf", [canon])
                         for canon, variants in VARIANTS.items() for v in variants])
    fst.add_start_state("q0")
    fst.add_final_state("qf")
    return fst


TRANSDUCER = build_transducer()


def normalize_term(raw):
    results = list(TRANSDUCER.translate([raw.strip().lower()]))
    return "".join(results[0]) if results else None


def sort_for_profile(terms, profile):
    order = PROFILE_ORDER[profile]
    rank = {t: i for i, t in enumerate(order)}
    return sorted(set(terms), key=lambda t: (rank.get(t, len(order)), t))


def normalize_resume(extracted_info):
    normalized, unrecognized = [], []
    for bucket in BUCKETS:
        for raw in extracted_info.get(bucket, []):
            canon = normalize_term(raw)
            if canon is None:
                unrecognized.append(raw)
            elif canon not in normalized:
                normalized.append(canon)
    return {
        "normalized": normalized,
        "unrecognized": unrecognized,
        "sorted_by_profile": {p: sort_for_profile(normalized, p) for p in PROFILE_ORDER},
    }


if __name__ == "__main__":
    path = os.path.join(BASE_DIR, "output", "extracted_resumes.json")
    with open(path, encoding="utf-8") as f:
        candidates = json.load(f)

    results = []
    for c in candidates:
        r = normalize_resume(c["extracted_info"])
        results.append({"candidate_name": c["candidate_name"], "target_profile": c["target_profile"], **r})
        print(f"{c['candidate_name']} [{c['target_profile']}]")
        print("  ", ", ".join(r["sorted_by_profile"][c["target_profile"]]))
        if r["unrecognized"]:
            print("   sin reconocer:", r["unrecognized"])

    out = os.path.join(BASE_DIR, "output", "normalized_resumes.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
    print(f"[OK] Saved JSON: {out}")