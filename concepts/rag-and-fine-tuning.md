# RAG and Fine-Tuning: How They Work, How They Differ, and When to Use Each

RAG and fine-tuning are two common ways to adapt an AI application to a particular need. They are related, but they solve different problems.

**RAG gives a model relevant information to use when answering a question. Fine-tuning uses additional training to adapt a model's behaviour or performance for a task.**

They are not mutually exclusive. A system can use both, but it should do so only when the combination solves a real requirement.

## 1. The Core Idea

Imagine you're building an AI assistant for a college. You want it to do two things:

1. Answer questions using the latest syllabus, examination timetable, attendance policy, and official notices.
2. Explain answers in a consistent, beginner-friendly style and follow a specific response format.

These are different needs.

- **RAG** is a natural fit for locating current, official information.
- **Fine-tuning** may help if you have persistent, measurable problems with task-specific behaviour that prompting and output validation do not adequately solve.

The assistant could use both: retrieve the current policy, then generate a clear, consistently structured answer from that evidence.

## 2. What Is RAG?

**RAG stands for Retrieval-Augmented Generation.** It is an approach in which an application retrieves relevant information from an external knowledge source and supplies it to a language model as context for generating an answer.

Break the term into three parts:

| Term | Meaning |
|---|---|
| Retrieval | Find information relevant to the user's question. |
| Augmented | Add the retrieved material to the context available to the model. |
| Generation | Use the model to compose an answer. |

The key point is that ordinary RAG does not train the model on every document. It retrieves selected information at answer time.

### 2.1 An everyday analogy

Imagine taking an open-book examination.

You already know how to read, reason, and write. When a question asks for a specific fact, you find the relevant page in your textbook, read it, and use it to write your answer.

The analogy maps to RAG like this:

- The language model is like the student who can understand and explain.
- The documents are like the textbooks.
- Retrieval is the process of finding the relevant pages.
- The retrieved passages are the material supplied for the current question.
- The generated response is the final answer.

The analogy is not a literal description of how an AI model works. It illustrates the central idea: provide relevant source information at answer time.

### 2.2 Why do we need RAG?

A language model learns patterns during its training process, but it does not automatically know every private document, new policy, updated product manual, or change made after training. A model may also lack access to information it was never trained to use.

Without RAG, an application might have to paste large amounts of information into every prompt or rely on the model to answer from its existing learned knowledge.

RAG provides another option:

1. Maintain a collection of information outside the model.
2. Search that information when a question arrives.
3. Select the most relevant passages.
4. Send those passages alongside the question to the language model.
5. Generate an answer using the model's general capabilities and the retrieved context.

This is useful when answers depend on private, specialised, or changing information.

### 2.3 A typical RAG pipeline

```text
                    DOCUMENT PREPARATION
PDFs / Markdown / web pages / approved data sources
                         |
                         v
              Extract and clean content
                         |
                         v
                 Split into chunks
                         |
                         v
                Build a searchable index
                         |
                         v
USER QUESTION ---> Retrieve relevant chunks
                         |
                         v
             Add chunks to model context
                         |
                         v
                  Language model
                         |
                         v
              Answer + possible citations
```

This is a common pattern, not a fixed architecture. Some systems add access-control filters, query rewriting, reranking, multiple retrieval steps, or other components.

### 2.4 Step 1 — Collect and prepare the source information

The knowledge source might include PDF manuals, Markdown files, HTML pages, product documentation, company policies, support articles, approved database records, or internal knowledge-base pages.

The content must be accessible to the application. Different file formats may need different extraction methods.

Preparation may include removing irrelevant navigation text, preserving headings, correcting extraction errors, recording source URLs, attaching metadata, and identifying the current version of a document.

The source of truth matters. If the source contains incorrect or outdated information, retrieval can surface that incorrect or outdated information.

### 2.5 Step 2 — Split information into chunks

A document can be too long to retrieve or pass to a model as one large piece for every question. Systems often split documents into smaller segments called **chunks**.

For example, an attendance policy could be split into:
- Chunk 1: Minimum attendance requirement
- Chunk 2: Eligibility for semester examinations
- Chunk 3: Rules for approved leave
- Chunk 4: Exceptions and appeal process

A question about examination eligibility should retrieve the relevant chunks instead of feeding the whole document to the model.

