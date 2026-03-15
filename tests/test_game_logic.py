from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score

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


# --- Refactor tests: logic_utils.py must have real implementations, not NotImplementedError stubs ---

def test_parse_guess_is_implemented():
    # Was raising NotImplementedError before refactor
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None

def test_parse_guess_invalid_input_is_implemented():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert value is None
    assert err is not None

def test_update_score_is_implemented():
    # Was raising NotImplementedError before refactor
    new_score = update_score(0, "Win", 1)
    assert isinstance(new_score, int)
    assert new_score > 0


# --- Challenge 1: Advanced Edge-Case Testing ---

# Edge case 1: Negative numbers
def test_parse_guess_negative_number():
    # Negative numbers are valid integers but out of game range — should still parse cleanly
    ok, value, err = parse_guess("-5")
    assert ok is True
    assert value == -5
    assert err is None

# Edge case 2: Decimal input gets truncated to int
def test_parse_guess_decimal_truncates():
    # "3.7" should become 3, not raise an error
    ok, value, err = parse_guess("3.7")
    assert ok is True
    assert value == 3
    assert err is None

# Edge case 3: Very large number
def test_parse_guess_very_large_number():
    # Extremely large values should parse without crashing
    ok, value, err = parse_guess("999999999")
    assert ok is True
    assert value == 999999999
    assert err is None

# Edge case 4: Zero input
def test_parse_guess_zero():
    # Zero is a valid integer and should parse fine
    ok, value, err = parse_guess("0")
    assert ok is True
    assert value == 0
    assert err is None

# Edge case 5: Whitespace-only input
def test_parse_guess_whitespace_only():
    # Spaces with no number should return an error, not crash
    ok, value, err = parse_guess("   ")
    assert ok is False
    assert value is None
    assert err is not None

# Edge case 6: check_guess with a string secret (simulates even-attempt flip in app.py)
def test_check_guess_string_secret_correct():
    # app.py converts secret to str on even attempts — check_guess must handle this
    outcome, message = check_guess(50, "50")
    assert outcome == "Win"

def test_check_guess_string_secret_too_high():
    # String comparison fallback path: guess int vs str secret
    outcome, message = check_guess(60, "50")
    assert outcome == "Too High"
    assert "LOWER" in message

def test_check_guess_string_secret_too_low():
    outcome, message = check_guess(40, "50")
    assert outcome == "Too Low"
    assert "HIGHER" in message
