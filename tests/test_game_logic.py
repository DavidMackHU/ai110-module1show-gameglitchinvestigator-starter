from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
)


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"


def test_guess_too_low_multidigit():
    # Regression test for the string-comparison bug: a small guess against
    # a large multi-digit secret must never be reported as "Too High".
    result = check_guess(9, 100)
    assert result == "Too Low"


def test_guess_too_high_multidigit():
    result = check_guess(100, 9)
    assert result == "Too High"


def test_get_range_easy():
    assert get_range_for_difficulty("Easy") == (1, 20)


def test_get_range_normal():
    assert get_range_for_difficulty("Normal") == (1, 100)


def test_get_range_hard():
    assert get_range_for_difficulty("Hard") == (1, 50)


def test_get_range_unknown_defaults_to_normal_range():
    assert get_range_for_difficulty("Nonsense") == (1, 100)


def test_parse_guess_valid_int():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None


def test_parse_guess_valid_float_truncates():
    ok, value, err = parse_guess("42.9")
    assert ok is True
    assert value == 42


def test_parse_guess_empty_string():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None
    assert err is not None


def test_parse_guess_none():
    ok, value, err = parse_guess(None)
    assert ok is False
    assert value is None


def test_parse_guess_non_numeric():
    ok, value, err = parse_guess("banana")
    assert ok is False
    assert value is None
    assert err is not None


def test_update_score_win_first_attempt():
    # 100 - 10 * 1 = 90
    assert update_score(0, "Win", 1) == 90


def test_update_score_win_never_drops_below_10():
    # attempt_number high enough that the raw formula would go negative
    assert update_score(0, "Win", 50) == 10


def test_update_score_too_high_always_penalizes():
    # Regression test: guessing too high must never award points,
    # regardless of whether the attempt number is odd or even.
    assert update_score(100, "Too High", 1) == 95
    assert update_score(100, "Too High", 2) == 95


def test_update_score_too_low_always_penalizes():
    assert update_score(100, "Too Low", 1) == 95
    assert update_score(100, "Too Low", 2) == 95
