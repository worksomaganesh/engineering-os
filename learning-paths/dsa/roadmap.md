# DSA Learning Roadmap

This roadmap assumes you are beginning to solve problems independently. It deliberately prioritizes order and repetition over covering every topic quickly.

**Default language:** choose one language you can comfortably write under time pressure. Python is concise for learning algorithmic ideas; C++ is common in competitive programming; Java is also widely used. You do not need to learn three languages at once. If your university coursework emphasizes C, use it to strengthen programming fundamentals, but choose one main practice language for consistency.

## How to use the roadmap

- Move forward when you can solve and explain the stage's core problems, not merely after watching the videos.
- A stage may take several days or several weeks. Do not treat the schedule as a deadline.
- Learn one idea, then solve a small set of problems using it.
- Re-solve problems after a delay. Pattern recognition grows through retrieval and transfer.
- Keep advanced topics such as segment trees and advanced graph algorithms for later.

## Stage 0 — Programming comfort

**Goal:** translate a simple idea into correct code.

Learn:
- variables, types, operators;
- conditions and loops;
- functions and return values;
- arrays/lists and strings;
- indexing and slicing where relevant;
- input/output;
- basic debugging and tracing;
- writing and calling helper functions.

Practice tasks:
- sum/minimum/maximum of a list;
- count even numbers;
- reverse a string;
- count character frequencies;
- check whether a string is a palindrome;
- find the second-largest distinct value, carefully handling duplicates.

Exit check: you can trace a loop by hand and explain the value of each variable after every iteration.

## Stage 1 — Understand complexity and arrays/strings

Learn:
- input size n;
- O(1), O(log n), O(n), O(n log n), O(n²);
- time versus auxiliary space;
- array traversal, mutation, copying, and indexing;
- string traversal and frequency counting;
- nested loops and why they create quadratic work.

Practice:
- linear search;
- reverse an array in place;
- move zeroes;
- remove duplicates from sorted array;
- merge two sorted arrays;
- check palindrome;
- find maximum frequency.

Exit check: estimate the complexity of your own code and identify whether a list copy consumes extra memory.

## Stage 2 — Hashing, sets, and frequency maps

Learn:
- hash map/dictionary and hash set;
- membership and frequency counting;
- expected O(1) operations and their assumptions;
- collisions at a conceptual level;
- why a hash table trades memory for lookup speed.

Patterns/problems:
- Two Sum;
- Contains Duplicate;
- Valid Anagram;
- first unique character;
- intersection of arrays;
- group anagrams after learning a suitable key.

Ask: what information do I keep so I do not need to search earlier elements again?

Exit check: you can explain when hashing improves a brute-force solution and what memory it costs.

## Stage 3 — Two pointers

Learn:
- pointers as indices, not memory pointers necessarily;
- inward-moving pointers;
- same-direction slow/fast pointers;
- sorted input and monotonic movement;
- invariants and pointer update decisions.

Practice:
- reverse string/array;
- palindrome validation;
- pair sum in sorted array;
- remove duplicates from sorted array;
- move zeroes;
- merge sorted arrays;
- container/area problems after understanding the pointer proof.

Exit check: for every pointer movement, explain why the discarded positions cannot contain a better/valid answer.

## Stage 4 — Sliding window and prefix sums

Learn:
- contiguous subarray versus subsequence;
- fixed-size windows;
- variable-size windows;
- when a window can be safely shrunk or expanded;
- prefix sums and range-sum formulas;
- why negative numbers can invalidate some sliding-window assumptions.

Practice:
- maximum sum of a fixed-size subarray;
- average of every k-length window;
- longest substring without repeating characters;
- minimum-size subarray sum when positivity assumptions hold;
- range sum queries using prefix sums;
- subarray-sum-equals-k using prefix sums plus hashing.

Exit check: explain why the window technique works for a given problem, and explicitly identify its assumptions. Do not assume every contiguous-subarray problem is a sliding window.

## Stage 5 — Sorting and binary search

Learn:
- sorting as a tool to expose order;
- comparison sorts conceptually;
- stable versus unstable sorting at a basic level;
- binary search on sorted arrays;
- search boundaries and loop invariants;
- lower bound / first true position;
- binary search on an answer when feasibility is monotonic.

Practice:
- binary search;
- first/last occurrence;
- search insertion position;
- first bad version / first true condition;
- square root by binary search;
- capacity/minimum feasible value problems after the basics.

Exit check: explain why the remaining search interval still contains the answer, and why binary search is invalid if the required ordering/monotonicity does not exist.

## Stage 6 — Stacks, queues, and linked lists

Learn:
- LIFO stack and FIFO queue;
- stack-based matching;
- monotonic stack as a maintained order;
- queue and BFS intuition;
- linked-list nodes and pointer updates;
- fast/slow pointers.

Practice:
- Valid Parentheses;
- implement stack/queue basics;
- reverse linked list;
- detect cycle in linked list;
- merge two sorted linked lists;
- next greater element;
- daily temperatures after understanding monotonic-stack logic.

Exit check: identify what a stack or queue remembers and why the most recent or earliest item must be processed next.

## Stage 7 — Recursion and backtracking