Chunking requires care:
- If chunks are too small, a passage may lose the context needed to interpret it.
- If chunks are too large, they may contain unrelated content and use more context than necessary.
- If a definition is separated from its conditions or exceptions, the retrieved text may be misleading.
- Some documents benefit from section-aware, page-aware, or parent-child chunking rather than splitting at an arbitrary character count.

Chunk size and overlap should be tested against the actual documents and questions, not selected from a universal rule.

### 2.6 Step 3 — Understand embeddings and vector search

An **embedding** is a numerical representation of content produced by an embedding model. Embedding systems are designed so that content with related meanings can often have similar vector representations.

Consider this policy sentence:

> Students must maintain the required attendance percentage to qualify for semester examinations.

Now consider this question:

> How many classes can I miss before I become ineligible to write my exams?

The wording differs, but the meanings are related. Semantic search using embeddings can help find relevant passages even when they don't share all the same keywords.

A common vector retrieval process is:

1. Split the documents into chunks.
2. Generate an embedding for each chunk.
3. Store the vectors and references to their source text.
4. Generate an embedding for the user's question.
5. Search for vectors close to the question vector.
6. Return the corresponding text passages.

A vector database or vector index can store and search these representations.

**Important:** Embeddings and vector search are common in RAG, but not mandatory for every RAG system. Keyword search, metadata filters, database queries, and hybrid search (combining keyword and semantic retrieval) can also be used.

Semantic similarity does not equal factual correctness. A retrieved passage may be topically related but still be outdated, incomplete, or unable to answer the actual question.

### 2.7 Step 4 — Retrieve and rank the passages

When a user asks a question, the system searches its index and selects candidate passages.

A simple retriever might return the top few matches. More advanced pipelines may:
- Filter by document type, date, product, or permissions.
- Rewrite the query to improve retrieval.
- Use keyword and vector search together.
- Rerank candidate passages with a separate model.
- Retrieve multiple times when the question requires several facts.

Relevance is not the only factor. A good system may need to prefer an official policy over an informal discussion, or a current document over an obsolete version.

The number of chunks retrieved is a trade-off. Too few passages may omit an essential detail; too many may add noise, increase cost, and make it harder for the model to focus.

### 2.8 Step 5 — Augment the model's context

After retrieval, the application supplies the passages to the language model alongside the question and instructions.

A simplified prompt might be:

```text
SYSTEM INSTRUCTION:
Answer using the supplied official information.
If the evidence does not support an answer, say that you cannot determine it.

RETRIEVED CONTEXT:
"The examination policy states that ..."

USER QUESTION:
"What is the attendance requirement for semester examinations?"

INSTRUCTION:
Answer clearly and identify the source when possible.
```

The exact prompt format varies by model and application. The important point is that the retrieved material becomes part of the model's input for this request.

The model can still use its language and reasoning capabilities, but the application has provided additional evidence relevant to the question.

### 2.9 Step 6 — Generate and verify the answer

The model generates a response based on the question, instructions, and retrieved context.

The application may also provide source links, document titles, page numbers, or citations. For these to be useful, the system must connect claims to the correct source passages and ensure that the evidence supports the claims.

RAG does **not** automatically eliminate hallucinations. The model may misread a passage, infer more than it supports, ignore a crucial qualification, or answer despite missing evidence.

For high-impact use cases, the application may need evidence checks, validation rules, human review, or a refusal to answer when reliable supporting information is unavailable.

### 2.10 What happens when the source data changes?

Suppose a college updates its exam timetable.

A RAG system can make the new timetable available by:
1. Updating the source document.
2. Reprocessing and reindexing the changed information.
3. Ensuring old versions are no longer selected as current.
4. Retrieving the latest relevant timetable for subsequent questions.

The model's underlying weights do not need to be fine-tuned just to make the changed document available through retrieval.

However, the change may not be instantaneous. Indexing jobs, caching, versioning mistakes, or duplicate old documents can cause delays or stale results. A sound design includes source versioning and a clear strategy for removing obsolete content.

### 2.11 Benefits of RAG

- **Current information:** Update the knowledge source without retraining the model every time a fact changes.
- **Private or specialised information:** Let an application use documents that weren't part of the model's original training.
- **Traceability:** Present source passages or citations when implemented correctly.
- **Manageable updates:** Maintain documents independently of the model's parameters.
- **Selective context:** Retrieve a subset of a large collection instead of passing the entire collection to every request.

