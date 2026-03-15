# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start
  (for example: "the secret number kept changing" or "the hints were backwards").

When I first ran the game, it looked like a normal guessing game but it was impossible to win by following the hints. The first thing I noticed was that the hints were completely backwards — every time I guessed too high, the game told me to go higher, which sent me in the wrong direction every single time. The second bug I caught was in the difficulty settings: Easy was actually harder than Normal because it gave you fewer attempts (6 vs 8), and Hard had a smaller range (1–50) than Normal (1–100), which made Hard easier than Normal. These bugs made the whole difficulty system feel broken and confusing.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?

I used Claude Code as my AI assistant for this entire project — for reading code, fixing bugs, writing tests, and updating documentation.

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

Claude correctly spotted that the hint messages inside `check_guess()` were swapped. It suggested flipping the return values so that `guess > secret` returns "Go LOWER!" and `guess < secret` returns "Go HIGHER!" — and it caught that the same swap needed to happen in the `TypeError` fallback path too, which I would have easily missed. I verified this by tracing through the logic myself: if my guess is above the secret number, I obviously need to go lower. I then ran the app, typed a guess that I knew was above the secret using the debug panel, and confirmed the hint said "Go LOWER" as expected.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

When I asked Claude to refactor the functions into `logic_utils.py`, it left all four functions as `raise NotImplementedError(...)` stubs instead of actually implementing them. At first glance the file looked fine — the functions were there with the right names. But when I ran `pytest tests/test_game_logic.py -v`, every single test crashed with `NotImplementedError`. I had to go back and specifically tell Claude to implement the functions by moving the real logic from `app.py` into `logic_utils.py`. This taught me to always run the tests immediately after any AI-assisted refactor, not just look at the code.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

I used two checks for every fix. First I read the corrected code and traced through it manually to make sure the logic made sense to me before trusting it. Then I tested the actual behavior in the running app — for the hints bug I submitted guesses above and below the secret and watched whether the hint pointed me in the right direction. Seeing it work in the real app gave me much more confidence than just reading the code.

- Describe at least one test you ran (manual or using pytest)
  and what it showed you about your code.

I added 4 new pytest tests to `test_game_logic.py` that each targeted one specific bug. The most useful one was `test_too_high_message_says_go_lower`, which calls `check_guess(60, 50)` and asserts the message contains "LOWER". When I looked at the original tests, none of them checked the message at all — they only checked the outcome label like "Too High". That gap is exactly where the bug was hiding, so the new test would have caught it immediately if it had existed before.

- Did AI help you design or understand any tests? How?

Yes — I asked Claude to write pytest cases specifically targeting each bug I fixed. The most useful thing Claude did was show me to unpack the tuple as `outcome, message = check_guess(...)` instead of comparing the whole return value to a string, which is what the original tests were doing wrong. That one change helped me understand why all the original tests were passing even when the hints were broken — they never checked the message half of the tuple at all.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
  -> In the original app, `random.randint()` was called every time the script ran without any guard. Since Streamlit re-runs the entire script on every user interaction (like clicking a button or typing), a new secret number was generated on each interaction, making it impossible to guess the same number twice.

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
  -> Imagine every time you click a button on a website, the entire page reloads from scratch. That's what Streamlit does — it reruns your whole Python script top to bottom on every interaction. Session state is like a small notepad that survives those reloads. Anything you store in `st.session_state` stays there between reruns, so the app can remember things like the secret number, your score, and how many attempts you've made.

- What change did you make that finally gave the game a stable secret number?
  -> The fix was wrapping the `random.randint()` call with a guard: `if "secret" not in st.session_state`. This means the secret number is only generated once — the very first time the app loads. On every rerun after that, the condition is False so the existing secret is kept, giving the game a stable target to guess.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  -> Writing pytest cases that specifically target each bug before and after fixing it. This gave me confidence that the fix actually worked and made it clear exactly what the broken behavior was. I will use this test-per-bug habit in future projects to keep bugs from quietly coming back.

- What is one thing you would do differently next time you work with AI on a coding task?
  -> I would ask the AI to explain the bug first before asking it to fix it. This time I let the AI jump straight to fixes, and sometimes the explanation came after. Understanding the root cause before seeing the solution would help me learn more deeply and catch cases where the AI's fix is wrong.

- In one or two sentences, describe how this project changed the way you think about AI generated code.
  -> This project showed me that AI-generated code can look completely correct on the surface but contain subtle logic bugs that only show up when you actually run or test it. I now treat AI output as a first draft that always needs to be read, tested, and verified — not trusted blindly.
