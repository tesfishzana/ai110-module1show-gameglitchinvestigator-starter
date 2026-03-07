# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

### 🎯 Game Purpose
Glitch Guesser is a number guessing game built with Streamlit. The player picks a difficulty level (Easy, Normal, or Hard), and the game generates a secret number within the corresponding range. The player has a limited number of attempts to guess the number, and the game gives "Too High" or "Too Low" hints after each guess until the player wins or runs out of attempts.

### 🐛 Bugs Found

| # | Bug | Location |
|---|-----|----------|
| 1 | Hint messages were backwards — "Go HIGHER" shown when guess was too high, "Go LOWER" when too low | `app.py` → `check_guess()` lines 37–47 |
| 2 | Easy difficulty had fewer attempts (6) than Normal (8), making it harder than Normal | `app.py` → `attempt_limit_map` line 81 |
| 3 | Hard difficulty had a smaller number range (1–50) than Normal (1–100), making it easier than Normal | `app.py` → `get_range_for_difficulty()` line 10 |

### 🔧 Fixes Applied

1. **Backwards hints** — Swapped the return messages in `check_guess()` so `guess > secret` returns "Go LOWER!" and `guess < secret` returns "Go HIGHER!", applied to both the normal path and the `TypeError` fallback.
2. **Easy attempt limit** — Changed Easy from `6` to `10` attempts so it is more forgiving than Normal (8).
3. **Hard range** — Changed Hard's upper bound from `50` to `200` so it is wider than Normal (1–100), making it genuinely harder.

### ✅ Tests Added (`tests/test_game_logic.py`)

Four new pytest cases were added to specifically catch each bug:
- `test_too_high_message_says_go_lower` — asserts the hint says "LOWER" when guess > secret
- `test_too_low_message_says_go_higher` — asserts the hint says "HIGHER" when guess < secret
- `test_hard_range_wider_than_normal` — asserts Hard's upper range bound exceeds Normal's
- `test_easy_has_more_attempts_than_normal` — asserts Easy allows more attempts than Normal

## 📸 Demo

> **Note:** Run the app with `python -m streamlit run app.py`, then use the Developer Debug Info panel to verify the secret number stays stable across guesses and the hints correctly guide you toward it.

- [ ] [Insert a screenshot of your fixed, winning game here]

### 🧪 Pytest Results (Challenge 1: Advanced Edge-Case Testing)

> **Note:** Screenshot of passing pytest results — take a screenshot of your terminal after running `pytest tests/test_game_logic.py -v` and insert it below once `logic_utils.py` functions are implemented.

- [ ] [Insert pytest screenshot here]

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]