### 2.12 Limitations of RAG

- **Poor retrieval:** The system may fail to find the necessary passage.
- **Bad source data:** Incorrect, outdated, or contradictory material may be retrieved.
- **Extra architecture:** Ingestion, indexing, storage, permissions, retrieval, and monitoring require engineering.
- **Latency and cost:** Retrieval and extra context add processing to requests.
- **Context constraints:** The selected passages must fit the model's available context and token budget.
- **Remaining model errors:** The LLM may misinterpret correct information or make unsupported claims.
- **Security and permissions:** Retrieval must enforce document-level access control, not merely hide inaccessible documents in the user interface.
- **Maintenance:** Documents and indexes need to stay synchronized, with old or deleted information handled properly.

A RAG system is only as useful as its sources, retrieval process, and answer-generation behaviour. Evaluate retrieval quality and answer quality separately.

## 3. What Is Fine-Tuning?

**Fine-tuning is an additional training process that adapts an already-trained model using task-specific examples, preferences, or other training signals.**

A model has learned numerical parameters, commonly called **weights**, during its original training. Fine-tuning updates trainable parameters to improve the model's performance on a chosen objective.

Unlike ordinary RAG, fine-tuning is a training step. It is not simply a process of searching for documents and inserting them into the current prompt.

### 3.1 An everyday analogy

Imagine you already know programming. A company wants you to review code according to its internal conventions.

It gives you many representative examples:
- Code with a bug and a high-quality review.
- Code with a naming problem and a corrected version.
- Correct code that should not be changed.
- Code with a security flaw and an explanation of the risk.

You practise on examples and receive feedback. The objective is to make you better at performing that specific task consistently.

Fine-tuning applies a related idea to a model. It uses additional training data to adapt model behaviour. Unlike a human learner, a neural network's training process updates numerical parameters through an optimization algorithm.

### 3.2 Why do we need fine-tuning?

Imagine you're building a customer-support classifier. Every incoming message must be labelled as one of:

- **BILLING**
- **TECHNICAL**
- **ACCOUNT_ACCESS**
- **REFUND**

The output must follow a specific schema, and the model repeatedly makes mistakes on specialised edge cases.

You could first improve the prompt, provide examples in context, and validate the output. If those approaches still fall short and you have suitable training data, fine-tuning may help the model learn the desired task patterns.

Fine-tuning is often considered when the goal is to improve **how a model performs a task**, rather than merely supplying it with reference material.

It is not automatically the right first step. Better instructions, structured-output constraints, deterministic code, or a different model may solve the problem more cheaply and simply.

### 3.3 A typical fine-tuning workflow

```text
               PRETRAINED MODEL
                      |
                      v
         Prepare representative examples
                      |
                      v
             Configure the training
                      |
                      v
       Update trainable model parameters
                      |
                      v
          Evaluate on unseen test cases
                      |
                      v
           Compare against the baseline
                      |
                      v
             Deploy if results justify it
```

The details depend on the training method, model, and provider.

### 3.4 Step 1 — Start with a pretrained model

Fine-tuning ordinarily begins with a model that already has general capabilities. You don't have to train a foundational model from scratch.

The existing model is the starting point. Fine-tuning aims to adapt its performance to the task represented in the additional training process.

### 3.5 Step 2 — Prepare a suitable dataset

For supervised fine-tuning, examples commonly pair an input with the desired output.

For a code-review assistant, a dataset might include:

| Input | Desired output |
|---|---|
| A function missing an edge-case check | A review that identifies the issue and suggests a correction |
| Code violating a naming convention | A review identifying the convention violation |
| Correct code that follows the conventions | A response indicating no change is needed |
| Code containing a security vulnerability | A review explaining the risk and a safer solution |

Useful training examples should be accurate, consistent, representative, and relevant to the deployed task.

The dataset should cover ordinary cases as well as edge cases that matter in practice. Duplicates, incorrect labels, inconsistent formatting, or unrealistic examples can weaken the outcome.

For an honest evaluation, keep test examples separate from the examples used to train the model. Otherwise, the result can look better than it generalizes to new inputs.

