def compute_readiness_score(
    profile_score: float,
    tests_attempted_score: float,
    avg_test_score: float,
    mock_interview_score: float,
) -> float:
    """Compute weighted readiness score from 0 to 100."""
    total = (
        (profile_score * 0.20)
        + (tests_attempted_score * 0.30)
        + (avg_test_score * 0.30)
        + (mock_interview_score * 0.20)
    )
    return round(max(0.0, min(100.0, total)), 2)
