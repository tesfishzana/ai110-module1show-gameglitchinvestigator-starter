# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start
  (for example: "the secret number kept changing" or "the hints were backwards").
  -> The first bug was that the hints were completely backwards — when my guess was too high, the game told me to go higher, and when it was too low, it told me to go lower, making the game unwinnable by following the hints.
  -> The second bug was in the difficulty settings: Easy allowed fewer attempts than Normal, and the Hard difficulty had a smaller number range (1–50) than Normal (1–100), which meant Hard was actually easier than Normal in terms of range.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
  -> I used Claude Code as my AI assistant throughout the project.

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  -> Claude correctly identified three logic bugs in `app.py`: the swapped hint messages in `check_guess` (including the `TypeError` fallback path), the Hard difficulty range being too narrow, and the Easy attempt limit being lower than Normal. I verified each fix by reading the corrected code and manually tracing through the logic to confirm the behavior matched what was expected.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
  -> Claude sometimes provided more detail and explanation than necessary, making it harder to quickly identify the key fix. I had to filter through lengthy explanations to extract the actual code change needed. This taught me to ask more focused, targeted questions to get cleaner responses.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  -> I verified each fix in two ways: first by reading the corrected code and tracing through the logic manually to confirm it made sense, and second by running the app and testing the specific behavior that was broken — for example, submitting a guess that was too high and checking that the hint correctly said "Go LOWER."

- Describe at least one test you ran (manual or using pytest)
  and what it showed you about your code.
  -> I added 4 new pytest tests to `test_game_logic.py`, each targeting a specific bug. For example, `test_too_high_message_says_go_lower` calls `check_guess(60, 50)` and asserts that the message contains "LOWER." This test would have caught the original bug immediately, since the old code returned "Go HIGHER!" in that case.

- Did AI help you design or understand any tests? How?
  -> Yes. I asked Claude to write pytest cases specifically targeting each bug I had fixed. Claude structured each test to unpack both the outcome and the message from `check_guess`, which helped me understand that the existing tests were only checking the outcome label and completely missing the message — the exact place where the bug was hiding.

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
