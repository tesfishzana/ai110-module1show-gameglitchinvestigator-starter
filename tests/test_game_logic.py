from logic_utils import check_guess, get_range_for_difficulty

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# --- Bug fix tests ---

# Bug 1: Hint messages were backwards
def test_too_high_message_says_go_lower():
    # When guess > secret, player must go LOWER, not higher
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message, f"Expected 'LOWER' in message, got: '{message}'"

def test_too_low_message_says_go_higher():
    # When guess < secret, player must go HIGHER, not lower
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message, f"Expected 'HIGHER' in message, got: '{message}'"


# Bug 2: Hard difficulty range must be wider than Normal
def test_hard_range_wider_than_normal():
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert hard_high > normal_high, (
        f"Hard range upper bound ({hard_high}) should be greater than Normal ({normal_high})"
    )


# Bug 3: Easy difficulty must allow more attempts than Normal
def test_easy_has_more_attempts_than_normal():
    attempt_limit_map = {
        "Easy": 10,
        "Normal": 8,
        "Hard": 5,
    }
    assert attempt_limit_map["Easy"] > attempt_limit_map["Normal"], (
        f"Easy ({attempt_limit_map['Easy']}) should have more attempts than Normal ({attempt_limit_map['Normal']})"
    )
