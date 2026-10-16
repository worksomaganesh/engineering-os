# How to Think Through a DSA Problem

This is the most important document in the DSA path. Algorithms become much easier to learn when you have a process for deciding what to do next.

## 1. What does “logic” mean in programming?

In problem solving, logic is not a mysterious talent. It is the process of making explicit statements about a problem and deriving steps that must produce the desired result.

For example, given a list of numbers and asked to find the largest:
1. The largest value seen so far is initially the first value.
2. Inspect each remaining value.
3. If the current value is larger than the best value seen so far, replace the best value.
4. After every element has been inspected, the stored value is the maximum.

The important idea is the **invariant**: after inspecting the first k values, the stored answer is the maximum among those k values. The algorithm is understandable because you can explain why each step preserves that statement.

You develop this ability by writing down assumptions, trying examples, explaining why each step is safe, and testing cases that could break it.

## 2. The 10-step method

Use this checklist on nearly every new problem. With experience, several steps become quick and mental, but do not skip them while learning.

### Step 1 — Read for meaning, not for a familiar keyword

Read the statement once without coding. Then explain it in your own words as if telling a classmate.

Ask:
- What am I given?
- What must I return or print?
- Is there one answer, a count, a boolean, a sequence, or an optimal value?
- Can input be empty? Can values be negative or repeated?
- Does order matter?
- Is the input sorted or does the statement promise any special property?

If you cannot explain the task in one or two sentences, reread it.

### Step 2 — Separate input, output, and constraints

Create a small specification:

| Item | Question |
|---|---|
| Input | What data arrives, and in what form? |
| Output | Exactly what format/result is required? |
| Constraints | How large can n be? What values are allowed? |
| Guarantees | Sorted? Unique? Connected? Valid input? |
| Edge cases | Empty, one item, duplicates, negative values, boundaries? |

Constraints are clues to the expected complexity. They are not a magical lookup table, but they help eliminate approaches that cannot finish in time.

### Step 3 — Solve a tiny example by hand

Choose a small example that is easy to inspect. Write down each step, not only the answer.

Then choose a second example that is different: duplicates, negatives, an already sorted list, or a boundary case. This often reveals a missing assumption.

### Step 4 — Try the most obvious solution

This is the **brute-force baseline**: a straightforward method that is easy to explain. It may be too slow; that is fine.

For each approach, state:
- the idea in plain language;
- why it should return the correct answer;
- time complexity;
- extra memory;
- what makes it too slow, if it is too slow.

A brute-force solution is not wasted work. It gives you a correctness baseline and reveals the repeated work that optimization may remove.

### Step 5 — Find the bottleneck

Ask what work is repeated:
- searching the same list repeatedly?
- comparing the same pair more than once?
- recalculating the same subproblem?
- recomputing a sum for each range?
- exploring a path that can no longer lead to a solution?
- sorting data when the required operation might support another approach?

Optimization usually begins with a specific bottleneck, not with guessing a fashionable pattern.

### Step 6 — Identify the structure of the problem

Look for properties:
- **Membership or frequency:** hash set/map.
- **Contiguous range:** sliding window or prefix sums.
- **Sorted order or monotonic condition:** binary search or two pointers.
- **Most recent unmatched item:** stack.
- **First item to finish/arrive:** queue or BFS.
- **Repeated choices with overlapping subproblems:** dynamic programming may fit.
- **Relationships and reachability:** graph traversal.
- **Many choices with constraints:** backtracking and pruning.
- **Intervals or resource allocation:** sorting plus greedy reasoning may fit.

These are clues, not guarantees. A problem can have multiple valid approaches. Verify the assumptions before committing.

### Step 7 — State the algorithm before coding

Write 3–8 steps in ordinary language or pseudocode. If the steps are unclear, code will usually make the confusion harder to see.

Example pseudocode for finding a pair that sums to target:
1. Create an empty set of previously seen values.
2. For each value x:
   - compute target − x;
   - if that complement is in the set, return the pair;
   - otherwise add x to the set.
3. If no pair is found, return the required “not found” result.

This describes a one-pass hash-set approach. Before coding, think about whether the current item is added before or after checking, because that affects duplicate and same-element behavior.

### Step 8 — Prove why it works

Use a short correctness argument:
- **Initialization:** is the claim true before the loop or recursion begins?
- **Maintenance:** does each step preserve the claim?
- **Termination:** when the algorithm stops, does the claim imply the required answer?

For a hash-based pair-sum method, before processing x, the set contains exactly the values from earlier elements. If target − x is present, it came from an earlier index, so a valid pair exists. If no complement is present, adding x makes it available for later elements. The algorithm checks each possible pair by its later element.

You do not need formal mathematical prose for every easy problem, but you should be able to explain the reasoning.

### Step 9 — Test deliberately

Do not test only the sample input. Try:
- the smallest valid input;
- all values equal;
- duplicates;
- negative and zero values;
- sorted and reverse-sorted data;
- no solution;
- a solution at the first or last position;
- maximum allowed input size;
- boundary values such as 0 or n−1.

For binary search, test target smaller than all values, larger than all values, absent between values, and duplicates if the problem allows them.

### Step 10 — Analyze, implement, and review

Analyze time and extra space, implement cleanly, run tests, then explain the solution without reading the code. After finishing, record the key insight and revisit it later.

## 3. Worked example: find the maximum

**Problem:** Return the largest number in a non-empty array.

