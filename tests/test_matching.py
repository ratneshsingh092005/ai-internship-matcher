from src.matching.ranking import skill_match_score, final_score
from src.matching.ranking import similarity_to_score

def test_similarity_mapping():
    assert similarity_to_score(1.0) == 100.0
    assert similarity_to_score(-1.0) == 0.0

def test_skill_match():
    assert skill_match_score(['Python','Docker'], ['Python','Docker','AWS']) == 66.67

def test_final_score():
    assert final_score(80, 60, 100) == 77.0
