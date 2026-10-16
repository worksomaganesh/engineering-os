# DSA Pattern Field Guide

A pattern is a reusable way to organize reasoning. It is not a keyword-to-template lookup. A problem's constraints, required output, and structural properties determine whether a pattern is valid.

## Quick pattern selector

| If you notice… | Consider… | Verify first |
|---|---|---|
| Need fast membership or counts | Hash set / map | Is extra memory acceptable? |
| Pair search in sorted data | Two pointers | Does pointer movement safely eliminate candidates? |
| Contiguous range, fixed length | Fixed sliding window | Is the range length fixed? |
| Contiguous range with a valid shrink/expand rule | Variable sliding window | Do the constraints make validity monotonic as the window changes? |
| Many range-sum queries | Prefix sums | Are updates absent or can the structure handle them? |
| Sorted data or monotonic true/false condition | Binary search | What exactly is monotonic? |
| Matching brackets / recent unresolved item | Stack | What must be resolved in reverse order? |
| Next greater/smaller element | Monotonic stack | Which candidates become permanently irrelevant? |
| Repeatedly need min/max among candidates | Heap / priority queue | Is the candidate set changing over time? |
| Level-by-level shortest path in unweighted graph | BFS | Are edges effectively equal cost? |
| Explore connectivity or components | DFS/BFS / Union-Find | Are edges directed, and do queries include updates? |
| Enumerate combinations or arrangements | Backtracking | Can invalid branches be pruned? |
| Overlapping subproblems + state recurrence | Dynamic programming | What does each state mean? |
| Choices ordered by an optimization criterion | Greedy | Can you prove the local choice is safe? |
| Prefix lookup across many strings | Trie | Is memory use justified? |
| Repeated range queries with updates | Fenwick/segment tree | What operations and complexity are required? |

## 1. Brute force first

**Signal:** you can describe the simplest way to enumerate possible answers.

**Method:** enumerate candidates, test each, keep the valid/best result.

**Why learn it:** it gives a correctness baseline and exposes expensive repeated work.

**Trap:** stopping at “it is O(n²)” without knowing what causes the quadratic work. Identify the inner operation and ask whether it can be reused or indexed.

## 2. Hashing: remember what you have seen

**Signal:** repeated questions such as “have I seen this?”, “how many times does this occur?”, or “which item has this key?”

Use:
- set for membership/uniqueness;
- map/dictionary for value-to-information mapping;
- frequency map for counts.

Typical examples:
- duplicate detection;
- two-sum complement lookup;
- anagram signatures;
- counting frequencies.

**Why it helps:** avoids repeated linear scans in many cases, usually trading O(n) additional memory for expected faster lookup.

**Traps:**
- relying on hash-map operations being worst-case O(1) in every implementation;
- forgetting duplicate values;
- updating the map in the wrong order;
- assuming hash-map iteration order when the language/API does not promise what you need.

## 3. Two pointers

### Inward pointers
Start at opposite ends and move inward.

Useful for:
- checking a palindrome;
- pair sum in a sorted array;
- comparing or partitioning from both ends.

**Reasoning question:** if the current pair is too small or too large, why is moving one particular pointer safe? The sorted order supplies the proof.

### Same-direction pointers
Use a read pointer and a write/slow pointer.

Useful for:
- removing duplicates in place;
- moving zeroes;
- partitioning or compacting data.

**Invariant:** the prefix before the write pointer contains the valid processed output.

**Trap:** two pointers are not automatically valid for an unsorted pair-sum problem. Sorting may help, but it can change index relationships and may cost O(n log n).

## 4. Sliding window

A window is a contiguous range, often represented by left and right indices.

### Fixed-size window
When every candidate range has exactly k elements:
- compute the first window;
- add the entering element;
- remove the leaving element;
- update the answer.

This changes repeated O(k) summation per window into O(n) total work.

### Variable-size window
Expand the right side, then move the left side when a condition is violated or a smaller valid window is desired.

Works when the problem's validity condition supports that movement strategy. For example, positive-number sum constraints often have monotonic behavior as a window expands or shrinks.

**Critical trap:** a classic variable sliding window for sum constraints may fail with negative numbers because extending a window can decrease its sum. Consider prefix sums plus hashing or other methods instead.

## 5. Prefix sums

Define a prefix array where each position stores the sum before or through that position. With a consistent convention, a range sum is the difference of two prefix values.

For example, if P[k] is the sum of the first k elements (P[0] = 0), then the sum from index l through r inclusive is:

`P[r + 1] - P[l]`

Useful for:
- many static range-sum queries;
- subarray sum problems;
- combining with a hash map to count prefix sums.

**Trap:** prefix sums make range queries fast, but they do not automatically make arbitrary point updates cheap. Choose a suitable data structure if updates are frequent.

## 6. Binary search

**Signal:** sorted order or a monotonic predicate lets you eliminate half the remaining candidates.

Two common forms:
- search for a target in a sorted array;
- search for the first value/answer where a predicate becomes true.

Define precisely:
- search interval;
- meaning of each boundary;
- invariant;
- condition that moves left or right;
- termination condition.

**Binary search on answer:** suppose a candidate capacity x is feasible, and all larger capacities are also feasible. You can search for the smallest feasible x—but only after proving feasibility is monotonic and defining a correct feasibility check.

