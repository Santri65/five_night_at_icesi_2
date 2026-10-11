"""
Sample Resumes for the 4 Professional Profiles:
1. Full Stack Developer (Wednesday Addams - Reference Profile)
2. Machine Learning Engineer (Mary Jane Watson - Reference Profile)
3. Data Engineer (Carlos Ruiz - Team Profile)
4. UI Developer (Gwen Stacy - Team Profile)

The resumes intentionally use different names and abbreviations
for qualifications to test the normalization stage.
"""

SAMPLE_RESUMES = [
    {
        "candidate_name": "Wednesday Addams",
        "target_profile": "Full Stack Developer",
        "raw_text": """
        Wednesday Addams
        Email: wednesday.addams@nevermore.edu | Phone: +1 555-0199
        GitHub: https://github.com/wednesday-addams
        Education: Bachelor of Computer Science (2018 - 2022)
        3 years of experience developing web applications.
        Technical Skills:
        JS, TypeScript, React.js, NodeJS, Postgres,
        RESTful APIs, Git.
        """
    },
    {
        "candidate_name": "Mary Jane Watson",
        "target_profile": "Machine Learning Engineer",
        "raw_text": """
        Mary Jane Watson
        Email: mj.watson@dailybugle.com | Phone: (123) 456-7890
        LinkedIn: linkedin.com/in/mary-jane-watson
        Education: M.S. in Artificial Intelligence
        2 years of experience developing predictive models
        and data-processing pipelines.
        Technical Skills:
        Python, pandas, sklearn, Tensor Flow,
        Py Torch, ML model development, SQL, Git.
        """
    },
    {
        "candidate_name": "Carlos Ruiz",
        "target_profile": "Data Engineer",
        "raw_text": """
        Carlos Ruiz
        Email: cruiz.data@example.com | Phone: +57 312 987 6543
        LinkedIn: https://www.linkedin.com/in/carlos-ruiz-data
        Education: Ingenieria de Sistemas, Postgrado en Data Science
        4 years of experience building high-throughput ETL data pipelines.
        Technical Skills:
        Python, SQL, Spark, ETL, Data Warehouse, Git.
        """
    },
    {
        "candidate_name": "Gwen Stacy",
        "target_profile": "UI Developer",
        "raw_text": """
        Gwen Stacy
        Email: gwen.stacy@example.com | Phone: +1 555-0123
        GitHub: https://github.com/gwenstacy
        Education: B.S. in Computer Science, Certified UI/UX Designer
        5+ years of experience developing responsive web interfaces.
        Technical Skills:
        HTML5, CSS3, JS, React.js, RWD, Git.
        """
    }
]