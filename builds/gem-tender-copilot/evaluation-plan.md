# GeM Tender Copilot — Evaluation and Testing Plan

A tender assistant is useful only if its extraction and comparisons are dependable enough for a user to review. A fluent report is not evidence of correctness. Evaluate the pipeline against an adjudicated dataset before describing the tool as reliable or using it with high-stakes bids.

## 1. Evaluation Goals

1. Detect the material requirements in a tender, including clauses buried in annexures, tables, footnotes, and amendments.
2. Preserve the correct source page, clause, quote, units, and conditions.
3. Extract factual fields without inventing values.
4. Link the correct seller evidence to each requirement.
5. Compare thresholds correctly when enough facts are available.
6. Treat missing/ambiguous evidence as unknown rather than false certainty.
7. Detect material changes between tender versions.
8. Make failure modes visible and reproducible.

## 2. Build a Reference Dataset

### Suggested first benchmark

Start with a modest, carefully labelled corpus—perhaps **30–50 tender packs for an initial development benchmark**, with a separate holdout set never used to tweak prompts. This number is a planning suggestion, not a claim that it is statistically sufficient or proves production reliability.

Try to include:
- Text-native PDFs and image/scanned PDFs.
- Different document lengths and page layouts.
- Single-column and multi-column pages.
- Tables, merged cells, footnotes, headers, and annexures.
- Similar-looking financial years and numeric thresholds.
- Multiple date formats and time zones.
- Documents containing OCR noise or rotated pages.
- Main tender documents plus one or more corrigenda.
- Conflicting clauses, exceptions, alternative qualifications, and conditional requirements.
- Various tender types only after the first supported category has been selected.

Use public documents only under permitted access and reuse conditions, and remove unnecessary personal or confidential information. Use synthetic documents for deliberate edge cases. Do not publish a training/evaluation set containing seller private documents without explicit permission and a valid data-handling basis.

### Annotation method

For each document version, annotators should record:
- Every material requirement and its complete relevant clause context.
- Category and requirement type.
- Mandatory/conditional status and exceptions.
- Threshold, unit, currency, period, count, and comparator where applicable.
- Source quote and page/section reference.
- Required evidence class.
- Deadline and raw date text.
- Severity, with reasons.
- What evidence would satisfy the condition.
- Whether interpreting the clause requires expert judgment.

Use two independent reviewers for at least the high-risk portion of the benchmark, then adjudicate disagreements. A procurement-experienced reviewer should approve the reference labels; an engineer alone should not decide ambiguous legal/procurement interpretations.

## 3. Metrics That Matter

| Metric | What it measures | Why it matters |
|---|---|---|
| Requirement precision | Of extracted requirements, what fraction are genuine requirements? | Avoid cluttering the report with invented or irrelevant checklist items |
| Requirement recall | Of reference requirements, what fraction did the system find? | Missing a mandatory clause may be more harmful than including an extra review item |
| Critical-requirement recall | Recall for critical disqualification/eligibility conditions | Measures whether the most important clauses are found |
| Field exact-match accuracy | Correct values, dates, units, periods, and comparators | Prevents bad numeric/date comparisons |
| Page citation accuracy | Whether the cited page is correct | Lets users verify the source rapidly |
| Quote grounding rate | Whether the displayed source quote is actually in that document version | Detects fabricated citations or paraphrases presented as quotations |
| Evidence-link precision/recall | Whether linked files support the requirement and whether relevant supplied files are found | A present document is not necessarily acceptable proof |
| Status accuracy | Agreement between output statuses and expert-adjudicated states | Tests the decision-support layer |
| Critical false-supported rate | Critical requirements labelled supported when the reference says failed, unknown, or unresolved | An especially serious failure mode |
| Corrigendum change recall | Material changed clauses/deadlines found between versions | Protects against stale checklists |
| OCR quality routing | Correctly flagged poor/unreadable pages | Prevents low-quality text silently feeding later analysis |
| Review time saved | Human review time with and without the tool | Tests whether the product reduces work in practice |
| Cost per reviewed tender | Processing spend and infrastructure cost for a given document profile | Helps validate the economics of an MVP |
| Completion / failure rate | How often an uploaded pack yields a usable report versus a visible failure | Measures operational reliability |

Report metrics by document class, not only as a single average. A strong average can hide poor performance on scanned annexures or complex tables.

## 4. Provisional Release Gates

These are starting targets to test and revise—not existing measured results and not guarantees:

- **Source grounding:** every material displayed requirement must have a valid document-version reference and page; no unsupported synthetic quote.
- **Critical requirement recall:** set a high gate, initially aim for at least 95% on a curated, held-out test corpus, and investigate every miss. Even this does not make the tool safe enough to act without human review.
- **Critical false-supported rate:** target zero critical false-supported results in the release benchmark. Any failure blocks release until investigated, fixed, and regression-tested; zero in a small dataset is not proof of zero real-world risk.
- **Page reference accuracy:** aim for at least 98% on the curated benchmark, with all known incorrect citations treated as defects.
- **Corrigendum coverage:** test deadline and threshold changes separately; manually verify every high-impact change in the pilot.
- **Traceability:** every final status should be reproducible from stored rule inputs, evidence links, and the analysis/rule-set version.
- **Security:** all authorization, tenant-isolation, upload-safety, secret-handling, and deletion tests pass before real seller data is used.

