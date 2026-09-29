from src.quality.analyzer import analyze_opportunity

def test_quality_flags_missing_fields():
    result = analyze_opportunity({'description':'Short post','company':'','salary':'','application_url':'','experience_required':'5 years'})
    assert result['quality_score'] < 100
    assert result['warnings']

def test_quality_flags_payment_request():
    result = analyze_opportunity({'description':'Pay a registration fee to apply for this internship.', 'company':'X', 'salary':'₹20,000/month', 'application_url':'https://x.test', 'experience_required':'0 years'})
    assert any('payment' in w.lower() or 'deposit' in w.lower() for w in result['warnings'])