**Traps:** off-by-one errors, infinite loops, incorrect midpoint/boundary updates, and applying binary search to a condition that is not monotonic.

## 7. Stack and monotonic stack

A stack is last-in, first-out. Use it when the latest unresolved item should be processed first.

Examples:
- matching brackets;
- expression parsing;
- undo-like behavior;
- maintaining candidates for next-greater-element problems.

A monotonic stack maintains increasing or decreasing order. When a new element makes older candidates irrelevant, pop them.

**Reasoning question:** what fact about the current element means a popped candidate can never be the answer for future elements?

**Trap:** choosing the wrong strict/non-strict comparison can mishandle duplicates. Decide how equal values should behave before coding.

## 8. Queue, BFS, and DFS

A queue processes first-in, first-out. BFS explores a graph by distance layers and finds shortest paths in unweighted graphs (or graphs where every edge has equal cost).

DFS explores deeply before backtracking; it is useful for reachability, components, traversal, and many structural questions.

Represent graphs commonly with adjacency lists when they are sparse.

**Traps:**
- mark nodes visited at the right time to avoid repeated enqueues;
- account for disconnected components;
- distinguish directed from undirected edges;
- do not use ordinary BFS for arbitrary weighted shortest paths.

## 9. Heap / priority queue

A heap efficiently exposes the current minimum or maximum. It is useful when candidates are repeatedly added and removed.

Examples:
- top-k items;
- merging sorted lists;
- scheduling by earliest finish time;
- Dijkstra's algorithm with non-negative weights;
- maintaining a running set of best candidates.

**Trap:** a heap is not a fully sorted array. It guarantees an extremum at the root, not sorted iteration of all elements.

## 10. Recursion and backtracking

Backtracking systematically explores choices:
1. choose;
2. recurse/explore;
3. undo the choice;
4. try the next option.

Useful for subsets, permutations, combinations, constraint satisfaction, and search over possible arrangements.

Before coding, define:
- state;
- choices available at this state;
- valid/invalid state;
- stopping condition;
- how the state is restored.

**Pruning:** stop exploring a branch once it cannot produce a valid answer. Pruning must be logically safe.

**Trap:** forgetting to undo mutable state, using a base case that stops too early, or assuming recursion is efficient simply because the code is short. Search spaces can grow exponentially.

## 11. Dynamic programming

DP is appropriate when a problem can be described through states that recur and share subproblems, often with an optimal substructure.

A disciplined DP process:
1. Define state in a complete sentence.
2. Write the recurrence from smaller states.
3. Define base cases.
4. Choose memoization or tabulation.
5. Ensure dependencies are computed first.
6. Count states and work per state.
7. Optimize memory only when the basic recurrence is correct.

Example: if dp[i] means “the maximum amount collectible from the first i houses under the no-adjacent-house rule,” then the last house is either skipped or taken, which leads to a recurrence based on earlier states. Write and verify the exact indexing before coding.

**Traps:** a vague state definition, missing base cases, incorrect iteration order, or optimizing the recurrence before understanding it.

## 12. Greedy

Greedy makes a choice that seems best now and does not reconsider it.

Examples can include interval scheduling, selecting compatible activities, or certain resource allocation problems.

But a plausible local choice is not enough. Justify it using:
- an exchange argument;
- a cut/property argument where appropriate;
- a proof that some optimal solution can include the choice;
- or a counterexample if the choice is unsafe.

**Trap:** assuming that a locally best choice always produces a globally optimal solution. Many problems that look greedy require DP or another method.

## 13. Union-Find (Disjoint Set Union)

Maintains a partition of elements into disjoint connected groups. The main operations are find-representative and union-groups; path compression and union by size/rank make operations very efficient in practice and amortized analysis.

Useful for:
- dynamic connectivity under edge additions;
- detecting cycles in certain undirected graph settings;
- Kruskal's minimum spanning tree algorithm.

**Trap:** standard DSU does not directly handle arbitrary edge deletions and does not replace BFS/DFS for every graph question.

## 14. Trie

A tree-like structure stores shared prefixes of strings.

Useful for:
- prefix search;
- autocomplete;
- word dictionaries;
- some bitwise-XOR problems.

**Trade-off:** fast prefix operations can require substantial memory, especially with large alphabets or many nodes.

## 15. Divide and conquer

Split a problem into smaller subproblems, solve them, and combine their results.

Examples:
- merge sort;
- binary search;
- many tree algorithms.

Ask:
- How is the problem split?
- Does each part get smaller?
- How are the results combined?
- What is the recurrence for the work?

## 16. How to choose between patterns

Do not ask only, “Which pattern does this problem belong to?” Ask:
1. What does a brute-force solution do?
2. What work repeats?
3. What property is guaranteed?
4. What information would make the next step cheaper?
5. Which approach preserves correctness?
6. What are the time and space costs?
7. What counterexample could break my assumption?

A pattern is learned when you can recognize it without the topic label and explain why it applies.

## Reference implementation study

After solving or making a serious attempt:
- locate the matching family in TheAlgorithms;
- compare the implementation's assumptions with the problem statement;
- read its tests;
- write down differences between the textbook algorithm and the implementation;
- close the source and reproduce the key idea from memory.

See [Using TheAlgorithms](using-thealgorithms.md).