Not all fine-tuning uses simple input-output pairs. Some methods use preference comparisons, feedback, or reward signals.

### 3.6 Step 3 — Understand what training changes

This is a central technical difference from RAG.

During supervised fine-tuning, a simplified training loop looks like this:

1. The model receives a training input.
2. It predicts an output.
3. A loss function measures how the prediction compares with the desired output.
4. An optimization algorithm calculates how trainable parameters should change.
5. The parameters are updated.
6. The process repeats over training examples and steps.

The exact mathematical details depend on the model and training method. For now, remember that **fine-tuning changes trainable model parameters to optimise a training objective**.

Some methods update most or all model weights. Parameter-efficient techniques instead train a smaller set of additional parameters, leaving most original weights unchanged. This can reduce some training and storage costs, depending on the setup.

### 3.7 What can a fine-tuned model learn?

Fine-tuning can improve patterns needed for tasks such as:
- Classifying messages or documents.
- Producing a consistent response style.
- Following specialised transformations or conventions.
- Generating outputs in a desired format.
- Performing a domain-specific task for which suitable examples are available.

These are possible outcomes, not guarantees. Performance depends on the dataset, model, training configuration, evaluation, and similarity between training inputs and real-world usage.

### 3.8 Does fine-tuning permanently insert documents into a searchable knowledge base?

No. Fine-tuning and document retrieval work differently.

Fine-tuning adapts the model's parameters based on training examples. It does not automatically create an auditable, searchable library from which the model can reliably retrieve every exact fact.

A model may learn patterns or information associated with the examples, but it is not a reliable substitute for a maintained source of truth when precise and changing facts must be retrieved.

Imagine a company changes its refund policy every week. Fine-tuning the model on the policy will not cause it to discover next week's change. A new training process or a separate up-to-date information source would be required.

If users need the current wording of a policy, retrieval is usually a more direct way to expose the current source.

### 3.9 Common categories of fine-tuning

**Supervised fine-tuning (SFT)**

The training dataset contains examples of inputs and desired outputs. The training process encourages the model to produce outputs that match the target patterns.

Example: training a classifier on customer messages paired with correct categories.

**Preference-based tuning**

Training uses signals about which outputs are preferred over alternatives. Depending on the method, this may involve preference comparisons and algorithms such as Direct Preference Optimization (DPO).

Example: preferring a clear and accurate support response over an unclear, irrelevant response.

**Reinforcement fine-tuning**

The training process uses scores or feedback from a grading process or reward signal to improve performance against a defined objective.

Example: optimising a model for structured code-generation tasks where outputs can be tested against verifiable requirements.

These methods are related but not interchangeable. The appropriate choice depends on the objective, the available data, the model, and how success can be measured.

### 3.10 Benefits of fine-tuning

- **Task-specific performance:** It may improve a model's reliability on a narrow task when the examples represent that task well.
- **Consistent patterns:** It may help establish desired output structures, styles, and transformations.
- **Less repeated prompting:** Some long instructions or demonstrations may no longer be necessary in every request.
- **Potential serving efficiency:** In some cases, an adapted smaller model can perform a specialised task at lower serving cost than a larger general model. This must be measured rather than assumed.
- **Specialisation:** It can adapt a general model to recurring patterns that are hard to specify reliably with prompts alone.

### 3.11 Limitations of fine-tuning

- **Training data preparation:** High-quality examples take time and care to create.
- **Training costs:** The resources required depend on the model, dataset, method, and provider.
- **Evaluation is essential:** Performance on training examples does not prove good performance on unseen cases.
- **Regression risk:** Fine-tuning may weaken some behaviours or capabilities that were already good.
- **Stale facts:** A policy or product change does not automatically update a previously fine-tuned model.
- **Lifecycle management:** Models, datasets, training configurations, and deployments need versioning and monitoring.
- **No guaranteed improvement:** A poorly designed training run may provide little benefit or make results worse.

## 4. The Main Difference: Information at Answer Time vs. Training-Time Adaptation

This is the most important concept to remember.

### RAG

The application retrieves information from an external source and includes relevant passages in the model's input for a particular request. The retrieval process itself does not update the model's weights.

### Fine-tuning

An additional training process updates trainable model parameters using examples or other training signals. The resulting model has been adapted to the training objective.

A short mental model:

- **RAG changes what information is supplied to the model for a particular answer.**
- **Fine-tuning changes what patterns the model has learned to perform.**

## 5. RAG vs. Fine-Tuning: Comparison Table

| Dimension | RAG | Fine-tuning |
|---|---|---|
| Primary purpose | Make relevant external information available at answer time | Adapt task performance or behaviour |
| Main mechanism | Retrieve information and add it to the input context | Additional training updates trainable parameters |
| Updates model weights? | Not through ordinary retrieval itself | Yes, in standard weight-based fine-tuning; some methods train only additional parameters |
| How information is used | Selected source passages are supplied with the current request | Training examples influence the learned parameters |
| Updating a changing fact | Update and reindex the source as needed | Usually requires further training or a separate retrieval source |
| Private document collections | Often a strong fit | Not a searchable document store |
| Consistent task patterns | Can be helped by retrieved instructions and examples | May improve persistent task-specific behaviour |
| Citations and provenance | Can return source passages and references when implemented correctly | Does not inherently provide source citations |
| Main infrastructure | Data ingestion, index, retrieval, context construction | Training data, training process, model versioning and deployment |
| Main failure mode | Relevant or authoritative evidence is not retrieved or is misinterpreted | The model fails to generalise or develops unwanted behaviours |
| Evaluation required? | Yes—evaluate retrieval and answers | Yes—compare task performance on held-out cases |
| Can the two be combined? | Yes | Yes |

Neither approach guarantees factual correctness or good output. Both need appropriate engineering and evaluation.

## 6. A Worked Example: Company Travel Policy Assistant

Imagine a company has thousands of pages of internal documentation. Employees ask:

> What is our current travel reimbursement limit? Explain it in three short steps and return the result in our standard JSON format.

There are two requirements hidden in that question.

### Requirement A — Find the current reimbursement limit

The system must identify the authoritative, up-to-date policy. This is primarily a knowledge retrieval problem.

RAG can retrieve the current travel policy and provide the relevant passage to the model. The system should prioritise the authoritative current version over outdated documents.

### Requirement B — Follow the required response format

The system must produce three short steps and valid JSON.

You could first solve this with precise instructions and structured-output constraints. If testing demonstrates persistent task-specific failures and you have good examples of the desired format, fine-tuning may be worth evaluating.

In a hybrid application, RAG can supply the policy while a suitably configured model generates the answer in the required format. The application can then validate the JSON before returning it.

This division of work is often more useful than asking a fine-tuned model to memorise every policy detail.

## 7. What If the Information Changes?

Suppose the reimbursement limit changes from ₹2,000 to ₹2,500.

### Using RAG

1. Update the authoritative policy.
2. Reprocess and reindex the changed material.
3. Ensure the old version is no longer treated as current.
4. Retrieve the new limit for subsequent questions.

No model fine-tuning is needed just to expose the revised document through retrieval, although the indexing and caching strategy must be correct.

### Using fine-tuning alone

The model does not automatically learn the updated limit when the policy changes. You could run another training process, but that may be a cumbersome way to maintain a frequently changing reference fact.

**Rule of thumb:** For frequently changing facts, consider retrieval from a maintained source of truth before considering fine-tuning.

## 8. What If the Model Has the Information but Behaves Poorly?

Suppose the application retrieves the correct policy, but the model repeatedly responds in a confusing format.

Adding more documents may not solve this issue.

Possible steps, from simplest to more involved:

1. Improve the prompt and make the instructions unambiguous.
2. Use structured-output features or a schema where available.
3. Validate the output in code and retry or handle invalid output appropriately.
4. Evaluate whether a different model solves the problem.
5. If a persistent task-specific failure remains and sufficient representative examples exist, experiment with fine-tuning.

**Rule of thumb:** For recurring task-performance problems, first identify the failure and test simpler controls. Consider fine-tuning when evidence shows that it adds value.

## 9. Can RAG and Fine-Tuning Work Together?

Yes. They are complementary, not mutually exclusive alternatives.

A combined application may look like this:

```text
User asks a question
       |
       v
RAG retrieves authoritative, relevant information
       |
       v
Question + retrieved context are passed to the model
       |
       v
Model generates the answer
(possibly using fine-tuned task behaviour)
       |
       v
Application validates output and permissions
       |
       v
Answer is returned, with source references if appropriate
```