Learn:
- base case;
- recursive state;
- progress toward termination;
- call stack;
- choose → explore → undo;
- pruning branches that cannot succeed;
- output-size limits.

Practice:
- factorial and recursive sum for intuition;
- generate subsets;
- generate permutations;
- combination sum;
- word search;
- N-Queens later as a deeper exercise.

Exit check: state the meaning of each recursive call and why every path terminates.

## Stage 8 — Trees and heaps

Learn:
- tree terminology;
- binary trees and BSTs;
- preorder, inorder, postorder;
- level-order traversal;
- recursion versus iterative traversal;
- min-heap/max-heap;
- priority queues and top-k problems.

Practice:
- maximum depth;
- same tree;
- invert tree;
- level-order traversal;
- validate BST;
- lowest common ancestor after basic tree reasoning;
- kth largest / top k frequent elements.

Exit check: explain what information a recursive function returns to its parent and why a heap is useful when repeatedly needing the current minimum/maximum.

## Stage 9 — Graphs

Learn:
- vertices, edges, directed/undirected, weighted/unweighted;
- adjacency list and matrix;
- visited sets;
- BFS and DFS;
- connected components;
- cycle detection;
- topological ordering for directed acyclic graphs;
- shortest-path distinctions.

Practice:
- number of islands;
- flood fill;
- connected components;
- clone graph;
- course schedule / cycle detection;
- unweighted shortest path with BFS;
- Dijkstra for suitable non-negative edge weights;
- union-find for connectivity problems.

Exit check: choose BFS or DFS based on the question, correctly track visited state, and explain why a traversal does not revisit forever.

## Stage 10 — Greedy algorithms

Learn:
- making a locally best choice;
- why a local choice needs proof;
- sorting by a useful criterion;
- exchange arguments and counterexamples;
- when greedy fails and DP may be needed.

Practice:
- interval scheduling / maximum non-overlapping intervals;
- merge intervals (sorting + sweep);
- assign cookies / resource matching;
- jump-game style reachability;
- minimum number of meeting rooms as a heap/sweep problem.

Exit check: do not write “greedy works because it is optimal.” Explain why the choice can be part of an optimal solution, or find a counterexample.

## Stage 11 — Dynamic programming (DP)

Learn in this order:
1. Define the state in words.
2. Write the recurrence.
3. Identify base cases.
4. Choose memoization or tabulation.
5. Determine evaluation order.
6. Analyze state count × work per state.
7. Optimize memory only after the recurrence is correct.

Start with:
- Fibonacci as a demonstration of repeated subproblems, not as the entire topic;
- climbing stairs;
- house robber;
- coin change;
- grid paths;
- longest common subsequence;
- longest increasing subsequence;
- knapsack variants.

Ask:
- What does dp[i] mean?
- What smaller states determine it?
- Why are all dependencies available before computing this state?
- Can the same state be reached from different paths?

Exit check: explain the state and recurrence without memorizing code. DP is not “recursion with an array”; it is a model of states and dependencies.

## Stage 12 — Bit manipulation, math, and advanced structures

Learn when relevant:
- binary representation, masks, AND/OR/XOR;
- modular arithmetic and gcd;
- combinatorics basics;
- trie for prefix lookup;
- union-find;
- Fenwick tree / segment tree for range queries;
- advanced string algorithms such as KMP;
- advanced graph algorithms and shortest paths.

Do not start here. These topics become easier after the earlier stages.

## Stage 13 — Interview and contest practice

Once the fundamentals are reasonably stable:
- mix patterns instead of always knowing the topic in advance;
- practise explaining aloud;
- solve timed sets occasionally;
- review problems that took too long;
- learn to write readable code quickly;
- add company-specific preparation only when you have a target and current role-specific information.

Use LeetCode or another problem platform for problem statements and submissions. Use TheAlgorithms to inspect algorithm implementations and tests. They serve different purposes.

## Example 16-week outline

This is a sample, not a promise. Stretch it as needed.

| Weeks | Focus |
|---|---|
| 1–2 | Programming comfort, complexity, arrays, strings |
| 3 | Hashing |
| 4 | Two pointers |
| 5 | Sliding window and prefix sums |
| 6 | Sorting and binary search |
| 7 | Stacks, queues, linked lists |
| 8 | Recursion and backtracking basics |
| 9 | Trees and heaps |
| 10–11 | Graphs and traversals |
| 12 | Greedy |
| 13–14 | Dynamic programming foundations |
| 15 | Mixed revision and weak areas |
| 16 | Timed practice, explanation, and mock interviews |

If you can only study a few hours each week, use a longer timeline. Deep understanding is more valuable than finishing the table quickly.

## A weekly rhythm

- 2 sessions: learn one pattern and solve 1–2 problems.
- 1 session: solve another problem without seeing the topic label.
- 1 session: revisit mistakes and re-solve old problems.
- Optional: one contest or timed session after basic confidence develops.

## What counts as mastery?

For a topic, aim to solve:
- a simple direct application;
- a variant with a small twist;
- a problem where you must recognize the pattern yourself;
- a previously solved problem after a delay.

Then move on while continuing spaced review. You do not need to solve every problem in a topic before learning the next one.