The numbers above are internal quality gates to validate, not product marketing claims. A procurement professional should review the acceptable residual risk for the target customer.

## 5. Test the Entire Pipeline Separately

### A. File and upload tests
- Valid small PDF.
- Very large PDF and excessive page count.
- Incorrect extension or spoofed content type.
- Corrupt, encrypted, empty, or unsupported file.
- Password-protected file with clear user experience.
- Same file uploaded more than once.
- Upload interrupted or repeated.
- Unauthorized user attempts access to another workspace's file.

### B. Extraction tests
- Digital PDF with text.
- Scanned PDF with clean text.
- Low-resolution, skewed, rotated, and noisy pages.
- Two-column layout.
- Header/footer that repeats every page.
- Tables with merged cells and units in column headings.
- Multi-page tables and footnotes.
- Clause references that continue across pages.
- An annexure containing a required declaration or prescribed form.
- Amounts expressed in rupees, lakh, crore, percentages, or ranges.
- Dates such as DD/MM/YYYY and ambiguous date formats.

### C. Requirement-interpretation tests
- "At least" versus "more than".
- Annual turnover versus average annual turnover.
- Number of completed projects versus number of purchase orders.
- Completed vs ongoing work.
- Experience period based on financial years or a fixed cut-off.
- Conditional applicability ("where applicable", "if the bidder is a manufacturer").
- Alternative ways to satisfy a requirement.
- Exceptions or relaxations elsewhere in the tender.
- Repeated clauses with different contexts.
- Same term used with different units.
- Tender-specific definition of "similar work".
- Contradictory language that needs expert review.

### D. Evidence-matching tests
- Right certificate, correct legal entity, valid dates.
- Certificate for a parent company rather than the bidding entity.
- Expired certificate.
- Incomplete financial-year coverage.
- Project completion proof with no value shown.
- Purchase order with no proof of completion.
- Technical datasheet that gives a near match but not exact compliance.
- Similar project title but different scope.
- Evidence document present but unreadable.
- Company did not upload a document, which must mean "not supplied to this workspace", not "does not exist".

### E. Corrigendum tests
- Bid deadline moved earlier and later.
- Qualification threshold raised or lowered.
- New mandatory certificate added.
- A clause deleted.
- Technical parameter changed.
- Amendment references a separate annexure not uploaded.
- The user uploads an older version after a newer one.
- Published date and document date differ.
- The comparison model misses a change; system must preserve both versions and request review.

### F. AI/prompt-injection tests
Treat tender files as untrusted data. Test documents containing text like "ignore previous instructions", fake system prompts, embedded links, or attempts to convince the model to declare the seller eligible. The model must extract tender information, not follow instructions embedded in the document. No model output should trigger submission, financial transactions, or privileged operations.

## 6. Human-in-the-Loop Review

A reviewer should be able to inspect:
- The exact tender page and clause.
- Original and OCR-rendered page when available.
- The extracted requirement and confidence.
- The evidence document and source page.
- The rule inputs and calculation.
- The reason for the assigned status.
- Which assumptions are not verified.

Reviewers should label errors by type:
- Missed requirement.
- Incorrect requirement classification.
- Wrong numeric/date extraction.
- Wrong page/quote.
- Missing relevant evidence.
- Incorrect semantic match.
- Incorrect rule/status.
- Corrigendum change missed.
- UI/interaction error.
- Unclear or misleading explanation.

Prioritize failures by severity, not just count. One missed critical clause can matter more than dozens of harmless formatting errors.

## 7. Pilot Design and Product Metrics

Pilot with a small group of willing MSME sellers and/or tender consultants. First secure permission to process their documents and define data handling/retention. Do not use real customer files to train or evaluate a hosted AI service unless the provider terms and user arrangements permit it.

Measure:
- Time to first useful readiness report.
- Time a human spends reviewing the same tender without and with the product.
- Percentage of requirements accepted, edited, or rejected by reviewers.
- Number of high-risk issues surfaced before manual review.
- Number of false-positive and false-negative findings.
- Number of report exports and subsequent repeat use.
- User trust calibrated to correctness—not merely whether the report looks convincing.
- Willingness to pay and preferred purchase model.
- Processing cost and support effort per tender.

Interview users after the workflow, not only after showing a mock UI. Ask them to verify report items against the original document; observing where they struggle will reveal missing workflow requirements.

## 8. Regression and Release Process

For each code, prompt, model, OCR, or rule-set change:
1. Run unit tests for parser normalizers, comparators, dates, units, and status logic.
2. Run schema validation tests.
3. Run the relevant labelled benchmark.
4. Compare errors against the previous release.
5. Manually inspect the high-severity subset.
6. Record provider/model/rule version and the evaluation dataset version.
7. Do not deploy if a critical false-supported result or material citation regression remains unexplained.

A new model version can change extraction behavior even with the same prompt. Version outputs and rerun the benchmark whenever a component capable of changing report conclusions is updated.

## 9. What Not to Claim

Do not claim:
- "100% accurate tender eligibility."
- "Guaranteed rejection prevention."
- "This bid will be accepted."
- "All GeM tender types are supported" without measured coverage.
- "Every corrigendum is detected" when the user must upload amendments manually.
- "AI verified certificate authenticity" unless a separate authoritative verification process actually exists.

A defensible claim is narrower: the system creates a source-linked preliminary checklist and highlights missing or inconsistent evidence for human review, within the tested document and tender scope.