A hybrid system can be useful when an application needs both current or private knowledge and consistent specialised behaviour.

However, combining them increases complexity. Do not add fine-tuning merely because you already have RAG, or add RAG merely because you have a fine-tuned model. Each component should solve a demonstrated requirement.

## 10. Decision Guide: Which One Should You Use?

### Consider RAG when:
- The answer depends on current or frequently updated information.
- You need to use private documents or an internal knowledge base.
- You want source references that users can inspect.
- Documents must be updated independently of model training.
- The model needs access to a large set of reference material.

### Consider fine-tuning when:
- The model repeatedly fails at a specialised task despite appropriate prompting and validation.
- You have representative, high-quality examples or suitable training feedback.
- A consistent style, format, classification, or transformation is important.
- You can evaluate improvements on examples the model has not seen during training.
- The expected improvement justifies training and maintenance costs.

### Consider using both when:
- The application needs up-to-date knowledge and specialised behaviour.
- RAG handles the source information, while fine-tuning addresses demonstrated task-performance gaps.
- You can measure the contribution of each component.

### Consider neither at first when:
- A normal model call with clear instructions already performs well.
- There is no need for an external document collection.
- You have no evidence that fine-tuning would improve the outcome.

A sensible approach is to build the simplest system that meets the need, evaluate its weaknesses, and add complexity only when the results justify it.

## 11. Evaluation: How Do You Know It Works?

RAG and fine-tuning should be evaluated differently because they fail in different ways.

### Evaluating RAG

Check at least two parts of the pipeline.

**Retrieval quality**
- Did the system find the right source?
- Did it retrieve the crucial passage, exception, or qualification?
- Did it prefer current and authoritative material?
- Did it respect document permissions?

**Answer quality**
- Is the answer supported by retrieved evidence?
- Does it preserve important qualifications?
- Are citations connected to the claims they support?
- Does the model acknowledge missing evidence instead of guessing?

Build a representative set of questions with expected sources or answers. Test difficult cases, ambiguous queries, missing information, and outdated documents—not only easy demonstrations.

### Evaluating fine-tuning

Compare the fine-tuned model against a suitable baseline, such as the original model using the same task instructions.

Measure:
- Task accuracy or another relevant metric.
- Output validity and adherence to required formats.
- Performance on edge cases.
- Generalisation to unseen examples.
- Regressions in unrelated but important behaviour.
- Latency and serving cost.
- Whether the improvement is large enough to justify ongoing maintenance.

Use a held-out test set that is not used for training. Otherwise, evaluation may exaggerate how well the model handles new inputs.

### Evaluating the full application

For a hybrid system, evaluate the complete user experience as well as each component independently. Good retrieval is not enough if the model misuses the evidence; good output formatting is not enough if retrieval supplied the wrong fact.

## 12. Common Misconceptions

### "RAG trains the model on my documents."

Ordinary RAG retrieves information and provides it as context at answer time. Retrieval itself does not update the LLM's weights.

### "Fine-tuning is always the best way to teach new facts."

No. For current, authoritative facts, maintaining a source and retrieving from it is often more direct.

### "RAG eliminates hallucinations."

No. The system can retrieve poor evidence, and the model can still misinterpret evidence or invent unsupported details.

### "Fine-tuning always improves performance."

No. Results depend on the model, data, training objective, configuration, and evaluation. Fine-tuning can produce little improvement or regressions.

### "You must choose only one."

No. Both can be combined when each serves a distinct purpose.

### "Fine-tuning should always come before prompt engineering."

No. Clear instructions, structured output, validation, and a suitable model are often simpler starting points.

### "A vector database is the same thing as RAG."

No. A vector database can store and retrieve embeddings, but it is only one possible component of a RAG system. RAG also involves preparing sources, retrieving relevant information, constructing model context, and generating the response. Some retrieval systems do not use a vector database at all.

### "A fine-tuned model becomes a perfect database."

No. Learned parameters are not equivalent to an auditable, searchable source of truth. Exact factual recall is not guaranteed.

## 13. Beginner-Friendly Glossary

**LLM (Large Language Model):** A model trained to process and generate language, and sometimes other modalities.

**Training:** The process of optimising a model's parameters using data and a training objective.