Input: `[4, -2, 9, 3]`  
Expected output: `9`

### Manual reasoning
- Start with best = 4.
- Compare −2 with 4; keep 4.
- Compare 9 with 4; best becomes 9.
- Compare 3 with 9; keep 9.
- Return 9.

### Pseudocode
```text
best = first element
for each remaining value x:
    if x > best:
        best = x
return best
```

### Why it works
After processing any prefix, best is the maximum of that prefix. The next value either becomes the new maximum or does not; therefore the invariant remains true. At the end, the prefix is the whole array.

### Complexity
- Time: O(n), because every element is inspected once.
- Extra space: O(1), because only a fixed number of variables are used.

### Common wrong approach
Initialize best to 0. This fails for an array such as `[-8, -3, -12]`, because 0 is not an element and is greater than every input. Initialize from the first element when non-empty input is guaranteed, or explicitly handle empty input according to the problem statement.

## 4. Worked example: pair sum

**Problem:** Return whether two distinct elements sum to target.

Input: `nums = [8, 3, 5, 1], target = 6`  
Expected answer: true, because 5 + 1 = 6.

### Approach A: brute force
For each index i, inspect each later index j and check `nums[i] + nums[j] == target`.

- Time: O(n²) in the worst case.
- Extra space: O(1).
- Strength: simple and easy to validate.

### Approach B: hash set
For each x, check whether `target - x` has appeared earlier; if not, store x.

- Expected time: O(n) with ordinary hash-set assumptions.
- Extra space: O(n).
- Strength: avoids scanning all later elements for each x.

### Important implementation detail
Check before inserting the current x. Otherwise, if the target is twice x, the current element might incorrectly match itself when the problem requires two distinct indices. Whether that matters depends on the exact problem definition.

### What did we learn?
The pattern was not “use a set because the problem says pair.” We noticed that brute force repeatedly asks whether a complement exists among other elements. A set makes membership checks efficient.

## 5. Complexity without fear

Big O describes how resource use grows as input size grows; it is not a stopwatch reading.

Common growth rates, from generally more scalable to less scalable:

| Complexity | Typical example |
|---|---|
| O(1) | Array index access |
| O(log n) | Binary search on sorted data |
| O(n) | One pass through an array |
| O(n log n) | Efficient comparison sorting |
| O(n²) | Checking all pairs |
| O(2ⁿ) | Some exhaustive subset searches |
| O(n!) | Enumerating all permutations |

The exact behavior depends on the algorithm and assumptions. O(n²) can be fine for small n; O(n) can still be expensive if it performs costly operations. Consider memory as well as time.

### A rough constraint check
If n is around 100, an O(n²) approach may be reasonable. If n is around 100,000, 10¹⁰ pair operations are generally not practical. These are rough intuition aids, not universal judge limits; language, constant factors, time limits, and the actual operation matter.

## 6. How to get unstuck

If you have stared at a problem for 10–15 minutes with no direction, do not immediately read the complete answer. Ask yourself in this order:

1. Can I solve a tiny version by hand?
2. Can I write brute force, even if slow?
3. Which operation repeats?
4. What information would help me avoid repeating it?
5. Does sorting reveal structure?
6. Is there a useful invariant or monotonic property?
7. Can I solve a smaller subproblem?
8. Can I ask for a hint about the pattern without seeing the code?

A useful hint request is: “I can explain the brute-force approach, but it is O(n²). Please give one hint about what repeated work I should remove; do not reveal the full solution.”

## 7. Debugging is reasoning, not random edits

When output is wrong:
1. Find the smallest input that reproduces the failure.
2. Write the expected output and actual output.
3. Trace variable values after each loop iteration.
4. Check loop bounds, update order, and return conditions.
5. Compare the implementation with your pseudocode.
6. Check whether the algorithm's assumptions hold.
7. Add a regression test so the bug cannot silently return.

When time limit is exceeded, do not randomly micro-optimize. Revisit the complexity and identify the expensive operation.

## 8. How to use AI without losing the skill

Use AI in graduated levels:
- **Level 1:** Ask it to restate the problem and identify ambiguities.
- **Level 2:** Ask for a tiny hint, not a solution.
- **Level 3:** Share your brute-force plan and ask what repeated work it contains.
- **Level 4:** Ask it to critique your proof and edge cases.
- **Level 5:** After your attempt, compare your implementation to another solution.
- **Level 6:** Close the answer and reproduce the approach from memory.

Do not accept a confident answer without running tests and checking complexity. AI can produce plausible but incorrect algorithms, overlook constraints, or use the wrong interpretation of the problem.

## 9. A reusable template for every problem

Copy this into your notes:

```text
Problem:
Input / output:
Constraints and guarantees:
Tiny example:
Edge cases:
Brute-force idea:
Brute-force complexity:
Bottleneck:
Pattern candidate and why:
Optimized algorithm:
Correctness argument / invariant:
Time complexity:
Auxiliary space:
Tests I ran:
Mistake or key insight:
Could I solve it again without help?
Next review date:
```

## 10. Readiness checklist

Before calling a problem “learned,” ask:
- Can I explain it without the original editorial?
- Can I implement it again without copying?
- Can I explain why it is correct?
- Can I derive its complexity?
- Can I name the edge cases?
- Can I recognize when the pattern applies to a different story?
- Can I solve it again after a few days?

A submission accepted by an online judge is evidence of passing its tests, not proof that you deeply understand the idea. Aim for understanding and transfer.
