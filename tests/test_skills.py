from src.skills.extractor import extract_skills, normalize_skill

def test_skill_normalization():
    assert normalize_skill('springboot') == 'Spring Boot'
    assert normalize_skill('Postgres') == 'PostgreSQL'
    assert normalize_skill('scikit learn') == 'Scikit-learn'
    assert normalize_skill('nodejs') == 'Node.js'

def test_skill_extraction():
    skills = extract_skills('Built APIs with Springboot and Postgres. Used nodejs, Docker and Python.')
    assert {'Spring Boot','PostgreSQL','Node.js','Docker','Python'} <= set(skills)