**Weights / parameters:** Numerical values inside a model that are learned or adjusted during training.

**Inference:** Using a trained model to produce an output for an input, rather than updating its parameters through training.

**Embedding:** A numerical representation of content used by systems such as semantic retrieval.

**Chunk:** A segment of a longer document that can be indexed or retrieved.

**Vector search:** A retrieval technique that finds vectors close to a query vector according to a chosen similarity or distance measure.

**Vector database:** A database or service that supports storing and searching vector representations, often with metadata.

**Context window:** The amount of input and conversation content a model can process for a request, subject to the model's limits.

**Fine-tuning dataset:** Examples or signals used to adapt a model to a target objective.

**Held-out test set:** Examples reserved for evaluation rather than training, used to check how well a system generalises.

**Reranking:** A second-stage process that reorders retrieved candidates to improve relevance.

**Grounding:** Connecting an answer to supporting evidence or external information instead of relying only on the model's general learned knowledge.

## 14. Questions for Revision

Try to answer these before checking the answer key.

1. What does RAG stand for?
2. What does retrieval-augmented generation do?
3. Why might a RAG application split a document into chunks?
4. What is an embedding?
5. Is vector search mandatory for every RAG system?
6. What is the difference between retrieval and generation?
7. What does fine-tuning mean?
8. What are model weights or parameters?
9. What role does a training dataset play in supervised fine-tuning?
10. How is fine-tuning different from supplying text in a prompt?
11. Why is fine-tuning not a reliable replacement for a changing policy database?
12. Give two situations where RAG is a strong fit.
13. Give two situations where fine-tuning may be useful.
14. How can RAG and fine-tuning work together?
15. Why should a RAG system evaluate retrieval and answer quality separately?
16. Why should fine-tuning be evaluated on held-out examples?
17. What is the principle behind starting with the simplest solution that works?

### Answer Key

1. Retrieval-Augmented Generation.
2. It retrieves relevant external information and supplies it to the model as context for generating an answer.
3. Smaller segments can make relevant passages easier to retrieve and avoid supplying an entire large document for every question.
4. A numerical representation of content produced by an embedding model, often used for semantic similarity and retrieval.
5. No. RAG can use keyword search, database queries, metadata filters, or other retrieval methods as well as vector search.
6. Retrieval finds relevant information; generation uses the model to compose an answer.
7. Additional training that adapts a pretrained model using task-specific examples or other training signals.
8. Numerical parameters learned or adjusted during model training.
9. The examples show the model the inputs and desired outputs for the training objective.
10. Prompting changes the input supplied for a request; fine-tuning is a training process that updates trainable parameters.
11. A previously fine-tuned model does not automatically learn new policy revisions. A maintained source and retrieval can expose current information more directly.
12. Answering from current official documents; querying a private company knowledge base.
13. Improving a repeated specialised classification task; improving consistent task-specific output patterns when simpler methods are insufficient.
14. RAG can retrieve current evidence, and the adapted model can process or present that evidence in a specialised way.
15. Retrieval can fail before the model receives the evidence, and the model can fail after receiving it. The two stages have different failure modes.
16. To measure generalisation to new examples rather than memorisation of the training set.
17. It helps reduce unnecessary complexity and cost. Add RAG, fine-tuning, or other components when evaluation shows that they solve a real problem.

## 15. Key Takeaway

> **RAG supplies relevant information at answer time. Fine-tuning adapts the model through additional training.**

Remember the simple pattern:

- **Need current or private facts?** Investigate RAG.
- **Need better performance on a repeated, specialised task?** Evaluate prompting, validation, and possibly fine-tuning.
- **Need both current knowledge and specialised behaviour?** Consider a hybrid and measure whether each component helps.

For most projects, start by defining the actual failure you need to solve, build a baseline, and evaluate it. Better AI engineering is not about using the most techniques—it is about choosing the simplest reliable design for the problem.

## 16. Further Reading

- [Microsoft Learn: Retrieval-augmented generation (RAG)](https://learn.microsoft.com/azure/search/retrieval-augmented-generation-overview)
- [OpenAI Platform: Model optimization](https://platform.openai.com/docs/guides/model-optimization)
- [OpenAI Platform: Fine-tuning](https://platform.openai.com/docs/guides/fine-tuning)
