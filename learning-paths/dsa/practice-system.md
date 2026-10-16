# DSA Practice and Review System

The goal is to build independent problem-solving ability, not maximize the number of accepted submissions.

## 1. Choose a problem at the right level

A useful practice sequence is:
1. **Learned pattern, direct application:** identify and use the pattern.
2. **Same pattern with a twist:** change the constraints or output.
3. **Mixed problem:** the topic label is hidden, so you must recognize the approach.
4. **Timed revisit:** solve an old problem after a delay.

If every problem is completely impossible, simplify the difficulty or review the prerequisite. If every problem is immediate, move to a variant rather than repeating only easy examples.

## 2. A hint ladder

When stuck, use the smallest amount of help that unlocks your next step.

- **Hint 0:** re-read and create a tiny example.
- **Hint 1:** ask for clarification of the statement or constraints.
- **Hint 2:** request a nudge about the repeated work.
- **Hint 3:** ask which family of technique may fit, without code.
- **Hint 4:** request pseudocode after making your own attempt.
- **Hint 5:** inspect a full solution only after recording your approach and where it failed.

After seeing a solution:
1. Close it.
2. Explain the idea from memory.
3. Implement without copying.
4. Create an edge case that might break it.
5. Re-solve it later.

If you look at a solution immediately and then mark the problem as solved, your progress data becomes misleading.

## 3. Spaced review

A simple review schedule is:
- same day: explain the insight in your own words;
- next day: solve or outline it again;
- 3–7 days later: solve without looking;
- 2–4 weeks later: solve it as part of mixed practice.

Adjust based on difficulty. A problem you can reproduce easily needs less review than one whose key insight you keep forgetting.

## 4. Track the quality of a solve

Use these states:
- **Independent:** solved without hints.
- **Hinted:** solved after a small hint.
- **Editorial-assisted:** understood after seeing the solution.
- **Reproduced:** solved later without help.
- **Transfer-tested:** recognized the pattern in a differently worded problem.

“Accepted” and “understood” are not synonyms.

## 5. A problem journal template

```text
Date:
Platform / problem:
Topic (after solving):
Difficulty:
My first interpretation:
Brute force:
Where I got stuck:
Hint level used:
Final approach:
Why it is correct:
Time / auxiliary space:
Edge cases:
Mistake type:
  [ ] misunderstood statement
  [ ] missed edge case
  [ ] wrong pattern
  [ ] incorrect proof
  [ ] implementation bug
  [ ] complexity too high
  [ ] language/API issue
Re-solve date:
Re-solve result:
Transfer problem:
```

## 6. Weekly review

At the end of each week:
- list the patterns studied;
- re-solve 2–4 older problems;
- select one problem whose topic is hidden;
- explain one solution aloud;
- identify the most common mistake;
- choose one small adjustment for next week.

Do not judge the week only by raw problem count. A week with fewer problems but better independent reproduction can be a stronger week.

## 7. A reasonable beginner target

A sustainable first goal is roughly 4–6 focused study sessions per week, even if some are short. Start with one carefully understood problem per session; some sessions may cover two simple problems, while a difficult problem may take several sessions. This is guidance, not a mandatory quota.

Build a habit that survives exams, projects, and busy weeks. Do not sacrifice sleep or core coursework to maintain a streak.

## 8. Platform strategy

You do not need to solve on every platform simultaneously.

- **LeetCode:** broad interview-style practice and curated topic lists.
- **HackerRank:** structured practice and language/problem-solving exercises.
- **CodeChef / Codeforces:** contests and competitive programming; useful after fundamentals, with a different time-pressure and rating ecosystem.
- **Smart Interviews:** follow its curriculum and assessment style if it matches your goals or college preparation.
- **TheAlgorithms:** reference implementations and tests, not primarily a graded problem bank.

Choose one main problem platform and one reference source first. Add another platform when you have a clear reason.

## 9. Use GitHub meaningfully

If you maintain a public DSA repository:
- organize by topic or problem ID;
- include a short explanation, complexity, and test cases where useful;
- avoid uploading copied editorials or content that violates platform rules;
- keep commits understandable;
- do not create hundreds of empty files just to appear active;
- use the repository as a learning record, not a substitute for understanding.

A short note explaining a mistake and later correction can be more useful than a code dump.

## 10. AI prompts that preserve learning

**Problem restatement**
> Restate this problem in simple language. Identify inputs, output, constraints, and ambiguities. Do not give me an algorithm yet.

**Brute-force critique**
> Here is my brute-force approach: [paste]. Check whether it is correct and derive its time and space complexity. Do not reveal an optimized solution yet.

**One-hint tutor**
> I am stuck at [specific point]. Give me one conceptual hint about the repeated work or property I should examine. Do not provide code or the full algorithm.

**Proof checker**
> Here is my algorithm and why I think it works: [paste]. Try to find a counterexample. If none is obvious, identify the invariant and any assumptions I have not justified.

**Test designer**
> Create edge and adversarial tests for this implementation. Do not rewrite the solution. Explain what bug each test is intended to catch.

**Post-solve review**
> Compare my solution to this alternative. Explain differences in correctness, complexity, memory, readability, and assumptions. Point out what I should learn, not just which one is shorter.

## 11. Monthly checkpoint

At the end of each month, try a small mixed set without topic labels. Review:
- How often did you need hints?
- Which mistakes recur?
- Can you derive complexity without looking it up?
- Can you explain code to another person?
- Which patterns transfer to unfamiliar wording?
- Are you spending too much time watching explanations and too little time attempting?

Use the answers to adjust your plan.
