from app.services.readiness import compute_readiness_score


def test_readiness_score_formula():
    score = compute_readiness_score(80, 60, 70, 50)
    assert score == 66.0
