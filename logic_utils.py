def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None or raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return the outcome.

    outcome examples: "Win", "Too High", "Too Low"
    """
    # BUG (FIXED): the original version had a TypeError fallback that
    # compared guess and secret as strings (e.g. "9" > "100") whenever
    # app.py passed secret in as a str, giving wrong Too High/Too Low
    # hints for multi-digit numbers. Now that app.py always passes secret
    # as an int, guess/secret are compared directly and correctly.
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


MIN_WIN_POINTS = 10
WRONG_GUESS_PENALTY = 5


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""

    if outcome == "Win":
        points = 100 - 10 * attempt_number
        if points < MIN_WIN_POINTS:
            points = MIN_WIN_POINTS
        return current_score + points

    if outcome in ("Too High", "Too Low"):
        return max(current_score - WRONG_GUESS_PENALTY, 0)

    return current_score
